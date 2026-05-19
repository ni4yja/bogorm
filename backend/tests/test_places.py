import uuid

import pytest

from places.admin import PlaceAdminForm  # adjust to your app name

BASE = "/api/v1/places"
# ---------------------------------------------------------------------------
# GET /api/v1/places/
# ---------------------------------------------------------------------------


class TestPlacesList:
    def test_returns_200_without_auth(self, client, db):
        response = client.get(f"{BASE}/")
        assert response.status_code == 200

    def test_returns_paginated_results(self, client, place):
        response = client.get(f"{BASE}/")
        # DRF cursor pagination wraps items in "results"
        assert "results" in response.data
        assert len(response.data["results"]) == 1

    def test_result_contains_expected_fields(self, client, place):
        response = client.get(f"{BASE}/")
        item = response.data["results"][0]
        for field in ("id", "title", "category"):
            assert field in item, f"Missing field: {field}"


# ---------------------------------------------------------------------------
# GET /api/v1/places/:id/
# ---------------------------------------------------------------------------


class TestPlaceDetail:
    def test_returns_200(self, client, place):
        response = client.get(f"{BASE}/{place.id}/")
        assert response.status_code == 200

    def test_returns_correct_place(self, client, place):
        response = client.get(f"{BASE}/{place.id}/")
        assert str(response.data["id"]) == str(place.id)
        assert response.data["title"] == place.title

    def test_returns_coordinates(self, client, place):
        response = client.get(f"{BASE}/{place.id}/")
        assert float(response.data["lat"]) == pytest.approx(place.location.y)
        assert float(response.data["lng"]) == pytest.approx(place.location.x)

    def test_returns_full_description(self, client, place):
        response = client.get(f"{BASE}/{place.id}/")
        assert response.data["description"] == place.description

    def test_404_for_nonexistent_uuid(self, client, db):
        fake_id = uuid.uuid4()
        response = client.get(f"{BASE}/{fake_id}/")
        assert response.status_code == 404

    def test_404_response_has_error_key(self, client, db):
        fake_id = uuid.uuid4()
        response = client.get(f"{BASE}/{fake_id}/")
        # DRF за замовчуванням повертає {"detail": "..."}
        assert "detail" in response.data


# ---------------------------------------------------------------------------
# lat/lng range validation (Admin form)
# ---------------------------------------------------------------------------

VALID_DATA = {"title": "Тестове місце", "lat": 49.84, "lng": 24.03, "category": 60}


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
