import pytest
from django.urls import reverse
from rest_framework import status

from tests.factories import UserFactory


def register_payload(**overrides):
    payload = {
        "email": "newreader@bogorm.app",
        "username": "test",
        "password": "correcthorse123battery",
    }
    payload.update(overrides)
    return payload


class TestLogin:
    def test_returns_tokens_with_valid_credentials(self, api_client, db):
        UserFactory(email="reader@bogorm.app", password="correcthorse123")

        response = api_client.post(
            reverse("token_obtain_pair"),
            {"email": "reader@bogorm.app", "password": "correcthorse123"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_rejects_wrong_password(self, api_client, db):
        UserFactory(email="reader@bogorm.app", password="correcthorse123")

        response = api_client.post(
            reverse("token_obtain_pair"),
            {"email": "reader@bogorm.app", "password": "wrongpassword"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_rejects_nonexistent_email(self, api_client, db):
        response = api_client.post(
            reverse("token_obtain_pair"),
            {"email": "ghost@bogorm.app", "password": "whatever123"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestTokenRefresh:
    def test_returns_new_access_token(self, api_client, db):
        UserFactory(email="reader@bogorm.app", password="correcthorse123")

        login_response = api_client.post(
            reverse("token_obtain_pair"),
            {"email": "reader@bogorm.app", "password": "correcthorse123"},
        )
        refresh_token = login_response.data["refresh"]

        response = api_client.post(reverse("token_refresh"), {"refresh": refresh_token})

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_rejects_invalid_refresh_token(self, api_client, db):
        response = api_client.post(
            reverse("token_refresh"), {"refresh": "not-a-real-token"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestRegister:
    def test_creates_user_with_valid_data(self, api_client, db):
        response = api_client.post(reverse("register"), register_payload())

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["email"] == "newreader@bogorm.app"
        assert response.data["username"] == "test"
        assert "password" not in response.data

    def test_rejects_duplicate_email(self, api_client, db):
        UserFactory(email="taken@bogorm.app")

        response = api_client.post(
            reverse("register"), register_payload(email="taken@bogorm.app")
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.data

    def test_rejects_weak_password(self, api_client, db):
        response = api_client.post(
            reverse("register"), register_payload(password="12345")
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data

    @pytest.mark.parametrize("missing_field", ["email", "username", "password"])
    def test_rejects_missing_field(self, api_client, db, missing_field):
        payload = register_payload()
        del payload[missing_field]

        response = api_client.post(reverse("register"), payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert missing_field in response.data


class TestRegisterAndLoginFlow:
    def test_registered_user_can_log_in(self, api_client, db):
        api_client.post(reverse("register"), register_payload())

        response = api_client.post(
            reverse("token_obtain_pair"),
            {"email": "newreader@bogorm.app", "password": "correcthorse123battery"},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
