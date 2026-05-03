"""
Grant service layer for handling business logic.
"""

from typing import Dict, List, Optional, Tuple
from decimal import Decimal
from datetime import datetime
from django.db.models import Q, QuerySet
from django.core.paginator import Paginator
from apps.grants.models import Grant, SavedGrant, Application


class GrantService:
    """Service for handling grant operations."""

    @staticmethod
    def list_grants(
        search: Optional[str] = None,
        categories: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
        min_amount: Optional[Decimal] = None,
        max_amount: Optional[Decimal] = None,
        geographic_scope: Optional[str] = None,
        is_active: Optional[bool] = None,
        deadline_before: Optional[datetime] = None,
        deadline_after: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "deadline",
        sort_order: str = "asc",
    ) -> Tuple[List[Grant], int, int]:
        """
        List grants with filtering, search, and pagination.

        Returns:
            Tuple of (grants_list, total_count, total_pages)
        """
        queryset = Grant.objects.all()

        # Apply filters
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search)
                | Q(description__icontains=search)
                | Q(funder_name__icontains=search)
            )

        if categories:
            # Filter grants that have any of the specified categories
            for category in categories:
                queryset = queryset.filter(categories__contains=[category])

        if tags:
            # Filter grants that have any of the specified tags
            for tag in tags:
                queryset = queryset.filter(tags__contains=[tag])

        if min_amount is not None:
            queryset = queryset.filter(funding_amount__gte=min_amount)

        if max_amount is not None:
            queryset = queryset.filter(funding_amount__lte=max_amount)

        if geographic_scope:
            queryset = queryset.filter(geographic_scope=geographic_scope)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)

        if deadline_before:
            queryset = queryset.filter(deadline__lte=deadline_before)

        if deadline_after:
            queryset = queryset.filter(deadline__gte=deadline_after)

        # Apply sorting
        sort_field = sort_by
        if sort_order == "desc":
            sort_field = f"-{sort_by}"

        queryset = queryset.order_by(sort_field)

        # Paginate
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        return (list(page_obj.object_list), paginator.count, paginator.num_pages)

    @staticmethod
    def get_grant(grant_id: str) -> Optional[Grant]:
        """Get grant by ID."""
        try:
            return Grant.objects.get(id=grant_id)
        except Grant.DoesNotExist:
            return None

    @staticmethod
    def save_grant(organization, grant: Grant, notes: str = "") -> SavedGrant:
        """
        Save/bookmark a grant for an organization.

        Returns:
            SavedGrant instance
        """
        saved_grant, created = SavedGrant.objects.get_or_create(
            organization=organization, grant=grant, defaults={"notes": notes}
        )

        if not created and notes:
            # Update notes if grant was already saved
            saved_grant.notes = notes
            saved_grant.save(update_fields=["notes"])

        return saved_grant

    @staticmethod
    def unsave_grant(organization, grant: Grant) -> bool:
        """
        Remove a saved grant.

        Returns:
            True if grant was unsaved, False if it wasn't saved
        """
        deleted_count, _ = SavedGrant.objects.filter(
            organization=organization, grant=grant
        ).delete()

        return deleted_count > 0

    @staticmethod
    def get_saved_grants(
        organization, page: int = 1, page_size: int = 20
    ) -> Tuple[List[SavedGrant], int, int]:
        """
        Get saved grants for an organization.

        Returns:
            Tuple of (saved_grants_list, total_count, total_pages)
        """
        queryset = (
            SavedGrant.objects.filter(organization=organization)
            .select_related("grant")
            .order_by("-saved_at")
        )

        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)

        return (list(page_obj.object_list), paginator.count, paginator.num_pages)

    @staticmethod
    def is_grant_saved(organization, grant: Grant) -> bool:
        """Check if a grant is saved by an organization."""
        return SavedGrant.objects.filter(
            organization=organization, grant=grant
        ).exists()

    @staticmethod
    def get_organization_applications(
        organization, status: Optional[str] = None
    ) -> QuerySet[Application]:
        """
        Get applications for an organization.

        Args:
            organization: Organization instance
            status: Optional status filter

        Returns:
            QuerySet of Application instances
        """
        queryset = (
            Application.objects.filter(organization=organization)
            .select_related("grant", "proposal")
            .order_by("-created_at")
        )

        if status:
            queryset = queryset.filter(status=status)

        return queryset


# Made with Bob
