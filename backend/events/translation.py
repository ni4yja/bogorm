from modeltranslation.translator import TranslationOptions, translator

from .models import Event


class EventTranslationOptions(TranslationOptions):
    fields = ("title", "description")
    empty_values = {"title": "both", "description": "both"}


translator.register(Event, EventTranslationOptions)
