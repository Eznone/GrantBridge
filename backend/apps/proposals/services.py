"""
Business logic for Proposal operations.
"""

from typing import List, Tuple, Optional
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone

from apps.proposals.models import Proposal
from apps.grants.models import Grant
from apps.organizations.models import Organization
from apps.authentication.models import User


class ProposalService:
    """Service class for proposal operations."""

    @staticmethod
    def list_proposals(
        organization: Organization,
        status: Optional[str] = None,
        grant_id: Optional[str] = None,
        ai_generated: Optional[bool] = None,
        search: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Proposal], int, int]:
        """
        List proposals with filtering and pagination.

        Returns: (proposals, total_count, total_pages)
        """
        queryset = Proposal.objects.filter(organization=organization).select_related(
            "grant", "created_by"
        )

        # Apply filters
        if status:
            queryset = queryset.filter(status=status)

        if grant_id:
            queryset = queryset.filter(grant_id=grant_id)

        if ai_generated is not None:
            queryset = queryset.filter(ai_generated=ai_generated)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )

        # Pagination
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        return (list(page_obj.object_list), paginator.count, paginator.num_pages)

    @staticmethod
    def get_proposal(proposal_id: str, organization: Organization) -> Proposal:
        """Get a single proposal by ID."""
        return get_object_or_404(Proposal, id=proposal_id, organization=organization)

    @staticmethod
    def create_proposal(
        organization: Organization,
        user: User,
        grant_id: str,
        title: str,
        content: str = "",
    ) -> Proposal:
        """Create a new proposal."""
        grant = get_object_or_404(Grant, id=grant_id)

        proposal = Proposal.objects.create(
            organization=organization,
            created_by=user,
            grant=grant,
            title=title,
            content=content,
            status="draft",
        )

        return proposal

    @staticmethod
    def update_proposal(
        proposal: Proposal,
        title: Optional[str] = None,
        content: Optional[str] = None,
        status: Optional[str] = None,
    ) -> Proposal:
        """Update an existing proposal."""
        if not proposal.is_editable and status != proposal.status:
            raise ValueError("Cannot edit a submitted/approved/rejected proposal")

        if title is not None:
            proposal.title = title

        if content is not None:
            proposal.content = content

        if status is not None:
            # Validate status transition
            valid_statuses = ["draft", "review", "submitted", "approved", "rejected"]
            if status not in valid_statuses:
                raise ValueError(f"Invalid status: {status}")
            proposal.status = status

        proposal.save()
        return proposal

    @staticmethod
    def delete_proposal(proposal: Proposal) -> None:
        """Delete a proposal (only if not submitted)."""
        if proposal.is_submitted:
            raise ValueError("Cannot delete a submitted proposal")

        proposal.delete()

    @staticmethod
    def submit_proposal(
        proposal: Proposal, submission_method: str = "portal"
    ) -> Proposal:
        """Submit a proposal."""
        if proposal.status == "submitted":
            raise ValueError("Proposal is already submitted")

        proposal.status = "submitted"
        proposal.submitted_at = timezone.now()
        proposal.submission_method = submission_method
        proposal.save()

        return proposal

    @staticmethod
    def create_version(proposal: Proposal) -> Proposal:
        """Create a new version of a proposal."""
        if not proposal.is_submitted:
            raise ValueError("Can only create versions of submitted proposals")

        return proposal.create_new_version()

    @staticmethod
    def get_proposal_versions(proposal: Proposal) -> List[Proposal]:
        """Get all versions of a proposal."""
        versions = []

        # Get all child versions
        versions.extend(
            Proposal.objects.filter(parent_version=proposal).order_by("version")
        )

        # Get parent versions
        current = proposal.parent_version
        while current:
            versions.insert(0, current)
            current = current.parent_version

        # Add current proposal
        versions.append(proposal)

        return versions

    @staticmethod
    def export_to_pdf(proposal: Proposal) -> bytes:
        """
        Export proposal to PDF format.
        This is a placeholder - actual implementation will use reportlab.
        """
        # TODO: Implement PDF generation using reportlab
        # For now, return a simple message
        content = f"""
        Proposal: {proposal.title}
        Status: {proposal.status}
        Organization: {proposal.organization.name}
        Grant: {proposal.grant.title}
        
        Content:
        {proposal.content}
        """
        return content.encode("utf-8")

    @staticmethod
    def export_to_docx(proposal: Proposal) -> bytes:
        """
        Export proposal to DOCX format.
        This is a placeholder - actual implementation will use python-docx.
        """
        # TODO: Implement DOCX generation using python-docx
        # For now, return a simple message
        content = f"""
        Proposal: {proposal.title}
        Status: {proposal.status}
        Organization: {proposal.organization.name}
        Grant: {proposal.grant.title}
        
        Content:
        {proposal.content}
        """
        return content.encode("utf-8")

    @staticmethod
    def get_proposal_stats(organization: Organization) -> dict:
        """Get statistics about proposals for an organization."""
        proposals = Proposal.objects.filter(organization=organization)

        return {
            "total": proposals.count(),
            "draft": proposals.filter(status="draft").count(),
            "review": proposals.filter(status="review").count(),
            "submitted": proposals.filter(status="submitted").count(),
            "approved": proposals.filter(status="approved").count(),
            "rejected": proposals.filter(status="rejected").count(),
            "ai_generated": proposals.filter(ai_generated=True).count(),
        }


# Made with Bob
