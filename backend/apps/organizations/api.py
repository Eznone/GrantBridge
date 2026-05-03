"""
Organization API endpoints.
"""

from ninja import Router
from django.http import HttpRequest

from apps.authentication.api import JWTAuth
from apps.organizations.schemas import (
    OrganizationResponseSchema,
    UpdateOrganizationSchema,
    PatchOrganizationSchema,
    OrganizationStatsSchema,
)
from apps.organizations.services import OrganizationService
from apps.authentication.schemas import ErrorResponseSchema

# Create router
router = Router(tags=["Organizations"])


@router.get(
    "/me",
    response={200: OrganizationResponseSchema, 404: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get current organization",
)
def get_my_organization(request: HttpRequest):
    """
    Get the current user's organization details.
    """
    user = request.auth
    organization = user.organization

    return 200, OrganizationResponseSchema(
        id=organization.id,
        name=organization.name,
        mission=organization.mission,
        description=organization.description,
        website=organization.website,
        annual_budget=organization.annual_budget,
        goals=organization.goals,
        categories=organization.categories,
        tags=organization.tags,
        contact_email=organization.contact_email,
        contact_phone=organization.contact_phone,
        address=organization.address,
        city=organization.city,
        country=organization.country,
        founded_year=organization.founded_year,
        team_size=organization.team_size,
        created_at=organization.created_at.isoformat(),
        updated_at=organization.updated_at.isoformat(),
    )


@router.put(
    "/me",
    response={200: OrganizationResponseSchema, 400: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Update organization (full update)",
)
def update_my_organization(request: HttpRequest, payload: UpdateOrganizationSchema):
    """
    Perform a full update of the current user's organization.
    All fields must be provided.
    """
    user = request.auth
    organization = user.organization

    try:
        updated_org = OrganizationService.update_organization(
            organization=organization,
            name=payload.name,
            mission=payload.mission,
            description=payload.description,
            website=payload.website,
            annual_budget=payload.annual_budget,
            goals=payload.goals,
            categories=payload.categories,
            tags=payload.tags,
            contact_email=payload.contact_email,
            contact_phone=payload.contact_phone,
            address=payload.address,
            city=payload.city,
            country=payload.country,
            founded_year=payload.founded_year,
            team_size=payload.team_size,
        )

        return 200, OrganizationResponseSchema(
            id=updated_org.id,
            name=updated_org.name,
            mission=updated_org.mission,
            description=updated_org.description,
            website=updated_org.website,
            annual_budget=updated_org.annual_budget,
            goals=updated_org.goals,
            categories=updated_org.categories,
            tags=updated_org.tags,
            contact_email=updated_org.contact_email,
            contact_phone=updated_org.contact_phone,
            address=updated_org.address,
            city=updated_org.city,
            country=updated_org.country,
            founded_year=updated_org.founded_year,
            team_size=updated_org.team_size,
            created_at=updated_org.created_at.isoformat(),
            updated_at=updated_org.updated_at.isoformat(),
        )

    except Exception as e:
        return 400, ErrorResponseSchema(
            detail="Failed to update organization", code="UPDATE_ERROR"
        )


@router.patch(
    "/me",
    response={200: OrganizationResponseSchema, 400: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Partially update organization",
)
def patch_my_organization(request: HttpRequest, payload: PatchOrganizationSchema):
    """
    Perform a partial update of the current user's organization.
    Only provided fields will be updated.
    """
    user = request.auth
    organization = user.organization

    try:
        # Build update dict with only provided fields
        update_data = payload.dict(exclude_unset=True)

        updated_org = OrganizationService.update_organization(
            organization=organization, **update_data
        )

        return 200, OrganizationResponseSchema(
            id=updated_org.id,
            name=updated_org.name,
            mission=updated_org.mission,
            description=updated_org.description,
            website=updated_org.website,
            annual_budget=updated_org.annual_budget,
            goals=updated_org.goals,
            categories=updated_org.categories,
            tags=updated_org.tags,
            contact_email=updated_org.contact_email,
            contact_phone=updated_org.contact_phone,
            address=updated_org.address,
            city=updated_org.city,
            country=updated_org.country,
            founded_year=updated_org.founded_year,
            team_size=updated_org.team_size,
            created_at=updated_org.created_at.isoformat(),
            updated_at=updated_org.updated_at.isoformat(),
        )

    except Exception as e:
        return 400, ErrorResponseSchema(
            detail="Failed to update organization", code="UPDATE_ERROR"
        )


@router.get(
    "/me/stats",
    response={200: OrganizationStatsSchema},
    auth=JWTAuth(),
    summary="Get organization statistics",
)
def get_my_organization_stats(request: HttpRequest):
    """
    Get comprehensive statistics for the current user's organization.

    Includes:
    - Application statistics (total, active, approved, rejected)
    - Proposal statistics (total, draft, submitted)
    - Funding statistics (requested, received)
    - Success rate
    - Grant match statistics
    """
    user = request.auth
    organization = user.organization

    stats = OrganizationService.get_organization_stats(organization)

    return 200, OrganizationStatsSchema(**stats)


# Made with Bob
