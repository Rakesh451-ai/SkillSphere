from django.contrib import admin
from .models import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill_name', 'category', 'level', 'hours_practiced', 'progress']
    list_filter = ['category', 'level']
    search_fields = ['skill_name', 'user__username']
