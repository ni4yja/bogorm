import uuid

from django.conf import settings
from django.db import models

from events.models import Event
from places.models import Place

BOOKMARK_TYPES = ("place", "event")


class Bookmark(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookmarks"
    )
    place = models.ForeignKey(
        Place, null=True, blank=True, on_delete=models.CASCADE, related_name="bookmarks"
    )
    event = models.ForeignKey(
        Event, null=True, blank=True, on_delete=models.CASCADE, related_name="bookmarks"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "place"],
                condition=models.Q(place__isnull=False),
                name="unique_user_place_bookmark",
            ),
            models.UniqueConstraint(
                fields=["user", "event"],
                condition=models.Q(event__isnull=False),
                name="unique_user_event_bookmark",
            ),
            models.CheckConstraint(
                check=(
                    models.Q(place__isnull=False, event__isnull=True)
                    | models.Q(place__isnull=True, event__isnull=False)
                ),
                name="bookmark_exactly_one_of_place_or_event",
            ),
        ]

    def __str__(self):
        target = self.place or self.event
        return f"{self.user} → {target}"
