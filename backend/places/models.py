import uuid

from django.contrib.gis.db import models


class PlaceCategory(models.IntegerChoices):
    LIBRARY = 10, 'Library'
    BOOKSHOP = 20, 'Bookshop'
    CULTURAL_CENTRE = 30, 'Cultural Centre'
    CAFE = 40, 'Café'
    MUSEUM = 50, 'Museum'
    OTHER = 60, 'Other'


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    location = models.PointField()
    category = models.IntegerField(
        choices=PlaceCategory.choices,
        default=PlaceCategory.OTHER
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title