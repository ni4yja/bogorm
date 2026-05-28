from rest_framework import serializers

from .models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "place",
            "title",
            "description",
            "event_date",
            "event_time",
            "created_at",
        ]
