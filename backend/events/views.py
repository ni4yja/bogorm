from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet

from places.models import Place

from .models import Event
from .serializers import EventListSerializer, EventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        place = get_object_or_404(Place, pk=self.kwargs["place_pk"])
        return Event.objects.upcoming().filter(place=place).order_by("event_time")


class AllEventsViewSet(ReadOnlyModelViewSet):
    serializer_class = EventListSerializer

    def get_queryset(self):
        status_param = self.request.query_params.get("status", "upcoming")

        if status_param == "upcoming":
            queryset = Event.objects.upcoming().order_by("event_time")
        elif status_param == "archived":
            queryset = Event.objects.archived().order_by("-event_time")
        else:
            raise ValidationError({"status": "Must be 'upcoming' or 'archived'."})

        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        return queryset
