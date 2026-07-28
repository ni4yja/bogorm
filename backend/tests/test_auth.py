from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from tests.factories import UserFactory


class TestLogin:
    def test_returns_tokens_with_valid_credentials(self, db):
        UserFactory(email="reader@bogorm.app", password="correcthorse123")
        client = APIClient()

        response = client.post(
            reverse("token_obtain_pair"),
            {"email": "reader@bogorm.app", "password": "correcthorse123"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_rejects_wrong_password(self, db):
        UserFactory(email="reader@bogorm.app", password="correcthorse123")
        client = APIClient()

        response = client.post(
            reverse("token_obtain_pair"),
            {"email": "reader@bogorm.app", "password": "wrongpassword"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_rejects_nonexistent_email(self, db):
        client = APIClient()

        response = client.post(
            reverse("token_obtain_pair"),
            {"email": "ghost@bogorm.app", "password": "whatever123"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTokenRefresh:
    def test_returns_new_access_token(self, db):
        UserFactory(email="reader@bogorm.app", password="correcthorse123")
        client = APIClient()

        login_response = client.post(
            reverse("token_obtain_pair"),
            {"email": "reader@bogorm.app", "password": "correcthorse123"},
        )
        refresh_token = login_response.data["refresh"]

        response = client.post(
            reverse("token_refresh"),
            {"refresh": refresh_token},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_rejects_invalid_refresh_token(self, db):
        client = APIClient()

        response = client.post(
            reverse("token_refresh"),
            {"refresh": "not-a-real-token"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
