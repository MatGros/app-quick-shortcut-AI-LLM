"""Abstract LLM Provider interface and factory pattern."""

from abc import ABC, abstractmethod
from typing import Dict, List, Generator, Optional


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, base_url: str, api_key: str = "", timeout: int = 30):
        """
        Initialize LLM provider.

        Args:
            base_url: API endpoint base URL
            api_key: API key/token (optional)
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    @abstractmethod
    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        Stream chat completion tokens.

        Args:
            messages: List of messages with role/content
            model: Model name/ID
            temperature: Sampling temperature (0.0-1.0)
            **kwargs: Additional provider-specific args

        Yields:
            String tokens from the response

        Raises:
            ConnectionError: If API connection fails
            ValueError: If invalid parameters
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get list of available models.

        Returns:
            List of model names/IDs

        Raises:
            ConnectionError: If API connection fails
        """
        pass

    @abstractmethod
    def health_check(self) -> bool:
        """
        Test provider connectivity.

        Returns:
            True if provider is accessible, False otherwise
        """
        pass

    @abstractmethod
    def supports_vision(self) -> bool:
        """
        Check if provider supports vision/image input.

        Returns:
            True if vision is supported, False otherwise
        """
        pass


class LLMProviderFactory:
    """Factory for creating LLM provider instances."""

    _providers = {}

    @classmethod
    def register(cls, provider_type: str, provider_class: type) -> None:
        """
        Register a new provider type.

        Args:
            provider_type: Provider type identifier (e.g., 'ollama')
            provider_class: Provider class (must inherit from LLMProvider)
        """
        if not issubclass(provider_class, LLMProvider):
            raise TypeError(f"{provider_class} must inherit from LLMProvider")
        cls._providers[provider_type] = provider_class

    @classmethod
    def create(cls, provider_type: str, config: Dict) -> LLMProvider:
        """
        Create provider instance from type and config.

        Args:
            provider_type: Provider type (e.g., 'ollama', 'openai')
            config: Configuration dict with base_url, api_key, etc.

        Returns:
            LLMProvider instance

        Raises:
            KeyError: If provider type not registered
            TypeError: If config is invalid
        """
        if provider_type not in cls._providers:
            raise KeyError(f"Unknown provider type: {provider_type}")

        provider_class = cls._providers[provider_type]
        try:
            return provider_class(**config)
        except TypeError as e:
            raise TypeError(f"Invalid config for {provider_type}: {e}")

    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of registered provider types."""
        return list(cls._providers.keys())


# Register built-in providers
from .ollama_provider import OllamaProvider  # noqa: E402
from .openai_provider import OpenAIProvider  # noqa: E402
from .anthropic_provider import AnthropicProvider  # noqa: E402

LLMProviderFactory.register("ollama", OllamaProvider)
LLMProviderFactory.register("openai", OpenAIProvider)
LLMProviderFactory.register("anthropic", AnthropicProvider)
