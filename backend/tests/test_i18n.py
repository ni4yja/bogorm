import pytest
from django.utils import translation

from tests.factories import PlaceFactory


class TestModeltranslationFallback:
    @pytest.mark.parametrize(
        "field, pl_value",
        [
            ("title", "Biblioteka Testowa"),
            ("description", "Opis po polsku"),
        ],
    )
    def test_falls_back_to_polish_when_english_is_empty_string(
        self, db, field, pl_value
    ):
        place = PlaceFactory(**{f"{field}_pl": pl_value, f"{field}_en": ""})

        with translation.override("en"):
            place.refresh_from_db()
            assert getattr(place, field) == pl_value

    @pytest.mark.parametrize(
        "field, pl_value",
        [
            ("title", "Biblioteka Testowa"),
            ("description", "Opis po polsku"),
        ],
    )
    def test_falls_back_when_english_is_raw_null_not_empty_string(
        self, db, field, pl_value
    ):
        # Simulates a pre-existing row created before modeltranslation was
        # registered: the _en column is a literal SQL NULL, not "" — this
        # must still fall back correctly, or it will crash once English
        # becomes reachable (e.g. via LocaleMiddleware).
        place = PlaceFactory(**{f"{field}_pl": pl_value})
        setattr(place, f"{field}_en", None)
        place.save()

        with translation.override("en"):
            place.refresh_from_db()
            assert getattr(place, field) == pl_value
