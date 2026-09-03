from drf_spectacular.utils import PolymorphicProxySerializer, extend_schema_field
from rest_framework import serializers

from events.serializers import EventMinimalSerializer
from places.serializers import PlaceMinimalSerializer

from .models import BOOKMARK_TYPES, Bookmark

# ---------------------------------------------------------------------------
# `target` is either a place or an event depending on `type`; this proxy
# tells drf-spectacular to document both real shapes instead of a
# hand-written stand-in that can drift from what get_target() returns.
#
# serializers is a dict (not a list) so the schema's discriminator values
# ("place"/"event") match what the API actually sends — a list would make
# drf-spectacular invent component names from the class names instead
# (e.g. "PlaceMinimal"), which wouldn't match the real "type" value.
# ---------------------------------------------------------------------------


class BookmarkPlaceTargetSerializer(PlaceMinimalSerializer):
    type = serializers.ChoiceField(choices=["place"], default="place")

    class Meta(PlaceMinimalSerializer.Meta):
        fields = [*PlaceMinimalSerializer.Meta.fields, "type"]


class BookmarkEventTargetSerializer(EventMinimalSerializer):
    type = serializers.ChoiceField(choices=["event"], default="event")

    class Meta(EventMinimalSerializer.Meta):
        fields = [*EventMinimalSerializer.Meta.fields, "type"]


BookmarkTargetSchema = PolymorphicProxySerializer(
    component_name="BookmarkTarget",
    serializers={
        "place": BookmarkPlaceTargetSerializer,
        "event": BookmarkEventTargetSerializer,
    },
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
