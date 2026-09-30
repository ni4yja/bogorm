import pytest
from django.urls import reverse
from rest_framework import status

from events.models import EventCategory
from places.models import PlaceCategory


@pytest.mark.parametrize(
    "lang, expected",
    [
        ("pl", "Parametr zapytania bbox jest wymagany"),
        ("en", "bbox query parameter is required"),
    ],
)
def test_custom_message_follows_accept_language(api_client, db, lang, expected):
    response = api_client.get(reverse("map"), headers={"Accept-Language": lang})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0] == expected


def test_falls_back_to_polish_without_accept_language(api_client, db):
    response = api_client.get(reverse("map"))

    assert response.data[0] == "Parametr zapytania bbox jest wymagany"


def test_message_with_placeholder_is_translated(authenticated_client, db):
    response = authenticated_client.get(
        reverse("bookmark-list"),
        {"type": "banana"},
        headers={"Accept-Language": "pl"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["type"][0] == "Dozwolone wartości: place, event."


def test_django_validation_message_is_polish(authenticated_client, db):
    response = authenticated_client.get(
        reverse("event-list"),
        {"status": "blah"},
        headers={"Accept-Language": "pl"},
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "status" in response.data
    assert "blah" in str(response.data["status"])
    assert "Select a valid choice" not in str(response.data["status"])


@pytest.mark.parametrize(
    "category, pl_label",
    [
        (PlaceCategory.LIBRARY, "Biblioteka"),
        (PlaceCategory.CAFE, "Kawiarnia"),
        (EventCategory.LECTURE, "Wykład"),
        (EventCategory.BOOK_CLUB, "Klub książki"),
    ],
)
def test_category_label_is_translated(category, pl_label):
    from django.utils import translation

    with translation.override("pl"):
        assert str(category.label) == pl_label
    with translation.override("en"):
        assert str(category.label) != pl_label


def test_response_varies_by_language(api_client, db):
    response = api_client.get(reverse("map"))

    assert "Accept-Language" in response["Vary"]
