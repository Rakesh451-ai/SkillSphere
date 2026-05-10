from django.contrib import admin
from .models import Recommendation


@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'category', 'priority', 'is_read', 'created_at']
    list_filter = ['priority', 'category', 'is_read']
    search_fields = ['message', 'user__username']
