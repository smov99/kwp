from modeltranslation.translator import register, TranslationOptions
from .models import Section, Article


@register(Section)
class SectionTranslationOptions(TranslationOptions):
    fields = ('label',)


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')
