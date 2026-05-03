"""
Pydantic schemas for Grant Matching API endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import Field
from ninja import Schema


class GrantMatchResponseSchema(Schema):
    """Schema for grant match response."""

    id: str
    grant_id: str
    organization_id: str
    match_score: float = Field(..., ge=0, le=100)
    match_percentage: str
    match_quality: str
    match_reasons: List[str]
    recommended_actions: List[str]
    algorithm_version: str
    is_dismissed: bool
    dismissed_at: Optional[datetime]
    dismissed_reason: Optional[str]
    created_at: datetime
    updated_at: datetime

    # Include grant details for convenience
    grant_title: Optional[str] = None
    grant_funder: Optional[str] = None
    grant_amount: Optional[float] = None
    grant_deadline: Optional[datetime] = None

    @staticmethod
    def from_orm(match) -> "GrantMatchResponseSchema":
        """Convert GrantMatch model to schema."""
        return GrantMatchResponseSchema(
            id=str(match.id),
            grant_id=str(match.grant_id),
            organization_id=str(match.organization_id),
            match_score=match.match_score,
            match_percentage=match.match_percentage,
            match_quality=match.match_quality,
            match_reasons=match.match_reasons,
            recommended_actions=match.recommended_actions,
            algorithm_version=match.algorithm_version,
            is_dismissed=match.is_dismissed,
            dismissed_at=match.dismissed_at,
            dismissed_reason=match.dismissed_reason,
            created_at=match.created_at,
            updated_at=match.updated_at,
            grant_title=match.grant.title if match.grant else None,
            grant_funder=match.grant.funder_name if match.grant else None,
            grant_amount=float(match.grant.funding_amount) if match.grant else None,
            grant_deadline=match.grant.deadline if match.grant else None,
        )


class MatchFilterSchema(Schema):
    """Schema for filtering matches."""

    min_score: Optional[float] = Field(None, ge=0, le=100)
    max_score: Optional[float] = Field(None, ge=0, le=100)
    quality: Optional[str] = Field(
        None, description="Filter by quality: Excellent, Good, Fair, Poor"
    )
    include_dismissed: bool = Field(
        default=False, description="Include dismissed matches"
    )
    limit: int = Field(default=20, ge=1, le=100)


class DismissMatchSchema(Schema):
    """Schema for dismissing a match."""

    reason: Optional[str] = Field(None, description="Optional reason for dismissing")


class CalculateMatchesSchema(Schema):
    """Schema for triggering match calculation."""

    grant_ids: Optional[List[str]] = Field(
        None, description="Specific grant IDs to match (if None, matches all)"
    )
    force_recalculate: bool = Field(
        default=False, description="Recalculate even if matches exist"
    )


class MatchStatsSchema(Schema):
    """Schema for match statistics."""

    total_matches: int
    excellent_matches: int
    good_matches: int
    fair_matches: int
    poor_matches: int
    dismissed_matches: int
    average_score: float
    top_match_score: Optional[float]

    @staticmethod
    def from_dict(data: dict) -> "MatchStatsSchema":
        """Create schema from dictionary."""
        return MatchStatsSchema(**data)


class CalculateMatchesResponseSchema(Schema):
    """Schema for match calculation response."""

    matches_created: int
    matches_updated: int
    total_grants_processed: int
    average_score: float
    message: str


# Made with Bob
