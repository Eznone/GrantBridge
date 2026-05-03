"""
Proposal API endpoints for GrantBridge.
Provides proposal CRUD, submission, and export functionality.
"""

from typing import List
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from ninja import Router
from ninja.pagination import paginate

from apps.authentication.api import JWTAuth
from apps.proposals.models import Proposal
from apps.proposals.schemas import (
    ProposalCreateSchema,
    ProposalUpdateSchema,
    ProposalSubmitSchema,
    ProposalResponseSchema,
    ProposalListItemSchema,
    ProposalFilterSchema,
    ExportFormat,
    ProposalVersionSchema,
)
from apps.proposals.services import ProposalService

router = Router(tags=["Proposals"])


@router.get(
    "/proposals",
    response=List[ProposalListItemSchema],
    auth=JWTAuth(),
    summary="List proposals",
)
def list_proposals(
    request,
    status: str = None,
    grant_id: str = None,
    ai_generated: bool = None,
    search: str = None,
    page: int = 1,
    page_size: int = 20,
):
    """
    List all proposals for the user's organization with filtering.

    Query Parameters:
    - status: Filter by status (draft, review, submitted, approved, rejected)
    - grant_id: Filter by grant ID
    - ai_generated: Filter by AI generation status
    - search: Search in title and content
    - page: Page number (default: 1)
    - page_size: Items per page (default: 20, max: 100)
    """
    organization = request.auth.organization

    proposals, total, pages = ProposalService.list_proposals(
        organization=organization,
        status=status,
        grant_id=grant_id,
        ai_generated=ai_generated,
        search=search,
        page=page,
        page_size=min(page_size, 100),
    )

    return [ProposalListItemSchema.from_orm(p) for p in proposals]


@router.post(
    "/proposals",
    response={201: ProposalResponseSchema},
    auth=JWTAuth(),
    summary="Create a new proposal",
)
def create_proposal(request, payload: ProposalCreateSchema):
    """
    Create a new proposal for a grant.
    """
    organization = request.auth.organization
    user = request.auth

    proposal = ProposalService.create_proposal(
        organization=organization,
        user=user,
        grant_id=payload.grant_id,
        title=payload.title,
        content=payload.content,
    )

    return 201, ProposalResponseSchema.from_orm(proposal)


@router.get(
    "/proposals/{proposal_id}",
    response=ProposalResponseSchema,
    auth=JWTAuth(),
    summary="Get proposal details",
)
def get_proposal(request, proposal_id: str):
    """
    Get detailed information about a specific proposal.
    """
    organization = request.auth.organization
    proposal = ProposalService.get_proposal(proposal_id, organization)

    return ProposalResponseSchema.from_orm(proposal)


@router.put(
    "/proposals/{proposal_id}",
    response=ProposalResponseSchema,
    auth=JWTAuth(),
    summary="Update a proposal",
)
def update_proposal(request, proposal_id: str, payload: ProposalUpdateSchema):
    """
    Update an existing proposal.
    Only draft and review proposals can be edited.
    """
    organization = request.auth.organization
    proposal = ProposalService.get_proposal(proposal_id, organization)

    try:
        updated_proposal = ProposalService.update_proposal(
            proposal=proposal,
            title=payload.title,
            content=payload.content,
            status=payload.status,
        )
        return ProposalResponseSchema.from_orm(updated_proposal)
    except ValueError as e:
        return {"error": str(e)}, 400


@router.patch(
    "/proposals/{proposal_id}",
    response=ProposalResponseSchema,
    auth=JWTAuth(),
    summary="Partially update a proposal",
)
def patch_proposal(request, proposal_id: str, payload: ProposalUpdateSchema):
    """
    Partially update a proposal (same as PUT for this endpoint).
    """
    return update_proposal(request, proposal_id, payload)


@router.delete(
    "/proposals/{proposal_id}",
    response={200: dict},
    auth=JWTAuth(),
    summary="Delete a proposal",
)
def delete_proposal(request, proposal_id: str):
    """
    Delete a proposal. Only draft proposals can be deleted.
    """
    organization = request.auth.organization
    proposal = ProposalService.get_proposal(proposal_id, organization)

    try:
        ProposalService.delete_proposal(proposal)
        return {"message": "Proposal deleted successfully"}
    except ValueError as e:
        return {"error": str(e)}, 400


@router.post(
    "/proposals/{proposal_id}/submit",
    response=ProposalResponseSchema,
    auth=JWTAuth(),
    summary="Submit a proposal",
)
def submit_proposal(request, proposal_id: str, payload: ProposalSubmitSchema):
    """
    Submit a proposal for review/approval.
    """
    organization = request.auth.organization
    proposal = ProposalService.get_proposal(proposal_id, organization)

    try:
        submitted = ProposalService.submit_proposal(
            proposal=proposal, submission_method=payload.submission_method
        )
        return ProposalResponseSchema.from_orm(submitted)
    except ValueError as e:
        return {"error": str(e)}, 400


@router.post(
    "/proposals/{proposal_id}/version",
    response={201: ProposalResponseSchema},
    auth=JWTAuth(),
    summary="Create a new version",
)
def create_version(request, proposal_id: str):
    """
    Create a new version of a submitted proposal.
    """
    organization = request.auth.organization
    proposal = ProposalService.get_proposal(proposal_id, organization)

    try:
        new_version = ProposalService.create_version(proposal)
        return 201, ProposalResponseSchema.from_orm(new_version)
    except ValueError as e:
        return {"error": str(e)}, 400


@router.get(
    "/proposals/{proposal_id}/versions",
    response=List[ProposalVersionSchema],
    auth=JWTAuth(),
    summary="Get proposal versions",
)
def get_versions(request, proposal_id: str):
    """
    Get all versions of a proposal.
    """
    organization = request.auth.organization
    proposal = ProposalService.get_proposal(proposal_id, organization)

    versions = ProposalService.get_proposal_versions(proposal)

    return [ProposalVersionSchema.from_orm(v, str(proposal.id)) for v in versions]


@router.post(
    "/proposals/{proposal_id}/export",
    auth=JWTAuth(),
    summary="Export proposal to PDF or DOCX",
)
def export_proposal(request, proposal_id: str, payload: ExportFormat):
    """
    Export a proposal to PDF or DOCX format.

    Returns the file as a download.
    """
    organization = request.auth.organization
    proposal = ProposalService.get_proposal(proposal_id, organization)

    if payload.format.lower() == "pdf":
        content = ProposalService.export_to_pdf(proposal)
        content_type = "application/pdf"
        filename = f"proposal_{proposal.id}.pdf"
    elif payload.format.lower() == "docx":
        content = ProposalService.export_to_docx(proposal)
        content_type = (
            "application/vnd.openxmlformats-officedocument." "wordprocessingml.document"
        )
        filename = f"proposal_{proposal.id}.docx"
    else:
        return {"error": "Invalid format. Use 'pdf' or 'docx'"}, 400

    response = HttpResponse(content, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@router.get(
    "/proposals/stats", response=dict, auth=JWTAuth(), summary="Get proposal statistics"
)
def get_proposal_stats(request):
    """
    Get statistics about proposals for the organization.
    """
    organization = request.auth.organization
    return ProposalService.get_proposal_stats(organization)


# Made with Bob
