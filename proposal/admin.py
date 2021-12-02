import datetime

from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin
from rangefilter.filters import DateTimeRangeFilter

from .models import (
    Session,
    SessionEvent,
    ErrorLog,
    StaticResource,
    SalesforceCategory
)


def false(*args, **kwargs):
    return False


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    model = Session
    list_display = (
        'id',
        'created',
        'proposal_id',
        'proposal_exists',
        '_email',
        'email_valid',
        '_with_error',
        'account_id',
        'contact_id',
        'contact_created',
        'message',
        'client_ip',
        'client_geolocation',
        'device'
    )
    readonly_fields = (
        'proposal_id',
        'id',
        'created',
        'proposal_exists',
        'email',
        'with_error',
        'email_valid',
        'account_id',
        'contact_id',
        'contact_created',
        'message',
        'client_ip',
        'client_geolocation',
        'device'
    )
    list_filter = (
        ('created', DateTimeRangeFilter),
        'proposal_exists',
        'with_error',
        'email_valid',
        'contact_created',
        'proposal_id',
        'email',
        'message',
        'account_id',
        'contact_id',
        'client_ip',
        'client_geolocation'
    )
    search_fields = ('proposal_id', 'account_id', 'contact_id', 'email', 'message')
    ordering = ('-created',)
    list_per_page = 10
    list_display_links = None
    actions = None
    has_add_permission = false
    has_delete_permission = false
    log_change = false

    def get_rangefilter_created_default(self, request):
        return (datetime.datetime.utcnow(), datetime.datetime.utcnow())

    def get_rangefilter_created_title(self, request, field_path):
        return 'Date filter'

    def _email(self, obj):
        base_url = reverse('admin:proposal_sessionevent_changelist')
        return mark_safe('<a href="{0}?session_id__id__exact={1}">{2}</a>'.format(base_url, obj.pk, obj.email))

    def _with_error(self, obj):
        if obj.with_error == 'Yes':
            base_url = reverse('admin:proposal_errorlog_changelist')
            return mark_safe('<a href="{0}?session_id__id__exact={1}">{2}</a>'.format(base_url, obj.pk, obj.with_error))
        else:
            return mark_safe(obj.with_error)

    class Media:
        js = ['assets/js/menu_filter_collapse.js']


@admin.register(SessionEvent)
class SessionEventAdmin(admin.ModelAdmin):
    model = SessionEvent
    list_display = ('session_id', 'id', 'created', 'document_name', 'event_type', 'event_name', 'message')
    ordering = ('-created',)
    search_fields = ('event_type', 'document_name')
    list_per_page = 10
    list_display_links = None
    actions = None
    has_add_permission = false
    has_delete_permission = false
    log_change = false


@admin.register(ErrorLog)
class ErrorLogAdmin(admin.ModelAdmin):
    model = ErrorLog
    list_display = ('session_id', 'id', 'created', 'error_type', 'api_call_type', 'sf_object', 'error')
    ordering = ('-created',)
    search_fields = ('sf_object', 'error', 'error_type')
    list_filter = ('sf_object', 'api_call_type', 'error_type')
    list_per_page = 10
    list_display_links = ('id', 'error')
    actions = None
    has_add_permission = false
    log_change = false
    readonly_fields = tuple(field.name for field in ErrorLog._meta.get_fields())

    class Media:
        js = ['assets/js/menu_filter_collapse.js']


@admin.register(StaticResource)
class StaticResourcesAdmin(TranslationAdmin):
    list_display = (
        'id',
        'created',
        'modified',
        'file_description',
        'is_active',
        'document',
        's3_file_location',
        'salesforce_category'
    )
    search_fields = (
        'file_description',
        's3_file_location',
        'salesforce_category',
        'created',
        'modified'
    )
    readonly_fields = ('id', 'created', 'modified')
    list_display_links = ('file_description',)
    ordering = ('-modified',)
    list_filter = ('salesforce_category', 'is_active')
    exclude = ('s3_file_location',)
    fieldsets = (
        ('General', {'fields': ('id', 'created', 'modified', 'is_active', 'salesforce_category')}),
        ('ES Document', {'fields': ('file_description_es', 'document_es')}),
        ('EN Document', {'fields': ('file_description_en', 'document_en')})
    )

    def render_change_form(self, request, context, *args, **kwargs):
        context['adminform'].form.fields['salesforce_category'].queryset = \
            SalesforceCategory.objects.filter(is_active=True)
        return super(StaticResourcesAdmin, self).render_change_form(request, context, *args, **kwargs)


@admin.register(SalesforceCategory)
class SalesforceCategoriesAdmin(admin.ModelAdmin):
    model = SalesforceCategory
    list_display = (
        'created',
        'modified',
        '_salesforce_category',
        'is_active'
    )
    ordering = ('-modified',)
    list_display_links = ('_salesforce_category',)
    list_filter = ('is_active',)
    readonly_fields = ('created', 'modified')

    def _salesforce_category(self, obj):
        try:
            return mark_safe(' '.join(obj.salesforce_category.split('__')[0].split('_')))
        except IndexError:
            return mark_safe(obj.salesforce_category)
