from modeltranslation.translator import register, TranslationOptions
from .models import StaticResources


@register(StaticResources)
class StaticResourcesTranslationOptions(TranslationOptions):
    fields = ('file_description',)
