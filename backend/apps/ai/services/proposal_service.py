"""
AI-powered proposal generation service.
"""

import logging
from typing import Dict, Any, Optional

from apps.ai.providers import WatsonxProvider
from apps.ai.prompts import (
    EXECUTIVE_SUMMARY_PROMPT,
    PROJECT_DESCRIPTION_PROMPT,
    BUDGET_JUSTIFICATION_PROMPT,
)
from apps.grants.models import Grant
from apps.organizations.models import Organization
from apps.proposals.models import Proposal

logger = logging.getLogger(__name__)


class ProposalGenerationService:
    """
    Service for AI-powered proposal generation.
    """

    def __init__(self):
        """Initialize the proposal generation service."""
        self.provider = WatsonxProvider()

    def generate_executive_summary(
        self,
        organization: Organization,
        grant: Grant,
        project_info: str,
        amount_requested: float,
    ) -> Optional[str]:
        """
        Generate an executive summary for a proposal.

        Args:
            organization: Organization instance
            grant: Grant instance
            project_info: Brief project information
            amount_requested: Amount being requested

        Returns:
            Generated executive summary or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = EXECUTIVE_SUMMARY_PROMPT.format(
                org_name=organization.name,
                org_mission=organization.mission or "Not specified",
                org_categories=", ".join(organization.categories or []),
                grant_title=grant.title,
                grant_funder=grant.funder_name,
                amount_requested=amount_requested,
                grant_categories=", ".join(grant.categories or []),
                project_info=project_info,
            )

            # Generate text
            summary = self.provider.generate_text(
                prompt=prompt, max_tokens=500, temperature=0.7
            )

            return summary.strip()

        except Exception as e:
            logger.error(f"Error generating executive summary: {e}")
            return None

    def generate_project_description(
        self,
        organization: Organization,
        grant: Grant,
        project_overview: str,
        amount_requested: float,
    ) -> Optional[str]:
        """
        Generate a detailed project description.

        Args:
            organization: Organization instance
            grant: Grant instance
            project_overview: Overview of the project
            amount_requested: Amount being requested

        Returns:
            Generated project description or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = PROJECT_DESCRIPTION_PROMPT.format(
                org_name=organization.name,
                org_mission=organization.mission or "Not specified",
                org_categories=", ".join(organization.categories or []),
                grant_title=grant.title,
                grant_funder=grant.funder_name,
                amount_requested=amount_requested,
                project_overview=project_overview,
            )

            # Generate text
            description = self.provider.generate_text(
                prompt=prompt, max_tokens=1500, temperature=0.7
            )

            return description.strip()

        except Exception as e:
            logger.error(f"Error generating project description: {e}")
            return None

    def generate_budget_justification(
        self,
        organization: Organization,
        grant: Grant,
        budget_items: str,
        amount_requested: float,
    ) -> Optional[str]:
        """
        Generate a budget justification.

        Args:
            organization: Organization instance
            grant: Grant instance
            budget_items: Breakdown of budget items
            amount_requested: Total amount requested

        Returns:
            Generated budget justification or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = BUDGET_JUSTIFICATION_PROMPT.format(
                org_name=organization.name,
                org_budget=organization.annual_budget or 0,
                grant_title=grant.title,
                amount_requested=amount_requested,
                budget_items=budget_items,
            )

            # Generate text
            justification = self.provider.generate_text(
                prompt=prompt, max_tokens=800, temperature=0.7
            )

            return justification.strip()

        except Exception as e:
            logger.error(f"Error generating budget justification: {e}")
            return None

    def generate_complete_proposal(
        self, organization: Organization, grant: Grant, project_info: Dict[str, Any]
    ) -> Optional[Dict[str, str]]:
        """
        Generate all sections of a proposal.

        Args:
            organization: Organization instance
            grant: Grant instance
            project_info: Dictionary with project information:
                - project_overview: Brief overview
                - amount_requested: Amount to request
                - budget_items: Budget breakdown

        Returns:
            Dictionary with generated sections or None if failed
        """
        try:
            project_overview = project_info.get("project_overview", "")
            amount_requested = project_info.get("amount_requested", 0)
            budget_items = project_info.get("budget_items", "")

            # Generate all sections
            executive_summary = self.generate_executive_summary(
                organization, grant, project_overview, amount_requested
            )

            project_description = self.generate_project_description(
                organization, grant, project_overview, amount_requested
            )

            budget_justification = self.generate_budget_justification(
                organization, grant, budget_items, amount_requested
            )

            # Return all sections
            return {
                "executive_summary": executive_summary,
                "project_description": project_description,
                "budget_justification": budget_justification,
            }

        except Exception as e:
            logger.error(f"Error generating complete proposal: {e}")
            return None

    def create_ai_proposal(
        self,
        organization: Organization,
        grant: Grant,
        project_info: Dict[str, Any],
        title: Optional[str] = None,
    ) -> Optional[Proposal]:
        """
        Create a new proposal with AI-generated content.

        Args:
            organization: Organization instance
            grant: Grant instance
            project_info: Project information dictionary
            title: Optional proposal title

        Returns:
            Created Proposal instance or None if failed
        """
        try:
            # Generate proposal content
            content = self.generate_complete_proposal(organization, grant, project_info)

            if not content:
                logger.error("Failed to generate proposal content")
                return None

            # Create proposal
            proposal = Proposal.objects.create(
                organization=organization,
                grant=grant,
                title=title or f"Proposal for {grant.title}",
                executive_summary=content.get("executive_summary"),
                project_description=content.get("project_description"),
                budget_justification=content.get("budget_justification"),
                amount_requested=project_info.get("amount_requested"),
                status="draft",
                ai_metadata={
                    "generated_by": "watsonx",
                    "provider": "IBM watsonx.ai",
                    "sections_generated": [
                        "executive_summary",
                        "project_description",
                        "budget_justification",
                    ],
                },
            )

            logger.info(f"Created AI proposal {proposal.id}")
            return proposal

        except Exception as e:
            logger.error(f"Error creating AI proposal: {e}")
            return None

    def enhance_proposal_section(
        self, proposal: Proposal, section: str, additional_context: Optional[str] = None
    ) -> Optional[str]:
        """
        Enhance or regenerate a specific proposal section.

        Args:
            proposal: Proposal instance
            section: Section name ('executive_summary', etc.)
            additional_context: Optional additional context

        Returns:
            Enhanced section text or None if failed
        """
        try:
            organization = proposal.organization
            grant = proposal.grant

            if section == "executive_summary":
                project_info = (
                    additional_context
                    or proposal.project_description
                    or "Project information"
                )
                return self.generate_executive_summary(
                    organization, grant, project_info, proposal.amount_requested or 0
                )

            elif section == "project_description":
                project_overview = (
                    additional_context
                    or proposal.executive_summary
                    or "Project overview"
                )
                return self.generate_project_description(
                    organization,
                    grant,
                    project_overview,
                    proposal.amount_requested or 0,
                )

            elif section == "budget_justification":
                budget_items = additional_context or "Budget breakdown not provided"
                return self.generate_budget_justification(
                    organization, grant, budget_items, proposal.amount_requested or 0
                )

            else:
                logger.warning(f"Unknown section: {section}")
                return None

        except Exception as e:
            logger.error(f"Error enhancing proposal section: {e}")
            return None


# Made with Bob
