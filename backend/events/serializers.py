from rest_framework import serializers

from places.models import Place

from .models import Event


class PlaceMinimalSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x

    class Meta:
        model = Place
        fields = ["id", "title", "lat", "lng"]


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "place",
            "title",
            "description",
            "event_time",
            "category",
            "created_at",
        ]


class EventListSerializer(serializers.ModelSerializer):
    place = PlaceMinimalSerializer(read_only=True)

    class Meta:
        model = Event
        fields = [
            "id",
            "place",
            "title",
            "description",
            "event_time",
            "category",
            "created_at",
        ]
