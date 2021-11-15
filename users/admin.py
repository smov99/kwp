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
    readonly_fields = ('created', 'modified', 'guid',)
    list_display = ('email', 'admin', 'backdoor')
    list_filter = ('admin', 'email_confirmed', 'is_active', 'staff', 'admin', 'backdoor',)
    fieldsets = (
        (None, {'fields': ('guid', 'full_name', 'email', 'password',)}),
        ('Confirmed', {'fields': ('email_confirmed', 'is_active',)}),
        ('Date', {'fields': ('created', 'modified',)}),
        ('Permissions', {'fields': ('admin', 'staff', 'backdoor',)}),
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
admin.site.site_header = 'Kiwapower administration'
admin.site.site_title = 'Kiwapower site admin'
