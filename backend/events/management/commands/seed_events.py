from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from tests.factories import EventFactory, WarsawPlaceFactory


class Command(BaseCommand):
    help = "Seed database with test events relative to today"

    def handle(self, *args, **kwargs):
        place = WarsawPlaceFactory()
        now = timezone.now()

        deltas = [
            ("Past event (last month)", timedelta(days=-30)),
            ("Past event (last week)", timedelta(days=-7)),
            ("Past event (yesterday)", timedelta(days=-1)),
            ("Upcoming event (tomorrow)", timedelta(days=1)),
            ("Upcoming event (this week)", timedelta(days=5)),
            ("Upcoming event (this month)", timedelta(days=20)),
            ("Upcoming event (next month)", timedelta(days=40)),
        ]

        for title, delta in deltas:
            EventFactory(place=place, title=title, event_time=now + delta)
            self.stdout.write(self.style.SUCCESS(f"Created: {title}"))

        self.stdout.write(self.style.SUCCESS("Done!"))
