"""OpenAI LLM provider implementation."""

from typing import Dict, List, Generator

import requests

from .llm_provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI API provider."""

    def __init__(
        self,
        base_url: str = "https://api.openai.com/v1",
        api_key: str = "",
        timeout: int = 30,
    ):
        """
        Initialize OpenAI provider.

        Args:
            base_url: OpenAI API endpoint
            api_key: OpenAI API key (required)
            timeout: Request timeout
        """
        if not api_key:
            raise ValueError("OpenAI API key is required")
        super().__init__(base_url, api_key, timeout)

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        **kwargs
    ) -> Generator[str, None, None]:
        """Stream chat completion from OpenAI."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
        }

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
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
                        if data_str == "[DONE]":
                            break
                        try:
                            import json
                            data = json.loads(data_str)
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except Exception:
                            continue

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"OpenAI connection failed: {e}")

    def get_available_models(self) -> List[str]:
        """Get list of available OpenAI models (hardcoded for now)."""
        # In production, you'd fetch from /models endpoint
        return ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]

    def health_check(self) -> bool:
        """Check if OpenAI API is accessible."""
        try:
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(
                f"{self.base_url}/models",
                headers=headers,
                timeout=min(5, self.timeout),
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def supports_vision(self) -> bool:
        """OpenAI models like gpt-4o support vision."""
        return True
