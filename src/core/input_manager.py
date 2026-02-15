"""
Global Input Manager - Keyboard/Mouse Hooks

Handles Ctrl+Right-Click detection globally across Windows without blocking the UI.
Uses pynput library in a separate QThread for non-blocking event capture.

Features:
  - Global Ctrl+Right-Click detection
  - Signal-based event emission (thread-safe via Qt signals)
  - Graceful start/stop without thread blocking
  - Position tracking (x, y coordinates)
"""

from PySide6.QtCore import QThread, Signal, QObject
from pynput import mouse, keyboard
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class InputManagerSignals(QObject):
    """
    Signals for InputManager (must be in QObject for Qt to work)

    Signals:
        sig_shortcut_triggered: (action_id, x, y) when Ctrl+Right-Click detected
        sig_error: (error_message) on exception
    """
    sig_shortcut_triggered = Signal(str, int, int)  # action_id, x, y
    sig_error = Signal(str)


class InputManager(QThread):
    """
    Global input hook listener running in separate thread.

    Detects Ctrl+Right-Click and emits signal to main thread.
    Non-blocking - runs in background QThread.

    Usage:
        input_mgr = InputManager()
        input_mgr.sig_shortcut_triggered.connect(on_shortcut_triggered)
        input_mgr.start()

        # Later:
        input_mgr.stop()
        input_mgr.wait()  # Wait for thread to finish
    """

    # Signals (must be defined at class level)
    sig_shortcut_triggered = Signal(str, int, int)  # action_id, x, y
    sig_error = Signal(str)
    sig_started = Signal()
    sig_stopped = Signal()

    def __init__(self):
        super().__init__()
        self._running = False
        self._listener = None
        self._ctrl_pressed = False
        self._right_click_pressed = False

        # Store cursor position
        self._last_x = 0
        self._last_y = 0

    def run(self):
        """
        Main thread loop - listen for keyboard/mouse events.
        Called when thread starts.
        """
        try:
            self._running = True
            logger.info("InputManager: Starting keyboard/mouse listener")

            # Create listener for mouse
            self._listener = mouse.Listener(
                on_click=self._on_mouse_click,
                on_move=self._on_mouse_move
            )
            self._listener.start()

            # Create listener for keyboard
            self._kb_listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self._kb_listener.start()

            self.sig_started.emit()
            logger.info("InputManager: Listeners started")

            # Keep thread alive
            while self._running:
                self.msleep(100)  # Check every 100ms if we should stop

        except Exception as e:
            error_msg = f"InputManager error: {str(e)}"
            logger.error(error_msg)
            self.sig_error.emit(error_msg)
        finally:
            self._cleanup()

    def _on_mouse_move(self, x: int, y: int):
        """Track cursor position"""
        self._last_x = x
        self._last_y = y

    def _on_mouse_click(self, x: int, y: int, button, pressed: bool):
        """
        Handle mouse click events.

        Detect right-click (button 3) when Ctrl is pressed.
        """
        if not self._running:
            return

        try:
            # Right-click is button 3 (Button.right)
            if button == mouse.Button.right:
                self._right_click_pressed = pressed

                # On RIGHT-CLICK RELEASE with CTRL pressed
                if not pressed and self._ctrl_pressed:
                    logger.debug(f"Ctrl+Right-Click at ({x}, {y})")
                    self.sig_shortcut_triggered.emit("show_menu", x, y)

        except Exception as e:
            logger.error(f"Mouse click handler error: {e}")

    def _on_key_press(self, key):
        """Handle keyboard key press"""
        if not self._running:
            return

        try:
            # Detect Ctrl (left or right)
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self._ctrl_pressed = True
        except AttributeError:
            # key.char might not exist for special keys
            pass
        except Exception as e:
            logger.error(f"Key press handler error: {e}")

    def _on_key_release(self, key):
        """Handle keyboard key release"""
        if not self._running:
            return

        try:
            # Detect Ctrl release
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self._ctrl_pressed = False
        except AttributeError:
            pass
        except Exception as e:
            logger.error(f"Key release handler error: {e}")

    def stop(self):
        """
        Stop listening and cleanup.

        Call this before exiting application.
        """
        logger.info("InputManager: Stopping listener")
        self._running = False

    def _cleanup(self):
        """Clean up listeners"""
        try:
            if self._listener:
                self._listener.stop()
            if hasattr(self, '_kb_listener') and self._kb_listener:
                self._kb_listener.stop()
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
        finally:
            self.sig_stopped.emit()
            logger.info("InputManager: Stopped")

    def get_last_position(self) -> tuple[int, int]:
        """Get last known cursor position"""
        return (self._last_x, self._last_y)

    def is_running(self) -> bool:
        """Check if listener is active"""
        return self._running


# Test function
if __name__ == "__main__":
    """Quick test - Ctrl+Right-Click 3 times then exit"""
    from PySide6.QtWidgets import QApplication
    from PySide6.QtCore import QTimer
    import sys

    logging.basicConfig(level=logging.DEBUG)

    app = QApplication(sys.argv)

    mgr = InputManager()

    def on_triggered(action_id: str, x: int, y: int):
        print(f"[TEST] Triggered: {action_id} at ({x}, {y})")

    def on_error(msg: str):
        print(f"[TEST] Error: {msg}")

    mgr.sig_shortcut_triggered.connect(on_triggered)
    mgr.sig_error.connect(on_error)
    mgr.start()

    print("InputManager test started. Try Ctrl+Right-Click 3 times...")
    print("(Test will auto-exit after 30 seconds)")

    def on_timeout():
        print("Test timeout - exiting")
        mgr.stop()
        mgr.wait()
        app.quit()

    timer = QTimer()
    timer.timeout.connect(on_timeout)
    timer.start(30000)  # 30 second timeout

    sys.exit(app.exec())
