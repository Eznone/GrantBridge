"""
Embedding generation service for grants and organizations.
"""

import logging
from typing import List, Optional
from django.conf import settings

from apps.ai.providers import WatsonxProvider
from apps.grants.models import Grant
from apps.organizations.models import Organization

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating and managing embeddings for semantic search.
    """

    def __init__(self):
        """Initialize the embedding service with AI provider."""
        self.provider = WatsonxProvider()
        self.embedding_dimension = 768  # Slate model dimension

    def generate_grant_embedding(self, grant: Grant) -> Optional[List[float]]:
        """
        Generate embedding for a grant.

        Args:
            grant: Grant instance

        Returns:
            Embedding vector or None if generation fails
        """
        try:
            # Create comprehensive text representation of the grant
            grant_text = self._create_grant_text(grant)

            # Generate embedding
            if self.provider.is_available():
                embeddings = self.provider.generate_embeddings([grant_text])
                return embeddings[0] if embeddings else None
            else:
                logger.warning("AI provider not available for embeddings")
                return None

        except Exception as e:
            logger.error(f"Error generating grant embedding: {e}")
            return None

    def generate_organization_embedding(
        self, organization: Organization
    ) -> Optional[List[float]]:
        """
        Generate embedding for an organization.

        Args:
            organization: Organization instance

        Returns:
            Embedding vector or None if generation fails
        """
        try:
            # Create comprehensive text representation
            org_text = self._create_organization_text(organization)

            # Generate embedding
            if self.provider.is_available():
                embeddings = self.provider.generate_embeddings([org_text])
                return embeddings[0] if embeddings else None
            else:
                logger.warning("AI provider not available for embeddings")
                return None

        except Exception as e:
            logger.error(f"Error generating organization embedding: {e}")
            return None

    def generate_batch_embeddings(
        self, texts: List[str]
    ) -> List[Optional[List[float]]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available for embeddings")
                return [None] * len(texts)

            embeddings = self.provider.generate_embeddings(texts)
            return embeddings

        except Exception as e:
            logger.error(f"Error generating batch embeddings: {e}")
            return [None] * len(texts)

    def update_grant_embeddings(self, grant_ids: Optional[List[int]] = None) -> int:
        """
        Update embeddings for grants.

        Args:
            grant_ids: Optional list of grant IDs to update.
                      If None, updates all grants.

        Returns:
            Number of grants updated
        """
        try:
            # Get grants to update
            if grant_ids:
                grants = Grant.objects.filter(id__in=grant_ids)
            else:
                grants = Grant.objects.all()

            updated_count = 0

            for grant in grants:
                embedding = self.generate_grant_embedding(grant)
                if embedding:
                    grant.embedding = embedding
                    grant.save(update_fields=["embedding"])
                    updated_count += 1

            logger.info(f"Updated embeddings for {updated_count} grants")
            return updated_count

        except Exception as e:
            logger.error(f"Error updating grant embeddings: {e}")
            return 0

    def update_organization_embeddings(
        self, org_ids: Optional[List[int]] = None
    ) -> int:
        """
        Update embeddings for organizations.

        Args:
            org_ids: Optional list of organization IDs to update.
                    If None, updates all organizations.

        Returns:
            Number of organizations updated
        """
        try:
            # Get organizations to update
            if org_ids:
                orgs = Organization.objects.filter(id__in=org_ids)
            else:
                orgs = Organization.objects.all()

            updated_count = 0

            for org in orgs:
                embedding = self.generate_organization_embedding(org)
                if embedding:
                    # Store in organization profile or separate table
                    # For now, we'll assume it's stored in a JSON field
                    org.embedding = embedding
                    org.save(update_fields=["embedding"])
                    updated_count += 1

            logger.info(f"Updated embeddings for {updated_count} organizations")
            return updated_count

        except Exception as e:
            logger.error(f"Error updating organization embeddings: {e}")
            return 0

    def _create_grant_text(self, grant: Grant) -> str:
        """
        Create a comprehensive text representation of a grant.

        Args:
            grant: Grant instance

        Returns:
            Text representation
        """
        parts = [
            f"Title: {grant.title}",
            f"Funder: {grant.funder_name}",
            f"Description: {grant.description}",
        ]

        if grant.categories:
            parts.append(f"Categories: {', '.join(grant.categories)}")

        if grant.tags:
            parts.append(f"Tags: {', '.join(grant.tags)}")

        if grant.eligibility_criteria:
            parts.append(f"Eligibility: {grant.eligibility_criteria}")

        if grant.focus_areas:
            parts.append(f"Focus Areas: {', '.join(grant.focus_areas)}")

        if grant.geographic_scope:
            parts.append(f"Geographic Scope: {', '.join(grant.geographic_scope)}")

        return "\n".join(parts)

    def _create_organization_text(self, organization: Organization) -> str:
        """
        Create a comprehensive text representation of an organization.

        Args:
            organization: Organization instance

        Returns:
            Text representation
        """
        parts = [
            f"Name: {organization.name}",
            f"Mission: {organization.mission}",
        ]

        if organization.description:
            parts.append(f"Description: {organization.description}")

        if organization.categories:
            parts.append(f"Categories: {', '.join(organization.categories)}")

        if organization.tags:
            parts.append(f"Tags: {', '.join(organization.tags)}")

        if organization.goals:
            goals_text = ", ".join(organization.goals)
            parts.append(f"Goals: {goals_text}")

        return "\n".join(parts)


# Made with Bob
