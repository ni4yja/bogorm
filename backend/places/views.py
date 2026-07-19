from django.contrib.gis.geos import Polygon
from django.db.models import Count, Q
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Place
from .serializers import PlaceMapSerializer, PlaceSerializer


class PlaceViewSet(ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class MapView(APIView):
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
            event_count=Count("events", filter=Q(events__event_time__gt=timezone.now()))
        )

        serializer = PlaceMapSerializer(places, many=True)
        return Response({"places": serializer.data})
