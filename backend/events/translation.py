from modeltranslation.translator import TranslationOptions, translator

from .models import Event


class EventTranslationOptions(TranslationOptions):
    fields = ("title", "description")


translator.register(Event, EventTranslationOptions)
