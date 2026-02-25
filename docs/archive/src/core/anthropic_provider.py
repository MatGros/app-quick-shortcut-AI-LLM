"""Anthropic Claude LLM provider implementation."""

from typing import Dict, List, Generator

import requests

from .llm_provider import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API provider."""

    def __init__(
        self,
        base_url: str = "https://api.anthropic.com/v1",
        api_key: str = "",
        timeout: int = 30,
    ):
        """
        Initialize Anthropic provider.

        Args:
            base_url: Anthropic API endpoint
            api_key: Anthropic API key (required)
            timeout: Request timeout
        """
        if not api_key:
            raise ValueError("Anthropic API key is required")
        super().__init__(base_url, api_key, timeout)

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        **kwargs
    ) -> Generator[str, None, None]:
        """Stream chat completion from Anthropic."""
        # Extract system message if present
        system_message = ""
        filtered_messages = []

        for msg in messages:
            if msg.get("role") == "system":
                system_message = msg.get("content", "")
            else:
                filtered_messages.append(msg)

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

        payload = {
            "model": model,
            "max_tokens": 2048,
            "messages": filtered_messages,
            "temperature": temperature,
            "stream": True,
        }

        if system_message:
            payload["system"] = system_message

        try:
            response = requests.post(
                f"{self.base_url}/messages",
                json=payload,
                headers=headers,
                stream=True,
                timeout=self.timeout,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8") if isinstance(line, bytes) else line
                    if line_str.startswith("data: "):
                        data_str = line_str[6:]
                        try:
                            import json
                            data = json.loads(data_str)
                            if data.get("type") == "content_block_delta":
                                delta = data.get("delta", {})
                                if delta.get("type") == "text_delta":
                                    yield delta.get("text", "")
                        except Exception:
                            continue

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Anthropic connection failed: {e}")

    def get_available_models(self) -> List[str]:
        """Get list of available Anthropic models (hardcoded)."""
        return ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]

    def health_check(self) -> bool:
        """Check if Anthropic API is accessible."""
        try:
            headers = {"x-api-key": self.api_key}
            # Simple health check by trying to get models
            response = requests.get(
                f"{self.base_url}/messages",
                headers=headers,
                timeout=min(5, self.timeout),
                json={"model": "claude-3-opus-20240229", "max_tokens": 1, "messages": []},
            )
            # Even 400 means API is reachable
            return response.status_code in [200, 400, 401]
        except requests.exceptions.RequestException:
            return False

    def supports_vision(self) -> bool:
        """Anthropic Claude models support vision."""
        return True
