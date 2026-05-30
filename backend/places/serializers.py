from rest_framework import serializers

from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x

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


class PlaceMapSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()
    event_count = serializers.IntegerField(read_only=True)

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x

    class Meta:
        model = Place
        fields = ["id", "title", "lat", "lng", "category", "event_count"]
