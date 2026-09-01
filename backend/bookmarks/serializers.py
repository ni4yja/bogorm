from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema_field
from rest_framework import serializers

from events.serializers import EventMinimalSerializer
from places.serializers import PlaceMinimalSerializer

from .models import BOOKMARK_TYPES, Bookmark

# ---------------------------------------------------------------------------
# `target` is either a place or an event depending on `type`; this proxy
# tells drf-spectacular to document both real shapes instead of a
# hand-written stand-in that can drift from what get_target() returns.
# ---------------------------------------------------------------------------

BookmarkTargetSchema = PolymorphicProxySerializer(
    component_name="BookmarkTarget",
    serializers=[PlaceMinimalSerializer, EventMinimalSerializer],
    resource_type_field_name="type",
)


class BookmarkSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ["id", "type", "target", "created_at"]

    @extend_schema_field(serializers.ChoiceField(choices=BOOKMARK_TYPES))
    def get_type(self, obj):
        return "place" if obj.place_id else "event"

    @extend_schema_field(BookmarkTargetSchema)
    def get_target(self, obj):
        bookmark_type = self.get_type(obj)
        if bookmark_type == "place":
            data = PlaceMinimalSerializer(obj.place).data
        else:
            data = EventMinimalSerializer(obj.event).data
        return {"type": bookmark_type, **data}
