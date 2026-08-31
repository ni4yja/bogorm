from django.contrib.gis.geos import Polygon
from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from bookmarks.models import Bookmark
from events.models import Event

from .models import Place
from .serializers import PlaceMapSerializer, PlaceSerializer


class PlaceViewSet(ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def get_permissions(self):
        if self.action == "retrieve":
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(
        detail=True, methods=["post", "delete"], permission_classes=[IsAuthenticated]
    )
    def bookmark(self, request, pk=None):
        place = get_object_or_404(Place, pk=pk)

        if request.method == "POST":
            _, created = Bookmark.objects.get_or_create(user=request.user, place=place)
            return Response(
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )

        deleted_count, _ = Bookmark.objects.filter(
            user=request.user, place=place
        ).delete()
        if deleted_count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


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
