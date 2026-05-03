"""
Business logic for Grant Matching operations.
"""

from typing import List, Optional, Tuple
from django.db.models import Avg, Max, Count, Q

from apps.matching.models import GrantMatch
from apps.grants.models import Grant
from apps.organizations.models import Organization


class MatchingService:
    """Service class for grant matching operations."""

    ALGORITHM_VERSION = "1.0.0"

    @staticmethod
    def get_matches(
        organization: Organization,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None,
        quality: Optional[str] = None,
        include_dismissed: bool = False,
        limit: int = 20,
    ) -> List[GrantMatch]:
        """
        Get grant matches for an organization with filtering.

        Args:
            organization: Organization to get matches for
            min_score: Minimum match score filter
            max_score: Maximum match score filter
            quality: Quality filter (Excellent, Good, Fair, Poor)
            include_dismissed: Whether to include dismissed matches
            limit: Maximum number of matches to return

        Returns:
            List of GrantMatch instances
        """
        queryset = GrantMatch.objects.filter(organization=organization).select_related(
            "grant"
        )

        # Filter by dismissed status
        if not include_dismissed:
            queryset = queryset.filter(is_dismissed=False)

        # Filter by score range
        if min_score is not None:
            queryset = queryset.filter(match_score__gte=min_score)
        if max_score is not None:
            queryset = queryset.filter(match_score__lte=max_score)

        # Filter by quality
        if quality:
            quality_ranges = {
                "Excellent": (80, 100),
                "Good": (60, 79.99),
                "Fair": (40, 59.99),
                "Poor": (0, 39.99),
            }
            if quality in quality_ranges:
                min_q, max_q = quality_ranges[quality]
                queryset = queryset.filter(
                    match_score__gte=min_q, match_score__lte=max_q
                )

        # Order by score and limit
        queryset = queryset.order_by("-match_score", "-created_at")[:limit]

        return list(queryset)

    @staticmethod
    def get_match(match_id: str, organization: Organization) -> GrantMatch:
        """Get a single match by ID."""
        return GrantMatch.objects.select_related("grant").get(
            id=match_id, organization=organization
        )

    @staticmethod
    def dismiss_match(match: GrantMatch, reason: Optional[str] = None) -> GrantMatch:
        """Dismiss a match."""
        match.dismiss(reason=reason or "")
        return match

    @staticmethod
    def undismiss_match(match: GrantMatch) -> GrantMatch:
        """Restore a dismissed match."""
        match.undismiss()
        return match

    @staticmethod
    def calculate_simple_match_score(
        organization: Organization, grant: Grant
    ) -> Tuple[float, List[str], List[str]]:
        """
        Calculate a simple match score between organization and grant.
        This is a placeholder for the AI-powered matching that will be
        implemented later with FAISS and watsonx.ai.

        Args:
            organization: Organization to match
            grant: Grant to match against

        Returns:
            Tuple of (score, reasons, recommended_actions)
        """
        score = 50.0  # Base score
        reasons = []
        recommended_actions = []

        # Category matching
        org_categories = set(organization.categories or [])
        grant_categories = set(grant.categories or [])
        category_overlap = org_categories & grant_categories

        if category_overlap:
            category_boost = min(len(category_overlap) * 10, 30)
            score += category_boost
            reasons.append(
                f"Matches {len(category_overlap)} of your focus areas: "
                f"{', '.join(list(category_overlap)[:3])}"
            )

        # Tag matching
        org_tags = set(organization.tags or [])
        grant_tags = set(grant.tags or [])
        tag_overlap = org_tags & grant_tags

        if tag_overlap:
            tag_boost = min(len(tag_overlap) * 5, 15)
            score += tag_boost
            reasons.append(f"Shares {len(tag_overlap)} keywords with your profile")

        # Goal alignment (simple keyword matching)
        org_goals = " ".join(organization.goals or []).lower()
        grant_desc = (grant.description or "").lower()

        goal_keywords = org_goals.split()[:10]  # First 10 words
        matching_keywords = [
            kw for kw in goal_keywords if kw in grant_desc and len(kw) > 4
        ]

        if matching_keywords:
            goal_boost = min(len(matching_keywords) * 3, 10)
            score += goal_boost
            reasons.append("Grant description aligns with your organizational goals")

        # Funding amount check
        if grant.funding_amount:
            if grant.funding_amount >= 10000:
                reasons.append(
                    f"Significant funding available: " f"${grant.funding_amount:,.0f}"
                )

        # Cap score at 100
        score = min(score, 100.0)

        # Generate recommended actions based on score
        if score >= 70:
            recommended_actions = [
                "Review grant requirements in detail",
                "Start drafting a proposal",
                "Assign a team member to this opportunity",
            ]
        elif score >= 50:
            recommended_actions = [
                "Review grant requirements",
                "Assess organizational capacity",
                "Consider if this aligns with strategic goals",
            ]
        else:
            recommended_actions = [
                "Review grant details",
                "Evaluate fit with organizational mission",
            ]

        # Ensure we have at least one reason
        if not reasons:
            reasons = ["This grant may be relevant to your organization"]

        return score, reasons, recommended_actions

    @staticmethod
    def calculate_matches(
        organization: Organization,
        grant_ids: Optional[List[str]] = None,
        force_recalculate: bool = False,
    ) -> dict:
        """
        Calculate matches for an organization.

        Args:
            organization: Organization to calculate matches for
            grant_ids: Specific grant IDs to match (None = all grants)
            force_recalculate: Recalculate even if matches exist

        Returns:
            Dictionary with calculation statistics
        """
        # Get grants to match
        if grant_ids:
            grants = Grant.objects.filter(id__in=grant_ids)
        else:
            # Get all active grants (not expired)
            from django.utils import timezone

            grants = Grant.objects.filter(deadline__gte=timezone.now())

        matches_created = 0
        matches_updated = 0
        total_score = 0.0

        for grant in grants:
            # Check if match already exists
            existing_match = GrantMatch.objects.filter(
                organization=organization, grant=grant
            ).first()

            if existing_match and not force_recalculate:
                continue

            # Calculate match score
            score, reasons, actions = MatchingService.calculate_simple_match_score(
                organization, grant
            )

            total_score += score

            if existing_match:
                # Update existing match
                existing_match.match_score = score
                existing_match.match_reasons = reasons
                existing_match.recommended_actions = actions
                existing_match.algorithm_version = MatchingService.ALGORITHM_VERSION
                existing_match.save()
                matches_updated += 1
            else:
                # Create new match
                GrantMatch.objects.create(
                    organization=organization,
                    grant=grant,
                    match_score=score,
                    match_reasons=reasons,
                    recommended_actions=actions,
                    algorithm_version=MatchingService.ALGORITHM_VERSION,
                )
                matches_created += 1

        total_processed = matches_created + matches_updated
        avg_score = total_score / total_processed if total_processed > 0 else 0

        return {
            "matches_created": matches_created,
            "matches_updated": matches_updated,
            "total_grants_processed": total_processed,
            "average_score": round(avg_score, 2),
            "message": (
                f"Successfully processed {total_processed} grants. "
                f"Created {matches_created} new matches, "
                f"updated {matches_updated} existing matches."
            ),
        }

    @staticmethod
    def get_match_stats(organization: Organization) -> dict:
        """Get statistics about matches for an organization."""
        matches = GrantMatch.objects.filter(organization=organization)

        stats = matches.aggregate(
            total=Count("id"),
            dismissed=Count("id", filter=Q(is_dismissed=True)),
            avg_score=Avg("match_score"),
            top_score=Max("match_score"),
        )

        # Count by quality
        excellent = matches.filter(match_score__gte=80).count()
        good = matches.filter(match_score__gte=60, match_score__lt=80).count()
        fair = matches.filter(match_score__gte=40, match_score__lt=60).count()
        poor = matches.filter(match_score__lt=40).count()

        return {
            "total_matches": stats["total"] or 0,
            "excellent_matches": excellent,
            "good_matches": good,
            "fair_matches": fair,
            "poor_matches": poor,
            "dismissed_matches": stats["dismissed"] or 0,
            "average_score": round(stats["avg_score"] or 0, 2),
            "top_match_score": stats["top_score"],
        }


# Made with Bob
