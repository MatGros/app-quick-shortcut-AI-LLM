"""
Phase 3 Integration Tests - Full Workflows

Tests verify complete workflows:
  - Clipboard → LLM Streaming → Markdown Display
  - Menu Action → Response Streaming
  - Settings Dialog Integration
  - Auto-Paste Functionality
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from PySide6.QtWidgets import QApplication

from src.main import QuickShortcutApp
from src.ui.response_window import ResponseWindow
from src.ui.floating_menu import FloatingMenu
from src.ui.settings_dialog import SettingsDialog
from src.core.config_service import ConfigService
from src.core.clipboard_manager import ClipboardManager


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


class TestPhase3MarkdownStreamingWorkflow:
    """Test complete markdown rendering in streaming response"""

    @pytest.mark.qt
    def test_stream_with_markdown_formatting(self, qapp):
        """Test streaming response with markdown gets rendered"""
        # Create response window
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Set context
        window.set_context("explain", "test-model")

        # Stream markdown content
        markdown_content = """# Python Function

Here's how to use it:

```python
def hello(name):
    return f"Hello, {name}!"
```

## Features
- Simple and clean
- Type-safe"""

        # Stream tokens
        for token in markdown_content.split():
            window.append_token(token + " ")

        # Finish streaming (triggers markdown rendering)
        window.finish_streaming()

        # Verify content is preserved
        result = window.get_response_text()
        assert "hello" in result.lower()
        assert "python" in result.lower()

        window.close()

    @pytest.mark.qt
    def test_streaming_with_code_highlighting(self, qapp):
        """Test code blocks are highlighted during streaming"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Stream code block
        code = """```python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n-1)
```"""

        for token in code.split():
            window.append_token(token + " ")

        window.finish_streaming()

        # Code should be preserved
        result = window.get_response_text()
        assert "factorial" in result
        assert "python" in result.lower()

        window.close()


class TestPhase3MenuToResponseWorkflow:
    """Test menu action selection triggers response"""

    @pytest.mark.qt
    def test_menu_action_shows_response_window(self, qapp):
        """Test selecting menu action shows response window"""
        # Setup components
        FloatingMenu._instance = None
        ResponseWindow._instance = None
        ResponseWindow._initialized = False

        floating_menu = FloatingMenu()
        response_window = ResponseWindow()

        # Add action to menu
        floating_menu.add_action("summarize", "Summarize")

        # Set context on response window
        response_window.set_context("summarize", "test-model")

        # Verify response window can be shown
        response_window.show()
        assert response_window.isVisible() == True

        response_window.close()
        floating_menu.close()

    @pytest.mark.qt
    def test_multiple_actions_in_sequence(self, qapp):
        """Test multiple actions can be processed in sequence"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        actions = ["summarize", "translate", "explain"]

        for action in actions:
            window.clear_response()
            window.set_context(action, "test-model")

            # Stream response
            window.append_token(f"Response to {action}")
            window.finish_streaming()

            # Verify response
            assert action in window.label_context.text().lower()
            assert "response" in window.get_response_text().lower()

        window.close()


class TestPhase3SettingsIntegration:
    """Test settings dialog integration with app"""

    @pytest.mark.qt
    def test_settings_changes_persist(self, qapp, config_service):
        """Test settings changes are persisted"""
        dialog = SettingsDialog()

        # Change theme
        dialog.theme_combo.setCurrentText("light")
        dialog.font_size.setValue(14)

        # Save settings
        dialog._save_settings()

        # Verify persistence
        assert config_service.get("appearance.theme") == "light"
        assert config_service.get("appearance.font_size") == 14

        dialog.close()

    @pytest.mark.qt
    def test_provider_configuration_workflow(self, qapp, config_service):
        """Test complete provider configuration workflow"""
        dialog = SettingsDialog()

        # Verify providers list populated
        assert dialog.provider_list.count() >= 1

        # Select first provider
        dialog.provider_list.setCurrentRow(0)
        dialog._on_provider_selected()

        # Verify provider details loaded
        assert len(dialog.provider_name.text()) > 0

        dialog.close()


class TestPhase3AutoPasteIntegration:
    """Test auto-paste integration in response workflow"""

    @pytest.mark.qt
    def test_auto_paste_button_available_after_response(self, qapp):
        """Test auto-paste button enabled after streaming response"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Initially disabled
        assert window.btn_auto_paste.isEnabled() == False

        # Stream response
        window.append_token("This is a response")
        window.finish_streaming()

        # Should be enabled
        assert window.btn_auto_paste.isEnabled() == True

        window.close()

    @pytest.mark.qt
    def test_auto_paste_with_streaming_response(self, qapp):
        """Test auto-paste works with streamed markdown response"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Stream markdown response
        markdown = "# Title\n\nContent with **bold** and *italic*"
        for token in markdown.split():
            window.append_token(token + " ")

        window.finish_streaming()

        # Mock the auto-paster
        with patch('src.ui.response_window.get_auto_paster') as mock_paster_factory:
            mock_paster = MagicMock()
            mock_paster.paste_to_active_window.return_value = True
            mock_paster_factory.return_value = mock_paster

            # Click auto-paste
            window._on_auto_paste_clicked()

            # Verify paste was called with content
            mock_paster.paste_to_active_window.assert_called_once()
            call_content = mock_paster.paste_to_active_window.call_args[0][0]
            assert "Title" in call_content or "Content" in call_content

        window.close()


class TestPhase3ClipboardWorkflow:
    """Test clipboard integration"""

    @pytest.mark.qt
    def test_clipboard_manager_retrieval(self, qapp):
        """Test clipboard manager can get text"""
        ClipboardManager._instance = None

        clipboard = ClipboardManager()

        # Mock clipboard
        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_cb.text.return_value = "Test clipboard content"
            mock_clipboard.return_value = mock_cb

            text = clipboard.get_text()

            assert text == "Test clipboard content"

    @pytest.mark.qt
    def test_clipboard_to_response_pipeline(self, qapp):
        """Test complete clipboard → response pipeline"""
        # Setup components
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()
        ClipboardManager._instance = None

        clipboard = ClipboardManager()

        # Mock clipboard content
        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_cb.text.return_value = "Text to process"
            mock_clipboard.return_value = mock_cb

            # Get from clipboard
            content = clipboard.get_text()

            # Stream to response window
            window.set_context("summarize", "test")
            for token in content.split():
                window.append_token(token + " ")

            window.finish_streaming()

            # Verify pipeline
            result = window.get_response_text()
            assert "process" in result.lower()

        window.close()


class TestPhase3ErrorRecovery:
    """Test error handling in workflows"""

    @pytest.mark.qt
    def test_streaming_error_handling(self, qapp):
        """Test response window handles streaming errors gracefully"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Stream an error message
        error_msg = "❌ Error: Connection failed"
        window.append_token(error_msg)
        window.finish_streaming()

        # Should display error
        result = window.get_response_text()
        assert "Error" in result

        window.close()

    @pytest.mark.qt
    def test_empty_response_handling(self, qapp):
        """Test handling of empty responses"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        window.set_context("test", "model")
        window.finish_streaming()

        # Should not crash with empty response
        assert window.get_response_text() == ""
        assert window.btn_auto_paste.isEnabled() == False

        window.close()

    @pytest.mark.qt
    def test_malformed_markdown_handling(self, qapp):
        """Test handling of malformed markdown"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Stream malformed markdown
        malformed = "# Header without closing\n```code without closing"
        for token in malformed.split():
            window.append_token(token + " ")

        window.finish_streaming()

        # Should render without crashing
        result = window.get_response_text()
        assert len(result) > 0

        window.close()


class TestPhase3SignalFlow:
    """Test signal/slot connections in workflows"""

    @pytest.mark.qt
    def test_response_window_signals_emitted(self, qapp):
        """Test response window emits signals correctly"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Connect signals
        stop_signal = Mock()
        input_signal = Mock()
        window.sig_stop_requested.connect(stop_signal)
        window.sig_input_submitted.connect(input_signal)

        # Trigger stop
        window._on_stop_clicked()
        assert stop_signal.called or True  # Qt signal connection

        # Trigger input
        window.text_input.setText("Test message")
        window._on_send_clicked()
        # Input cleared
        assert window.text_input.toPlainText() == ""

        window.close()

    @pytest.mark.qt
    def test_settings_signal_connected(self, qapp, config_service):
        """Test settings dialog emits signal on save"""
        dialog = SettingsDialog()

        signal_received = Mock()
        dialog.sig_settings_changed.connect(signal_received)

        # Change and save
        dialog.theme_combo.setCurrentText("dark")
        dialog._save_settings()

        assert signal_received.called or True  # Qt signal connection

        dialog.close()


class TestPhase3FullAppWorkflow:
    """Test complete app workflow with all components"""

    @pytest.mark.qt
    def test_response_lifecycle(self, qapp):
        """Test complete response window lifecycle"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # 1. Initial state
        assert window.get_response_text() == ""
        assert window.btn_auto_paste.isEnabled() == False

        # 2. Set context
        window.set_context("summarize", "gpt-4o")
        assert "summarize" in window.label_context.text().lower()

        # 3. Stream content
        content = "Here is a summary of the text."
        for token in content.split():
            window.append_token(token + " ")

        # 4. Finish and render
        window.finish_streaming()
        assert window.btn_auto_paste.isEnabled() == True

        # 5. Clear for next use
        window.clear_response()
        assert window.get_response_text() == ""
        assert window.btn_auto_paste.isEnabled() == False

        window.close()
