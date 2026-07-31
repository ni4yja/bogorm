import pytest
from rest_framework.test import APIClient

from tests.factories import EventFactory, UserFactory, WarsawPlaceFactory


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def place(db):
    return WarsawPlaceFactory()


@pytest.fixture
def event(db, place):
    return EventFactory(place=place)
