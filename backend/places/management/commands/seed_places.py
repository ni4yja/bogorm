from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand

from places.models import Place, PlaceCategory

PLACES_PER_CATEGORY = 3


class Command(BaseCommand):
    help = "Seed database with test places across Warsaw, covering all categories"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing places before seeding",
        )

    def handle(self, *args, **options):
        if not settings.SEED_COMMANDS_ENABLED:
            raise CommandError(
                "Seed commands are disabled in this environment "
                "(SEED_COMMANDS_ENABLED=False)."
            )

        from tests.factories import PlaceFactory

        if options["clear"]:
            deleted_count, _ = Place.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} places"))

        for category in PlaceCategory:
            for _ in range(PLACES_PER_CATEGORY):
                place = PlaceFactory(category=category)
                self.stdout.write(
                    self.style.SUCCESS(f"Created: {place.title} ({category.label})")
                )

        self.stdout.write(self.style.SUCCESS("Done!"))
