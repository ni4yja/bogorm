from rest_framework import serializers

from places.serializers import PlaceMinimalSerializer

from .models import Event


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


class EventMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "event_time", "category"]
