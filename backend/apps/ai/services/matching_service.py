"""
AI-powered grant matching service with semantic similarity.
"""

import json
import logging
from typing import List, Dict, Any, Optional

from apps.ai.providers import WatsonxProvider
from apps.ai.prompts import GRANT_MATCHING_PROMPT
from apps.ai.services.vector_store import VectorStore
from apps.ai.services.embedding_service import EmbeddingService
from apps.grants.models import Grant
from apps.organizations.models import Organization
from apps.matching.models import GrantMatch

logger = logging.getLogger(__name__)


class AIMatchingService:
    """
    AI-powered service for matching grants to organizations.
    Combines semantic similarity with rule-based scoring.
    """

    def __init__(self):
        """Initialize the AI matching service."""
        self.provider = WatsonxProvider()
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStore()

    def find_semantic_matches(
        self, organization: Organization, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Find grants using semantic similarity.

        Args:
            organization: Organization to match
            limit: Maximum number of matches to return

        Returns:
            List of match dictionaries with grant info and scores
        """
        try:
            # Generate organization embedding
            org_embedding = self.embedding_service.generate_organization_embedding(
                organization
            )

            if not org_embedding:
                logger.warning("Could not generate organization embedding")
                return []

            # Search vector store
            results = self.vector_store.search(
                org_embedding, k=limit, return_metadata=True
            )

            # Format results
            matches = []
            for grant_id, similarity, metadata in results:
                try:
                    grant = Grant.objects.get(id=grant_id)
                    matches.append(
                        {
                            "grant": grant,
                            "semantic_score": similarity,
                            "metadata": metadata,
                        }
                    )
                except Grant.DoesNotExist:
                    continue

            return matches

        except Exception as e:
            logger.error(f"Error finding semantic matches: {e}")
            return []

    def analyze_match_with_ai(
        self, organization: Organization, grant: Grant
    ) -> Optional[Dict[str, Any]]:
        """
        Use AI to analyze the match quality between org and grant.

        Args:
            organization: Organization instance
            grant: Grant instance

        Returns:
            Dictionary with AI analysis or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = GRANT_MATCHING_PROMPT.format(
                org_name=organization.name,
                org_mission=organization.mission or "Not specified",
                org_categories=", ".join(organization.categories or []),
                org_budget=organization.annual_budget or 0,
                org_goals=", ".join(organization.goals or []),
                grant_title=grant.title,
                grant_funder=grant.funder_name,
                grant_amount_min=grant.amount_min or 0,
                grant_amount_max=grant.amount_max or 0,
                grant_categories=", ".join(grant.categories or []),
                grant_eligibility=grant.eligibility or "Not specified",
                grant_description=grant.description or "Not specified",
            )

            # Generate AI analysis
            response = self.provider.generate_text(
                prompt=prompt,
                max_tokens=1000,
                temperature=0.3,  # Lower temp for more consistent output
            )

            # Parse JSON response
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                logger.warning("Could not parse AI response as JSON")
                # Try to extract JSON from response
                start = response.find("{")
                end = response.rfind("}") + 1
                if start >= 0 and end > start:
                    try:
                        analysis = json.loads(response[start:end])
                        return analysis
                    except json.JSONDecodeError:
                        pass
                return None

        except Exception as e:
            logger.error(f"Error analyzing match with AI: {e}")
            return None

    def create_ai_enhanced_match(
        self,
        organization: Organization,
        grant: Grant,
        semantic_score: Optional[float] = None,
    ) -> Optional[GrantMatch]:
        """
        Create a grant match with AI-enhanced scoring and reasoning.

        Args:
            organization: Organization instance
            grant: Grant instance
            semantic_score: Optional pre-computed semantic similarity score

        Returns:
            GrantMatch instance or None if failed
        """
        try:
            # Get AI analysis
            ai_analysis = self.analyze_match_with_ai(organization, grant)

            # Calculate final match score
            if ai_analysis and "match_score" in ai_analysis:
                ai_score = float(ai_analysis["match_score"])
            else:
                ai_score = 50.0  # Default if AI fails

            # Combine with semantic score if available
            if semantic_score is not None:
                final_score = (ai_score * 0.6) + (semantic_score * 0.4)
            else:
                final_score = ai_score

            # Determine match quality
            if final_score >= 80:
                quality = "excellent"
            elif final_score >= 60:
                quality = "good"
            elif final_score >= 40:
                quality = "fair"
            else:
                quality = "poor"

            # Create match record
            match = GrantMatch.objects.create(
                organization=organization,
                grant=grant,
                match_score=final_score,
                match_quality=quality,
                reasoning=ai_analysis.get("reasoning") if ai_analysis else None,
                strengths=ai_analysis.get("strengths") if ai_analysis else [],
                concerns=ai_analysis.get("concerns") if ai_analysis else [],
                recommendations=(
                    ai_analysis.get("recommendations") if ai_analysis else []
                ),
                ai_metadata=(
                    {
                        "ai_score": ai_score,
                        "semantic_score": semantic_score,
                        "provider": "watsonx",
                    }
                    if ai_analysis
                    else None
                ),
            )

            return match

        except Exception as e:
            logger.error(f"Error creating AI-enhanced match: {e}")
            return None

    def batch_match_organization(
        self, organization: Organization, use_semantic: bool = True, limit: int = 50
    ) -> List[GrantMatch]:
        """
        Find and create matches for an organization.

        Args:
            organization: Organization to match
            use_semantic: Whether to use semantic similarity
            limit: Maximum number of matches to create

        Returns:
            List of created GrantMatch instances
        """
        try:
            matches_created = []

            if use_semantic and self.vector_store.get_stats()["available"]:
                # Use semantic search
                semantic_matches = self.find_semantic_matches(organization, limit=limit)

                for match_data in semantic_matches:
                    grant = match_data["grant"]
                    semantic_score = match_data["semantic_score"]

                    # Check if match already exists
                    existing = GrantMatch.objects.filter(
                        organization=organization, grant=grant
                    ).first()

                    if existing:
                        continue

                    # Create AI-enhanced match
                    match = self.create_ai_enhanced_match(
                        organization, grant, semantic_score
                    )

                    if match:
                        matches_created.append(match)
            else:
                # Fallback to rule-based matching
                logger.info("Using rule-based matching (semantic not available)")
                # This would call the existing MatchingService
                from apps.matching.services import MatchingService

                rule_service = MatchingService()
                matches_created = rule_service.calculate_matches(organization)

            logger.info(
                f"Created {len(matches_created)} matches for {organization.name}"
            )
            return matches_created

        except Exception as e:
            logger.error(f"Error in batch matching: {e}")
            return []

    def refresh_vector_store(self) -> Dict[str, int]:
        """
        Refresh the vector store with all grants.

        Returns:
            Dictionary with counts of processed items
        """
        try:
            grants = Grant.objects.all()

            vectors = []
            ids = []
            metadata = []

            for grant in grants:
                embedding = self.embedding_service.generate_grant_embedding(grant)

                if embedding:
                    vectors.append(embedding)
                    ids.append(grant.id)
                    metadata.append(
                        {
                            "title": grant.title,
                            "funder": grant.funder_name,
                            "categories": grant.categories or [],
                        }
                    )

            # Add to vector store
            if vectors:
                self.vector_store.add_vectors(vectors, ids, metadata)
                self.vector_store.save()

            return {
                "total_grants": grants.count(),
                "processed": len(vectors),
                "failed": grants.count() - len(vectors),
            }

        except Exception as e:
            logger.error(f"Error refreshing vector store: {e}")
            return {"total_grants": 0, "processed": 0, "failed": 0}


# Made with Bob
