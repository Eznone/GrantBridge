"""
Authentication API endpoints.
"""

from typing import Dict
from ninja import Router
from ninja.security import HttpBearer
from django.http import HttpRequest
from pydantic import ValidationError

from apps.authentication.schemas import (
    RegisterSchema,
    LoginSchema,
    TokenResponseSchema,
    RefreshTokenSchema,
    UserResponseSchema,
    ChangePasswordSchema,
    UpdateProfileSchema,
    MessageResponseSchema,
    ErrorResponseSchema,
)
from apps.authentication.services import AuthenticationService
from apps.authentication.models import User

# JWT Token Generation (using PyJWT directly)
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class JWTAuth(HttpBearer):
    """JWT authentication for protected endpoints."""

    def authenticate(self, request: HttpRequest, token: str):
        """Authenticate request using JWT token."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            if user_id:
                user = AuthenticationService.get_user_by_id(user_id)
                if user and user.is_active:
                    return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        return None


def generate_tokens(user: User) -> Dict[str, str]:
    """
    Generate access and refresh tokens for a user.

    Args:
        user: User instance

    Returns:
        Dictionary with access and refresh tokens
    """
    access_payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=15),
        "iat": datetime.utcnow(),
        "type": "access",
    }

    refresh_payload = {
        "user_id": str(user.id),
        "exp": datetime.utcnow() + timedelta(days=7),
        "iat": datetime.utcnow(),
        "type": "refresh",
    }

    access_token = jwt.encode(access_payload, settings.SECRET_KEY, algorithm="HS256")

    refresh_token = jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm="HS256")

    return {"access": access_token, "refresh": refresh_token}


# Create router
router = Router(tags=["Authentication"])


@router.post(
    "/register",
    response={201: TokenResponseSchema, 400: ErrorResponseSchema},
    summary="Register a new user",
)
def register(request: HttpRequest, payload: RegisterSchema):
    """
    Register a new user and create their organization.

    Returns JWT tokens upon successful registration.
    """
    try:
        user, organization = AuthenticationService.register_user(
            email=payload.email,
            password=payload.password,
            name=payload.name,
            organization_name=payload.organization_name,
        )

        tokens = generate_tokens(user)
        return 201, TokenResponseSchema(**tokens)

    except ValueError as e:
        return 400, ErrorResponseSchema(detail=str(e), code="REGISTRATION_ERROR")
    except Exception as e:
        return 400, ErrorResponseSchema(
            detail="Registration failed", code="INTERNAL_ERROR"
        )


@router.post(
    "/login",
    response={200: TokenResponseSchema, 401: ErrorResponseSchema},
    summary="Login user",
)
def login(request: HttpRequest, payload: LoginSchema):
    """
    Authenticate user and return JWT tokens.
    """
    user = AuthenticationService.authenticate_user(
        email=payload.email, password=payload.password
    )

    if not user:
        return 401, ErrorResponseSchema(
            detail="Invalid email or password", code="INVALID_CREDENTIALS"
        )

    tokens = generate_tokens(user)
    return 200, TokenResponseSchema(**tokens)


@router.post(
    "/refresh",
    response={200: TokenResponseSchema, 401: ErrorResponseSchema},
    summary="Refresh access token",
)
def refresh_token(request: HttpRequest, payload: RefreshTokenSchema):
    """
    Refresh access token using refresh token.
    """
    try:
        decoded = jwt.decode(payload.refresh, settings.SECRET_KEY, algorithms=["HS256"])

        if decoded.get("type") != "refresh":
            return 401, ErrorResponseSchema(
                detail="Invalid token type", code="INVALID_TOKEN"
            )

        user_id = decoded.get("user_id")
        user = AuthenticationService.get_user_by_id(user_id)

        if not user or not user.is_active:
            return 401, ErrorResponseSchema(
                detail="User not found or inactive", code="USER_NOT_FOUND"
            )

        tokens = generate_tokens(user)
        return 200, TokenResponseSchema(**tokens)

    except jwt.ExpiredSignatureError:
        return 401, ErrorResponseSchema(
            detail="Refresh token has expired", code="TOKEN_EXPIRED"
        )
    except jwt.InvalidTokenError:
        return 401, ErrorResponseSchema(
            detail="Invalid refresh token", code="INVALID_TOKEN"
        )


@router.get(
    "/me",
    response={200: UserResponseSchema, 401: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Get current user",
)
def get_current_user(request: HttpRequest):
    """
    Get current authenticated user information.
    """
    user = request.auth

    return 200, UserResponseSchema(
        id=user.id,
        email=user.email,
        name=user.name,
        role=user.role,
        organization_id=user.organization.id,
        organization_name=user.organization.name,
        is_active=user.is_active,
        created_at=user.created_at.isoformat(),
    )


@router.post(
    "/change-password",
    response={200: MessageResponseSchema, 400: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Change user password",
)
def change_password(request: HttpRequest, payload: ChangePasswordSchema):
    """
    Change the current user's password.
    """
    user = request.auth

    success = AuthenticationService.change_password(
        user=user, old_password=payload.old_password, new_password=payload.new_password
    )

    if not success:
        return 400, ErrorResponseSchema(
            detail="Current password is incorrect", code="INVALID_PASSWORD"
        )

    return 200, MessageResponseSchema(
        message="Password changed successfully", success=True
    )


@router.patch(
    "/profile",
    response={200: UserResponseSchema, 400: ErrorResponseSchema},
    auth=JWTAuth(),
    summary="Update user profile",
)
def update_profile(request: HttpRequest, payload: UpdateProfileSchema):
    """
    Update current user's profile information.
    """
    user = request.auth

    try:
        updated_user = AuthenticationService.update_profile(
            user=user, name=payload.name, email=payload.email
        )

        return 200, UserResponseSchema(
            id=updated_user.id,
            email=updated_user.email,
            name=updated_user.name,
            role=updated_user.role,
            organization_id=updated_user.organization.id,
            organization_name=updated_user.organization.name,
            is_active=updated_user.is_active,
            created_at=updated_user.created_at.isoformat(),
        )

    except ValueError as e:
        return 400, ErrorResponseSchema(detail=str(e), code="UPDATE_ERROR")


@router.post(
    "/logout",
    response={200: MessageResponseSchema},
    auth=JWTAuth(),
    summary="Logout user",
)
def logout(request: HttpRequest):
    """
    Logout user (client should discard tokens).
    """
    return 200, MessageResponseSchema(message="Logged out successfully", success=True)


# Made with Bob
