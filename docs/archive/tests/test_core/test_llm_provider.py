"""Tests for LLM provider abstraction and implementations."""

import json
import pytest
from unittest.mock import Mock, patch, MagicMock

from src.core.llm_provider import LLMProvider, LLMProviderFactory
from src.core.ollama_provider import OllamaProvider
from src.core.openai_provider import OpenAIProvider
from src.core.anthropic_provider import AnthropicProvider


class TestLLMProviderFactory:
    """Test LLMProviderFactory."""

    def test_factory_register_provider(self):
        """Test registering a new provider."""
        class DummyProvider(LLMProvider):
            def stream_chat(self, messages, model, temperature=0.7, **kwargs):
                yield "test"
            def get_available_models(self):
                return []
            def health_check(self):
                return True
            def supports_vision(self):
                return False

        factory = LLMProviderFactory()
        factory.register("dummy", DummyProvider)
        assert "dummy" in factory.get_available_providers()

    def test_factory_create_provider(self):
        """Test creating provider instance."""
        factory = LLMProviderFactory()
        config = {
            "base_url": "http://localhost:11434",
            "api_key": "",
        }
        provider = factory.create("ollama", config)
        assert isinstance(provider, OllamaProvider)

    def test_factory_create_invalid_provider(self):
        """Test creating invalid provider type."""
        factory = LLMProviderFactory()
        with pytest.raises(KeyError):
            factory.create("invalid_provider", {})

    def test_factory_invalid_config(self):
        """Test creating provider with invalid config."""
        factory = LLMProviderFactory()
        with pytest.raises((TypeError, ValueError)):
            factory.create("openai", {"base_url": "http://test"})  # Missing api_key


class TestOllamaProvider:
    """Test Ollama provider."""

    def test_ollama_init(self):
        """Test Ollama provider initialization."""
        provider = OllamaProvider(
            base_url="http://localhost:11434",
            api_key="",
            timeout=30,
        )
        assert provider.base_url == "http://localhost:11434"
        assert provider.api_key == ""
        assert provider.timeout == 30

    def test_ollama_stream_chat(self):
        """Test Ollama streaming chat."""
        provider = OllamaProvider()

        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'{"message": {"content": "Hello"}}',
            b'{"message": {"content": " World"}}',
        ]

        with patch("requests.post", return_value=mock_response):
            messages = [{"role": "user", "content": "Hi"}]
            result = list(provider.stream_chat(messages, "llama3.2"))

        assert result == ["Hello", " World"]

    def test_ollama_get_available_models(self):
        """Test getting Ollama models."""
        provider = OllamaProvider()

        mock_response = Mock()
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3.2"},
                {"name": "gemma3"},
            ]
        }

        with patch("requests.get", return_value=mock_response):
            models = provider.get_available_models()

        assert models == ["llama3.2", "gemma3"]

    def test_ollama_health_check_success(self):
        """Test successful Ollama health check."""
        provider = OllamaProvider()

        mock_response = Mock()
        mock_response.status_code = 200

        with patch("requests.get", return_value=mock_response):
            assert provider.health_check() is True

    def test_ollama_health_check_failure(self):
        """Test failed Ollama health check."""
        provider = OllamaProvider()

        import requests
        with patch("requests.get", side_effect=requests.exceptions.ConnectionError("Connection failed")):
            assert provider.health_check() is False

    def test_ollama_connection_error(self):
        """Test connection error handling."""
        provider = OllamaProvider()

        import requests
        with patch("requests.post", side_effect=requests.exceptions.ConnectionError("Network error")):
            messages = [{"role": "user", "content": "Hi"}]
            with pytest.raises(ConnectionError):
                list(provider.stream_chat(messages, "llama3.2"))

    def test_ollama_supports_vision(self):
        """Test vision support detection."""
        provider = OllamaProvider()

        mock_response = Mock()
        mock_response.json.return_value = {
            "models": [
                {"name": "llama3.2-vision"},
                {"name": "llava"},
            ]
        }

        with patch("requests.get", return_value=mock_response):
            assert provider.supports_vision() is True


class TestOpenAIProvider:
    """Test OpenAI provider."""

    def test_openai_init_requires_api_key(self):
        """Test OpenAI requires API key."""
        with pytest.raises(ValueError):
            OpenAIProvider(api_key="")

    def test_openai_init_success(self):
        """Test OpenAI initialization with API key."""
        provider = OpenAIProvider(api_key="sk-test-key")
        assert provider.api_key == "sk-test-key"

    def test_openai_stream_chat(self):
        """Test OpenAI streaming chat."""
        provider = OpenAIProvider(api_key="sk-test")

        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'data: {"choices": [{"delta": {"content": "Hello"}}]}',
            b'data: {"choices": [{"delta": {"content": " World"}}]}',
            b'data: [DONE]',
        ]

        with patch("requests.post", return_value=mock_response):
            messages = [{"role": "user", "content": "Hi"}]
            result = list(provider.stream_chat(messages, "gpt-4o"))

        assert result == ["Hello", " World"]

    def test_openai_health_check(self):
        """Test OpenAI health check."""
        provider = OpenAIProvider(api_key="sk-test")

        mock_response = Mock()
        mock_response.status_code = 200

        with patch("requests.get", return_value=mock_response):
            assert provider.health_check() is True

    def test_openai_supports_vision(self):
        """Test OpenAI vision support."""
        provider = OpenAIProvider(api_key="sk-test")
        assert provider.supports_vision() is True


class TestAnthropicProvider:
    """Test Anthropic provider."""

    def test_anthropic_init_requires_api_key(self):
        """Test Anthropic requires API key."""
        with pytest.raises(ValueError):
            AnthropicProvider(api_key="")

    def test_anthropic_stream_chat(self):
        """Test Anthropic streaming chat."""
        provider = AnthropicProvider(api_key="sk-ant-test")

        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'data: {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "Hello"}}',
            b'data: {"type": "content_block_delta", "delta": {"type": "text_delta", "text": " World"}}',
        ]

        with patch("requests.post", return_value=mock_response):
            messages = [{"role": "user", "content": "Hi"}]
            result = list(provider.stream_chat(messages, "claude-3-opus"))

        assert result == ["Hello", " World"]

    def test_anthropic_supports_vision(self):
        """Test Anthropic vision support."""
        provider = AnthropicProvider(api_key="sk-ant-test")
        assert provider.supports_vision() is True

    def test_anthropic_system_message_extraction(self):
        """Test system message is extracted correctly."""
        provider = AnthropicProvider(api_key="sk-ant-test")

        mock_response = Mock()
        mock_response.iter_lines.return_value = [
            b'data: {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "OK"}}',
        ]

        with patch("requests.post", return_value=mock_response) as mock_post:
            messages = [
                {"role": "system", "content": "You are helpful"},
                {"role": "user", "content": "Hi"},
            ]
            list(provider.stream_chat(messages, "claude-3-opus"))

            # Verify system message was extracted
            call_args = mock_post.call_args
            payload = call_args[1]["json"]
            assert payload["system"] == "You are helpful"
            assert len(payload["messages"]) == 1  # Only user message left
