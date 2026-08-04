from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from accounts.models import User
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'user__username', 'message']
    actions = ['mark_as_read', 'mark_as_unread', 'broadcast_notification_action']

    @admin.action(description="Mark selected notifications as Read")
    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.", messages.SUCCESS)

    @admin.action(description="Mark selected notifications as Unread")
    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} notification(s) marked as unread.", messages.SUCCESS)

    @admin.action(description="📢 Send Broadcast Notification to All Users")
    def broadcast_notification_action(self, request, queryset):
        return redirect('dashboard:admin_user_dashboard')

