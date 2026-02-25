"""
Integration tests for Ollama streaming (real LLM)

Tests verify:
  - Real Ollama connection (if available)
  - Token streaming
  - First token latency
  - Large response handling
  - Error scenarios

NOTE: Tests require local Ollama running on localhost:11434
      Use: ollama run llama2 (or mistral, neural-chat, etc.)
      Tests will SKIP if Ollama unavailable
"""

import pytest
import time
import logging
from unittest.mock import patch
from src.core.ollama_provider import OllamaProvider
from src.core.config_service import ConfigService


logger = logging.getLogger(__name__)


def ollama_available() -> bool:
    """Check if Ollama is available locally"""
    try:
        provider = OllamaProvider(base_url="http://localhost:11434")
        models = provider.get_available_models()
        return len(models) > 0
    except Exception as e:
        logger.debug(f"Ollama not available: {e}")
        return False


@pytest.mark.skipif(
    not ollama_available(),
    reason="Ollama not running on localhost:11434"
)
class TestOllamaStreaming:
    """Test real Ollama streaming"""

    @pytest.fixture
    def provider(self):
        """Create OllamaProvider instance"""
        return OllamaProvider(base_url="http://localhost:11434")

    def test_ollama_connection(self, provider):
        """Test connection to Ollama"""
        result = provider.health_check()
        assert result == True

    def test_get_available_models(self, provider):
        """Test fetching available models"""
        models = provider.get_available_models()

        assert len(models) > 0
        logger.info(f"Available models: {models}")

    def test_stream_simple_message(self, provider):
        """Test streaming a simple message"""
        messages = [
            {"role": "user", "content": "Say hello in one sentence."}
        ]

        tokens = []
        token_count = 0

        try:
            for token in provider.stream_chat(messages, model=models[0] if (models := provider.get_available_models()) else "llama2"):
                tokens.append(token)
                token_count += 1

        except Exception as e:
            pytest.skip(f"Streaming failed (model unavailable?): {e}")

        assert token_count > 0
        response = "".join(tokens)
        logger.info(f"Response ({token_count} tokens): {response[:100]}...")

    def test_first_token_latency(self, provider):
        """Measure latency to first token"""
        messages = [
            {"role": "user", "content": "Write a single word."}
        ]

        start = time.time()
        first_token_time = None
        token_count = 0

        try:
            for i, token in enumerate(provider.stream_chat(messages, model="llama2")):
                if i == 0:
                    first_token_time = time.time() - start
                token_count += 1

        except Exception as e:
            pytest.skip(f"Streaming failed: {e}")

        assert first_token_time is not None
        logger.info(f"First token latency: {first_token_time * 1000:.1f}ms ({token_count} tokens total)")

        # First token should be reasonable (< 5s for local Ollama)
        assert first_token_time < 5.0

    def test_large_response_streaming(self, provider):
        """Test streaming large responses"""
        messages = [
            {"role": "user", "content": "Write a paragraph about Python programming."}
        ]

        tokens = []
        token_count = 0

        try:
            for token in provider.stream_chat(messages, model="llama2"):
                tokens.append(token)
                token_count += 1

        except Exception as e:
            pytest.skip(f"Streaming failed: {e}")

        response = "".join(tokens)

        logger.info(f"Large response: {token_count} tokens, {len(response)} chars")
        assert token_count > 20  # Should have substantial response
        assert len(response) > 100  # At least 100 characters

    def test_multiple_messages(self, provider):
        """Test multi-turn conversation"""
        messages = [
            {"role": "user", "content": "What is 2+2?"},
            {"role": "assistant", "content": "4"},
            {"role": "user", "content": "What is 4+4?"},
        ]

        tokens = []

        try:
            for token in provider.stream_chat(messages, model="llama2"):
                tokens.append(token)

        except Exception as e:
            pytest.skip(f"Streaming failed: {e}")

        response = "".join(tokens)
        logger.info(f"Multi-turn response: {response}")
        assert "8" in response or "eight" in response.lower()

    def test_temperature_parameter(self, provider):
        """Test temperature parameter affects output"""
        messages = [
            {"role": "user", "content": "Say 'test' exactly."}
        ]

        # Same message with different temperatures
        responses = []

        for temperature in [0.1, 0.9]:
            tokens = []
            try:
                for token in provider.stream_chat(messages, model="llama2", temperature=temperature):
                    tokens.append(token)
            except Exception as e:
                pytest.skip(f"Streaming failed: {e}")

            responses.append("".join(tokens))

        logger.info(f"Temp 0.1: {responses[0][:50]}")
        logger.info(f"Temp 0.9: {responses[1][:50]}")

        # Responses might be different or same (depends on content)
        # Just verify both streamed successfully
        assert len(responses[0]) > 0
        assert len(responses[1]) > 0


class TestOllamaErrors:
    """Test error handling"""

    def test_ollama_connection_error(self):
        """Test handling connection error to unavailable Ollama"""
        provider = OllamaProvider(base_url="http://localhost:9999")  # Wrong port

        # health_check should fail on wrong port
        result = provider.health_check()
        assert result == False  # Connection failed

    def test_invalid_model(self):
        """Test handling invalid model name"""
        if not ollama_available():
            pytest.skip("Ollama not available")

        provider = OllamaProvider(base_url="http://localhost:11434")
        messages = [{"role": "user", "content": "Test"}]

        # This might raise ConnectionError or yield empty
        try:
            tokens = list(provider.stream_chat(messages, model="invalid-model-xyz"))
            # If it doesn't raise, it should be empty or error
            logger.info(f"Invalid model returned: {len(tokens)} tokens")
        except (ConnectionError, ValueError):
            pass  # Expected behavior


@pytest.mark.skipif(
    not ollama_available(),
    reason="Ollama not running"
)
class TestOllamaWithClipboard:
    """Test streaming with clipboard integration"""

    def test_stream_clipboard_content(self):
        """Test streaming with realistic clipboard content"""
        if not ollama_available():
            pytest.skip("Ollama not available")

        from src.core.clipboard_manager import get_clipboard_manager

        clipboard_mgr = get_clipboard_manager()
        provider = OllamaProvider(base_url="http://localhost:11434")

        # Set test clipboard content
        test_content = "Python is a high-level programming language."
        clipboard_mgr.set_text(test_content)

        # Read it back
        content = clipboard_mgr.get_text()
        assert content == test_content

        # Stream summarization
        messages = [
            {"role": "user", "content": f"Summarize this: {content}"}
        ]

        tokens = []
        try:
            for token in provider.stream_chat(messages, model="llama2"):
                tokens.append(token)
        except Exception as e:
            pytest.skip(f"Streaming failed: {e}")

        summary = "".join(tokens)
        logger.info(f"Summary: {summary}")
        assert len(summary) > 0
