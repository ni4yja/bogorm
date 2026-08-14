import uuid
from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone

from places.models import Place


class EventCategory(models.IntegerChoices):
    BOOK_PRESENTATION = 10, "Book Presentation"
    AUTHOR_MEETING = 20, "Author Meeting"
    DISCUSSION = 30, "Discussion"
    LECTURE = 40, "Lecture"
    BOOK_CLUB = 50, "Book Club"
    OTHER = 60, "Other"


class EventQuerySet(models.QuerySet):
    def upcoming(self):
        return self.filter(event_time__gt=timezone.now()).order_by("event_time")

    def archived(self):
        return self.filter(event_time__lte=timezone.now()).order_by("-event_time")

    def this_week(self):
        now = timezone.now()
        start_of_week = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_of_week = start_of_week + timedelta(days=7)
        return self.filter(event_time__gte=start_of_week, event_time__lt=end_of_week)


class EventManager(models.Manager):
    def get_queryset(self):
        return EventQuerySet(self.model, using=self._db)

    def upcoming(self):
        return self.get_queryset().upcoming()

    def archived(self):
        return self.get_queryset().archived()

    def this_week(self):
        return self.get_queryset().this_week()

    @staticmethod
    def upcoming_filter():
        return Q(events__event_time__gt=timezone.now())


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    event_time = models.DateTimeField()
    category = models.IntegerField(
        choices=EventCategory.choices,
        default=EventCategory.OTHER,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    objects = EventManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
