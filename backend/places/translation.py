from modeltranslation.translator import TranslationOptions, translator

from .models import Place


class PlaceTranslationOptions(TranslationOptions):
    fields = ("title", "description")


translator.register(Place, PlaceTranslationOptions)
