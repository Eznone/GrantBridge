"""
Models for AI-powered grant matching functionality.
"""

import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class GrantMatch(models.Model):
    """
    Represents an AI-generated match between an organization and a grant.

    Stores the match score, reasons for the match, and recommended actions.
    Supports dismissal by users if they don't want to pursue a particular grant.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Relationships
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="grant_matches",
        help_text="Organization for which this match was generated",
    )

    grant = models.ForeignKey(
        "grants.Grant",
        on_delete=models.CASCADE,
        related_name="organization_matches",
        help_text="Grant that was matched to the organization",
    )

    # Match Score (0-100)
    match_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        db_index=True,
        help_text="AI-calculated match score between 0 and 100",
    )

    # AI Analysis Results (stored as JSON)
    match_reasons = models.JSONField(
        default=list,
        help_text="List of reasons why this grant matches the organization",
    )

    recommended_actions = models.JSONField(
        default=list, help_text="List of recommended next steps for the organization"
    )

    # Algorithm Tracking
    algorithm_version = models.CharField(
        max_length=50, help_text="Version of the matching algorithm used"
    )

    # User Actions
    is_dismissed = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Whether the user has dismissed this match",
    )

    dismissed_at = models.DateTimeField(
        null=True, blank=True, help_text="When the match was dismissed"
    )

    dismissed_reason = models.TextField(
        blank=True, help_text="Optional reason for dismissing the match"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "grant_matches"
        verbose_name = "Grant Match"
        verbose_name_plural = "Grant Matches"
        ordering = ["-match_score", "-created_at"]
        indexes = [
            models.Index(
                fields=["organization", "grant"], name="grantmatch_org_grant_idx"
            ),
            models.Index(
                fields=["organization", "-match_score"], name="grantmatch_org_score_idx"
            ),
            models.Index(
                fields=["grant", "-match_score"], name="grantmatch_grant_score_idx"
            ),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "grant"], name="unique_organization_grant_match"
            )
        ]

    def __str__(self):
        return (
            f"{self.organization.name} - {self.grant.title} "
            f"(Score: {self.match_score:.1f})"
        )

    def dismiss(self, reason: str = ""):
        """
        Mark this match as dismissed by the user.

        Args:
            reason: Optional reason for dismissing the match
        """
        self.is_dismissed = True
        self.dismissed_at = timezone.now()
        self.dismissed_reason = reason
        self.save(
            update_fields=[
                "is_dismissed",
                "dismissed_at",
                "dismissed_reason",
                "updated_at",
            ]
        )

    def undismiss(self):
        """Restore a dismissed match."""
        self.is_dismissed = False
        self.dismissed_at = None
        self.dismissed_reason = ""
        self.save(
            update_fields=[
                "is_dismissed",
                "dismissed_at",
                "dismissed_reason",
                "updated_at",
            ]
        )

    @property
    def match_percentage(self) -> str:
        """Return match score as a formatted percentage string."""
        return f"{self.match_score:.1f}%"

    @property
    def match_quality(self) -> str:
        """
        Return a qualitative assessment of the match quality.

        Returns:
            String indicating match quality: 'Excellent', 'Good', 'Fair', 'Poor'
        """
        if self.match_score >= 80:
            return "Excellent"
        elif self.match_score >= 60:
            return "Good"
        elif self.match_score >= 40:
            return "Fair"
        else:
            return "Poor"

    @classmethod
    def get_top_matches(cls, organization, limit: int = 10):
        """
        Get the top matches for an organization.

        Args:
            organization: Organization instance
            limit: Maximum number of matches to return

        Returns:
            QuerySet of top GrantMatch instances
        """
        return (
            cls.objects.filter(organization=organization, is_dismissed=False)
            .select_related("grant")
            .order_by("-match_score")[:limit]
        )

    @classmethod
    def get_matches_by_quality(cls, organization, quality: str):
        """
        Get matches filtered by quality level.

        Args:
            organization: Organization instance
            quality: Quality level ('Excellent', 'Good', 'Fair', 'Poor')

        Returns:
            QuerySet of GrantMatch instances
        """
        quality_ranges = {
            "Excellent": (80, 100),
            "Good": (60, 79.99),
            "Fair": (40, 59.99),
            "Poor": (0, 39.99),
        }

        if quality not in quality_ranges:
            raise ValueError(
                f"Invalid quality level. Must be one of: "
                f"{', '.join(quality_ranges.keys())}"
            )

        min_score, max_score = quality_ranges[quality]
        return (
            cls.objects.filter(
                organization=organization,
                is_dismissed=False,
                match_score__gte=min_score,
                match_score__lte=max_score,
            )
            .select_related("grant")
            .order_by("-match_score")
        )


# Made with Bob
