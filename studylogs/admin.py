from django.contrib import admin
from .models import StudyLog


@admin.register(StudyLog)
class StudyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'hours', 'productivity', 'category', 'date']
    list_filter = ['category', 'date']
    search_fields = ['topic', 'user__username']
