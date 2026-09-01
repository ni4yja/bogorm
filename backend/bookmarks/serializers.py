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
        bookmark_type = self.get_type(obj)
        if bookmark_type == "place":
            data = PlaceMinimalSerializer(obj.place).data
        else:
            data = EventMinimalSerializer(obj.event).data
        return {"type": bookmark_type, **data}
