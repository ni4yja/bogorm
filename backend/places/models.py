import uuid

from django.contrib.gis.db import models


class PlaceCategory(models.IntegerChoices):
    LIBRARY = 10, "Library"
    BOOKSHOP = 20, "Bookshop"
    CULTURAL_CENTRE = 30, "Cultural Centre"
    CAFE = 40, "Café"
    MUSEUM = 50, "Museum"
    OTHER = 60, "Other"


class Place(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    location = models.PointField()
    category = models.IntegerField(
        choices=PlaceCategory.choices, default=PlaceCategory.OTHER
    )
    address = models.CharField(max_length=255, blank=True, default="")
    website = models.URLField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
