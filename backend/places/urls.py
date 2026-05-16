from django.urls import path

from .views import PlaceDetailView, PlaceListView

urlpatterns = [
    path('places/', PlaceListView.as_view(), name='place-list'),
    path('places/<uuid:pk>/', PlaceDetailView.as_view(), name='place-detail'),
]