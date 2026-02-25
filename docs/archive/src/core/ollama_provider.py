"""Ollama LLM provider implementation."""

import json
from typing import Dict, List, Generator

import requests

from .llm_provider import LLMProvider


class OllamaProvider(LLMProvider):
    """Ollama local/cloud LLM provider."""

    def __init__(self, base_url: str = "http://localhost:11434", api_key: str = "", timeout: int = 30):
        """
        Initialize Ollama provider.

        Args:
            base_url: Ollama API endpoint (default: local)
            api_key: Bearer token if cloud-hosted
            timeout: Request timeout
        """
        super().__init__(base_url, api_key, timeout)
        self.api_endpoint = f"{self.base_url}/api/chat"

    def stream_chat(
        self,
        messages: List[Dict[str, str]],
        model: str,
        temperature: float = 0.7,
        **kwargs
    ) -> Generator[str, None, None]:
        """Stream chat completion from Ollama."""
        payload = {
            "model": model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
            },
        }

        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        try:
            response = requests.post(
                self.api_endpoint,
                json=payload,
                headers=headers,
                stream=True,
                timeout=self.timeout,
            )
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "message" in data and "content" in data["message"]:
                            yield data["message"]["content"]
                    except json.JSONDecodeError:
                        continue

        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Ollama connection failed: {e}")

    def get_available_models(self) -> List[str]:
        """Get list of available Ollama models."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=self.timeout,
            )
            response.raise_for_status()
            data = response.json()
            return [model["name"] for model in data.get("models", [])]
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Failed to fetch Ollama models: {e}")

    def health_check(self) -> bool:
        """Check if Ollama is accessible."""
        try:
            response = requests.get(
                f"{self.base_url}/api/tags",
                timeout=min(5, self.timeout),  # Short timeout for health check
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def supports_vision(self) -> bool:
        """Check if any vision model is available."""
        try:
            models = self.get_available_models()
            vision_keywords = ["vision", "llava", "qwen-vl"]
            return any(kw in model.lower() for model in models for kw in vision_keywords)
        except ConnectionError:
            return False
