from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserAdminCreationForm, UserAdminChangeForm

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    readonly_fields = ('created', 'modified',)
    list_display = ('email', 'admin',)
    list_filter = ('admin', 'email_confirmed', 'is_active',)
    fieldsets = (
        (None, {'fields': ('guid', 'full_name', 'email', 'password',)}),
        ('Confirmed', {'fields': ('email_confirmed',)}),
        ('Date', {'fields': ('created', 'modified',)}),
        ('Permissions', {'fields': ('admin', 'staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email', 'full_name',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.unregister(Group)
