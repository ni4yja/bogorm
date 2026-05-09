import uuid
from django.contrib.gis.db import models # pyright: ignore[reportMissingModuleSource]
from django.contrib.gis.geos import Point # pyright: ignore[reportMissingModuleSource]


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
    lat = models.FloatField()
    lng = models.FloatField()
    location = models.PointField(blank=True, null=True)
    category = models.IntegerField(
        choices=PlaceCategory.choices,
        default=PlaceCategory.OTHER
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.location = Point(self.lng, self.lat)
        super().save(*args, **kwargs)