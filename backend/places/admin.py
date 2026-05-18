from django import forms
from django.contrib import admin
from django.contrib.gis.geos import Point
from django.core.validators import MaxValueValidator, MinValueValidator

from .models import Place


class PlaceAdminForm(forms.ModelForm):
    lat = forms.FloatField(
        label="Latitude",
        help_text="e.g. 52.2458425",
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
    )
    lng = forms.FloatField(
        label="Longitude",
        help_text="e.g. 20.9934177",
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
    )

    class Meta:
        model = Place
        fields = ["title", "description", "lat", "lng", "category"]

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.location = Point(
            self.cleaned_data["lng"],
            self.cleaned_data["lat"],
            srid=4326,
        )
        if commit:
            instance.save()
        return instance


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ["title", "category", "created_at"]
