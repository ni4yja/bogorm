from rest_framework_nested import routers

from places.views import PlaceViewSet

from .views import EventViewSet

router = routers.SimpleRouter()
router.register("places", PlaceViewSet, basename="place")

places_router = routers.NestedSimpleRouter(router, "places", lookup="place")
places_router.register("events", EventViewSet, basename="place-events")

urlpatterns = router.urls + places_router.urls
