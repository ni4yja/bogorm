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
            'id',
            'title',
            'description',
            'lat',
            'lng',
            'category',
            'created_at',
        ]