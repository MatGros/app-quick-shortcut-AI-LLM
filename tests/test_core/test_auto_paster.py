"""
Tests for AutoPaster (Task #4)

Tests verify:
  - Clipboard copying
  - Keyboard simulation
  - Window focus handling
  - Error recovery
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from src.core.auto_paster import AutoPaster, get_auto_paster
import time


class TestAutoPasterBasics:
    """Test AutoPaster initialization"""

    def test_auto_paster_creation(self):
        """Test AutoPaster initializes"""
        paster = AutoPaster()
        assert paster is not None
        assert paster.delay_ms == 100

    def test_auto_paster_custom_delay(self):
        """Test AutoPaster with custom delay"""
        paster = AutoPaster(delay_ms=200)
        assert paster.delay_ms == 200




class TestAutoPasterSingleton:
    """Test singleton pattern"""

    def test_get_auto_paster_singleton(self):
        """Test get_auto_paster returns singleton"""
        paster1 = get_auto_paster()
        paster2 = get_auto_paster()

        assert paster1 is paster2

    def test_singleton_different_delays(self):
        """Test singleton ignores delay parameter after first call"""
        # Reset module state
        import src.core.auto_paster as ap
        ap._instance = None

        paster1 = get_auto_paster(delay_ms=100)
        paster2 = get_auto_paster(delay_ms=500)

        # Should still be same instance with original delay
        assert paster1 is paster2
        assert paster1.delay_ms == 100


class TestAutoPasterClipboard:
    """Test clipboard operations"""

    def test_copy_to_clipboard(self):
        """Test copying text to clipboard"""
        paster = AutoPaster()
        text = "Test clipboard content"

        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_clipboard.return_value = mock_cb

            paster._copy_to_clipboard(text)

            mock_cb.setText.assert_called_with(text)

    def test_copy_empty_string(self):
        """Test copying empty string"""
        paster = AutoPaster()

        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_clipboard.return_value = mock_cb

            paster._copy_to_clipboard("")

            mock_cb.setText.assert_called_with("")

    def test_copy_large_text(self):
        """Test copying large text"""
        paster = AutoPaster()
        large_text = "x" * 10000

        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_clipboard.return_value = mock_cb

            paster._copy_to_clipboard(large_text)

            mock_cb.setText.assert_called_with(large_text)


class TestAutoPasterKeyboard:
    """Test keyboard simulation"""

    def test_paste_via_keyboard(self):
        """Test sending Ctrl+V"""
        paster = AutoPaster()

        with patch('src.core.auto_paster.keyboard.send') as mock_send:
            paster._paste_via_keyboard()

            # Should have called send with 'ctrl+v'
            assert mock_send.called
            mock_send.assert_called_once_with('ctrl+v')

    def test_keyboard_sequence(self):
        """Test correct keyboard sequence for Ctrl+V"""
        paster = AutoPaster()

        with patch('src.core.auto_paster.keyboard.send') as mock_send:
            paster._paste_via_keyboard()

            # Verify send was called
            assert mock_send.call_count == 1
            mock_send.assert_called_with('ctrl+v')


class TestAutoPasterWindowFocus:
    """Test window focus handling"""

    def test_get_active_window(self):
        """Test getting active window handle"""
        paster = AutoPaster()

        with patch('ctypes.windll.user32') as mock_user32:
            mock_user32.GetForegroundWindow.return_value = 12345

            handle = paster._get_active_window()

            assert handle == 12345
            mock_user32.GetForegroundWindow.assert_called_once()

    def test_get_active_window_none(self):
        """Test get_active_window handles no window"""
        paster = AutoPaster()

        with patch('ctypes.windll.user32') as mock_user32:
            mock_user32.GetForegroundWindow.return_value = None

            handle = paster._get_active_window()

            assert handle is None

    def test_restore_focus(self):
        """Test restoring focus to window"""
        paster = AutoPaster()

        with patch('ctypes.windll.user32') as mock_user32:
            mock_user32.SetForegroundWindow.return_value = True

            paster._restore_focus(12345)

            mock_user32.SetForegroundWindow.assert_called_with(12345)

    def test_restore_focus_failure_handled(self):
        """Test restore focus failure is handled gracefully"""
        paster = AutoPaster()

        with patch('ctypes.windll.user32') as mock_user32:
            mock_user32.SetForegroundWindow.return_value = False

            # Should not raise
            paster._restore_focus(99999)


class TestAutoPasterIntegration:
    """Test full paste workflow"""

    def test_paste_to_active_window_success(self):
        """Test successful paste to active window"""
        paster = AutoPaster()
        text = "Test content"

        with patch.object(paster, '_get_active_window') as mock_get_window, \
             patch.object(paster, '_copy_to_clipboard') as mock_copy, \
             patch.object(paster, '_paste_via_keyboard') as mock_paste, \
             patch.object(paster, '_restore_focus') as mock_restore:

            mock_get_window.return_value = 12345

            result = paster.paste_to_active_window(text)

            assert result == True
            mock_get_window.assert_called_once()
            mock_copy.assert_called_once_with(text)
            mock_paste.assert_called_once()
            mock_restore.assert_called_once_with(12345)

    def test_paste_to_active_window_no_original_window(self):
        """Test paste when original window cannot be determined"""
        paster = AutoPaster()
        text = "Test content"

        with patch.object(paster, '_get_active_window') as mock_get_window, \
             patch.object(paster, '_copy_to_clipboard') as mock_copy, \
             patch.object(paster, '_paste_via_keyboard') as mock_paste, \
             patch.object(paster, '_restore_focus') as mock_restore:

            mock_get_window.return_value = None

            result = paster.paste_to_active_window(text)

            assert result == True
            mock_copy.assert_called_once()
            mock_paste.assert_called_once()
            # restore_focus should not be called if no window
            mock_restore.assert_not_called()

    def test_paste_handles_clipboard_error(self):
        """Test paste handles clipboard errors gracefully"""
        paster = AutoPaster()

        with patch.object(paster, '_copy_to_clipboard') as mock_copy:
            mock_copy.side_effect = Exception("Clipboard error")

            result = paster.paste_to_active_window("text")

            assert result == False

    def test_paste_handles_keyboard_error(self):
        """Test paste handles keyboard errors gracefully"""
        paster = AutoPaster()

        with patch.object(paster, '_get_active_window'), \
             patch.object(paster, '_copy_to_clipboard'), \
             patch.object(paster, '_paste_via_keyboard') as mock_paste:

            mock_paste.side_effect = Exception("Keyboard error")

            result = paster.paste_to_active_window("text")

            assert result == False

    def test_paste_empty_text(self):
        """Test paste with empty text"""
        paster = AutoPaster()

        with patch.object(paster, '_get_active_window') as mock_get_window, \
             patch.object(paster, '_copy_to_clipboard') as mock_copy:

            mock_get_window.return_value = 12345

            # Empty text should still attempt paste
            result = paster.paste_to_active_window("")

            # Should still succeed (caller's responsibility to validate)
            assert result == True
            mock_copy.assert_called_once_with("")

    def test_paste_with_special_characters(self):
        """Test paste with special characters"""
        paster = AutoPaster()
        text = "Test with special chars: !@#$%^&*()\nNewline\tTab"

        with patch.object(paster, '_get_active_window') as mock_get_window, \
             patch.object(paster, '_copy_to_clipboard') as mock_copy, \
             patch.object(paster, '_paste_via_keyboard') as mock_paste:

            mock_get_window.return_value = 12345

            result = paster.paste_to_active_window(text)

            assert result == True
            mock_copy.assert_called_once_with(text)

    def test_paste_delay_applied(self):
        """Test that configured delay is respected"""
        paster = AutoPaster(delay_ms=50)

        with patch.object(paster, '_get_active_window') as mock_get_window, \
             patch.object(paster, '_copy_to_clipboard'), \
             patch.object(paster, '_paste_via_keyboard'), \
             patch.object(paster, '_restore_focus'), \
             patch('time.sleep') as mock_sleep:

            mock_get_window.return_value = 12345

            result = paster.paste_to_active_window("text")

            assert result == True
            # Should have called sleep with delay
            sleep_calls = [call[0][0] for call in mock_sleep.call_args_list]
            # Should have at least the configured delay call
            assert any(delay >= 0.05 for delay in sleep_calls)
