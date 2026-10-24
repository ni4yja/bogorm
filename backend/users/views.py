from django.db import transaction
from django.utils.translation import gettext as _
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import (
    CurrentUserSerializer,
    DeleteAccountSerializer,
    EmailNormalizingTokenObtainPairSerializer,
    RegisterSerializer,
)
from .tokens import blacklist_all_tokens


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class EmailNormalizingTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailNormalizingTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": _("refresh token is required")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {"error": _("invalid or already blacklisted token")},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(status=status.HTTP_205_RESET_CONTENT)


class CurrentUserView(generics.RetrieveDestroyAPIView):
    serializer_class = CurrentUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    @extend_schema(request=DeleteAccountSerializer, responses={204: None})
    def delete(self, request, *args, **kwargs):
        user = self.get_object()

        # Staff accounts are managed in Django Admin only
        if user.is_staff:
            raise PermissionDenied(_("Staff accounts cannot be deleted via the API."))

        serializer = DeleteAccountSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            blacklist_all_tokens(user)
            user.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
