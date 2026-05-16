from rest_framework.generics import (  # pyright: ignore[reportMissingImports]
    ListAPIView,
    RetrieveAPIView,
)

from .models import Place
from .serializers import PlaceSerializer


class PlaceListView(ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class PlaceDetailView(RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer