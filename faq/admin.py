from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Section, Article
from modeltranslation.admin import TranslationAdmin


@admin.register(Section)
class SectionAdmin(TranslationAdmin):
    list_display = ('id', 'order', '_label', 'is_active', 'label_en', 'label_es')
    list_display_links = ('id',)
    search_fields = ('label_en', 'label_es')
    list_filter = ('is_active',)
    ordering = ('order', '-is_active')

    def _label(self, obj):
        base_url = reverse('admin:faq_article_changelist')
        return mark_safe('<a href="{0}?section__id__exact={1}">{2}</a>'.format(base_url, obj.id, obj.label))


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('order', 'is_active', 'section', 'question', 'answer')
    search_fields = ('section', 'question', 'answer')
    list_filter = ('section', 'is_active')
    list_display_links = ('question',)
    ordering = ('order', '-is_active')
