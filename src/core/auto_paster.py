"""
Auto-Paster - Paste text to active window

Handles:
  - Capturing active window handle
  - Simulating keyboard input (Ctrl+V)
  - Focus restoration with configurable delay
  - Error handling for various window states
"""

import ctypes
import time
import logging
from typing import Optional
import keyboard

logger = logging.getLogger(__name__)


class AutoPaster:
    """Paste text to the active window."""

    def __init__(self, delay_ms: int = 100):
        """
        Initialize AutoPaster.

        Args:
            delay_ms: Delay in milliseconds after paste before restoring focus
        """
        self.delay_ms = delay_ms

    def paste_to_active_window(self, text: str) -> bool:
        """
        Paste text to the active window.

        Steps:
        1. Save current active window handle
        2. Copy text to clipboard
        3. Send Ctrl+V to paste
        4. Restore focus with delay
        5. Restore clipboard (optional)

        Args:
            text: Text to paste

        Returns:
            bool: True if paste succeeded, False otherwise
        """
        try:
            # 1. Get active window handle
            original_window = self._get_active_window()

            # 2. Copy text to clipboard
            self._copy_to_clipboard(text)

            # 3. Small delay to ensure clipboard is updated
            time.sleep(0.05)

            # 4. Send Ctrl+V to paste
            self._paste_via_keyboard()

            # 5. Wait configured delay
            time.sleep(self.delay_ms / 1000.0)

            # 6. Restore focus if we have original window
            if original_window:
                self._restore_focus(original_window)

            logger.info(f"Auto-paste succeeded ({len(text)} chars)")
            return True

        except Exception as e:
            logger.error(f"Auto-paste failed: {e}", exc_info=True)
            return False

    def _get_active_window(self) -> Optional[int]:
        """
        Get the handle of the active window.

        Returns:
            Window handle or None
        """
        try:
            # Get foreground window handle
            user32 = ctypes.windll.user32
            window_handle = user32.GetForegroundWindow()

            if window_handle:
                logger.debug(f"Got active window handle: {window_handle}")
                return window_handle
            return None

        except Exception as e:
            logger.warning(f"Could not get active window: {e}")
            return None

    def _copy_to_clipboard(self, text: str):
        """
        Copy text to clipboard using Windows API.

        Args:
            text: Text to copy
        """
        try:
            from PySide6.QtWidgets import QApplication
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            logger.debug(f"Text copied to clipboard ({len(text)} chars)")

        except Exception as e:
            logger.error(f"Failed to copy to clipboard: {e}")
            raise

    def _paste_via_keyboard(self):
        """
        Send Ctrl+V to paste from clipboard.
        """
        try:
            # Send Ctrl+V using keyboard library
            keyboard.send('ctrl+v')

            logger.debug("Ctrl+V sent to active window")

        except Exception as e:
            logger.error(f"Failed to send Ctrl+V: {e}")
            raise

    def _restore_focus(self, window_handle: int):
        """
        Restore focus to original window.

        Args:
            window_handle: Window handle to restore focus to
        """
        try:
            user32 = ctypes.windll.user32

            # Set focus to original window
            result = user32.SetForegroundWindow(window_handle)

            if result:
                logger.debug(f"Focus restored to window {window_handle}")
            else:
                logger.warning(f"Could not restore focus to window {window_handle}")

        except Exception as e:
            logger.warning(f"Error restoring focus: {e}")
            # Don't raise - this is non-critical


# Singleton instance
_instance: Optional[AutoPaster] = None


def get_auto_paster(delay_ms: int = 100) -> AutoPaster:
    """Get or create AutoPaster singleton instance."""
    global _instance
    if _instance is None:
        _instance = AutoPaster(delay_ms)
    return _instance
