import django_filters
from django_filters.rest_framework import FilterSet
from rest_framework.exceptions import ValidationError

from .models import Event, EventCategory


class EventFilterSet(FilterSet):
    status = django_filters.ChoiceFilter(
        choices=[("upcoming", "Upcoming"), ("archived", "Archived")],
        method="noop",
    )
    week = django_filters.ChoiceFilter(
        choices=[("current", "Current")],
        method="noop",
    )
    category = django_filters.ChoiceFilter(
        choices=EventCategory.choices,
        method="noop",
    )

    class Meta:
        model = Event
        fields = ["status", "week", "category"]

    def noop(self, queryset, name, value):
        # status/week/category need cross-field logic or run in `qs` below
        # for consistent error messages — these methods only exist so
        # django-filter validates the choices and shows the fields in
        # the schema.
        return queryset

    @property
    def qs(self):
        queryset = super().qs  # validates status/week/category choices

        status_value = self.data.get("status")
        if status_value == "":
            raise ValidationError({"status": ["Must be 'upcoming' or 'archived'."]})
        status_value = status_value or "upcoming"
        queryset = (
            queryset.upcoming() if status_value == "upcoming" else queryset.archived()
        )

        week_value = self.data.get("week")
        if week_value == "current":
            if status_value != "upcoming":
                raise ValidationError(
                    {"week": ["Only valid when status is 'upcoming'."]}
                )
            queryset = queryset.this_week()

        category_value = self.data.get("category")
        if category_value == "":
            raise ValidationError({"category": ["Must be a valid category."]})
        if category_value:
            queryset = queryset.filter(category=category_value)

        return queryset
