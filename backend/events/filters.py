import django_filters
from rest_framework.exceptions import ValidationError

from .models import Event


class EventFilterSet(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=[("upcoming", "Upcoming"), ("archived", "Archived")],
        method="noop",
    )
    week = django_filters.ChoiceFilter(
        choices=[("current", "Current")],
        method="noop",
    )

    class Meta:
        model = Event
        # category auto-generates a ChoiceFilter from the model's
        # IntegerField(choices=EventCategory.choices) — validates itself
        fields = ["status", "week", "category"]

    def noop(self, queryset, name, value):
        # status/week need cross-field logic, so real filtering happens
        # in `qs` below — these methods only exist so django-filter
        # validates the choices and shows the fields in the schema.
        return queryset

    @property
    def qs(self):
        queryset = super().qs  # validates status/week/category choices

        status_value = self.data.get("status") or "upcoming"
        queryset = (
            queryset.upcoming() if status_value == "upcoming" else queryset.archived()
        )

        week_value = self.data.get("week")
        if week_value == "current":
            if status_value != "upcoming":
                raise ValidationError({"week": "Only valid when status is 'upcoming'."})
            queryset = queryset.this_week()

        return queryset
