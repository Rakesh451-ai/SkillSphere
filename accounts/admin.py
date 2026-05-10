from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'college', 'branch', 'year', 'xp_points', 'current_streak']
    list_filter = ['year', 'college', 'is_active']
    search_fields = ['username', 'email', 'college']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {
            'fields': (
                'college', 'branch', 'year', 'bio', 'skills_list',
                'github_link', 'linkedin_link', 'profile_image',
            ),
        }),
        ('Gamification', {
            'fields': ('xp_points', 'current_streak', 'longest_streak', 'last_activity_date'),
        }),
    )
