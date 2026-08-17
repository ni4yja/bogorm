from rest_framework import serializers

from .models import Place


class CoordinatesMixin(serializers.Serializer):
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x


class PlaceSerializer(CoordinatesMixin, serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = [
            "id",
            "title",
            "description",
            "lat",
            "lng",
            "category",
            "address",
            "website",
            "created_at",
        ]


class PlaceMapSerializer(CoordinatesMixin, serializers.ModelSerializer):
    event_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Place
        fields = ["id", "title", "lat", "lng", "category", "event_count"]


class PlaceMinimalSerializer(CoordinatesMixin, serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ["id", "title", "lat", "lng"]
