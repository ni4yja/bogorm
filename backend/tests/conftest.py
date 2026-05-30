import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient

from events.models import Event, EventCategory
from places.models import Place, PlaceCategory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def place(db):
    return Place.objects.create(
        title="Poliglotka",
        description="Library on your favorite street",
        location=Point(21.01, 52.23, srid=4326),
        category=PlaceCategory.LIBRARY,
    )


@pytest.fixture
def event(db, place):
    return Event.objects.create(
        place=place,
        title="Test Event",
        category=EventCategory.OTHER,
    )
