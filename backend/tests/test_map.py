from datetime import timedelta

from django.contrib.gis.geos import Point
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from tests.factories import EventFactory, PlaceFactory, WarsawPlaceFactory

WARSAW_BBOX = "20.85,52.10,21.15,52.35"
OUTSIDE_POINT = Point(19.0, 50.0, srid=4326)


class TestMapEndpoint:
    def test_returns_200_without_auth(self, api_client, db):
        response = api_client.get(reverse("map"), {"bbox": WARSAW_BBOX})
        assert response.status_code == status.HTTP_200_OK

    def test_returns_places_key(self, api_client, db):
        response = api_client.get(reverse("map"), {"bbox": WARSAW_BBOX})
        assert "places" in response.data

    def test_returns_place_within_bbox(self, api_client, db):
        place = WarsawPlaceFactory()
        response = api_client.get(reverse("map"), {"bbox": WARSAW_BBOX})
        ids = [str(p["id"]) for p in response.data["places"]]
        assert str(place.id) in ids

    def test_excludes_place_outside_bbox(self, api_client, db):
        place = PlaceFactory(location=OUTSIDE_POINT)
        response = api_client.get(reverse("map"), {"bbox": WARSAW_BBOX})
        ids = [str(p["id"]) for p in response.data["places"]]
        assert str(place.id) not in ids

    def test_returns_expected_fields(self, api_client, db):
        WarsawPlaceFactory()
        response = api_client.get(reverse("map"), {"bbox": WARSAW_BBOX})
        item = response.data["places"][0]
        for field in ("id", "title", "lat", "lng", "category", "event_count"):
            assert field in item, f"Missing field: {field}"

    def test_event_count_annotation(self, api_client, place, event):
        response = api_client.get(reverse("map"), {"bbox": WARSAW_BBOX})
        item = next(p for p in response.data["places"] if str(p["id"]) == str(place.id))
        assert item["event_count"] == 1

    def test_event_count_excludes_past_events(self, api_client, db):
        place = WarsawPlaceFactory()
        EventFactory(place=place, event_time=timezone.now() - timedelta(days=1))
        response = api_client.get(reverse("map"), {"bbox": WARSAW_BBOX})
        item = next(p for p in response.data["places"] if str(p["id"]) == str(place.id))
        assert item["event_count"] == 0

    def test_returns_400_without_bbox(self, api_client, db):
        response = api_client.get(reverse("map"))
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_returns_400_for_invalid_bbox(self, api_client, db):
        response = api_client.get(reverse("map"), {"bbox": "invalid"})
        assert response.status_code == status.HTTP_400_BAD_REQUEST
