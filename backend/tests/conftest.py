import pytest
from django.contrib.gis.geos import Point
from rest_framework.test import APIClient

from places.models import Place, PlaceCategory


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def place(db):
    return Place.objects.create(
        title="Poliglotka",
        description="Library on your favorite street",
        location=Point(24.03, 49.84, srid=4326),
        category=PlaceCategory.LIBRARY,
    )
