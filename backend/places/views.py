from django.contrib.gis.geos import Polygon
from django.db.models import Count, Exists, OuterRef, Q
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from bookmarks.mixins import BookmarkableMixin
from bookmarks.models import Bookmark
from events.models import Event

from .models import Place
from .serializers import PlaceMapSerializer, PlaceSerializer


class PlaceViewSet(BookmarkableMixin, ReadOnlyModelViewSet):
    serializer_class = PlaceSerializer
    bookmark_field = "place"

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            is_bookmarked = Exists(
                Bookmark.objects.filter(user=user, place=OuterRef("pk"))
            )
        else:
            is_bookmarked = Q(pk__isnull=True)  # always False, no query needed

        return Place.objects.annotate(is_bookmarked=is_bookmarked)

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny()]
        return super().get_permissions()


class MapView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        bbox = request.query_params.get("bbox")
        if not bbox:
            raise ValidationError("bbox query parameter is required")

        try:
            min_lng, min_lat, max_lng, max_lat = map(float, bbox.split(","))
        except ValueError:
            raise ValidationError("bbox must be: minLng,minLat,maxLng,maxLat")

        bounds = Polygon.from_bbox((min_lng, min_lat, max_lng, max_lat))
        bounds.srid = 4326

        places = Place.objects.filter(location__within=bounds).annotate(
            event_count=Count("events", filter=Event.objects.upcoming_filter())
        )

        serializer = PlaceMapSerializer(places, many=True)
        return Response({"places": serializer.data})
