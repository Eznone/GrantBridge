"""
Grant API endpoints for GrantBridge.
Provides grant discovery, search, filtering, and bookmark functionality.
"""

from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.pagination import paginate

from apps.authentication.api import JWTAuth
from apps.grants.models import Grant, SavedGrant
from apps.grants.schemas import (
    GrantResponseSchema,
    GrantListResponseSchema,
    GrantFilterSchema,
    SavedGrantResponseSchema,
    SaveGrantSchema,
    ApplicationResponseSchema,
)
from apps.grants.services import GrantService

router = Router(tags=["Grants"])


@router.get(
    "/grants",
    response=GrantListResponseSchema,
    auth=JWTAuth(),
    summary="List grants with filters",
)
def list_grants(
    request,
    page: int = 1,
    page_size: int = 20,
    search: str = None,
    categories: str = None,
    tags: str = None,
    min_amount: float = None,
    max_amount: float = None,
    deadline_from: str = None,
    deadline_to: str = None,
    geographic_scope: str = None,
    sort_by: str = "deadline",
):
    """
    List grants with advanced filtering and pagination.

    Query Parameters:
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20, max: 100)
    - search: Search in title, description, funder_name
    - categories: Comma-separated categories
    - tags: Comma-separated tags
    - min_amount: Minimum funding amount
    - max_amount: Maximum funding amount
    - deadline_from: Filter deadlines from date (ISO format)
    - deadline_to: Filter deadlines to date (ISO format)
    - geographic_scope: Geographic scope filter
    - sort_by: Sort field (deadline, funding_amount, -deadline, etc.)
    """
    # Parse comma-separated values
    categories_list = [c.strip() for c in categories.split(",")] if categories else None
    tags_list = [t.strip() for t in tags.split(",")] if tags else None

    # Handle sorting order
    sort_order = "asc"
    if sort_by and sort_by.startswith("-"):
        sort_order = "desc"
        sort_by = sort_by[1:]

    # Get grants from service
    grants, total, total_pages = GrantService.list_grants(
        search=search,
        categories=categories_list,
        tags=tags_list,
        min_amount=min_amount,
        max_amount=max_amount,
        deadline_after=deadline_from,
        deadline_before=deadline_to,
        geographic_scope=geographic_scope,
        page=page,
        page_size=min(page_size, 100),
        sort_by=sort_by or "deadline",
        sort_order=sort_order,
    )

    return {
        "grants": grants,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
    }


@router.get(
    "/grants/{grant_id}",
    response=GrantResponseSchema,
    auth=JWTAuth(),
    summary="Get grant details",
)
def get_grant(request, grant_id: str):
    """
    Get detailed information about a specific grant.
    """
    grant = GrantService.get_grant(grant_id)

    # Check if user's organization has saved this grant
    is_saved = False
    if hasattr(request.auth, "organization"):
        is_saved = GrantService.is_grant_saved(request.auth.organization, grant)

    grant_data = GrantResponseSchema.from_orm(grant)
    grant_data.is_saved = is_saved

    return grant_data


@router.post(
    "/grants/{grant_id}/save",
    response=SavedGrantResponseSchema,
    auth=JWTAuth(),
    summary="Save/bookmark a grant",
)
def save_grant(request, grant_id: str, payload: SaveGrantSchema):
    """
    Save a grant to the organization's bookmarks.
    """
    organization = request.auth.organization
    grant = get_object_or_404(Grant, id=grant_id)

    saved_grant = GrantService.save_grant(
        organization=organization, grant=grant, notes=payload.notes
    )

    return SavedGrantResponseSchema.from_orm(saved_grant)


@router.delete(
    "/grants/{grant_id}/save",
    response={200: dict},
    auth=JWTAuth(),
    summary="Unsave/unbookmark a grant",
)
def unsave_grant(request, grant_id: str):
    """
    Remove a grant from the organization's bookmarks.
    """
    organization = request.auth.organization
    grant = get_object_or_404(Grant, id=grant_id)

    GrantService.unsave_grant(organization, grant)

    return {"message": "Grant removed from saved list"}


@router.get(
    "/grants/saved",
    response=List[SavedGrantResponseSchema],
    auth=JWTAuth(),
    summary="List saved grants",
)
@paginate
def list_saved_grants(request):
    """
    List all grants saved by the user's organization.
    Supports pagination.
    """
    organization = request.auth.organization
    return GrantService.get_saved_grants(organization)


@router.get(
    "/applications",
    response=List[ApplicationResponseSchema],
    auth=JWTAuth(),
    summary="List organization's applications",
)
@paginate
def list_applications(request, status: str = None):
    """
    List all grant applications for the user's organization.

    Query Parameters:
    - status: Filter by status (draft, submitted, under_review, etc.)
    """
    organization = request.auth.organization
    return GrantService.get_organization_applications(organization, status=status)


@router.get(
    "/applications/{application_id}",
    response=ApplicationResponseSchema,
    auth=JWTAuth(),
    summary="Get application details",
)
def get_application(request, application_id: str):
    """
    Get detailed information about a specific application.
    """
    from apps.grants.models import Application

    organization = request.auth.organization
    application = get_object_or_404(
        Application, id=application_id, organization=organization
    )

    return ApplicationResponseSchema.from_orm(application)


# Made with Bob
