"""
AI prompts for various tasks.
"""

from .grant_matching import GRANT_MATCHING_PROMPT
from .proposal_generation import (
    EXECUTIVE_SUMMARY_PROMPT,
    PROJECT_DESCRIPTION_PROMPT,
    BUDGET_JUSTIFICATION_PROMPT,
)
from .text_improvement import (
    REWRITE_PROMPT,
    TONE_ADJUSTMENT_PROMPT,
    EXPAND_PROMPT,
    SUMMARIZE_PROMPT,
)

__all__ = [
    "GRANT_MATCHING_PROMPT",
    "EXECUTIVE_SUMMARY_PROMPT",
    "PROJECT_DESCRIPTION_PROMPT",
    "BUDGET_JUSTIFICATION_PROMPT",
    "REWRITE_PROMPT",
    "TONE_ADJUSTMENT_PROMPT",
    "EXPAND_PROMPT",
    "SUMMARIZE_PROMPT",
]

# Made with Bob
