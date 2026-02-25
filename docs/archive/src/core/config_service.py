"""Configuration service for managing app settings."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from .llm_provider import LLMProviderFactory


class ConfigService:
    """Singleton service for configuration management."""

    _instance: Optional["ConfigService"] = None
    _config: Dict[str, Any] = {}
    _config_path: Optional[Path] = None
    _initialized: bool = False

    def __new__(cls, config_path: Optional[Path] = None):
        """Ensure singleton pattern."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize ConfigService.

        Args:
            config_path: Custom config file path. If None, uses %APPDATA%
        """
        if self._initialized:
            return

        if config_path:
            ConfigService._config_path = Path(config_path)
        elif not ConfigService._config_path:
            # Default: %APPDATA%\QuickShortcutAI\config.json
            appdata = os.getenv("APPDATA", os.path.expanduser("~"))
            ConfigService._config_path = Path(appdata) / "QuickShortcutAI" / "config.json"

        if not ConfigService._config:
            self.load()

        ConfigService._initialized = True

    @classmethod
    def get_instance(cls, config_path: Optional[Path] = None) -> "ConfigService":
        """Get singleton instance."""
        return cls(config_path)

    def load(self) -> None:
        """Load configuration from file."""
        if ConfigService._config_path and ConfigService._config_path.exists():
            try:
                with open(ConfigService._config_path, "r") as f:
                    ConfigService._config = json.load(f)
                    self._validate_config()
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}. Using defaults.")
                ConfigService._config = self._get_default_config()
        else:
            ConfigService._config = self._get_default_config()

    def save(self) -> None:
        """Save configuration to file."""
        if ConfigService._config_path:
            ConfigService._config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(ConfigService._config_path, "w") as f:
                json.dump(ConfigService._config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get config value by dot-notation key (e.g., 'appearance.theme').

        Args:
            key: Configuration key (supports nested keys with dots)
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def set(self, key: str, value: Any) -> None:
        """
        Set config value by dot-notation key.

        Args:
            key: Configuration key (supports nested keys with dots)
            value: Value to set
        """
        keys = key.split(".")
        config = self._config

        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]

        config[keys[-1]] = value

    def reset_to_defaults(self) -> None:
        """Reset all configuration to defaults."""
        ConfigService._config = self._get_default_config()
        self.save()

    def add_provider(self, provider_id: str, provider_config: Dict[str, Any]) -> None:
        """
        Add LLM provider configuration.

        Args:
            provider_id: Unique provider identifier
            provider_config: Provider configuration dict
        """
        if "providers" not in ConfigService._config:
            ConfigService._config["providers"] = []

        # Check if provider already exists
        for i, p in enumerate(ConfigService._config["providers"]):
            if p.get("id") == provider_id:
                ConfigService._config["providers"][i] = provider_config
                return

        ConfigService._config["providers"].append(provider_config)

    def get_providers(self) -> list:
        """Get list of configured providers."""
        return ConfigService._config.get("providers", [])

    def get_default_provider(self) -> Optional[Dict[str, Any]]:
        """Get the default provider configuration."""
        provider_id = ConfigService._config.get("default_provider")
        if provider_id:
            for p in self.get_providers():
                if p.get("id") == provider_id:
                    return p
        return None

    def _validate_config(self) -> None:
        """Validate config structure."""
        required_keys = ["version", "providers", "default_provider", "shortcuts", "appearance"]
        for key in required_keys:
            if key not in ConfigService._config:
                print(f"Missing config key: {key}. Using defaults.")
                ConfigService._config = self._get_default_config()
                return

    @staticmethod
    def _get_default_config() -> Dict[str, Any]:
        """Get default configuration with Ollama provider."""
        return {
            "version": "1.0.0",
            "app": {
                "first_run": True,
            },
            "providers": [
                {
                    "id": "ollama-local",
                    "type": "ollama",
                    "name": "Ollama Local",
                    "base_url": "http://localhost:11434",
                    "api_key": "",
                    "default_model": "llama3.2:latest",
                    "enabled": True,
                }
            ],
            "default_provider": "ollama-local",
            "shortcuts": {
                "context_menu": "Ctrl+RightClick",
                "screenshot": "Ctrl+Shift+S",
                "settings": "Ctrl+Comma",
                "history": "Ctrl+H",
            },
            "appearance": {
                "theme": "dark",
                "font_family": "Segoe UI",
                "font_size": 11,
                "animation_speed_ms": 200,
            },
            "behavior": {
                "auto_paste_enabled": False,
                "auto_paste_delay_ms": 100,
                "clipboard_monitoring": True,
                "toast_duration_ms": 3000,
            },
        }
