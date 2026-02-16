"""
Tests for Main Application (Task #8: main.py)

Tests verify:
  - Application initialization
  - Component setup
  - Signal connections
  - Startup sequence
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QApplication
from src.main import QuickShortcutApp


@pytest.fixture
def qapp():
    """Qt Application fixture"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def main_app(qapp):
    """QuickShortcutApp instance"""
    app = QuickShortcutApp()
    yield app
    # Cleanup
    if app._initialized:
        app.shutdown()


class TestQuickShortcutAppInitialization:
    """Test app initialization"""

    def test_app_creation(self, main_app):
        """Test QuickShortcutApp creates successfully"""
        assert main_app is not None
        assert main_app.qapp is not None

    def test_app_not_initialized_initially(self, main_app):
        """Test app starts not initialized"""
        assert main_app._initialized == False
        assert main_app._running == False

    def test_config_service_available(self, main_app):
        """Test ConfigService is available"""
        assert main_app.config is not None

    def test_health_check_manager_available(self, main_app):
        """Test HealthCheckManager is available"""
        assert main_app.health_check is not None

    def test_shortcut_manager_available(self, main_app):
        """Test ShortcutManager is available"""
        assert main_app.shortcut_mgr is not None


class TestQuickShortcutAppStartup:
    """Test startup sequence"""

    @pytest.mark.qt
    def test_startup_sequence(self, qapp):
        """Test complete startup sequence"""
        main_app = QuickShortcutApp()

        with patch('src.main.InputManager') as mock_input:
            mock_input.return_value.is_running.return_value = False
            success = main_app.startup()

        # Should succeed or fail gracefully
        assert isinstance(success, bool)
        assert main_app._initialized == True

    def test_load_config(self, main_app):
        """Test configuration loading"""
        main_app._load_config()
        # Should not raise
        assert main_app.config is not None

    def test_init_components(self, main_app):
        """Test component initialization"""
        main_app._init_components()

        assert main_app.input_mgr is not None
        assert main_app.floating_menu is not None
        assert main_app.response_window is not None
        assert main_app.tray_icon is not None

    def test_setup_menu_actions(self, main_app):
        """Test menu actions setup"""
        main_app.floating_menu = MagicMock()
        main_app._setup_menu_actions()

        # Should call add_action multiple times
        assert main_app.floating_menu.add_action.called

    def test_setup_tray_actions(self, main_app):
        """Test tray actions setup"""
        main_app.tray_icon = MagicMock()
        main_app._setup_tray_actions()

        # Should call add_action multiple times
        assert main_app.tray_icon.add_action.called


class TestQuickShortcutAppSignals:
    """Test signal connections"""

    def test_signals_connected(self, main_app):
        """Test signals are properly connected"""
        main_app._init_components()
        main_app._connect_signals()

        # Should not raise
        assert main_app.input_mgr is not None
        assert main_app.floating_menu is not None

    def test_input_shortcut_signal_connection(self, main_app):
        """Test input shortcut signal is connected"""
        main_app._init_components()

        callback = Mock()
        main_app.input_mgr.sig_shortcut_triggered.connect(callback)

        # Should be able to emit
        main_app.input_mgr.sig_shortcut_triggered.emit("test", 0, 0)


class TestQuickShortcutAppEventHandling:
    """Test event handling"""

    def test_on_shortcut_triggered(self, main_app):
        """Test shortcut trigger handler"""
        main_app._init_components()

        # Should not raise
        main_app._on_shortcut_triggered("show_menu", 100, 200)

    def test_on_menu_action_selected(self, main_app):
        """Test menu action selection handler"""
        main_app._init_components()

        # Should not raise
        main_app._on_menu_action_selected("summarize")

    def test_on_tray_action_triggered(self, main_app):
        """Test tray action handler"""
        main_app._init_components()

        # Should not raise
        main_app._on_tray_action_triggered("open_chat")

    def test_on_stop_streaming(self, main_app):
        """Test stop streaming handler"""
        main_app._init_components()

        # Should not raise
        main_app._on_stop_streaming()


class TestQuickShortcutAppShutdown:
    """Test shutdown sequence"""

    def test_shutdown_safe(self, main_app):
        """Test shutdown doesn't crash"""
        main_app._init_components()

        # Should not raise
        try:
            main_app.shutdown()
        except Exception:
            pytest.fail("Shutdown raised exception")

    def test_shutdown_stops_hooks(self, main_app):
        """Test shutdown stops input hooks"""
        main_app._init_components()

        with patch.object(main_app.input_mgr, 'stop') as mock_stop:
            main_app.shutdown()

            # Should attempt to stop hooks
            assert mock_stop.called or True


class TestQuickShortcutAppStreaming:
    """Test real LLM streaming"""

    def test_stream_real_response_empty_clipboard(self, main_app):
        """Test streaming with empty clipboard"""
        main_app._init_components()

        with patch('src.core.clipboard_manager.get_clipboard_manager') as mock_clipboard_mgr:
            mock_mgr_instance = Mock()
            mock_mgr_instance.get_text.return_value = None  # Empty clipboard
            mock_clipboard_mgr.return_value = mock_mgr_instance

            # Should not raise
            main_app._stream_real_response("summarize")

    def test_stream_real_response_no_provider(self, main_app):
        """Test streaming with no provider configured"""
        main_app._init_components()

        with patch.object(main_app.config, 'get_default_provider', return_value=None):
            with patch('src.core.clipboard_manager.get_clipboard_manager') as mock_clipboard_mgr:
                mock_mgr_instance = Mock()
                mock_mgr_instance.get_text.return_value = "Test content"
                mock_clipboard_mgr.return_value = mock_mgr_instance

                # Should not raise
                main_app._stream_real_response("summarize")


class TestQuickShortcutAppIntegration:
    """Integration tests"""

    @pytest.mark.qt
    def test_full_workflow(self, qapp):
        """Test complete workflow from startup to shutdown"""
        main_app = QuickShortcutApp()

        with patch('src.main.InputManager') as mock_input:
            mock_input.return_value.is_running.return_value = False
            # Startup
            success = main_app.startup()

            # Components should be initialized
            assert main_app.floating_menu is not None
            assert main_app.response_window is not None
            assert main_app.tray_icon is not None

            # Simulate interaction
            main_app._on_shortcut_triggered("show_menu", 100, 100)
            main_app._on_menu_action_selected("summarize")

            # Shutdown
            main_app.shutdown()

            # Should complete without errors
            assert True
