from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.viewsets import ReadOnlyModelViewSet

from places.models import Place

from .filters import EventFilterSet
from .models import Event, EventCategory
from .serializers import EventListSerializer, EventSerializer


class EventViewSet(ReadOnlyModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        place = get_object_or_404(Place, pk=self.kwargs["place_pk"])
        return Event.objects.upcoming().filter(place=place)


class AllEventsViewSet(ReadOnlyModelViewSet):
    serializer_class = EventListSerializer
    filterset_class = EventFilterSet
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return Event.objects.select_related("place")

    def filter_queryset(self, queryset):
        if self.action != "list":
            return queryset
        return super().filter_queryset(queryset)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="status",
                type=str,
                enum=["upcoming", "archived"],
                default="upcoming",
                description="Defaults to 'upcoming' if omitted.",
            ),
            OpenApiParameter(
                name="week",
                type=str,
                enum=["current"],
                required=False,
                description="Only valid when status is 'upcoming'.",
            ),
            OpenApiParameter(
                name="category",
                type=int,
                enum=[choice.value for choice in EventCategory],
                required=False,
                description="Optional — no filtering applied if omitted.",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
