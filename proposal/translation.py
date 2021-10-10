from modeltranslation.translator import register, TranslationOptions
from .models import StaticResource


@register(StaticResource)
class StaticResourcesTranslationOptions(TranslationOptions):
    fields = ('file_description',)
