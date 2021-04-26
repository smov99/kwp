from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from rangefilter.filters import DateTimeRangeFilter

from .models import Session, SessionEvent


def false(*args, **kwargs):
    return False


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    model = Session
    list_display = (
        'id',
        'created',
        'proposal_exists',
        '_email',
        'email_valid',
        'account_id',
        'contact_id',
        'contact_created',
        'message',
        'client_ip'
    )
    readonly_fields = (
        'proposal_id',
        'id',
        'created',
        'proposal_exists',
        'email',
        'email_valid',
        'account_id',
        'contact_id',
        'contact_created',
        'message',
        'client_ip'
    )
    list_filter = (
        ('created', DateTimeRangeFilter),
        'proposal_exists',
        'email_valid',
        'contact_created',
        'proposal_id',
        'email',
        'account_id',
        'contact_id',
        'client_ip'
    )
    search_fields = ('proposal_id', 'account_id', 'contact_id')
    ordering = ('-created',)
    list_display_links = None
    actions = None
    has_add_permission = false
    has_delete_permission = false
    log_change = false

    def _email(self, obj):
        base_url = reverse('admin:proposal_sessionevent_changelist')
        return mark_safe('<a href="{0}?session_id__id__exact={1}">{2}</a>'.format(base_url, obj.pk, obj.email))


@admin.register(SessionEvent)
class SessionEventAdmin(admin.ModelAdmin):
    model = SessionEvent
    list_display = ('session_id', 'id', 'created', 'event_type', 'event_name', 'message')
    ordering = ('-created',)
    list_display_links = None
    actions = None
    has_add_permission = false
    has_delete_permission = false
    log_change = false
