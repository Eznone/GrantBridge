"""
IBM watsonx.ai provider implementation.
"""

import os
import logging
from typing import List, Dict, Any
from django.conf import settings

from .base import BaseAIProvider

logger = logging.getLogger(__name__)


class WatsonxProvider(BaseAIProvider):
    """
    IBM watsonx.ai provider for text generation and embeddings.

    Requires:
        - ibm-watsonx-ai package
        - WATSONX_API_KEY environment variable
        - WATSONX_PROJECT_ID environment variable
        - WATSONX_URL environment variable (optional)
    """

    def __init__(self):
        """Initialize the Watsonx provider."""
        self.api_key = getattr(settings, "WATSONX_API_KEY", None)
        self.project_id = getattr(settings, "WATSONX_PROJECT_ID", None)
        self.url = getattr(settings, "WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
        self.model_id = getattr(settings, "WATSONX_MODEL_ID", "ibm/granite-13b-chat-v2")
        self.embedding_model_id = getattr(
            settings, "WATSONX_EMBEDDING_MODEL_ID", "ibm/slate-125m-english-rtrvr"
        )

        self._client = None
        self._credentials = None

    def _get_client(self):
        """Get or create the Watsonx client."""
        if self._client is None:
            try:
                from ibm_watsonx_ai import APIClient
                from ibm_watsonx_ai import Credentials

                self._credentials = Credentials(
                    url=self.url,
                    api_key=self.api_key,
                )

                self._client = APIClient(self._credentials)
                self._client.set.default_project(self.project_id)

                logger.info("Watsonx client initialized successfully")
            except ImportError:
                logger.error(
                    "ibm-watsonx-ai package not installed. "
                    "Install with: pip install ibm-watsonx-ai"
                )
                raise
            except Exception as e:
                logger.error(f"Failed to initialize Watsonx client: {e}")
                raise

        return self._client

    def generate_text(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7, **kwargs
    ) -> str:
        """
        Generate text using Watsonx foundation model.

        Args:
            prompt: The input prompt
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
            **kwargs: Additional parameters

        Returns:
            Generated text
        """
        try:
            from ibm_watsonx_ai.foundation_models import ModelInference

            client = self._get_client()

            model = ModelInference(
                model_id=self.model_id,
                api_client=client,
                project_id=self.project_id,
                params={
                    "max_new_tokens": max_tokens,
                    "temperature": temperature,
                    "decoding_method": "greedy" if temperature == 0 else "sample",
                    **kwargs,
                },
            )

            response = model.generate_text(prompt=prompt)
            return response

        except Exception as e:
            logger.error(f"Error generating text with Watsonx: {e}")
            raise

    def generate_embeddings(self, texts: List[str], **kwargs) -> List[List[float]]:
        """
        Generate embeddings using Watsonx embedding model.

        Args:
            texts: List of text strings to embed
            **kwargs: Additional parameters

        Returns:
            List of embedding vectors
        """
        try:
            from ibm_watsonx_ai.foundation_models import Embeddings

            client = self._get_client()

            embedding_model = Embeddings(
                model_id=self.embedding_model_id,
                api_client=client,
                project_id=self.project_id,
                params=kwargs,
            )

            embeddings = []
            for text in texts:
                result = embedding_model.embed_query(text)
                embeddings.append(result)

            return embeddings

        except Exception as e:
            logger.error(f"Error generating embeddings with Watsonx: {e}")
            raise

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1000,
        temperature: float = 0.7,
        **kwargs,
    ) -> str:
        """
        Generate chat completion using Watsonx.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Maximum number of tokens to generate
            temperature: Sampling temperature
            **kwargs: Additional parameters

        Returns:
            Generated response text
        """
        # Convert messages to a single prompt
        prompt = self._format_chat_prompt(messages)
        return self.generate_text(
            prompt=prompt, max_tokens=max_tokens, temperature=temperature, **kwargs
        )

    def _format_chat_prompt(self, messages: List[Dict[str, str]]) -> str:
        """
        Format chat messages into a prompt for the model.

        Args:
            messages: List of message dicts

        Returns:
            Formatted prompt string
        """
        prompt_parts = []

        for message in messages:
            role = message.get("role", "user")
            content = message.get("content", "")

            if role == "system":
                prompt_parts.append(f"System: {content}")
            elif role == "user":
                prompt_parts.append(f"User: {content}")
            elif role == "assistant":
                prompt_parts.append(f"Assistant: {content}")

        prompt_parts.append("Assistant:")
        return "\n\n".join(prompt_parts)

    def is_available(self) -> bool:
        """
        Check if Watsonx provider is properly configured.

        Returns:
            True if available, False otherwise
        """
        if not self.api_key or not self.project_id:
            logger.warning(
                "Watsonx provider not configured. "
                "Set WATSONX_API_KEY and WATSONX_PROJECT_ID"
            )
            return False

        try:
            # Try to initialize client
            self._get_client()
            return True
        except Exception as e:
            logger.error(f"Watsonx provider not available: {e}")
            return False

    def get_model_info(self) -> Dict[str, Any]:
        """Get Watsonx model information."""
        return {
            "provider": "IBM watsonx.ai",
            "available": self.is_available(),
            "model_id": self.model_id,
            "embedding_model_id": self.embedding_model_id,
            "url": self.url,
            "project_id": self.project_id[:8] + "..." if self.project_id else None,
        }


# Made with Bob
