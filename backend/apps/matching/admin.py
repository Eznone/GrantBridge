"""
Admin configuration for matching models.
"""

from django.contrib import admin
from .models import GrantMatch


@admin.register(GrantMatch)
class GrantMatchAdmin(admin.ModelAdmin):
    """Admin interface for GrantMatch model."""

    list_display = [
        "organization",
        "grant",
        "match_score",
        "algorithm_version",
        "created_at",
        "is_dismissed",
    ]
    list_filter = ["is_dismissed", "algorithm_version", "created_at"]
    search_fields = ["organization__name", "grant__title"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-match_score", "-created_at"]

    fieldsets = (
        (
            "Match Information",
            {"fields": ("id", "organization", "grant", "match_score")},
        ),
        (
            "AI Analysis",
            {"fields": ("match_reasons", "recommended_actions", "algorithm_version")},
        ),
        (
            "User Actions",
            {"fields": ("is_dismissed", "dismissed_at", "dismissed_reason")},
        ),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )


# Made with Bob
