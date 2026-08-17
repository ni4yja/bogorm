from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import MapView, PlaceViewSet

router = DefaultRouter()
router.register("places", PlaceViewSet, basename="place")

urlpatterns = [
    path("map", MapView.as_view(), name="map"),
]
