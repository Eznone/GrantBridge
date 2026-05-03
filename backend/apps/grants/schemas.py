"""
Pydantic schemas for grant endpoints.
"""

from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, Field


class GrantResponseSchema(BaseModel):
    """Schema for grant response."""

    id: UUID
    title: str
    description: str
    funder_name: str
    funder_website: str
    funding_amount: Decimal
    currency: str
    deadline: str
    application_url: str
    tags: List[str]
    categories: List[str]
    eligibility: List[str]
    requirements: List[str]
    focus_areas: List[str]
    geographic_scope: str
    is_active: bool
    days_until_deadline: Optional[int]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class GrantListResponseSchema(BaseModel):
    """Schema for paginated grant list response."""

    grants: List[GrantResponseSchema]
    total: int
    page: int
    page_size: int
    total_pages: int


class GrantFilterSchema(BaseModel):
    """Schema for filtering grants."""

    search: Optional[str] = Field(
        None, description="Search in title, description, funder name"
    )
    categories: Optional[List[str]] = Field(None, description="Filter by categories")
    tags: Optional[List[str]] = Field(None, description="Filter by tags")
    min_amount: Optional[Decimal] = Field(
        None, ge=0, description="Minimum funding amount"
    )
    max_amount: Optional[Decimal] = Field(
        None, ge=0, description="Maximum funding amount"
    )
    geographic_scope: Optional[str] = Field(
        None, description="Filter by geographic scope"
    )
    is_active: Optional[bool] = Field(None, description="Filter by active status")
    deadline_before: Optional[datetime] = Field(
        None, description="Deadline before this date"
    )
    deadline_after: Optional[datetime] = Field(
        None, description="Deadline after this date"
    )
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(20, ge=1, le=100, description="Items per page")
    sort_by: Optional[str] = Field(
        "deadline", description="Sort field: deadline, funding_amount, created_at"
    )
    sort_order: Optional[str] = Field("asc", description="Sort order: asc or desc")


class SavedGrantResponseSchema(BaseModel):
    """Schema for saved grant response."""

    id: UUID
    grant: GrantResponseSchema
    saved_at: str
    notes: str

    class Config:
        from_attributes = True


class SaveGrantSchema(BaseModel):
    """Schema for saving a grant."""

    notes: Optional[str] = Field(
        "",
        max_length=1000,
        description="Optional notes about why this grant is interesting",
    )


class ApplicationResponseSchema(BaseModel):
    """Schema for application response."""

    id: UUID
    grant_id: UUID
    grant_title: str
    status: str
    progress: int
    submitted_at: Optional[str]
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# Made with Bob
