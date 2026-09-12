import pytest
from django.utils import translation

from tests.factories import PlaceFactory


@pytest.mark.parametrize(
    "field, pl_value",
    [
        ("title", "Biblioteka Testowa"),
        ("description", "Opis po polsku"),
    ],
)
@pytest.mark.parametrize("en_value", ["", None])  # "" = explicitly untranslated,
# None = row predating registration: literal SQL NULL, not ""
def test_falls_back_to_polish_when_english_is_empty(db, field, pl_value, en_value):
    place = PlaceFactory(**{f"{field}_pl": pl_value, f"{field}_en": en_value})

    with translation.override("en"):
        place.refresh_from_db()
        assert getattr(place, field) == pl_value
