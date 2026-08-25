from django import forms
from django.contrib import admin
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
    website = forms.URLField(
        assume_scheme="https",
        required=False,
        empty_value="",
    )

    class Meta:
        model = Place
        fields = [
            "title",
            "description",
            "lat",
            "lng",
            "category",
            "address",
            "website",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.location:
            self.fields["lat"].initial = self.instance.lat
            self.fields["lng"].initial = self.instance.lng

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.location = Place.make_point(
            self.cleaned_data["lat"], self.cleaned_data["lng"]
        )
        if commit:
            instance.save()
        return instance


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    form = PlaceAdminForm
    list_display = ["title", "category", "created_at"]
