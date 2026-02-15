"""Health check service for startup validation."""

from typing import Dict, List, Optional, Tuple

from src.core import ConfigService, LLMProviderFactory


class HealthCheckResult:
    """Result of a single health check."""

    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message

    def __repr__(self) -> str:
        status = "✅" if self.passed else "❌"
        return f"{status} {self.name}: {self.message}"


class HealthCheckManager:
    """Manager for startup health checks."""

    def __init__(self, config: Optional[ConfigService] = None):
        """
        Initialize health check manager.

        Args:
            config: ConfigService instance (default: singleton)
        """
        self.config = config or ConfigService()
        self.results: List[HealthCheckResult] = []

    def run_all_checks(self) -> Tuple[bool, List[HealthCheckResult]]:
        """
        Run all health checks.

        Returns:
            (all_passed, results) - True if all critical checks pass
        """
        self.results = []

        self._check_config()
        self._check_llm_connectivity()
        self._check_permissions()

        all_passed = all(r.passed for r in self.results)
        return all_passed, self.results

    def _check_config(self) -> None:
        """Check configuration integrity."""
        try:
            providers = self.config.get_providers()
            default_provider = self.config.get_default_provider()

            if not providers:
                self.results.append(
                    HealthCheckResult("Config Integrity", False, "No providers configured")
                )
            elif default_provider is None:
                self.results.append(
                    HealthCheckResult("Config Integrity", False, "Default provider not found")
                )
            else:
                self.results.append(
                    HealthCheckResult(
                        "Config Integrity", True, f"✓ {len(providers)} providers, {len(providers)} OK"
                    )
                )
        except Exception as e:
            self.results.append(
                HealthCheckResult("Config Integrity", False, f"Error: {str(e)}")
            )

    def _check_llm_connectivity(self) -> None:
        """Check LLM provider connectivity."""
        try:
            default_provider_config = self.config.get_default_provider()
            if not default_provider_config:
                self.results.append(
                    HealthCheckResult("LLM Connectivity", False, "No default provider")
                )
                return

            provider_type = default_provider_config.get("type", "ollama")

            try:
                provider = LLMProviderFactory.create(provider_type, default_provider_config)
                is_healthy = provider.health_check()

                if is_healthy:
                    self.results.append(
                        HealthCheckResult(
                            "LLM Connectivity",
                            True,
                            f"✓ {default_provider_config.get('name')} is accessible",
                        )
                    )
                else:
                    self.results.append(
                        HealthCheckResult(
                            "LLM Connectivity",
                            False,
                            f"✗ {default_provider_config.get('name')} is not responding",
                        )
                    )
            except Exception as e:
                self.results.append(
                    HealthCheckResult("LLM Connectivity", False, f"Error: {str(e)}")
                )

        except Exception as e:
            self.results.append(
                HealthCheckResult("LLM Connectivity", False, f"Unexpected error: {str(e)}")
            )

    def _check_permissions(self) -> None:
        """Check necessary permissions."""
        import os
        from pathlib import Path

        try:
            # Check AppData write access
            appdata = Path(os.getenv("APPDATA", os.path.expanduser("~")))
            test_dir = appdata / "QuickShortcutAI"
            test_dir.mkdir(parents=True, exist_ok=True)

            # Try writing test file
            test_file = test_dir / ".health_check_test"
            test_file.write_text("test")
            test_file.unlink()

            self.results.append(
                HealthCheckResult("Permissions", True, "✓ AppData write access OK")
            )
        except Exception as e:
            self.results.append(
                HealthCheckResult("Permissions", False, f"AppData access denied: {str(e)}")
            )
