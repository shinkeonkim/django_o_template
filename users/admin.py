from users.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext_lazy as _

from users.forms import BaseCreationForm, BaseEditionForm


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = BaseEditionForm
    add_form = BaseCreationForm

    list_display = [
        'full_name',
        'email',
        'nickname',
        'is_active',
        'is_superuser',
        'created_at',
    ]

    list_display_links = [
        'full_name',
        'email',
    ]

    list_filter = [
        'is_superuser',
        'is_active',
    ]

    search_fields = [
        'email',
        'nickname',
        'first_name',
        'last_name',
    ]

    ordering = [
        'created_at',
    ]

    fieldsets = [
        (None, {
            'fields': ('email', 'password')
        }),
        (_('Personal info'), {
            'fields': ('nickname', )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_superuser',)
        }),
    ]

    add_fieldsets = (
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'nickname', 'password1', 'password2'],
        }),
    )
