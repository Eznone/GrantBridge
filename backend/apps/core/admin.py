"""
Admin configuration for core models.
"""

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""

    list_display = ["user", "notification_type", "title", "is_read", "created_at"]
    list_filter = ["notification_type", "is_read", "created_at"]
    search_fields = ["user__email", "user__name", "title", "message"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Notification Details",
            {"fields": ("id", "user", "notification_type", "title", "message")},
        ),
        (
            "Related Objects",
            {
                "fields": (
                    "related_grant",
                    "related_proposal",
                    "related_application",
                    "action_url",
                )
            },
        ),
        ("Status", {"fields": ("is_read", "read_at")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )

    actions = ["mark_as_read", "mark_as_unread"]

    def mark_as_read(self, request, queryset):
        """Mark selected notifications as read."""
        updated = queryset.filter(is_read=False).update(is_read=True)
        self.message_user(request, f"{updated} notification(s) marked as read.")

    mark_as_read.short_description = "Mark selected as read"

    def mark_as_unread(self, request, queryset):
        """Mark selected notifications as unread."""
        updated = queryset.filter(is_read=True).update(is_read=False, read_at=None)
        self.message_user(request, f"{updated} notification(s) marked as unread.")

    mark_as_unread.short_description = "Mark selected as unread"


# Made with Bob
