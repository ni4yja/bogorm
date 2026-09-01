from rest_framework import serializers

from events.serializers import EventMinimalSerializer
from places.serializers import PlaceMinimalSerializer

from .models import Bookmark


class BookmarkSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ["id", "type", "target", "created_at"]

    def get_type(self, obj):
        return "place" if obj.place_id else "event"

    def get_target(self, obj):
        if obj.place_id:
            return PlaceMinimalSerializer(obj.place).data
        return EventMinimalSerializer(obj.event).data
