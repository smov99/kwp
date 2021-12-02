from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Section, Article
from modeltranslation.admin import TranslationAdmin


@admin.register(Section)
class SectionAdmin(TranslationAdmin):
    list_display = ('guid', 'order', '_label', 'is_active', 'label_en', 'label_es')
    list_display_links = ('guid', '_label')
    search_fields = ('label_en', 'label_es')
    readonly_fields = ('guid',)
    list_filter = ('is_active',)
    ordering = ('order', '-is_active')
    list_per_page = 10

    def _label(self, obj):
        base_url = reverse('admin:faq_article_changelist')
        return mark_safe('<a href="{0}?section__id__exact={1}">{2}</a>'.format(
            base_url,
            obj.id,
            obj.label
        ))

    class Media:
        js = ['assets/js/menu_filter_collapse.js']


@admin.register(Article)
class ArticleAdmin(TranslationAdmin):
    list_display = ('guid', 'order', 'is_active', 'section', 'question', 'answer')
    search_fields = ('section__label', 'question', 'answer')
    list_filter = ('section', 'is_active')
    list_display_links = ('question', 'guid')
    ordering = ('section', 'order', '-is_active')
    list_per_page = 10
    readonly_fields = ('guid', 'created', 'modified')
    fieldsets = (
        ('General', {'fields': ('guid', 'created', 'modified', 'is_active')}),
        ('EN', {'fields': ('question_en', 'answer_en')}),
        ('ES', {'fields': ('question_es', 'answer_es')})
    )

    class Media:
        js = ['assets/js/menu_filter_collapse.js']
