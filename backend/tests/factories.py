import random

import factory
from django.contrib.gis.geos import Point

from events.models import Event, EventCategory
from places.models import Place, PlaceCategory

WARSAW_POINT = Point(21.01, 52.23, srid=4326)


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Place

    title = factory.Faker("company")
    description = factory.Faker("text")
    location = factory.LazyFunction(
        lambda: Point(
            random.uniform(20.85, 21.27),  # longitude
            random.uniform(52.10, 52.36),  # latitude
            srid=4326,
        )
    )
    category = PlaceCategory.LIBRARY


class WarsawPlaceFactory(PlaceFactory):
    location = WARSAW_POINT


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    place = factory.SubFactory(PlaceFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text")
    category = EventCategory.OTHER
