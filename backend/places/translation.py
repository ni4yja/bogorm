from modeltranslation.translator import TranslationOptions, translator

from .models import Place


class PlaceTranslationOptions(TranslationOptions):
    fields = ("title", "description")
    empty_values = {"title": "both", "description": "both"}


translator.register(Place, PlaceTranslationOptions)
