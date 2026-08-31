from rest_framework import serializers

from events.serializers import EventMinimalSerializer
from places.serializers import PlaceMinimalSerializer

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    place = PlaceMinimalSerializer(read_only=True)
    event = EventMinimalSerializer(read_only=True)

    class Meta:
        model = Bookmark
        fields = ["id", "type", "place", "event", "created_at"]

    def get_type(self, obj):
        return "place" if obj.place_id else "event"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if data["place"] is None:
            data.pop("place")
        else:
            data.pop("event")
        return data
