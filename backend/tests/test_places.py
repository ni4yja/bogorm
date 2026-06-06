import uuid

import pytest
from django.urls import reverse
from rest_framework import status

from places.admin import PlaceAdminForm
from places.models import PlaceCategory
from tests.factories import PlaceFactory

VALID_DATA = {
    "title": "Test place",
    "lat": 49.84,
    "lng": 24.03,
    "category": PlaceCategory.OTHER,
}


# ---------------------------------------------------------------------------
# GET /api/v1/places/
# ---------------------------------------------------------------------------


class TestPlacesList:
    def test_returns_200_without_auth(self, api_client, db):
        response = api_client.get(reverse("place-list"))
        assert response.status_code == status.HTTP_200_OK

    def test_returns_paginated_results(self, api_client, place):
        PlaceFactory.create_batch(21)
        response = api_client.get(reverse("place-list"))
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data["results"]) == 20

    def test_result_contains_expected_fields(self, api_client, place):
        response = api_client.get(reverse("place-list"))
        item = response.data["results"][0]
        for field in ("id", "title", "category"):
            assert field in item, f"Missing field: {field}"


# ---------------------------------------------------------------------------
# GET /api/v1/places/:id/
# ---------------------------------------------------------------------------


class TestPlaceDetail:
    def test_returns_200(self, api_client, place):
        response = api_client.get(reverse("place-detail", args=[place.id]))
        assert response.status_code == status.HTTP_200_OK

    def test_returns_correct_place(self, api_client, place):
        response = api_client.get(reverse("place-detail", args=[place.id]))
        assert str(response.data["id"]) == str(place.id)
        assert response.data["title"] == place.title

    def test_returns_coordinates(self, api_client, place):
        response = api_client.get(reverse("place-detail", args=[place.id]))
        assert float(response.data["lat"]) == pytest.approx(place.location.y)
        assert float(response.data["lng"]) == pytest.approx(place.location.x)

    def test_returns_full_description(self, api_client, place):
        response = api_client.get(reverse("place-detail", args=[place.id]))
        assert response.data["description"] == place.description

    def test_404_for_nonexistent_uuid(self, api_client, db):
        response = api_client.get(reverse("place-detail", args=[uuid.uuid4()]))
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_404_response_has_error_key(self, api_client, db):
        response = api_client.get(reverse("place-detail", args=[uuid.uuid4()]))
        assert "detail" in response.data


# ---------------------------------------------------------------------------
# lat/lng range validation (Admin form)
# ---------------------------------------------------------------------------


class TestPlaceAdminFormValidation:
    @pytest.mark.parametrize(
        "lat,expected_error_field",
        [
            (90.1, "lat"),
            (-90.1, "lat"),
            (91, "lat"),
            (-91, "lat"),
        ],
    )
    def test_rejects_lat_out_of_range(self, lat, expected_error_field, db):
        form = PlaceAdminForm(data={**VALID_DATA, "lat": lat})
        assert not form.is_valid()
        assert expected_error_field in form.errors

    @pytest.mark.parametrize(
        "lng,expected_error_field",
        [
            (180.1, "lng"),
            (-180.1, "lng"),
            (181, "lng"),
            (-181, "lng"),
        ],
    )
    def test_rejects_lng_out_of_range(self, lng, expected_error_field, db):
        form = PlaceAdminForm(data={**VALID_DATA, "lng": lng})
        assert not form.is_valid()
        assert expected_error_field in form.errors

    @pytest.mark.parametrize(
        "lat,lng",
        [
            (90, 180),
            (-90, -180),
            (0, 0),
            (49.84, 24.03),
        ],
    )
    def test_accepts_valid_boundary_coordinates(self, lat, lng, db):
        form = PlaceAdminForm(data={**VALID_DATA, "lat": lat, "lng": lng})
        assert form.is_valid(), form.errors

    def test_save_writes_point_geometry(self, db):
        form = PlaceAdminForm(data=VALID_DATA)
        assert form.is_valid(), form.errors
        place = form.save()
        assert place.location is not None
        assert place.location.x == pytest.approx(VALID_DATA["lng"])
        assert place.location.y == pytest.approx(VALID_DATA["lat"])
        assert place.location.srid == 4326
