from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ReadOnlyModelViewSet

from places.models import Place

from .filters import EventFilterSet
from .models import Event
from .serializers import EventListSerializer, EventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        place = get_object_or_404(Place, pk=self.kwargs["place_pk"])
        return Event.objects.upcoming().filter(place=place)


class AllEventsViewSet(ReadOnlyModelViewSet):
    serializer_class = EventListSerializer
    filterset_class = EventFilterSet

    def get_queryset(self):
        return Event.objects.select_related("place")

    def filter_queryset(self, queryset):
        if self.action != "list":
            return queryset
        return DjangoFilterBackend().filter_queryset(self.request, queryset, self)
