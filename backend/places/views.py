from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
