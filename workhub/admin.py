from django.contrib import admin
from .models import Resume, TechStack

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'user__username', 'content')
    filter_horizontal = ('tech_stack',)

@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
