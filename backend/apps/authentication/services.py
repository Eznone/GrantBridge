"""
Authentication service layer for handling user authentication logic.
"""

from typing import Dict, Optional, Tuple
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.db import transaction
from apps.authentication.models import User
from apps.organizations.models import Organization


class AuthenticationService:
    """Service for handling authentication operations."""

    @staticmethod
    def register_user(
        email: str, password: str, name: str, organization_name: str
    ) -> Tuple[User, Organization]:
        """
        Register a new user and create their organization.

        Args:
            email: User email address
            password: User password
            name: User full name
            organization_name: Name of the organization

        Returns:
            Tuple of (User, Organization)

        Raises:
            ValueError: If email already exists
        """
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            raise ValueError("A user with this email already exists")

        # Create user and organization in a transaction
        with transaction.atomic():
            # Create organization first
            organization = Organization.objects.create(
                name=organization_name,
                mission="",  # Can be updated later
                description="",
                website="",
                annual_budget=0,
            )

            # Create user
            user = User.objects.create(
                email=email,
                name=name,
                password=make_password(password),
                organization=organization,
                role="admin",  # First user is admin
                is_active=True,
            )

        return user, organization

    @staticmethod
    def authenticate_user(email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            email: User email address
            password: User password

        Returns:
            User instance if authentication successful, None otherwise
        """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password) and user.is_active:
                return user
        except User.DoesNotExist:
            pass
        return None

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str) -> bool:
        """
        Change user password.

        Args:
            user: User instance
            old_password: Current password
            new_password: New password

        Returns:
            True if password changed successfully, False otherwise
        """
        if not user.check_password(old_password):
            return False

        user.password = make_password(new_password)
        user.save(update_fields=["password"])
        return True

    @staticmethod
    def update_profile(
        user: User, name: Optional[str] = None, email: Optional[str] = None
    ) -> User:
        """
        Update user profile information.

        Args:
            user: User instance
            name: New name (optional)
            email: New email (optional)

        Returns:
            Updated User instance

        Raises:
            ValueError: If email already exists
        """
        update_fields = []

        if name is not None:
            user.name = name
            update_fields.append("name")

        if email is not None and email != user.email:
            # Check if email already exists
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                raise ValueError("A user with this email already exists")
            user.email = email
            update_fields.append("email")

        if update_fields:
            update_fields.append("updated_at")
            user.save(update_fields=update_fields)

        return user

    @staticmethod
    def deactivate_user(user: User) -> None:
        """
        Deactivate a user account.

        Args:
            user: User instance
        """
        user.is_active = False
        user.save(update_fields=["is_active", "updated_at"])

    @staticmethod
    def activate_user(user: User) -> None:
        """
        Activate a user account.

        Args:
            user: User instance
        """
        user.is_active = True
        user.save(update_fields=["is_active", "updated_at"])

    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User UUID

        Returns:
            User instance or None
        """
        try:
            return User.objects.select_related("organization").get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Get user by email.

        Args:
            email: User email address

        Returns:
            User instance or None
        """
        try:
            return User.objects.select_related("organization").get(email=email)
        except User.DoesNotExist:
            return None


# Made with Bob
