"""
AI-powered text improvement service.
"""

import logging
from typing import Optional

from apps.ai.providers import WatsonxProvider
from apps.ai.prompts import (
    REWRITE_PROMPT,
    TONE_ADJUSTMENT_PROMPT,
    EXPAND_PROMPT,
    SUMMARIZE_PROMPT,
)

logger = logging.getLogger(__name__)


class TextImprovementService:
    """
    Service for AI-powered text improvement operations.
    """

    def __init__(self):
        """Initialize the text improvement service."""
        self.provider = WatsonxProvider()

    def rewrite_text(
        self,
        original_text: str,
        document_type: str = "grant proposal",
        purpose: str = "persuade funders",
    ) -> Optional[str]:
        """
        Rewrite text to be clearer and more professional.

        Args:
            original_text: Text to rewrite
            document_type: Type of document
            purpose: Purpose of the text

        Returns:
            Rewritten text or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = REWRITE_PROMPT.format(
                original_text=original_text,
                document_type=document_type,
                purpose=purpose,
            )

            # Generate improved text
            rewritten = self.provider.generate_text(
                prompt=prompt,
                max_tokens=len(original_text.split()) * 2,
                temperature=0.7,
            )

            return rewritten.strip()

        except Exception as e:
            logger.error(f"Error rewriting text: {e}")
            return None

    def adjust_tone(
        self,
        original_text: str,
        current_tone: str = "informal",
        desired_tone: str = "professional",
    ) -> Optional[str]:
        """
        Adjust the tone of text.

        Args:
            original_text: Text to adjust
            current_tone: Current tone description
            desired_tone: Desired tone description

        Returns:
            Tone-adjusted text or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = TONE_ADJUSTMENT_PROMPT.format(
                original_text=original_text,
                current_tone=current_tone,
                desired_tone=desired_tone,
            )

            # Generate adjusted text
            adjusted = self.provider.generate_text(
                prompt=prompt,
                max_tokens=len(original_text.split()) * 2,
                temperature=0.6,
            )

            return adjusted.strip()

        except Exception as e:
            logger.error(f"Error adjusting tone: {e}")
            return None

    def expand_text(
        self,
        brief_text: str,
        section_name: str = "project description",
        target_length: int = 500,
        key_points: str = "",
    ) -> Optional[str]:
        """
        Expand brief text into a longer, detailed version.

        Args:
            brief_text: Brief text to expand
            section_name: Name of the section
            target_length: Target word count
            key_points: Key points to include

        Returns:
            Expanded text or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = EXPAND_PROMPT.format(
                brief_text=brief_text,
                section_name=section_name,
                target_length=target_length,
                key_points=key_points or "None specified",
            )

            # Generate expanded text
            expanded = self.provider.generate_text(
                prompt=prompt, max_tokens=target_length * 2, temperature=0.7
            )

            return expanded.strip()

        except Exception as e:
            logger.error(f"Error expanding text: {e}")
            return None

    def summarize_text(self, full_text: str, target_length: int = 100) -> Optional[str]:
        """
        Summarize long text into a concise version.

        Args:
            full_text: Full text to summarize
            target_length: Target word count for summary

        Returns:
            Summarized text or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Format the prompt
            prompt = SUMMARIZE_PROMPT.format(
                full_text=full_text,
                target_length=target_length,
            )

            # Generate summary
            summary = self.provider.generate_text(
                prompt=prompt, max_tokens=target_length * 2, temperature=0.5
            )

            return summary.strip()

        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return None

    def improve_grammar(self, text: str) -> Optional[str]:
        """
        Improve grammar and fix errors in text.

        Args:
            text: Text to improve

        Returns:
            Grammar-corrected text or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            # Use rewrite with specific instructions
            prompt = f"""Fix grammar, spelling, and punctuation errors in the following text.
Keep the meaning and style the same, only fix errors.

Text:
{text}

Corrected text:"""

            # Generate corrected text
            corrected = self.provider.generate_text(
                prompt=prompt,
                max_tokens=len(text.split()) * 2,
                temperature=0.3,  # Lower temp for accuracy
            )

            return corrected.strip()

        except Exception as e:
            logger.error(f"Error improving grammar: {e}")
            return None

    def make_more_persuasive(
        self, text: str, context: str = "grant proposal"
    ) -> Optional[str]:
        """
        Make text more persuasive and compelling.

        Args:
            text: Text to enhance
            context: Context for the text

        Returns:
            More persuasive text or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            prompt = f"""Rewrite the following text to be more persuasive and compelling for a {context}.
Use strong, active language and emphasize impact and benefits.
Keep the same length and factual content.

Original text:
{text}

More persuasive version:"""

            # Generate persuasive text
            persuasive = self.provider.generate_text(
                prompt=prompt, max_tokens=len(text.split()) * 2, temperature=0.7
            )

            return persuasive.strip()

        except Exception as e:
            logger.error(f"Error making text persuasive: {e}")
            return None

    def simplify_text(
        self, text: str, reading_level: str = "general audience"
    ) -> Optional[str]:
        """
        Simplify complex text for better readability.

        Args:
            text: Text to simplify
            reading_level: Target reading level

        Returns:
            Simplified text or None if failed
        """
        try:
            if not self.provider.is_available():
                logger.warning("AI provider not available")
                return None

            prompt = f"""Simplify the following text for a {reading_level}.
Use shorter sentences, simpler words, and clearer structure.
Keep all important information and meaning.

Original text:
{text}

Simplified version:"""

            # Generate simplified text
            simplified = self.provider.generate_text(
                prompt=prompt, max_tokens=len(text.split()) * 2, temperature=0.6
            )

            return simplified.strip()

        except Exception as e:
            logger.error(f"Error simplifying text: {e}")
            return None


# Made with Bob
