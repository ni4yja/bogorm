from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Bookmark
from .serializers import BookmarkSerializer

VALID_TYPES = ("place", "event")


class BookmarkViewSet(ReadOnlyModelViewSet):
    serializer_class = BookmarkSerializer
    http_method_names = ["get", "options", "head"]

    def get_queryset(self):
        queryset = Bookmark.objects.filter(user=self.request.user).select_related(
            "place", "event"
        )

        type_param = self.request.query_params.get("type")
        if type_param is not None:
            if type_param not in VALID_TYPES:
                raise ValidationError(
                    {"type": f"Must be one of: {', '.join(VALID_TYPES)}."}
                )
            queryset = queryset.filter(**{f"{type_param}__isnull": False})

        return queryset

    @action(detail=False, methods=["get"])
    def ids(self, request):
        bookmarks = self.get_queryset().values_list("place_id", "event_id")
        place_ids = [str(place_id) for place_id, _ in bookmarks if place_id]
        event_ids = [str(event_id) for _, event_id in bookmarks if event_id]

        return Response({"place_ids": place_ids, "event_ids": event_ids})
