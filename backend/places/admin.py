from django.contrib import admin
from django.contrib.gis.forms import OSMWidget

from .models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_at']
    formfield_overrides = {
        __import__('django.contrib.gis.db.models', fromlist=['PointField']).PointField: {
            'widget': OSMWidget(attrs={'display_raw': True})
        },
    }