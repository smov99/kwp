from django.contrib import admin
from .models import Section, Article
from modeltranslation.admin import TranslationAdmin


@admin.register(Section)
class SectionAdmin(TranslationAdmin):
    list_display = ('label',)
    search_fields = ('label',)


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('order', 'section', 'question', 'answer')
    search_fields = ('section', 'question', 'answer')
    list_filter = ('section',)
    list_display_links = ('question',)
