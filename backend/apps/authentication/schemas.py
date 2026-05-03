"""
Pydantic schemas for authentication endpoints.
"""

from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator


class RegisterSchema(BaseModel):
    """Schema for user registration."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=8, description="Password (minimum 8 characters)"
    )
    name: str = Field(..., min_length=1, max_length=255, description="User name")
    organization_name: str = Field(
        ..., min_length=1, max_length=255, description="Organization name"
    )

    @validator("password")
    def validate_password(cls, v):
        """Validate password strength."""
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v


class LoginSchema(BaseModel):
    """Schema for user login."""

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponseSchema(BaseModel):
    """Schema for token response."""

    access: str = Field(..., description="Access token")
    refresh: str = Field(..., description="Refresh token")
    token_type: str = Field(default="Bearer", description="Token type")


class RefreshTokenSchema(BaseModel):
    """Schema for token refresh."""

    refresh: str = Field(..., description="Refresh token")


from datetime import datetime

class UserResponseSchema(BaseModel):
    """Schema for user response."""

    id: UUID
    email: EmailStr
    name: str
    role: str
    organization_id: UUID
    organization_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ChangePasswordSchema(BaseModel):
    """Schema for changing password."""

    old_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ..., min_length=8, description="New password (minimum 8 characters)"
    )

    @validator("new_password")
    def validate_new_password(cls, v, values):
        """Validate new password."""
        if "old_password" in values and v == values["old_password"]:
            raise ValueError("New password must be different from old password")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isalpha() for char in v):
            raise ValueError("Password must contain at least one letter")
        return v


class UpdateProfileSchema(BaseModel):
    """Schema for updating user profile."""

    name: Optional[str] = Field(
        None, min_length=1, max_length=255, description="User name"
    )
    email: Optional[EmailStr] = Field(None, description="User email address")


class MessageResponseSchema(BaseModel):
    """Schema for simple message responses."""

    message: str = Field(..., description="Response message")
    success: bool = Field(default=True, description="Operation success status")


class ErrorResponseSchema(BaseModel):
    """Schema for error responses."""

    detail: str = Field(..., description="Error detail message")
    code: Optional[str] = Field(None, description="Error code")


# Made with Bob
