# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, EmployerAccount

@admin.register(UserAccount)
class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ['username', 'email', 'full_name', 'is_staff']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'email', 'full_name', 'password1', 'password2'),
        }),
    )
    search_fields = ['username', 'email', 'full_name']
    ordering = ['username']

admin.site.register(EmployerAccount)
