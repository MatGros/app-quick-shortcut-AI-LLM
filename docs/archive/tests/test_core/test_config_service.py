"""Tests for ConfigService."""

import json
import tempfile
from pathlib import Path

import pytest

from src.core.config_service import ConfigService


class TestConfigService:
    """Test ConfigService."""

    @pytest.fixture
    def temp_config_file(self):
        """Create a temporary config file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = Path(f.name)
            json.dump(ConfigService._get_default_config(), f)
        yield temp_path
        temp_path.unlink()

    @pytest.fixture(autouse=True)
    def reset_singleton(self):
        """Reset singleton between tests."""
        ConfigService._instance = None
        ConfigService._config = {}
        ConfigService._config_path = None
        ConfigService._initialized = False
        yield
        ConfigService._instance = None
        ConfigService._config = {}
        ConfigService._config_path = None
        ConfigService._initialized = False

    def test_config_singleton(self):
        """Test ConfigService singleton pattern."""
        config1 = ConfigService()
        config2 = ConfigService()
        assert config1 is config2

    def test_config_get_default(self, temp_config_file):
        """Test getting config with defaults."""
        config = ConfigService(temp_config_file)
        theme = config.get("appearance.theme")
        assert theme == "dark"

    def test_config_get_nested(self, temp_config_file):
        """Test getting nested config values."""
        config = ConfigService(temp_config_file)
        font_size = config.get("appearance.font_size")
        assert font_size == 11

    def test_config_get_with_default(self, temp_config_file):
        """Test getting non-existent key with default."""
        config = ConfigService(temp_config_file)
        value = config.get("nonexistent.key", "default_value")
        assert value == "default_value"

    def test_config_set(self, temp_config_file):
        """Test setting config values."""
        config = ConfigService(temp_config_file)
        config.set("appearance.theme", "light")
        assert config.get("appearance.theme") == "light"

    def test_config_set_nested_creation(self, temp_config_file):
        """Test setting creates nested structure."""
        config = ConfigService(temp_config_file)
        config.set("new.nested.key", "value")
        assert config.get("new.nested.key") == "value"

    def test_config_save_and_load(self, temp_config_file):
        """Test saving and loading config."""
        config1 = ConfigService(temp_config_file)
        config1.set("appearance.theme", "light")
        config1.save()

        # Reset singleton and load again
        ConfigService._instance = None
        ConfigService._config = {}
        ConfigService._config_path = None
        ConfigService._initialized = False
        config2 = ConfigService(temp_config_file)
        assert config2.get("appearance.theme") == "light"

    def test_config_add_provider(self, temp_config_file):
        """Test adding provider configuration."""
        config = ConfigService(temp_config_file)
        new_provider = {
            "id": "openai-test",
            "type": "openai",
            "name": "OpenAI Test",
            "base_url": "https://api.openai.com/v1",
            "api_key": "sk-test",
        }
        config.add_provider("openai-test", new_provider)

        providers = config.get_providers()
        assert len(providers) > 1
        assert any(p["id"] == "openai-test" for p in providers)

    def test_config_update_existing_provider(self, temp_config_file):
        """Test updating existing provider."""
        config = ConfigService(temp_config_file)
        original_count = len(config.get_providers())

        updated_provider = {
            "id": "ollama-local",
            "type": "ollama",
            "name": "Ollama Updated",
            "base_url": "http://localhost:11434",
            "api_key": "",
        }
        config.add_provider("ollama-local", updated_provider)

        providers = config.get_providers()
        assert len(providers) == original_count
        assert any(p["name"] == "Ollama Updated" for p in providers)

    def test_config_get_default_provider(self, temp_config_file):
        """Test getting default provider."""
        config = ConfigService(temp_config_file)
        default = config.get_default_provider()
        assert default is not None
        assert default["id"] == "ollama-local"

    def test_config_reset_to_defaults(self, temp_config_file):
        """Test resetting to defaults."""
        config = ConfigService(temp_config_file)
        config.set("appearance.theme", "light")
        config.reset_to_defaults()

        assert config.get("appearance.theme") == "dark"

    def test_config_load_invalid_json(self):
        """Test loading invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            f.write("invalid json{{{")
            temp_path = Path(f.name)

        try:
            config = ConfigService(temp_path)
            # Should load defaults on error
            assert config.get("appearance.theme") == "dark"
        finally:
            temp_path.unlink()

    def test_config_file_not_found(self):
        """Test loading non-existent file."""
        config = ConfigService(Path("/nonexistent/path/config.json"))
        # Should create with defaults
        assert config.get("appearance.theme") == "dark"

    def test_config_all_providers_registered(self, temp_config_file):
        """Test all default providers are valid."""
        from src.core import LLMProviderFactory

        config = ConfigService(temp_config_file)
        providers = config.get_providers()

        for provider_config in providers:
            provider_type = provider_config.get("type")
            assert provider_type in LLMProviderFactory.get_available_providers()
