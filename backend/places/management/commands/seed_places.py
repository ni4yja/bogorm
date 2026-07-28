from django.core.management.base import BaseCommand

from places.models import PlaceCategory
from tests.factories import PlaceFactory

PLACES_PER_CATEGORY = 3


class Command(BaseCommand):
    help = "Seed database with test places across Warsaw, covering all categories"

    def handle(self, *args, **kwargs):
        for category in PlaceCategory:
            for _ in range(PLACES_PER_CATEGORY):
                place = PlaceFactory(category=category)
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {place.title} ({category.label})")
                )

        self.stdout.write(self.style.SUCCESS("Done!"))
