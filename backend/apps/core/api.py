"""
Core API endpoints for dashboard, notifications, and analytics.
"""

from typing import List
from django.http import HttpRequest
from ninja import Router
from ninja.pagination import paginate

from apps.authentication.api import JWTAuth
from apps.authentication.schemas import ErrorResponseSchema
from .schemas import (
    DashboardStatsOut,
    UpcomingDeadlineOut,
    NotificationOut,
    AnalyticsTrendsOut,
    AnalyticsCategoriesOut,
    AnalyticsSuccessRateOut,
    AnalyticsFundingOut,
)
from .services import DashboardService, NotificationService, AnalyticsService
from .models import Notification

router = Router(tags=["Core"])


# Dashboard Endpoints
@router.get(
    "/dashboard/stats",
    response={200: DashboardStatsOut, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get dashboard statistics",
)
def get_dashboard_stats(request: HttpRequest):
    """
    Get comprehensive dashboard statistics for the authenticated
    user's organization.

    Returns:
        - Total proposals count
        - Active applications count
        - Saved grants count
        - Pending matches count
        - Success rate percentage
        - Total funding amount
    """
    user = request.auth
    organization = user.organization
    service = DashboardService()
    stats = service.get_dashboard_stats(organization, user)

    # Calculate additional metrics for the response
    total_apps = stats.get("total_applications", 0)
    approved_apps = stats.get("approved_applications", 0)
    success_rate = (approved_apps / total_apps * 100) if total_apps > 0 else 0.0

    return 200, DashboardStatsOut(
        total_proposals=stats.get("total_proposals", 0),
        active_applications=stats.get("submitted_applications", 0),
        saved_grants=stats.get("saved_grants", 0),
        pending_matches=stats.get("total_matches", 0),
        success_rate=success_rate,
        total_funding=0.0,  # Will be calculated from applications
    )


@router.get(
    "/dashboard/deadlines",
    response={200: List[UpcomingDeadlineOut], 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get upcoming deadlines",
)
def get_upcoming_deadlines(request: HttpRequest, days: int = 30):
    """
    Get upcoming grant deadlines for saved grants and active applications.

    Args:
        days: Number of days to look ahead (default: 30)

    Returns:
        List of grants with upcoming deadlines, sorted by deadline date
    """
    user = request.auth
    organization = user.organization
    service = DashboardService()
    deadlines = service.get_upcoming_deadlines(organization, days)

    return 200, [
        UpcomingDeadlineOut(
            grant_id=d["grant_id"],
            grant_title=d["grant_title"],
            deadline=d["deadline"],
            days_remaining=d["days_remaining"],
            application_id=None,
            is_saved=d.get("has_application", False),
        )
        for d in deadlines
    ]


# Notification Endpoints
@router.get(
    "/notifications",
    response={200: List[NotificationOut], 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="List notifications",
)
@paginate
def list_notifications(request: HttpRequest, unread_only: bool = False):
    """
    List notifications for the authenticated user's organization.

    Args:
        unread_only: If True, only return unread notifications

    Returns:
        Paginated list of notifications, sorted by creation date
    """
    user = request.auth
    service = NotificationService()
    notifications = service.get_notifications(user, unread_only)

    return [
        NotificationOut(
            id=n.id,
            type=n.notification_type,
            title=n.title,
            message=n.message,
            is_read=n.is_read,
            created_at=n.created_at,
            related_object_id=n.related_object_id,
        )
        for n in notifications
    ]


@router.post(
    "/notifications/{notification_id}/read",
    response={200: dict, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Mark notification as read",
)
def mark_notification_read(request: HttpRequest, notification_id: int):
    """
    Mark a specific notification as read.

    Args:
        notification_id: ID of the notification to mark as read

    Returns:
        Success message
    """
    user = request.auth

    try:
        notification = Notification.objects.get(id=notification_id, user=user)
        service = NotificationService()
        service.mark_as_read(notification)
        return 200, {"message": "Notification marked as read"}
    except Notification.DoesNotExist:
        return 404, {"detail": "Notification not found"}


@router.post(
    "/notifications/read-all",
    response={200: dict, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Mark all notifications as read",
)
def mark_all_notifications_read(request: HttpRequest):
    """
    Mark all notifications as read for the authenticated user.

    Returns:
        Success message with count of notifications marked as read
    """
    user = request.auth
    service = NotificationService()
    count = service.mark_all_as_read(user)
    return 200, {"message": f"{count} notifications marked as read"}


@router.delete(
    "/notifications/{notification_id}",
    response={204: None, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Delete notification",
)
def delete_notification(request: HttpRequest, notification_id: int):
    """
    Delete a specific notification.

    Args:
        notification_id: ID of the notification to delete

    Returns:
        204 No Content on success
    """
    user = request.auth

    try:
        notification = Notification.objects.get(id=notification_id, user=user)
        service = NotificationService()
        service.delete_notification(notification)
        return 204, None
    except Notification.DoesNotExist:
        return 404, {"detail": "Notification not found"}


@router.get(
    "/notifications/unread-count",
    response={200: dict, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get unread notification count",
)
def get_unread_count(request: HttpRequest):
    """
    Get the count of unread notifications.

    Returns:
        Dictionary with unread_count
    """
    user = request.auth
    count = Notification.objects.filter(user=user, is_read=False).count()
    return 200, {"unread_count": count}


# Analytics Endpoints
@router.get(
    "/analytics/trends",
    response={200: AnalyticsTrendsOut, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get analytics trends",
)
def get_analytics_trends(request: HttpRequest, days: int = 90):
    """
    Get analytics trends over time for proposals, applications, and matches.

    Args:
        days: Number of days to analyze (default: 90)

    Returns:
        Time-series data showing trends
    """
    user = request.auth
    organization = user.organization
    service = AnalyticsService()
    trends = service.get_trends(organization, days)

    return 200, AnalyticsTrendsOut(**trends)


@router.get(
    "/analytics/categories",
    response={200: AnalyticsCategoriesOut, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get analytics by category",
)
def get_analytics_categories(request: HttpRequest):
    """
    Get analytics breakdown by grant categories.

    Returns:
        Distribution of applications and success rates by category
    """
    user = request.auth
    organization = user.organization
    service = AnalyticsService()
    categories = service.get_category_breakdown(organization)

    return 200, AnalyticsCategoriesOut(**categories)


@router.get(
    "/analytics/success-rate",
    response={200: AnalyticsSuccessRateOut, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get success rate analytics",
)
def get_success_rate(request: HttpRequest):
    """
    Get detailed success rate analytics.

    Returns:
        Overall success rate, success by category, and success by amount
    """
    user = request.auth
    organization = user.organization
    service = AnalyticsService()
    success_rate = service.get_success_rate(organization)

    return 200, AnalyticsSuccessRateOut(**success_rate)


@router.get(
    "/analytics/funding",
    response={200: AnalyticsFundingOut, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get funding analytics",
)
def get_funding_analytics(request: HttpRequest):
    """
    Get funding analytics including total requested, awarded, and pending.

    Returns:
        Funding statistics and breakdown by status
    """
    user = request.auth
    organization = user.organization
    service = AnalyticsService()
    funding = service.get_funding_analytics(organization)

    return 200, AnalyticsFundingOut(**funding)


# Made with Bob
