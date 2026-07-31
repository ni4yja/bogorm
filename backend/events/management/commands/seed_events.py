import random
from datetime import timedelta

from django.conf import settings
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Event
from places.models import Place

EVENT_TEMPLATES = [
    ("Past event (last month)", timedelta(days=-30)),
    ("Past event (last week)", timedelta(days=-7)),
    ("Past event (yesterday)", timedelta(days=-1)),
    ("Upcoming event (tomorrow)", timedelta(days=1)),
    ("Upcoming event (this week)", timedelta(days=5)),
    ("Upcoming event (this month)", timedelta(days=20)),
    ("Upcoming event (next month)", timedelta(days=40)),
]


class Command(BaseCommand):
    help = "Seed database with test events spread across existing places"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing events before seeding",
        )

    def handle(self, *args, **options):
        if not settings.SEED_COMMANDS_ENABLED:
            raise CommandError(
                "Seed commands are disabled in this environment "
                "(SEED_COMMANDS_ENABLED=False)."
            )

        from tests.factories import EventFactory

        if options["clear"]:
            deleted_count, _ = Event.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} events"))

        places = list(Place.objects.all())

        if not places:
            raise CommandError(
                "No places found. Run `seed_places` before `seed_events`."
            )

        now = timezone.now()

        for title, delta in EVENT_TEMPLATES:
            place = random.choice(places)
            EventFactory(place=place, title=title, event_time=now + delta)
            self.stdout.write(self.style.SUCCESS(f"Created: {title} @ {place.title}"))

        self.stdout.write(self.style.SUCCESS("Done!"))
