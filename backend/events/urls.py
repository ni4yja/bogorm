from rest_framework_nested import routers

from places.urls import router as places_router

from .views import AllEventsViewSet, EventViewSet

places_router.register("events", AllEventsViewSet, basename="event")

places_router_nested = routers.NestedSimpleRouter(
    places_router, "places", lookup="place"
)
places_router_nested.register("events", EventViewSet, basename="place-events")

urlpatterns = places_router_nested.urls
