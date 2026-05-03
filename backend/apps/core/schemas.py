"""
Core schemas for dashboard, notifications, and analytics.
"""

from datetime import datetime
from typing import List, Optional
from ninja import Schema


from uuid import UUID

# Dashboard Schemas
class DashboardStatsOut(Schema):
    """Dashboard statistics output schema."""

    total_proposals: int
    active_applications: int
    saved_grants: int
    pending_matches: int
    success_rate: float
    total_funding: float


class UpcomingDeadlineOut(Schema):
    """Upcoming deadline output schema."""

    grant_id: UUID
    grant_title: str
    deadline: datetime
    days_remaining: int
    application_id: Optional[UUID] = None
    is_saved: bool


# Notification Schemas
class NotificationOut(Schema):
    """Notification output schema."""

    id: UUID
    type: str
    title: str
    message: str
    is_read: bool
    created_at: datetime
    related_object_id: Optional[UUID] = None


class NotificationMarkReadIn(Schema):
    """Schema for marking notification as read."""

    notification_id: UUID


# Analytics Schemas
class TrendDataPoint(Schema):
    """Single data point in a trend."""

    date: str
    count: int


class AnalyticsTrendsOut(Schema):
    """Analytics trends output schema."""

    proposals: List[TrendDataPoint]
    applications: List[TrendDataPoint]
    matches: List[TrendDataPoint]
    period_days: int


class CategoryBreakdown(Schema):
    """Category breakdown data."""

    category: str
    total_applications: int
    successful_applications: int
    success_rate: float
    total_funding_requested: float
    total_funding_awarded: float


class AnalyticsCategoriesOut(Schema):
    """Analytics categories output schema."""

    categories: List[CategoryBreakdown]
    total_categories: int


class SuccessRateByCategory(Schema):
    """Success rate by category."""

    category: str
    success_rate: float
    total_applications: int


class SuccessRateByAmount(Schema):
    """Success rate by amount range."""

    range_label: str
    min_amount: float
    max_amount: Optional[float]
    success_rate: float
    total_applications: int


class AnalyticsSuccessRateOut(Schema):
    """Analytics success rate output schema."""

    overall_success_rate: float
    total_applications: int
    successful_applications: int
    by_category: List[SuccessRateByCategory]
    by_amount_range: List[SuccessRateByAmount]


class FundingByStatus(Schema):
    """Funding breakdown by status."""

    status: str
    count: int
    total_amount: float
    average_amount: float


class AnalyticsFundingOut(Schema):
    """Analytics funding output schema."""

    total_requested: float
    total_awarded: float
    total_pending: float
    total_rejected: float
    by_status: List[FundingByStatus]
    average_request_amount: float
    average_award_amount: float


# Made with Bob
