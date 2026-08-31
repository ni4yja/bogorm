from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Bookmark


class BookmarkableMixin:
    """Adds POST/DELETE :id/bookmark/ to a ViewSet.

    Set `bookmark_field` on the ViewSet to the Bookmark FK name
    that corresponds to this resource ("place" or "event").
    """

    bookmark_field = None

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def bookmark(self, request, pk=None):
        obj = get_object_or_404(self.get_queryset().model, pk=pk)

        if request.method == "POST":
            _, created = Bookmark.objects.get_or_create(
                user=request.user, **{self.bookmark_field: obj}
            )
            return Response(
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        deleted_count, _ = Bookmark.objects.filter(
            user=request.user, **{self.bookmark_field: obj}
        ).delete()
        if deleted_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
