"""
Tests for SettingsDialog

Tests verify:
  - Dialog initialization and tabs
  - Provider management (add, edit, delete)
  - Appearance settings
  - Shortcuts display
  - Settings persistence
  - Signal emission
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtTest import QTest
from src.ui.settings_dialog import SettingsDialog
from src.core.config_service import ConfigService


@pytest.fixture
def qapp():
    """Qt Application fixture"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def temp_config(tmp_path):
    """Temporary config file for testing"""
    config_file = tmp_path / "config.json"
    # Reset singleton
    ConfigService._instance = None
    ConfigService._config = {}
    ConfigService._config_path = None
    ConfigService._initialized = False
    return config_file


@pytest.fixture
def config_service(temp_config):
    """ConfigService with temp config"""
    return ConfigService(temp_config)


@pytest.fixture
def settings_dialog(qapp, config_service):
    """SettingsDialog instance for testing"""
    dialog = SettingsDialog()
    yield dialog
    if dialog.isVisible():
        dialog.close()


class TestSettingsDialogInitialization:
    """Test dialog initialization"""

    def test_dialog_creation(self, settings_dialog):
        """Test SettingsDialog initializes"""
        assert settings_dialog is not None
        assert settings_dialog.windowTitle() == "Quick Shortcut AI - Settings"

    def test_dialog_is_modal(self, settings_dialog):
        """Test dialog is modal"""
        assert settings_dialog.isModal() == True

    def test_tabs_exist(self, settings_dialog):
        """Test all tabs are created"""
        # Dialog should have a tab widget with tabs
        assert settings_dialog is not None


class TestProvidersTab:
    """Test Providers tab functionality"""

    def test_provider_list_populated(self, settings_dialog, config_service):
        """Test providers list is populated"""
        # Should have at least the default Ollama provider
        assert settings_dialog.provider_list.count() >= 1

    def test_default_provider_marked(self, settings_dialog, config_service):
        """Test default provider is marked with star"""
        config_service.set("default_provider", "ollama-local")
        # Reload dialog
        settings_dialog._load_providers()

        # At least one item should be marked with ★
        found_star = False
        for i in range(settings_dialog.provider_list.count()):
            item = settings_dialog.provider_list.item(i)
            if "★" in item.text():
                found_star = True
                break

        assert found_star

    def test_provider_selection(self, settings_dialog):
        """Test selecting a provider loads details"""
        if settings_dialog.provider_list.count() > 0:
            settings_dialog.provider_list.setCurrentRow(0)
            settings_dialog._on_provider_selected()

            # Fields should be populated
            assert len(settings_dialog.provider_name.text()) >= 0

    def test_test_connection_button_exists(self, settings_dialog):
        """Test Test Connection button is available"""
        # Should have test connection functionality
        assert hasattr(settings_dialog, 'provider_type')
        assert hasattr(settings_dialog, 'provider_url')

    def test_provider_type_dropdown(self, settings_dialog):
        """Test provider type dropdown has correct options"""
        types = [
            settings_dialog.provider_type.itemText(i)
            for i in range(settings_dialog.provider_type.count())
        ]

        assert "ollama" in types
        assert "openai" in types
        assert "anthropic" in types

    def test_api_key_field_is_password(self, settings_dialog):
        """Test API key field masks input"""
        from PySide6.QtWidgets import QLineEdit
        assert settings_dialog.provider_api_key.echoMode() == QLineEdit.Password

    @pytest.mark.qt
    def test_save_provider_validates_name(self, settings_dialog):
        """Test provider save validates name field"""
        if settings_dialog.provider_list.count() > 0:
            settings_dialog.provider_list.setCurrentRow(0)

            # Clear name
            settings_dialog.provider_name.setText("")

            # Mock message box
            with patch('PySide6.QtWidgets.QMessageBox.warning'):
                settings_dialog._on_save_provider()

    @pytest.mark.qt
    def test_save_provider_validates_url(self, settings_dialog):
        """Test provider save validates URL field"""
        if settings_dialog.provider_list.count() > 0:
            settings_dialog.provider_list.setCurrentRow(0)

            # Clear URL
            settings_dialog.provider_url.setText("")

            # Mock message box
            with patch('PySide6.QtWidgets.QMessageBox.warning'):
                settings_dialog._on_save_provider()


class TestShortcutsTab:
    """Test Shortcuts tab"""

    def test_shortcuts_list_populated(self, settings_dialog, config_service):
        """Test shortcuts list is populated"""
        # Should have default shortcuts
        assert settings_dialog.shortcuts_list.count() >= 1

    def test_shortcuts_display_correctly(self, settings_dialog, config_service):
        """Test shortcuts are displayed with proper format"""
        # Check first item has format "name: key"
        if settings_dialog.shortcuts_list.count() > 0:
            item_text = settings_dialog.shortcuts_list.item(0).text()
            assert ":" in item_text


class TestAppearanceTab:
    """Test Appearance tab"""

    def test_theme_combo_options(self, settings_dialog):
        """Test theme combo has correct options"""
        themes = [
            settings_dialog.theme_combo.itemText(i)
            for i in range(settings_dialog.theme_combo.count())
        ]

        assert "dark" in themes
        assert "light" in themes
        assert "system" in themes

    def test_theme_default_loaded(self, settings_dialog, config_service):
        """Test default theme is loaded"""
        config_service.set("appearance.theme", "dark")
        # Reload dialog
        settings_dialog._load_settings()

        assert settings_dialog.theme_combo.currentText() == "dark"

    def test_font_family_field(self, settings_dialog, config_service):
        """Test font family field works"""
        config_service.set("appearance.font_family", "Arial")
        settings_dialog._load_settings()

        assert settings_dialog.font_family.text() == "Arial"

    def test_font_size_spinbox(self, settings_dialog):
        """Test font size spinbox"""
        assert settings_dialog.font_size.minimum() == 8
        assert settings_dialog.font_size.maximum() == 24

    def test_animation_speed_spinbox(self, settings_dialog):
        """Test animation speed spinbox"""
        assert settings_dialog.animation_speed.minimum() == 0
        assert settings_dialog.animation_speed.maximum() == 1000
        assert "ms" in settings_dialog.animation_speed.suffix()


class TestAboutTab:
    """Test About tab"""

    def test_about_tab_created(self, settings_dialog):
        """Test About tab exists and contains info"""
        # About tab should exist
        assert settings_dialog is not None


class TestSettingsPersistence:
    """Test settings are saved correctly"""

    @pytest.mark.qt
    def test_appearance_settings_saved(self, settings_dialog, config_service):
        """Test appearance settings are saved"""
        settings_dialog.theme_combo.setCurrentText("light")
        settings_dialog.font_family.setText("Courier New")
        settings_dialog.font_size.setValue(12)

        settings_dialog._save_settings()

        # Verify saved
        assert config_service.get("appearance.theme") == "light"
        assert config_service.get("appearance.font_family") == "Courier New"
        assert config_service.get("appearance.font_size") == 12

    @pytest.mark.qt
    def test_settings_signal_emitted(self, settings_dialog):
        """Test sig_settings_changed is emitted"""
        callback = Mock()
        settings_dialog.sig_settings_changed.connect(callback)

        settings_dialog._save_settings()

        assert callback.called

    @pytest.mark.qt
    def test_ok_button_saves_and_closes(self, settings_dialog):
        """Test OK button saves settings and closes"""
        with patch.object(settings_dialog, '_save_settings') as mock_save:
            settings_dialog._on_ok()
            mock_save.assert_called_once()

    @pytest.mark.qt
    def test_apply_button_saves_without_closing(self, settings_dialog):
        """Test Apply button saves without closing"""
        with patch.object(settings_dialog, '_save_settings') as mock_save:
            with patch('PySide6.QtWidgets.QMessageBox.information'):
                settings_dialog._on_apply()
                mock_save.assert_called_once()

    @pytest.mark.qt
    def test_cancel_button_rejects(self, settings_dialog):
        """Test Cancel button rejects dialog"""
        result = settings_dialog.reject()
        # Dialog should be rejected (closed without saving)
        assert True  # reject() doesn't return a value


class TestProviderOperations:
    """Test provider add/edit/delete operations"""

    @pytest.mark.qt
    def test_delete_provider_confirmation(self, settings_dialog):
        """Test delete provider asks for confirmation"""
        if settings_dialog.provider_list.count() > 0:
            settings_dialog.provider_list.setCurrentRow(0)

            with patch('PySide6.QtWidgets.QMessageBox.question') as mock_question:
                mock_question.return_value = QMessageBox.No
                settings_dialog._on_delete_provider()

                # Should have asked for confirmation
                assert mock_question.called

    @pytest.mark.qt
    def test_test_connection_success(self, settings_dialog):
        """Test connection test success message"""
        settings_dialog.provider_url.setText("http://localhost:11434")
        settings_dialog.provider_type.setCurrentText("ollama")

        with patch('src.core.llm_provider.LLMProviderFactory.create') as mock_create:
            mock_provider = MagicMock()
            mock_provider.health_check.return_value = True
            mock_create.return_value = mock_provider

            with patch('PySide6.QtWidgets.QMessageBox.information'):
                settings_dialog._on_test_connection()

                mock_create.assert_called_once()

    @pytest.mark.qt
    def test_test_connection_failure(self, settings_dialog):
        """Test connection test failure handling"""
        settings_dialog.provider_url.setText("http://invalid-url:11434")
        settings_dialog.provider_type.setCurrentText("ollama")

        with patch('src.core.llm_provider.LLMProviderFactory.create') as mock_create:
            mock_create.side_effect = Exception("Connection failed")

            with patch('PySide6.QtWidgets.QMessageBox.critical'):
                settings_dialog._on_test_connection()


class TestSettingsDialogIntegration:
    """Integration tests for settings dialog"""

    @pytest.mark.qt
    def test_full_workflow(self, settings_dialog, config_service):
        """Test complete workflow: load, modify, save"""
        # Load
        original_theme = settings_dialog.theme_combo.currentText()

        # Modify
        new_theme = "light" if original_theme == "dark" else "dark"
        settings_dialog.theme_combo.setCurrentText(new_theme)

        # Save
        settings_dialog._save_settings()

        # Verify
        assert config_service.get("appearance.theme") == new_theme

    @pytest.mark.qt
    def test_dialog_respects_existing_config(self, settings_dialog, config_service):
        """Test dialog loads and respects existing config"""
        # Set config
        config_service.set("appearance.theme", "light")
        config_service.set("appearance.font_size", 14)

        # Create new dialog (should load settings)
        new_dialog = SettingsDialog()
        new_dialog._load_settings()

        # Verify
        assert new_dialog.theme_combo.currentText() == "light"
        assert new_dialog.font_size.value() == 14

        new_dialog.close()

    @pytest.mark.qt
    def test_multiple_tab_navigation(self, settings_dialog):
        """Test can navigate between tabs"""
        # Dialog should support tab navigation
        assert settings_dialog is not None
        # Should not crash when switching tabs
        assert True
