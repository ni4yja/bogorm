from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Bookmark


class BookmarkStateSerializer(serializers.Serializer):
    bookmarked = serializers.BooleanField()


class BookmarkableMixin:
    # ------------------------------------------------------------
    # Adds PUT :id/bookmark/ to a ViewSet.
    #
    # Set `bookmark_field` on the ViewSet to the Bookmark FK name
    # that corresponds to this resource ("place" or "event").
    #
    # Body: {"bookmarked": true|false} — idempotent, always returns
    # the resulting state.
    # ------------------------------------------------------------

    bookmark_field = None

    @action(detail=True, methods=["put"], permission_classes=[IsAuthenticated])
    def bookmark(self, request, pk=None):
        state = BookmarkStateSerializer(data=request.data)
        state.is_valid(raise_exception=True)

        obj = self.get_object()

        if state.validated_data["bookmarked"]:
            Bookmark.objects.get_or_create(
                user=request.user, **{self.bookmark_field: obj}
            )
        else:
            Bookmark.objects.filter(
                user=request.user, **{self.bookmark_field: obj}
            ).delete()

        return Response(
            {"bookmarked": state.validated_data["bookmarked"]},
            status=status.HTTP_200_OK,
        )
