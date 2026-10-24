import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from bookmarks.models import Bookmark
from tests.factories import PlaceFactory, UserFactory
from users.tokens import blacklist_all_tokens

User = get_user_model()

EMAIL = "reader@bogorm.app"
PASSWORD = "correcthorse123"


def register_payload(**overrides):
    payload = {
        "email": "newreader@bogorm.app",
        "username": "test",
        "password": "correcthorse123battery",
    }
    payload.update(overrides)
    return payload


def login(api_client, email=EMAIL, password=PASSWORD):
    """Log in, attach the access token to the client, return the token pair."""
    response = api_client.post(
        reverse("token_obtain_pair"), {"email": email, "password": password}
    )
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return response.data


def delete_me(api_client, password=PASSWORD):
    return api_client.delete(reverse("me"), {"password": password}, format="json")


@pytest.fixture
def reader(db):
    return UserFactory(email=EMAIL, username="reader", password=PASSWORD)


class TestLogin:
    def test_returns_tokens_with_valid_credentials(self, api_client, reader):
        response = api_client.post(
            reverse("token_obtain_pair"), {"email": EMAIL, "password": PASSWORD}
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data
        assert "refresh" in response.data

    def test_rejects_wrong_password(self, api_client, reader):
        response = api_client.post(
            reverse("token_obtain_pair"), {"email": EMAIL, "password": "wrongpassword"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_rejects_nonexistent_email(self, api_client, db):
        response = api_client.post(
            reverse("token_obtain_pair"),
            {"email": "ghost@bogorm.app", "password": "whatever123"},
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_is_case_insensitive_for_email(self, api_client, reader):
        response = api_client.post(
            reverse("token_obtain_pair"),
            {"email": "Reader@Bogorm.app", "password": PASSWORD},
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data


class TestTokenRefresh:
    def test_returns_new_access_token(self, api_client, reader):
        tokens = login(api_client)

        response = api_client.post(
            reverse("token_refresh"), {"refresh": tokens["refresh"]}
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access" in response.data

    def test_rotation_returns_new_refresh_token(self, api_client, reader):
        tokens = login(api_client)

        response = api_client.post(
            reverse("token_refresh"), {"refresh": tokens["refresh"]}
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["refresh"] != tokens["refresh"]

    def test_rejects_reused_refresh_token_after_rotation(self, api_client, reader):
        tokens = login(api_client)
        api_client.post(reverse("token_refresh"), {"refresh": tokens["refresh"]})

        response = api_client.post(
            reverse("token_refresh"), {"refresh": tokens["refresh"]}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

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

    @pytest.mark.parametrize(
        "password, rule",
        [
            ("kd9wpq", "too short"),
            ("password", "too common"),
            ("58201947", "entirely numeric"),
            ("newreader@bogorm.app", "too similar to the email"),
        ],
    )
    def test_rejects_password_violating_policy(self, api_client, db, password, rule):
        response = api_client.post(
            reverse("register"), register_payload(password=password)
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


class TestLogout:
    def test_returns_205_and_blacklists_token(self, api_client, reader):
        tokens = login(api_client)

        response = api_client.post(reverse("logout"), {"refresh": tokens["refresh"]})

        assert response.status_code == status.HTTP_205_RESET_CONTENT

        refresh_response = api_client.post(
            reverse("token_refresh"), {"refresh": tokens["refresh"]}
        )
        assert refresh_response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_requires_authentication(self, api_client, db):
        response = api_client.post(reverse("logout"), {"refresh": "irrelevant"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_rejects_missing_refresh_token(self, api_client, reader):
        login(api_client)

        response = api_client.post(reverse("logout"), {})

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_rejects_already_blacklisted_token(self, api_client, reader):
        tokens = login(api_client)
        api_client.post(reverse("logout"), {"refresh": tokens["refresh"]})

        response = api_client.post(reverse("logout"), {"refresh": tokens["refresh"]})

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestMeRetrieve:
    def test_returns_current_user(self, api_client, reader):
        login(api_client)

        response = api_client.get(reverse("me"))

        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"id": reader.id, "email": EMAIL, "username": "reader"}

    def test_requires_authentication(self, api_client, db):
        response = api_client.get(reverse("me"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestMeDelete:
    def test_deletes_user_and_their_bookmarks(self, api_client, reader):
        Bookmark.objects.create(user=reader, place=PlaceFactory())
        login(api_client)

        response = delete_me(api_client)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not User.objects.filter(pk=reader.pk).exists()
        assert not Bookmark.objects.filter(user_id=reader.pk).exists()

    def test_keeps_other_users_bookmarks(self, api_client, reader):
        other = UserFactory()
        Bookmark.objects.create(user=other, place=PlaceFactory())
        login(api_client)

        delete_me(api_client)

        assert Bookmark.objects.filter(user=other).exists()

    @pytest.mark.parametrize("payload", [{"password": "wrongpassword"}, {}])
    def test_rejects_wrong_or_missing_password(self, api_client, reader, payload):
        login(api_client)

        response = api_client.delete(reverse("me"), payload, format="json")

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "password" in response.data
        assert User.objects.filter(pk=reader.pk).exists()

    def test_rejects_staff_account(self, api_client, db):
        staff = UserFactory(email="admin@bogorm.app", password=PASSWORD, is_staff=True)
        login(api_client, email="admin@bogorm.app")

        response = delete_me(api_client)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert User.objects.filter(pk=staff.pk).exists()

    def test_requires_authentication(self, api_client, db):
        response = delete_me(api_client)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_refresh_token_is_dead_after_deletion(self, api_client, reader):
        tokens = login(api_client)
        delete_me(api_client)
        api_client.credentials()

        response = api_client.post(
            reverse("token_refresh"), {"refresh": tokens["refresh"]}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_token_is_dead_after_deletion(self, api_client, reader):
        login(api_client)
        delete_me(api_client)

        response = api_client.get(reverse("me"))

        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestBlacklistAllTokens:
    def test_blacklists_every_token_and_skips_already_blacklisted(
        self, api_client, reader
    ):
        first = login(api_client)
        login(api_client)
        api_client.post(reverse("logout"), {"refresh": first["refresh"]})

        blacklist_all_tokens(reader)

        outstanding = OutstandingToken.objects.filter(user=reader)
        assert outstanding.count() == 2
        assert BlacklistedToken.objects.filter(token__in=outstanding).count() == 2
