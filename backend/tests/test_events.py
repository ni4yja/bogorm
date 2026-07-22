import uuid

from django.urls import reverse
from rest_framework import status

from tests.factories import EventFactory, PlaceFactory


class TestEventsList:
    def test_returns_200_without_auth(self, api_client, place):
        response = api_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        assert response.status_code == status.HTTP_200_OK

    def test_returns_events_for_place(self, api_client, place, event):
        response = api_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == event.title

    def test_returns_expected_fields(self, api_client, place, event):
        response = api_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        item = response.data["results"][0]
        for field in ("id", "title", "category"):
            assert field in item, f"Missing field: {field}"

    def test_404_for_nonexistent_place(self, api_client, db):
        response = api_client.get(
            reverse("place-events-list", kwargs={"place_pk": uuid.uuid4()})
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_returns_only_events_for_given_place(self, api_client, place, event):
        other_place = PlaceFactory()
        EventFactory(place=other_place)
        response = api_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["title"] == event.title

    def test_returns_events_ordered_by_event_time_asc(self, api_client, place):
        event_later = EventFactory(place=place, days_from_now=5)
        event_sooner = EventFactory(place=place, days_from_now=1)
        response = api_client.get(
            reverse("place-events-list", kwargs={"place_pk": place.id})
        )
        results = response.data["results"]
        assert results[0]["id"] == str(event_sooner.id)
        assert results[1]["id"] == str(event_later.id)


class TestEventDetail:
    def test_returns_200(self, api_client, place, event):
        response = api_client.get(
            reverse(
                "place-events-detail", kwargs={"place_pk": place.id, "pk": event.id}
            )
        )
        assert response.status_code == status.HTTP_200_OK

    def test_returns_correct_event(self, api_client, place, event):
        response = api_client.get(
            reverse(
                "place-events-detail", kwargs={"place_pk": place.id, "pk": event.id}
            )
        )
        assert str(response.data["id"]) == str(event.id)
        assert response.data["title"] == event.title

    def test_404_for_nonexistent_event(self, api_client, place, db):
        response = api_client.get(
            reverse(
                "place-events-detail", kwargs={"place_pk": place.id, "pk": uuid.uuid4()}
            )
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
