from rest_framework import serializers

from .models import Place


class CoordinatesMixin(serializers.Serializer):
    lat = serializers.FloatField(read_only=True)
    lng = serializers.FloatField(read_only=True)


class PlaceSerializer(CoordinatesMixin, serializers.ModelSerializer):
    is_bookmarked = serializers.BooleanField(read_only=True)

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
            "is_bookmarked",
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
