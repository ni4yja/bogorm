from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from events.serializers import EventMinimalSerializer
from places.serializers import PlaceMinimalSerializer

from .models import Bookmark


class BookmarkTargetSerializer(serializers.Serializer):
    """Documents the shape of `target` for OpenAPI — never used to
    serialize data directly, since the real fields differ by type."""

    type = serializers.ChoiceField(choices=["place", "event"])
    id = serializers.UUIDField()
    title = serializers.CharField()


class BookmarkSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ["id", "type", "target", "created_at"]

    @extend_schema_field(serializers.ChoiceField(choices=["place", "event"]))
    def get_type(self, obj):
        return "place" if obj.place_id else "event"

    @extend_schema_field(BookmarkTargetSerializer)
    def get_target(self, obj):
        bookmark_type = self.get_type(obj)
        if bookmark_type == "place":
            data = PlaceMinimalSerializer(obj.place).data
        else:
            data = EventMinimalSerializer(obj.event).data
        return {"type": bookmark_type, **data}
