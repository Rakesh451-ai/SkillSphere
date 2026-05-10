from django.contrib import admin
from .models import ResumeAnalysis


@admin.register(ResumeAnalysis)
class ResumeAnalysisAdmin(admin.ModelAdmin):
    list_display = ['user', 'score', 'created_at']
    list_filter = ['score']
    search_fields = ['user__username']
