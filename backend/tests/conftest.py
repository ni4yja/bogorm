import pytest
from rest_framework.test import APIClient

from tests.factories import EventFactory, WarsawPlaceFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def place(db):
    return WarsawPlaceFactory()


@pytest.fixture
def event(db, place):
    return EventFactory(place=place)
