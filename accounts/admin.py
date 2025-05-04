from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount

@admin.register(UserAccount)
class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ['username', 'email', 'full_name', 'is_company', 'is_staff', 'is_active']
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'full_name', 'password')}),
        ('기업 정보', {'fields': ('is_company', 'company_name', 'contact_person', 'phone_number', 'company_website')}),
        ('권한 설정', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'is_company', 'password1', 'password2'),
        }),
    )

    search_fields = ['username', 'email', 'full_name', 'company_name']
    ordering = ['username']
