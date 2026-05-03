"""
Grant Matching API endpoints for GrantBridge.
Provides AI-powered grant matching and recommendation functionality.
"""

from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router

from apps.authentication.api import JWTAuth
from apps.matching.models import GrantMatch
from apps.matching.schemas import (
    GrantMatchResponseSchema,
    MatchFilterSchema,
    DismissMatchSchema,
    CalculateMatchesSchema,
    MatchStatsSchema,
    CalculateMatchesResponseSchema,
)
from apps.matching.services import MatchingService

router = Router(tags=["Matching"])


@router.get(
    "/matches",
    response=List[GrantMatchResponseSchema],
    auth=JWTAuth(),
    summary="Get grant matches",
)
def get_matches(
    request,
    min_score: float = None,
    max_score: float = None,
    quality: str = None,
    include_dismissed: bool = False,
    limit: int = 20,
):
    """
    Get AI-powered grant matches for the organization.

    Query Parameters:
    - min_score: Minimum match score (0-100)
    - max_score: Maximum match score (0-100)
    - quality: Filter by quality (Excellent, Good, Fair, Poor)
    - include_dismissed: Include dismissed matches
    - limit: Maximum number of matches (default: 20, max: 100)
    """
    organization = request.auth.organization

    matches = MatchingService.get_matches(
        organization=organization,
        min_score=min_score,
        max_score=max_score,
        quality=quality,
        include_dismissed=include_dismissed,
        limit=min(limit, 100),
    )

    return [GrantMatchResponseSchema.from_orm(m) for m in matches]


@router.get(
    "/matches/{match_id}",
    response=GrantMatchResponseSchema,
    auth=JWTAuth(),
    summary="Get match details",
)
def get_match(request, match_id: str):
    """
    Get detailed information about a specific grant match.
    """
    organization = request.auth.organization

    try:
        match = MatchingService.get_match(match_id, organization)
        return GrantMatchResponseSchema.from_orm(match)
    except GrantMatch.DoesNotExist:
        return {"error": "Match not found"}, 404


@router.post(
    "/matches/{match_id}/dismiss",
    response=GrantMatchResponseSchema,
    auth=JWTAuth(),
    summary="Dismiss a match",
)
def dismiss_match(request, match_id: str, payload: DismissMatchSchema):
    """
    Dismiss a grant match if not interested.
    """
    organization = request.auth.organization

    try:
        match = MatchingService.get_match(match_id, organization)
        dismissed_match = MatchingService.dismiss_match(match, reason=payload.reason)
        return GrantMatchResponseSchema.from_orm(dismissed_match)
    except GrantMatch.DoesNotExist:
        return {"error": "Match not found"}, 404


@router.post(
    "/matches/{match_id}/undismiss",
    response=GrantMatchResponseSchema,
    auth=JWTAuth(),
    summary="Restore a dismissed match",
)
def undismiss_match(request, match_id: str):
    """
    Restore a previously dismissed match.
    """
    organization = request.auth.organization

    try:
        match = MatchingService.get_match(match_id, organization)
        restored_match = MatchingService.undismiss_match(match)
        return GrantMatchResponseSchema.from_orm(restored_match)
    except GrantMatch.DoesNotExist:
        return {"error": "Match not found"}, 404


@router.post(
    "/matches/calculate",
    response=CalculateMatchesResponseSchema,
    auth=JWTAuth(),
    summary="Calculate grant matches",
)
def calculate_matches(request, payload: CalculateMatchesSchema):
    """
    Trigger calculation of grant matches for the organization.

    This will analyze all available grants and create match scores
    based on organization profile, goals, and categories.

    Note: This uses a simple algorithm. AI-powered matching with
    FAISS and watsonx.ai will be implemented in later steps.
    """
    organization = request.auth.organization

    result = MatchingService.calculate_matches(
        organization=organization,
        grant_ids=payload.grant_ids,
        force_recalculate=payload.force_recalculate,
    )

    return CalculateMatchesResponseSchema(**result)


@router.get(
    "/matches/stats",
    response=MatchStatsSchema,
    auth=JWTAuth(),
    summary="Get match statistics",
)
def get_match_stats(request):
    """
    Get statistics about grant matches for the organization.
    """
    organization = request.auth.organization
    stats = MatchingService.get_match_stats(organization)

    return MatchStatsSchema.from_dict(stats)


@router.get(
    "/matches/top",
    response=List[GrantMatchResponseSchema],
    auth=JWTAuth(),
    summary="Get top matches",
)
def get_top_matches(request, limit: int = 10):
    """
    Get the top grant matches for the organization.

    Query Parameters:
    - limit: Number of top matches to return (default: 10, max: 50)
    """
    organization = request.auth.organization

    matches = GrantMatch.get_top_matches(organization, limit=min(limit, 50))

    return [GrantMatchResponseSchema.from_orm(m) for m in matches]


# Made with Bob
