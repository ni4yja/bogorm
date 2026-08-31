import uuid
from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from bookmarks.models import Bookmark
from tests.factories import EventFactory, PlaceFactory, UserFactory


class TestEventsList:
    def test_returns_401_without_auth(self, api_client, place):
        response = api_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_events_for_place(self, authenticated_client, place, event):
        response = authenticated_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == event.title

    def test_returns_expected_fields(self, authenticated_client, place, event):
        response = authenticated_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        item = response.data["results"][0]
        for field in ("id", "title", "category"):
            assert field in item, f"Missing field: {field}"

    def test_404_for_nonexistent_place(self, authenticated_client, db):
        response = authenticated_client.get(
            reverse("place-events-list", kwargs={"place_pk": uuid.uuid4()})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_only_events_for_given_place(
        self, authenticated_client, place, event
    ):
        other_place = PlaceFactory()
        EventFactory(place=other_place)
        response = authenticated_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == event.title

    def test_returns_events_ordered_by_event_time_asc(
        self, authenticated_client, place
    ):
        event_later = EventFactory(place=place, days_from_now=5)
        event_sooner = EventFactory(place=place, days_from_now=1)
        response = authenticated_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        results = response.data["results"]
        assert results[0]["id"] == str(event_sooner.id)
        assert results[1]["id"] == str(event_later.id)

    def test_week_current_filters_to_current_calendar_week(
        self, authenticated_client, place
    ):
        now = timezone.now()
        start_of_week = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_of_week = start_of_week + timedelta(days=7)

        within_week_time = min(
            now + timedelta(hours=1), end_of_week - timedelta(hours=1)
        )
        event_this_week = EventFactory(place=place, event_time=within_week_time)
        EventFactory(place=place, event_time=end_of_week + timedelta(days=1))

        response = authenticated_client.get(
            reverse("event-list"), {"status": "upcoming", "week": "current"}
        )

        ids = [item["id"] for item in response.data["results"]]
        assert ids == [str(event_this_week.id)]

    def test_week_current_rejects_archived_status(self, authenticated_client, db):
        response = authenticated_client.get(
            reverse("event-list"), {"status": "archived", "week": "current"}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "week" in response.data


class TestEventDetail:
    def test_returns_200(self, authenticated_client, place, event):
        response = authenticated_client.get(
            reverse(
                "place-events-detail", kwargs={"place_pk": place.id, "pk": event.id}
            )
        )
        assert response.status_code == status.HTTP_200_OK

    def test_returns_correct_event(self, authenticated_client, place, event):
        response = authenticated_client.get(
            reverse(
                "place-events-detail", kwargs={"place_pk": place.id, "pk": event.id}
            )
        )
        assert str(response.data["id"]) == str(event.id)
        assert response.data["title"] == event.title

    def test_404_for_nonexistent_event(self, authenticated_client, place, db):
        response = authenticated_client.get(
            reverse(
                "place-events-detail", kwargs={"place_pk": place.id, "pk": uuid.uuid4()}
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestAllEventsList:
    def test_returns_401_without_auth(self, api_client, db):
        response = api_client.get(reverse("event-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_defaults_to_upcoming(self, authenticated_client, place):
        upcoming_event = EventFactory(place=place, days_from_now=1)
        EventFactory(place=place, days_from_now=-1)

        response = authenticated_client.get(reverse("event-list"))

        assert response.status_code == status.HTTP_200_OK
        ids = [item["id"] for item in response.data["results"]]
        assert ids == [str(upcoming_event.id)]

    def test_upcoming_ordered_by_event_time_asc(self, authenticated_client, place):
        event_later = EventFactory(place=place, days_from_now=5)
        event_sooner = EventFactory(place=place, days_from_now=1)

        response = authenticated_client.get(
            reverse("event-list"), {"status": "upcoming"}
        )

        results = response.data["results"]
        assert results[0]["id"] == str(event_sooner.id)
        assert results[1]["id"] == str(event_later.id)

    def test_archived_ordered_by_event_time_desc(self, authenticated_client, place):
        event_older = EventFactory(place=place, days_from_now=-5)
        event_newer = EventFactory(place=place, days_from_now=-1)

        response = authenticated_client.get(
            reverse("event-list"), {"status": "archived"}
        )

        results = response.data["results"]
        assert results[0]["id"] == str(event_newer.id)
        assert results[1]["id"] == str(event_older.id)

    def test_rejects_invalid_status(self, authenticated_client, db):
        response = authenticated_client.get(reverse("event-list"), {"status": "blah"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "status" in response.data

    def test_rejects_empty_status(self, authenticated_client, db):
        response = authenticated_client.get(reverse("event-list"), {"status": ""})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "status" in response.data

    def test_filters_by_category(self, authenticated_client, place):
        matching_event = EventFactory(place=place, days_from_now=1, category=10)
        EventFactory(place=place, days_from_now=1, category=20)

        response = authenticated_client.get(reverse("event-list"), {"category": 10})

        ids = [item["id"] for item in response.data["results"]]
        assert ids == [str(matching_event.id)]

    def test_category_filter_combines_with_status(self, authenticated_client, place):
        matching_event = EventFactory(place=place, days_from_now=1, category=10)
        EventFactory(place=place, days_from_now=-1, category=10)  # archived, excluded
        EventFactory(place=place, days_from_now=1, category=20)  # wrong category

        response = authenticated_client.get(
            reverse("event-list"), {"status": "upcoming", "category": 10}
        )

        ids = [item["id"] for item in response.data["results"]]
        assert ids == [str(matching_event.id)]

    def test_rejects_non_integer_category(self, authenticated_client, place):
        EventFactory(place=place, days_from_now=1)

        response = authenticated_client.get(reverse("event-list"), {"category": "abc"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "category" in response.data

    def test_rejects_unknown_category_value(self, authenticated_client, place):
        EventFactory(place=place, days_from_now=1, category=10)

        response = authenticated_client.get(reverse("event-list"), {"category": 999})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "category" in response.data

    def test_returns_nested_place(self, authenticated_client, place, event):
        response = authenticated_client.get(reverse("event-list"))

        item = response.data["results"][0]
        assert item["place"]["id"] == str(place.id)
        assert item["place"]["title"] == place.title
        assert item["place"]["lat"] == pytest.approx(place.lat)
        assert item["place"]["lng"] == pytest.approx(place.lng)

    def test_pagination_envelope_present(self, authenticated_client, place, event):
        response = authenticated_client.get(reverse("event-list"))

        for key in ("count", "next", "previous", "results"):
            assert key in response.data


class TestAllEventsDetail:
    def test_returns_200(self, authenticated_client, place, event):
        response = authenticated_client.get(reverse("event-detail", args=[event.id]))
        assert response.status_code == status.HTTP_200_OK

    def test_returns_correct_event_with_nested_place(
        self, authenticated_client, place, event
    ):
        response = authenticated_client.get(reverse("event-detail", args=[event.id]))
        assert str(response.data["id"]) == str(event.id)
        assert response.data["place"]["id"] == str(place.id)

    def test_404_for_nonexistent_event(self, authenticated_client, db):
        response = authenticated_client.get(
            reverse("event-detail", args=[uuid.uuid4()])
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_archived_event_without_status_param(
        self, authenticated_client, place
    ):
        archived = EventFactory(place=place, days_from_now=-3)

        response = authenticated_client.get(reverse("event-detail", args=[archived.id]))

        assert response.status_code == status.HTTP_200_OK
        assert str(response.data["id"]) == str(archived.id)

    def test_requires_auth(self, api_client, place, event):
        response = api_client.get(reverse("event-detail", args=[event.id]))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


# ---------------------------------------------------------------------------
# POST/DELETE /api/v1/events/:id/bookmark/
# ---------------------------------------------------------------------------


class TestEventBookmark:
    def test_returns_401_without_auth(self, api_client, event):
        response = api_client.post(reverse("event-bookmark", args=[event.id]))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_creates_bookmark(self, authenticated_client, user, event):
        response = authenticated_client.post(reverse("event-bookmark", args=[event.id]))

        assert response.status_code == status.HTTP_201_CREATED
        assert Bookmark.objects.filter(user=user, event=event).exists()

    def test_bookmarking_twice_is_idempotent(self, authenticated_client, user, event):
        authenticated_client.post(reverse("event-bookmark", args=[event.id]))
        response = authenticated_client.post(reverse("event-bookmark", args=[event.id]))

        assert response.status_code == status.HTTP_200_OK
        assert Bookmark.objects.filter(user=user, event=event).count() == 1

    def test_404_for_nonexistent_event(self, authenticated_client, db):
        response = authenticated_client.post(
            reverse("event-bookmark", args=[uuid.uuid4()])
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_deletes_bookmark(self, authenticated_client, user, event):
        Bookmark.objects.create(user=user, event=event)

        response = authenticated_client.delete(
            reverse("event-bookmark", args=[event.id])
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Bookmark.objects.filter(user=user, event=event).exists()

    def test_delete_returns_404_when_not_bookmarked(self, authenticated_client, event):
        response = authenticated_client.delete(
            reverse("event-bookmark", args=[event.id])
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_bookmark_is_scoped_to_user(self, authenticated_client, user, event):
        other_user = UserFactory()
        Bookmark.objects.create(user=other_user, event=event)

        response = authenticated_client.delete(
            reverse("event-bookmark", args=[event.id])
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert Bookmark.objects.filter(user=other_user, event=event).exists()
