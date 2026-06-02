import factory
from django.contrib.gis.geos import Point

from events.models import Event, EventCategory
from places.models import Place, PlaceCategory


class PlaceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Place

    title = factory.Faker("company")
    description = factory.Faker("text")
    location = factory.LazyFunction(lambda: Point(21.01, 52.23, srid=4326))
    category = PlaceCategory.LIBRARY


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    place = factory.SubFactory(PlaceFactory)
    title = factory.Faker("sentence", nb_words=4)
    description = factory.Faker("text")
    category = EventCategory.OTHER
