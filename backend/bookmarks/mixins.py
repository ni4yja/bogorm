from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Bookmark


class BookmarkableMixin:
    # ------------------------------------------------------------
    # Adds PUT/DELETE :id/bookmark/ to a ViewSet.
    #
    # Set `bookmark_field` on the ViewSet to the Bookmark FK name
    # that corresponds to this resource ("place" or "event").
    #
    # No request body — both methods are idempotent and always
    # return {"bookmarked": true|false}.
    # ------------------------------------------------------------

    bookmark_field = None

    @action(
        detail=True, methods=["put", "delete"], permission_classes=[IsAuthenticated]
    )
    def bookmark(self, request, pk=None):
        obj = self.get_object()

        if request.method == "PUT":
            Bookmark.objects.get_or_create(
                user=request.user, **{self.bookmark_field: obj}
            )
            bookmarked = True
        else:
            Bookmark.objects.filter(
                user=request.user, **{self.bookmark_field: obj}
            ).delete()
            bookmarked = False

        return Response({"bookmarked": bookmarked})
