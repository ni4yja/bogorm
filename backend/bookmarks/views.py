from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Bookmark
from .serializers import BookmarkSerializer


class BookmarkViewSet(ReadOnlyModelViewSet):
    serializer_class = BookmarkSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        queryset = Bookmark.objects.filter(user=self.request.user).select_related(
            "place", "event"
        )

        type_param = self.request.query_params.get("type")
        if type_param == "place":
            queryset = queryset.filter(place__isnull=False)
        elif type_param == "event":
            queryset = queryset.filter(event__isnull=False)

        return queryset
