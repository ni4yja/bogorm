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
