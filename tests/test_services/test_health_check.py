"""Tests for health check service."""

from unittest.mock import Mock, patch

import pytest

from src.core.config_service import ConfigService
from src.services.health_check import HealthCheckManager, HealthCheckResult


class TestHealthCheckResult:
    """Test HealthCheckResult."""

    def test_result_passed(self):
        """Test passed result."""
        result = HealthCheckResult("Test Check", True, "All good")
        assert result.passed is True
        assert "✅" in str(result)

    def test_result_failed(self):
        """Test failed result."""
        result = HealthCheckResult("Test Check", False, "Failed")
        assert result.passed is False
        assert "❌" in str(result)


class TestHealthCheckManager:
    """Test HealthCheckManager."""

    @pytest.fixture
    def health_check(self):
        """Create health check instance."""
        # Reset config singleton to ensure fresh state
        from src.core.config_service import ConfigService
        ConfigService._instance = None
        ConfigService._config = {}
        ConfigService._config_path = None
        ConfigService._initialized = False

        manager = HealthCheckManager()
        # Ensure default provider is set
        manager.config._config["providers"] = [
            {
                "id": "ollama-local",
                "type": "ollama",
                "name": "Ollama Local",
                "base_url": "http://localhost:11434",
                "api_key": "",
            }
        ]
        manager.config._config["default_provider"] = "ollama-local"
        return manager

    def test_health_check_config_valid(self, health_check):
        """Test config check with valid config."""
        health_check._check_config()
        assert any(r.name == "Config Integrity" for r in health_check.results)
        assert any(r.passed for r in health_check.results)

    def test_health_check_config_no_providers(self, health_check):
        """Test config check with no providers."""
        health_check.config._config["providers"] = []
        health_check._check_config()

        config_result = next(r for r in health_check.results if r.name == "Config Integrity")
        assert config_result.passed is False

    def test_health_check_llm_connectivity_default(self, health_check):
        """Test LLM connectivity check with default provider."""
        # Ensure default provider exists
        if not health_check.config.get_default_provider():
            health_check.config.set("default_provider", "ollama-local")

        with patch("src.services.health_check.LLMProviderFactory.create") as mock_create:
            mock_provider = Mock()
            mock_provider.health_check.return_value = True
            mock_create.return_value = mock_provider

            health_check._check_llm_connectivity()

            llm_result = next((r for r in health_check.results if r.name == "LLM Connectivity"), None)
            assert llm_result is not None
            assert llm_result.passed is True

    def test_health_check_llm_connectivity_failure(self, health_check):
        """Test LLM connectivity check when provider fails."""
        with patch("src.services.health_check.LLMProviderFactory.create") as mock_create:
            mock_provider = Mock()
            mock_provider.health_check.return_value = False
            mock_create.return_value = mock_provider

            health_check._check_llm_connectivity()

            llm_result = next(r for r in health_check.results if r.name == "LLM Connectivity")
            assert llm_result.passed is False

    def test_health_check_permissions_success(self, health_check):
        """Test permissions check."""
        health_check._check_permissions()

        perm_result = next(r for r in health_check.results if r.name == "Permissions")
        assert perm_result.passed is True

    def test_run_all_checks(self, health_check):
        """Test running all health checks."""
        with patch("src.services.health_check.LLMProviderFactory.create") as mock_create:
            mock_provider = Mock()
            mock_provider.health_check.return_value = True
            mock_create.return_value = mock_provider

            all_passed, results = health_check.run_all_checks()

            assert isinstance(results, list)
            assert len(results) > 0
            assert all(hasattr(r, "name") and hasattr(r, "passed") for r in results)

    def test_health_check_with_custom_config(self):
        """Test health check with custom config."""
        custom_config = ConfigService()
        custom_config._config = ConfigService._get_default_config()

        health_check = HealthCheckManager(custom_config)
        all_passed, results = health_check.run_all_checks()

        assert len(results) > 0
