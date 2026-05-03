"""
Business logic for Core operations (Dashboard, Notifications, Analytics).
"""

from typing import List, Dict
from datetime import timedelta, datetime
from django.utils import timezone
from django.db.models import Count, Q, Sum, Avg, F
from collections import defaultdict

from apps.core.models import Notification
from apps.authentication.models import User
from apps.organizations.models import Organization
from apps.grants.models import Grant, Application, SavedGrant
from apps.proposals.models import Proposal
from apps.matching.models import GrantMatch


class DashboardService:
    """Service class for dashboard operations."""

    @staticmethod
    def get_dashboard_stats(organization: Organization, user: User) -> dict:
        """
        Get comprehensive dashboard statistics.

        Args:
            organization: Organization instance
            user: User instance

        Returns:
            Dictionary with dashboard statistics
        """
        now = timezone.now()
        seven_days_ago = now - timedelta(days=7)
        thirty_days_ahead = now + timedelta(days=30)

        # Grant stats
        total_grants = Grant.objects.filter(deadline__gte=now).count()
        saved_grants = SavedGrant.objects.filter(organization=organization).count()

        # Application stats
        applications = Application.objects.filter(organization=organization)
        app_stats = applications.aggregate(
            total=Count("id"),
            draft=Count("id", filter=Q(status="draft")),
            submitted=Count("id", filter=Q(status="submitted")),
            approved=Count("id", filter=Q(status="approved")),
        )

        # Proposal stats
        proposals = Proposal.objects.filter(organization=organization)
        proposal_stats = proposals.aggregate(
            total=Count("id"),
            draft=Count("id", filter=Q(status="draft")),
            submitted=Count("id", filter=Q(status="submitted")),
        )

        # Match stats
        matches = GrantMatch.objects.filter(
            organization=organization, is_dismissed=False
        )
        match_stats = matches.aggregate(
            total=Count("id"),
            excellent=Count("id", filter=Q(match_score__gte=80)),
            good=Count("id", filter=Q(match_score__gte=60, match_score__lt=80)),
        )

        # Recent matches (last 7 days)
        recent_matches = GrantMatch.objects.filter(
            organization=organization, created_at__gte=seven_days_ago
        ).count()

        # Upcoming deadlines (next 30 days)
        upcoming_deadlines = Grant.objects.filter(
            deadline__gte=now, deadline__lte=thirty_days_ahead
        ).count()

        # Unread notifications
        unread_notifications = Notification.objects.filter(
            user=user, is_read=False
        ).count()

        return {
            "total_grants": total_grants,
            "saved_grants": saved_grants,
            "total_applications": app_stats["total"] or 0,
            "draft_applications": app_stats["draft"] or 0,
            "submitted_applications": app_stats["submitted"] or 0,
            "approved_applications": app_stats["approved"] or 0,
            "total_proposals": proposal_stats["total"] or 0,
            "draft_proposals": proposal_stats["draft"] or 0,
            "submitted_proposals": proposal_stats["submitted"] or 0,
            "total_matches": match_stats["total"] or 0,
            "excellent_matches": match_stats["excellent"] or 0,
            "good_matches": match_stats["good"] or 0,
            "unread_notifications": unread_notifications,
            "recent_matches": recent_matches,
            "upcoming_deadlines": upcoming_deadlines,
        }

    @staticmethod
    def get_upcoming_deadlines(
        organization: Organization, days: int = 30, limit: int = 10
    ) -> List[dict]:
        """
        Get upcoming grant deadlines.

        Args:
            organization: Organization instance
            days: Number of days to look ahead
            limit: Maximum number of deadlines to return

        Returns:
            List of deadline dictionaries
        """
        now = timezone.now()
        future_date = now + timedelta(days=days)

        grants = Grant.objects.filter(
            deadline__gte=now, deadline__lte=future_date
        ).order_by("deadline")[:limit]

        deadlines = []
        for grant in grants:
            days_remaining = (grant.deadline - now).days

            # Check if organization has application/proposal
            has_application = Application.objects.filter(
                organization=organization, grant=grant
            ).exists()

            has_proposal = Proposal.objects.filter(
                organization=organization, grant=grant
            ).exists()

            deadlines.append(
                {
                    "grant_id": str(grant.id),
                    "grant_title": grant.title,
                    "funder_name": grant.funder_name,
                    "deadline": grant.deadline,
                    "days_remaining": days_remaining,
                    "has_application": has_application,
                    "has_proposal": has_proposal,
                }
            )

        return deadlines


class NotificationService:
    """Service class for notification operations."""

    @staticmethod
    def get_notifications(
        user: User,
        unread_only: bool = False,
        notification_type: str = None,
        limit: int = 50,
    ) -> List[Notification]:
        """
        Get notifications for a user.

        Args:
            user: User instance
            unread_only: Only return unread notifications
            notification_type: Filter by notification type
            limit: Maximum number of notifications

        Returns:
            List of Notification instances
        """
        queryset = Notification.objects.filter(user=user)

        if unread_only:
            queryset = queryset.filter(is_read=False)

        if notification_type:
            queryset = queryset.filter(notification_type=notification_type)

        return list(queryset.order_by("-created_at")[:limit])

    @staticmethod
    def mark_as_read(notification: Notification) -> Notification:
        """Mark a notification as read."""
        notification.mark_as_read()
        return notification

    @staticmethod
    def mark_all_as_read(user: User) -> int:
        """
        Mark all notifications as read for a user.

        Returns:
            Number of notifications marked as read
        """
        unread = Notification.objects.filter(user=user, is_read=False)
        count = unread.count()

        now = timezone.now()
        unread.update(is_read=True, read_at=now)

        return count

    @staticmethod
    def delete_notification(notification: Notification) -> None:
        """Delete a notification."""
        notification.delete()


# Made with Bob


class AnalyticsService:
    """Service class for analytics operations."""

    @staticmethod
    def get_trends(organization: Organization, days: int = 90) -> Dict:
        """
        Get analytics trends over time.

        Args:
            organization: Organization instance
            days: Number of days to analyze

        Returns:
            Dictionary with trend data
        """
        now = timezone.now()
        start_date = now - timedelta(days=days)

        # Initialize data structures
        proposals_by_date = defaultdict(int)
        applications_by_date = defaultdict(int)
        matches_by_date = defaultdict(int)

        # Get proposals
        proposals = (
            Proposal.objects.filter(
                organization=organization, created_at__gte=start_date
            )
            .values("created_at__date")
            .annotate(count=Count("id"))
        )

        for item in proposals:
            date_str = item["created_at__date"].strftime("%Y-%m-%d")
            proposals_by_date[date_str] = item["count"]

        # Get applications
        applications = (
            Application.objects.filter(
                organization=organization, created_at__gte=start_date
            )
            .values("created_at__date")
            .annotate(count=Count("id"))
        )

        for item in applications:
            date_str = item["created_at__date"].strftime("%Y-%m-%d")
            applications_by_date[date_str] = item["count"]

        # Get matches
        matches = (
            GrantMatch.objects.filter(
                organization=organization, created_at__gte=start_date
            )
            .values("created_at__date")
            .annotate(count=Count("id"))
        )

        for item in matches:
            date_str = item["created_at__date"].strftime("%Y-%m-%d")
            matches_by_date[date_str] = item["count"]

        # Convert to list format
        proposals_trend = [
            {"date": date, "count": count}
            for date, count in sorted(proposals_by_date.items())
        ]
        applications_trend = [
            {"date": date, "count": count}
            for date, count in sorted(applications_by_date.items())
        ]
        matches_trend = [
            {"date": date, "count": count}
            for date, count in sorted(matches_by_date.items())
        ]

        return {
            "proposals": proposals_trend,
            "applications": applications_trend,
            "matches": matches_trend,
            "period_days": days,
        }

    @staticmethod
    def get_category_breakdown(organization: Organization) -> Dict:
        """
        Get analytics breakdown by category.

        Args:
            organization: Organization instance

        Returns:
            Dictionary with category breakdown
        """
        applications = Application.objects.filter(organization=organization)

        # Group by grant categories
        category_stats = {}

        for app in applications:
            grant = app.grant
            categories = grant.categories or []

            for category in categories:
                if category not in category_stats:
                    category_stats[category] = {
                        "category": category,
                        "total_applications": 0,
                        "successful_applications": 0,
                        "total_funding_requested": 0.0,
                        "total_funding_awarded": 0.0,
                    }

                category_stats[category]["total_applications"] += 1

                if app.status == "approved":
                    category_stats[category]["successful_applications"] += 1
                    if app.amount_requested:
                        category_stats[category]["total_funding_awarded"] += float(
                            app.amount_requested
                        )

                if app.amount_requested:
                    category_stats[category]["total_funding_requested"] += float(
                        app.amount_requested
                    )

        # Calculate success rates
        categories = []
        for stats in category_stats.values():
            total = stats["total_applications"]
            successful = stats["successful_applications"]
            stats["success_rate"] = (successful / total * 100) if total > 0 else 0.0
            categories.append(stats)

        return {
            "categories": categories,
            "total_categories": len(categories),
        }

    @staticmethod
    def get_success_rate(organization: Organization) -> Dict:
        """
        Get detailed success rate analytics.

        Args:
            organization: Organization instance

        Returns:
            Dictionary with success rate data
        """
        applications = Application.objects.filter(organization=organization)

        total_apps = applications.count()
        successful_apps = applications.filter(status="approved").count()
        overall_rate = (successful_apps / total_apps * 100) if total_apps > 0 else 0.0

        # Success by category
        category_success = {}
        for app in applications:
            grant = app.grant
            categories = grant.categories or []

            for category in categories:
                if category not in category_success:
                    category_success[category] = {"total": 0, "successful": 0}

                category_success[category]["total"] += 1
                if app.status == "approved":
                    category_success[category]["successful"] += 1

        by_category = []
        for category, stats in category_success.items():
            total = stats["total"]
            successful = stats["successful"]
            rate = (successful / total * 100) if total > 0 else 0.0

            by_category.append(
                {
                    "category": category,
                    "success_rate": rate,
                    "total_applications": total,
                }
            )

        # Success by amount range
        amount_ranges = [
            {"label": "Under $10K", "min": 0, "max": 10000},
            {"label": "$10K - $50K", "min": 10000, "max": 50000},
            {"label": "$50K - $100K", "min": 50000, "max": 100000},
            {"label": "$100K - $500K", "min": 100000, "max": 500000},
            {"label": "Over $500K", "min": 500000, "max": None},
        ]

        by_amount = []
        for range_def in amount_ranges:
            if range_def["max"]:
                apps_in_range = applications.filter(
                    amount_requested__gte=range_def["min"],
                    amount_requested__lt=range_def["max"],
                )
            else:
                apps_in_range = applications.filter(
                    amount_requested__gte=range_def["min"]
                )

            total = apps_in_range.count()
            successful = apps_in_range.filter(status="approved").count()
            rate = (successful / total * 100) if total > 0 else 0.0

            by_amount.append(
                {
                    "range_label": range_def["label"],
                    "min_amount": float(range_def["min"]),
                    "max_amount": (
                        float(range_def["max"]) if range_def["max"] else None
                    ),
                    "success_rate": rate,
                    "total_applications": total,
                }
            )

        return {
            "overall_success_rate": overall_rate,
            "total_applications": total_apps,
            "successful_applications": successful_apps,
            "by_category": by_category,
            "by_amount_range": by_amount,
        }

    @staticmethod
    def get_funding_analytics(organization: Organization) -> Dict:
        """
        Get funding analytics.

        Args:
            organization: Organization instance

        Returns:
            Dictionary with funding data
        """
        applications = Application.objects.filter(organization=organization)

        # Aggregate by status
        status_stats = applications.values("status").annotate(
            count=Count("id"),
            total_amount=Sum("amount_requested"),
            avg_amount=Avg("amount_requested"),
        )

        by_status = []
        total_requested = 0.0
        total_awarded = 0.0
        total_pending = 0.0
        total_rejected = 0.0

        for stat in status_stats:
            status = stat["status"]
            count = stat["count"]
            total = float(stat["total_amount"] or 0)
            avg = float(stat["avg_amount"] or 0)

            by_status.append(
                {
                    "status": status,
                    "count": count,
                    "total_amount": total,
                    "average_amount": avg,
                }
            )

            total_requested += total

            if status == "approved":
                total_awarded += total
            elif status in ["submitted", "under_review"]:
                total_pending += total
            elif status == "rejected":
                total_rejected += total

        # Calculate averages
        total_count = applications.count()
        avg_request = applications.aggregate(avg=Avg("amount_requested"))["avg"] or 0
        approved_apps = applications.filter(status="approved")
        avg_award = approved_apps.aggregate(avg=Avg("amount_requested"))["avg"] or 0

        return {
            "total_requested": total_requested,
            "total_awarded": total_awarded,
            "total_pending": total_pending,
            "total_rejected": total_rejected,
            "by_status": by_status,
            "average_request_amount": float(avg_request),
            "average_award_amount": float(avg_award),
        }


# Made with Bob
