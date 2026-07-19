from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from events.models import Event
from places.models import Place


class Command(BaseCommand):
    help = "Seed database with test events relative to today"

    def handle(self, *args, **kwargs):
        places = Place.objects.all()

        if not places.exists():
            self.stdout.write(self.style.ERROR("No places found. Add places first."))
            return

        place = places.first()
        now = timezone.now()

        events = [
            {"title": "Past event (last month)", "delta": timedelta(days=-30)},
            {"title": "Past event (last week)", "delta": timedelta(days=-7)},
            {"title": "Past event (yesterday)", "delta": timedelta(days=-1)},
            {"title": "Upcoming event (tomorrow)", "delta": timedelta(days=1)},
            {"title": "Upcoming event (this week)", "delta": timedelta(days=5)},
            {"title": "Upcoming event (this month)", "delta": timedelta(days=20)},
            {"title": "Upcoming event (next month)", "delta": timedelta(days=40)},
        ]

        for e in events:
            Event.objects.create(
                place=place,
                title=e["title"],
                event_time=now + e["delta"],
            )
            self.stdout.write(self.style.SUCCESS(f"Created: {e['title']}"))

        self.stdout.write(self.style.SUCCESS("Done!"))
