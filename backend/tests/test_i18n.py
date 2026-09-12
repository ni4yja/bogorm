from django.utils import translation

from tests.factories import PlaceFactory


class TestModeltranslationFallback:
    def test_falls_back_to_polish_title_when_english_missing(self, db):
        place = PlaceFactory(title_pl="Biblioteka Testowa", title_en="")

        with translation.override("en"):
            place.refresh_from_db()
            assert place.title == "Biblioteka Testowa"

    def test_falls_back_to_polish_description_when_english_missing(self, db):
        place = PlaceFactory(description_pl="Opis po polsku", description_en="")

        with translation.override("en"):
            place.refresh_from_db()
            assert place.description == "Opis po polsku"

    def test_falls_back_when_english_is_raw_null_not_empty_string(self, db):
        # Simulates a pre-existing row created before modeltranslation was
        # registered: title_en is a literal SQL NULL, not "" — this must
        # still fall back correctly, or it will crash once English becomes
        # reachable (e.g. via LocaleMiddleware).
        place = PlaceFactory(title_pl="Biblioteka Testowa")
        place.title_en = None
        place.save()

        with translation.override("en"):
            place.refresh_from_db()
            assert place.title == "Biblioteka Testowa"
