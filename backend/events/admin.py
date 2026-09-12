from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from .models import Event


@admin.register(Event)
class EventAdmin(TranslationAdmin):
    list_display = ["title", "place", "category", "event_time", "created_at"]
