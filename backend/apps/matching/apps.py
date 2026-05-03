"""
Matching app configuration.
"""

from django.apps import AppConfig


class MatchingConfig(AppConfig):
    """Configuration for the matching app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.matching"
    verbose_name = "Grant Matching"


# Made with Bob
