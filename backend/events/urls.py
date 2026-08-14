from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from places.urls import router as places_router

from .views import AllEventsViewSet, EventViewSet

places_router_nested = routers.NestedSimpleRouter(
    places_router, "places", lookup="place"
)
places_router_nested.register("events", EventViewSet, basename="place-events")

events_router = DefaultRouter()
events_router.register("events", AllEventsViewSet, basename="event")

urlpatterns = places_router_nested.urls + events_router.urls
