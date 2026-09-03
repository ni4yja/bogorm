from rest_framework import serializers

from places.serializers import PlaceMinimalSerializer

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    is_bookmarked = serializers.BooleanField(read_only=True)

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
            "is_bookmarked",
        ]


class EventListSerializer(serializers.ModelSerializer):
    place = PlaceMinimalSerializer(read_only=True)
    is_bookmarked = serializers.BooleanField(read_only=True)

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
            "is_bookmarked",
        ]


class EventMinimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "title", "event_time", "category"]
