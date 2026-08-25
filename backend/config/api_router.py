from rest_framework_nested import routers

from events.views import AllEventsViewSet, EventViewSet
from places.views import PlaceViewSet

router = routers.DefaultRouter()
router.register("places", PlaceViewSet, basename="place")
router.register("events", AllEventsViewSet, basename="event")

places_router_nested = routers.NestedSimpleRouter(router, "places", lookup="place")
places_router_nested.register("events", EventViewSet, basename="place-events")

urlpatterns = router.urls + places_router_nested.urls
