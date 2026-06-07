import pytest
from rest_framework.test import APIClient

from tests.factories import EventFactory, PlaceFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def place(db):
    return PlaceFactory()


@pytest.fixture
def event(db, place):
    return EventFactory(place=place)
