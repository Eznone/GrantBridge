"""
Pydantic schemas for Proposal API endpoints.
"""

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from ninja import Schema


class ProposalCreateSchema(Schema):
    """Schema for creating a new proposal."""

    grant_id: str = Field(..., description="Grant ID this proposal is for")
    title: str = Field(..., min_length=1, max_length=500)
    content: str = Field(default="", description="Proposal content")


class ProposalUpdateSchema(Schema):
    """Schema for updating a proposal."""

    title: Optional[str] = Field(None, min_length=1, max_length=500)
    content: Optional[str] = None
    status: Optional[str] = Field(
        None, description="Status: draft, review, submitted, approved, rejected"
    )


class ProposalSubmitSchema(Schema):
    """Schema for submitting a proposal."""

    submission_method: str = Field(
        default="portal", description="How proposal was submitted"
    )


class AIGenerationMetadataSchema(Schema):
    """Schema for AI generation metadata."""

    model: str
    tokens_used: int = 0
    confidence: float = 0.0
    generated_at: str


class ProposalResponseSchema(Schema):
    """Schema for proposal response."""

    id: str
    grant_id: str
    organization_id: str
    created_by_id: Optional[str]
    title: str
    content: str
    status: str

    # AI metadata
    ai_generated: bool
    ai_model_used: Optional[str]
    ai_generation_summary: Optional[dict]

    # Submission info
    submitted_at: Optional[datetime]
    submission_method: Optional[str]

    # Versioning
    version: int
    parent_version_id: Optional[str]
    has_versions: bool
    version_count: int

    # Computed properties
    is_submitted: bool
    is_editable: bool
    word_count: int

    # Timestamps
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_orm(proposal) -> "ProposalResponseSchema":
        """Convert Proposal model to schema."""
        return ProposalResponseSchema(
            id=str(proposal.id),
            grant_id=str(proposal.grant_id),
            organization_id=str(proposal.organization_id),
            created_by_id=(
                str(proposal.created_by_id) if proposal.created_by_id else None
            ),
            title=proposal.title,
            content=proposal.content,
            status=proposal.status,
            ai_generated=proposal.ai_generated,
            ai_model_used=proposal.ai_model_used,
            ai_generation_summary=proposal.ai_generation_summary,
            submitted_at=proposal.submitted_at,
            submission_method=proposal.submission_method,
            version=proposal.version,
            parent_version_id=(
                str(proposal.parent_version_id) if proposal.parent_version_id else None
            ),
            has_versions=proposal.has_versions,
            version_count=proposal.version_count,
            is_submitted=proposal.is_submitted,
            is_editable=proposal.is_editable,
            word_count=proposal.word_count,
            created_at=proposal.created_at,
            updated_at=proposal.updated_at,
        )


class ProposalListItemSchema(Schema):
    """Schema for proposal list item (lighter version)."""

    id: str
    grant_id: str
    title: str
    status: str
    ai_generated: bool
    version: int
    word_count: int
    is_editable: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_orm(proposal) -> "ProposalListItemSchema":
        """Convert Proposal model to list item schema."""
        return ProposalListItemSchema(
            id=str(proposal.id),
            grant_id=str(proposal.grant_id),
            title=proposal.title,
            status=proposal.status,
            ai_generated=proposal.ai_generated,
            version=proposal.version,
            word_count=proposal.word_count,
            is_editable=proposal.is_editable,
            created_at=proposal.created_at,
            updated_at=proposal.updated_at,
        )


class ProposalFilterSchema(Schema):
    """Schema for filtering proposals."""

    status: Optional[str] = None
    grant_id: Optional[str] = None
    ai_generated: Optional[bool] = None
    search: Optional[str] = None
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class ExportFormat(Schema):
    """Schema for export format selection."""

    format: str = Field(..., description="Export format: pdf or docx")


class ExportResponseSchema(Schema):
    """Schema for export response."""

    file_url: str = Field(..., description="URL to download the exported file")
    file_name: str
    format: str
    expires_at: Optional[datetime] = None


class ProposalVersionSchema(Schema):
    """Schema for proposal version info."""

    id: str
    version: int
    title: str
    created_at: datetime
    is_current: bool

    @staticmethod
    def from_orm(proposal, current_id: str) -> "ProposalVersionSchema":
        """Convert Proposal model to version schema."""
        return ProposalVersionSchema(
            id=str(proposal.id),
            version=proposal.version,
            title=proposal.title,
            created_at=proposal.created_at,
            is_current=(str(proposal.id) == current_id),
        )


# Made with Bob
