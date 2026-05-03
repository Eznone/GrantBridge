"""
Base AI provider interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BaseAIProvider(ABC):
    """
    Abstract base class for AI providers.
    All AI providers must implement these methods.
    """

    @abstractmethod
    def generate_text(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7, **kwargs
    ) -> str:
        """
        Generate text based on a prompt.

        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    def generate_embeddings(self, texts: List[str], **kwargs) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings to embed
            **kwargs: Additional provider-specific parameters

        Returns:
            List of embedding vectors
        """
        pass

    @abstractmethod
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Generate a chat completion based on a conversation history.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional provider-specific parameters

        Returns:
            Generated response text
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is properly configured and available.

        Returns:
            True if provider is available, False otherwise
        """
        pass

    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model configuration.

        Returns:
            Dictionary with model information
        """
        return {
            "provider": self.__class__.__name__,
            "available": self.is_available(),
        }


# Made with Bob
