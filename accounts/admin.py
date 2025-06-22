# accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User

    # Поля, отображаемые на странице списка
    list_display = (
        'username', 'email', 'first_name', 'last_name',
        'role', 'is_active', 'is_staff', 'is_superuser'
    )
    list_filter = (
        'role', 'is_active', 'is_staff', 'is_superuser', 'groups'
    )

    # Группировка полей на странице редактирования
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
            'fields': (
                'role',
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Поля для формы создания пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'role',
                'password1',
                'password2',
                'is_active',
                'is_staff',
            ),
        }),
    )

    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

    actions = ['make_students', 'make_leaders', 'make_admins']

    @admin.action(description="Сделать выбранных пользователей студентами")
    def make_students(self, request, queryset):
        queryset.update(role='student')

    @admin.action(description="Сделать выбранных пользователей руководителями")
    def make_leaders(self, request, queryset):
        queryset.update(role='leader')

    @admin.action(description="Сделать выбранных пользователей администраторами")
    def make_admins(self, request, queryset):
        queryset.update(role='admin', is_staff=True, is_superuser=True)
