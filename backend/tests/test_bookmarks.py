from django.urls import reverse
from rest_framework import status

from bookmarks.models import Bookmark
from tests.factories import PlaceFactory, UserFactory

# ---------------------------------------------------------------------------
# GET /api/v1/bookmarks/
# ---------------------------------------------------------------------------


class TestBookmarksList:
    def test_returns_401_without_auth(self, api_client, db):
        response = api_client.get(reverse("bookmark-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_place_bookmark(self, authenticated_client, user, place):
        Bookmark.objects.create(user=user, place=place)

        response = authenticated_client.get(reverse("bookmark-list"))

        assert response.status_code == status.HTTP_200_OK
        item = response.data["results"][0]
        assert item["type"] == "place"
        assert item["target"]["id"] == str(place.id)

    def test_returns_event_bookmark(self, authenticated_client, user, event):
        Bookmark.objects.create(user=user, event=event)

        response = authenticated_client.get(reverse("bookmark-list"))

        assert response.status_code == status.HTTP_200_OK
        item = response.data["results"][0]
        assert item["type"] == "event"
        assert item["target"]["id"] == str(event.id)

    def test_only_returns_current_users_bookmarks(
        self, authenticated_client, user, place
    ):
        Bookmark.objects.create(user=user, place=place)
        other_user = UserFactory()
        Bookmark.objects.create(user=other_user, place=PlaceFactory())

        response = authenticated_client.get(reverse("bookmark-list"))

        assert response.data["count"] == 1
        assert response.data["results"][0]["target"]["id"] == str(place.id)

    def test_filters_by_type_place(self, authenticated_client, user, place, event):
        Bookmark.objects.create(user=user, place=place)
        Bookmark.objects.create(user=user, event=event)

        response = authenticated_client.get(reverse("bookmark-list"), {"type": "place"})

        assert response.data["count"] == 1
        assert response.data["results"][0]["type"] == "place"

    def test_filters_by_type_event(self, authenticated_client, user, place, event):
        Bookmark.objects.create(user=user, place=place)
        Bookmark.objects.create(user=user, event=event)

        response = authenticated_client.get(reverse("bookmark-list"), {"type": "event"})

        assert response.data["count"] == 1
        assert response.data["results"][0]["type"] == "event"

    def test_rejects_invalid_type_value(self, authenticated_client, user, place):
        Bookmark.objects.create(user=user, place=place)

        response = authenticated_client.get(reverse("bookmark-list"), {"type": "plum"})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "type" in response.data

    def test_ordered_by_created_at_desc(self, authenticated_client, user):
        older = Bookmark.objects.create(user=user, place=PlaceFactory())
        newer = Bookmark.objects.create(user=user, place=PlaceFactory())

        response = authenticated_client.get(reverse("bookmark-list"))

        ids = [item["id"] for item in response.data["results"]]
        assert ids == [str(newer.id), str(older.id)]

    def test_pagination_envelope_present(self, authenticated_client, user, place):
        Bookmark.objects.create(user=user, place=place)

        response = authenticated_client.get(reverse("bookmark-list"))

        for key in ("count", "next", "previous", "results"):
            assert key in response.data


# ---------------------------------------------------------------------------
# GET /api/v1/bookmarks/ids/
# ---------------------------------------------------------------------------


class TestBookmarkIds:
    def test_returns_401_without_auth(self, api_client, db):
        response = api_client.get(reverse("bookmark-ids"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_returns_place_and_event_ids(
        self, authenticated_client, user, place, event
    ):
        Bookmark.objects.create(user=user, place=place)
        Bookmark.objects.create(user=user, event=event)

        response = authenticated_client.get(reverse("bookmark-ids"))

        assert response.status_code == status.HTTP_200_OK
        assert response.data["place_ids"] == [str(place.id)]
        assert response.data["event_ids"] == [str(event.id)]

    def test_returns_empty_lists_when_no_bookmarks(self, authenticated_client, db):
        response = authenticated_client.get(reverse("bookmark-ids"))

        assert response.data["place_ids"] == []
        assert response.data["event_ids"] == []

    def test_only_returns_current_users_ids(self, authenticated_client, user, place):
        Bookmark.objects.create(user=user, place=place)
        other_user = UserFactory()
        Bookmark.objects.create(user=other_user, place=PlaceFactory())

        response = authenticated_client.get(reverse("bookmark-ids"))

        assert response.data["place_ids"] == [str(place.id)]

    def test_response_is_not_paginated(self, authenticated_client, user, place):
        Bookmark.objects.create(user=user, place=place)

        response = authenticated_client.get(reverse("bookmark-ids"))

        assert "count" not in response.data
        assert "results" not in response.data
