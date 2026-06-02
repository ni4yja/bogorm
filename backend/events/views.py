from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet

from places.models import Place

from .models import Event
from .serializers import EventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        place = get_object_or_404(Place, pk=self.kwargs["place_pk"])
        return Event.objects.filter(place=place)
