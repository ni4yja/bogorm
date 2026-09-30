import uuid

from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.utils.translation import gettext_lazy as _


class PlaceCategory(models.IntegerChoices):
    LIBRARY = 10, _("Library")
    BOOKSHOP = 20, _("Bookshop")
    CULTURAL_CENTRE = 30, _("Cultural Centre")
    CAFE = 40, _("Café")
    MUSEUM = 50, _("Museum")
    OTHER = 60, _("Other")


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

    @property
    def lat(self):
        return self.location.y

    @property
    def lng(self):
        return self.location.x

    @classmethod
    def make_point(cls, lat, lng):
        return Point(lng, lat, srid=4326)
