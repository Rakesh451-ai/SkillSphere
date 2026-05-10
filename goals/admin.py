from django.contrib import admin
from .models import Goal


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'goal_type', 'status', 'progress', 'deadline']
    list_filter = ['goal_type', 'status']
    search_fields = ['title', 'user__username']
