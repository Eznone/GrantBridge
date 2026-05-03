"""
Pydantic schemas for organization endpoints.
"""

from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from pydantic import BaseModel, Field, HttpUrl, validator


from datetime import datetime

class OrganizationResponseSchema(BaseModel):
    """Schema for organization response."""

    id: UUID
    name: str
    mission: str
    description: str
    website: str
    annual_budget: Decimal
    goals: List[str]
    categories: List[str]
    tags: List[str]
    contact_email: str
    contact_phone: str
    address: str
    city: str
    country: str
    founded_year: Optional[int]
    team_size: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UpdateOrganizationSchema(BaseModel):
    """Schema for updating organization (full update)."""

    name: str = Field(..., min_length=1, max_length=255)
    mission: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    website: str = Field(default="")
    annual_budget: Decimal = Field(..., ge=0)
    goals: List[str] = Field(default_factory=list)
    categories: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    contact_email: str = Field(default="")
    contact_phone: str = Field(default="")
    address: str = Field(default="")
    city: str = Field(default="")
    country: str = Field(default="")
    founded_year: Optional[int] = Field(None, ge=1800, le=2100)
    team_size: Optional[int] = Field(None, ge=1)


class PatchOrganizationSchema(BaseModel):
    """Schema for partial organization update."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    mission: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    website: Optional[str] = None
    annual_budget: Optional[Decimal] = Field(None, ge=0)
    goals: Optional[List[str]] = None
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    founded_year: Optional[int] = Field(None, ge=1800, le=2100)
    team_size: Optional[int] = Field(None, ge=1)


class OrganizationStatsSchema(BaseModel):
    """Schema for organization statistics."""

    total_grants_applied: int = Field(
        ..., description="Total number of grants applied to"
    )
    active_applications: int = Field(..., description="Number of active applications")
    approved_applications: int = Field(
        ..., description="Number of approved applications"
    )
    rejected_applications: int = Field(
        ..., description="Number of rejected applications"
    )
    total_proposals: int = Field(..., description="Total number of proposals created")
    draft_proposals: int = Field(..., description="Number of draft proposals")
    submitted_proposals: int = Field(..., description="Number of submitted proposals")
    total_funding_requested: Decimal = Field(
        ..., description="Total amount of funding requested"
    )
    total_funding_received: Decimal = Field(
        ..., description="Total amount of funding received"
    )
    success_rate: float = Field(..., description="Application success rate (0-100)")
    grant_matches_count: int = Field(
        ..., description="Number of AI-generated grant matches"
    )
    top_grant_matches_count: int = Field(
        ..., description="Number of high-quality matches (score >= 80)"
    )


# Made with Bob
