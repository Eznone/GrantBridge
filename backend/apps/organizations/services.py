"""
Organization service layer for handling business logic.
"""

from typing import Dict, Optional
from decimal import Decimal
from django.db.models import Count, Q, Sum
from apps.organizations.models import Organization
from apps.grants.models import Application
from apps.proposals.models import Proposal
from apps.matching.models import GrantMatch


class OrganizationService:
    """Service for handling organization operations."""

    @staticmethod
    def get_organization(organization_id: str) -> Optional[Organization]:
        """
        Get organization by ID.

        Args:
            organization_id: Organization UUID

        Returns:
            Organization instance or None
        """
        try:
            return Organization.objects.get(id=organization_id)
        except Organization.DoesNotExist:
            return None

    @staticmethod
    def update_organization(organization: Organization, **kwargs) -> Organization:
        """
        Update organization with provided fields.

        Args:
            organization: Organization instance
            **kwargs: Fields to update

        Returns:
            Updated Organization instance
        """
        update_fields = []

        for field, value in kwargs.items():
            if value is not None and hasattr(organization, field):
                setattr(organization, field, value)
                update_fields.append(field)

        if update_fields:
            update_fields.append("updated_at")
            organization.save(update_fields=update_fields)

        return organization

    @staticmethod
    def get_organization_stats(organization: Organization) -> Dict:
        """
        Get comprehensive statistics for an organization.

        Args:
            organization: Organization instance

        Returns:
            Dictionary with organization statistics
        """
        # Get application statistics
        applications = Application.objects.filter(organization=organization)

        total_grants_applied = applications.count()

        active_applications = applications.filter(
            status__in=["draft", "submitted", "under_review"]
        ).count()

        approved_applications = applications.filter(status="approved").count()

        rejected_applications = applications.filter(status="rejected").count()

        # Get proposal statistics
        proposals = Proposal.objects.filter(organization=organization)

        total_proposals = proposals.count()
        draft_proposals = proposals.filter(status="draft").count()
        submitted_proposals = proposals.filter(
            status__in=["submitted", "under_review", "approved"]
        ).count()

        # Calculate funding statistics
        funding_requested = applications.aggregate(total=Sum("grant__funding_amount"))[
            "total"
        ] or Decimal("0")

        funding_received = applications.filter(status="approved").aggregate(
            total=Sum("grant__funding_amount")
        )["total"] or Decimal("0")

        # Calculate success rate
        completed_applications = applications.filter(
            status__in=["approved", "rejected"]
        ).count()

        if completed_applications > 0:
            success_rate = (approved_applications / completed_applications) * 100
        else:
            success_rate = 0.0

        # Get grant match statistics
        grant_matches = GrantMatch.objects.filter(
            organization=organization, is_dismissed=False
        )

        grant_matches_count = grant_matches.count()
        top_grant_matches_count = grant_matches.filter(match_score__gte=80).count()

        return {
            "total_grants_applied": total_grants_applied,
            "active_applications": active_applications,
            "approved_applications": approved_applications,
            "rejected_applications": rejected_applications,
            "total_proposals": total_proposals,
            "draft_proposals": draft_proposals,
            "submitted_proposals": submitted_proposals,
            "total_funding_requested": funding_requested,
            "total_funding_received": funding_received,
            "success_rate": round(success_rate, 2),
            "grant_matches_count": grant_matches_count,
            "top_grant_matches_count": top_grant_matches_count,
        }


# Made with Bob
