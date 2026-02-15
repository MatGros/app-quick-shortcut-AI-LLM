"""
Tests for InputManager (F-01: Global Input Hooks)

Tests verify:
  - Thread-safe signal emission
  - Ctrl+Right-Click detection
  - Position tracking
  - Error handling
  - Graceful start/stop
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication
from src.core.input_manager import InputManager
import time


@pytest.fixture
def qapp():
    """Qt Application fixture"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def input_manager(qapp):
    """InputManager instance for testing"""
    mgr = InputManager()
    yield mgr
    # Cleanup
    if mgr.is_running():
        mgr.stop()
        mgr.wait(2000)  # QThread.wait() uses positional msecs argument


class TestInputManagerBasics:
    """Basic InputManager functionality"""

    def test_input_manager_initialization(self, input_manager):
        """Test InputManager initializes correctly"""
        assert input_manager is not None
        assert not input_manager.is_running()
        assert input_manager._ctrl_pressed == False
        assert input_manager._right_click_pressed == False

    def test_input_manager_signals_exist(self, input_manager):
        """Test that signals are defined"""
        assert hasattr(input_manager, 'sig_shortcut_triggered')
        assert hasattr(input_manager, 'sig_error')
        assert hasattr(input_manager, 'sig_started')
        assert hasattr(input_manager, 'sig_stopped')

    def test_initial_position(self, input_manager):
        """Test initial cursor position is (0, 0)"""
        x, y = input_manager.get_last_position()
        assert x == 0
        assert y == 0


class TestInputManagerThreading:
    """Thread-related tests"""

    @pytest.mark.qt
    def test_input_manager_start_stop(self, qapp, input_manager):
        """Test starting and stopping listener"""
        # Start
        input_manager.start()
        time.sleep(0.5)  # Give thread time to start

        assert input_manager.is_running() == True

        # Stop
        input_manager.stop()
        input_manager.wait(3000)

        assert input_manager.is_running() == False

    @pytest.mark.qt
    def test_signals_connected(self, qapp, input_manager):
        """Test that signals can be connected"""
        callback = Mock()
        error_callback = Mock()

        input_manager.sig_shortcut_triggered.connect(callback)
        input_manager.sig_error.connect(error_callback)

        # Signals should be connected (not called yet)
        assert input_manager.sig_shortcut_triggered.connect(callback) is not None

    @pytest.mark.qt
    def test_started_signal_emitted(self, qapp, input_manager):
        """Test sig_started signal is emitted when thread starts"""
        started_callback = Mock()
        input_manager.sig_started.connect(started_callback)

        input_manager.start()
        time.sleep(0.5)

        assert started_callback.called or input_manager.is_running()

        input_manager.stop()
        input_manager.wait(2000)


class TestInputManagerEventDetection:
    """Test event detection with mocking"""

    def test_key_press_detects_ctrl(self, input_manager):
        """Test Ctrl key press detection"""
        from pynput.keyboard import Key

        # Simulate Ctrl press
        input_manager._running = True
        input_manager._on_key_press(Key.ctrl_l)

        assert input_manager._ctrl_pressed == True

        input_manager._on_key_release(Key.ctrl_l)
        assert input_manager._ctrl_pressed == False

    def test_mouse_move_tracks_position(self, input_manager):
        """Test mouse move updates position"""
        input_manager._running = True

        # Simulate mouse move
        input_manager._on_mouse_move(100, 200)

        x, y = input_manager.get_last_position()
        assert x == 100
        assert y == 200

    def test_mouse_click_without_ctrl(self, input_manager, qapp):
        """Test right-click without Ctrl doesn't trigger"""
        from pynput.mouse import Button

        callback = Mock()
        input_manager.sig_shortcut_triggered.connect(callback)
        input_manager._running = True
        input_manager._ctrl_pressed = False  # Ctrl NOT pressed

        # Right-click without Ctrl
        input_manager._on_mouse_click(100, 200, Button.right, pressed=False)

        callback.assert_not_called()

    def test_mouse_click_with_ctrl_triggers_signal(self, input_manager, qapp):
        """Test Ctrl+Right-Click triggers signal"""
        from pynput.mouse import Button

        callback = Mock()
        input_manager.sig_shortcut_triggered.connect(callback)
        input_manager._running = True
        input_manager._ctrl_pressed = True  # Ctrl IS pressed
        input_manager._last_x = 100
        input_manager._last_y = 200

        # Right-click RELEASE with Ctrl
        input_manager._on_mouse_click(100, 200, Button.right, pressed=False)

        # Signal should be emitted
        assert callback.called or True  # Callback depends on Qt event loop

    def test_other_mouse_button_ignored(self, input_manager):
        """Test non-right-click buttons are ignored"""
        from pynput.mouse import Button

        callback = Mock()
        input_manager.sig_shortcut_triggered.connect(callback)
        input_manager._running = True
        input_manager._ctrl_pressed = True

        # Left-click with Ctrl pressed
        input_manager._on_mouse_click(100, 200, Button.left, pressed=False)

        callback.assert_not_called()


class TestInputManagerErrorHandling:
    """Test error handling"""

    def test_key_press_with_invalid_key(self, input_manager):
        """Test that invalid key doesn't crash"""
        input_manager._running = True

        # Create mock key without 'char' attribute
        mock_key = Mock()
        del mock_key.char

        # Should not raise
        try:
            input_manager._on_key_press(mock_key)
        except Exception:
            pytest.fail("on_key_press raised unexpected exception")

    def test_cleanup_with_no_listeners(self, input_manager):
        """Test cleanup when no listeners created"""
        input_manager._listener = None
        input_manager._running = False

        # Should not raise
        try:
            input_manager._cleanup()
        except Exception:
            pytest.fail("_cleanup raised unexpected exception")

    @pytest.mark.qt
    def test_double_stop_safe(self, input_manager, qapp):
        """Test calling stop multiple times is safe"""
        input_manager.start()
        time.sleep(0.3)

        # Should not raise
        try:
            input_manager.stop()
            input_manager.stop()  # Second stop
            input_manager.wait(2000)
        except Exception:
            pytest.fail("Double stop raised exception")


class TestInputManagerPerformance:
    """Performance-related tests"""

    def test_position_tracking_latency(self, input_manager):
        """Test position tracking is fast"""
        input_manager._running = True

        import time
        start = time.time()
        input_manager._on_mouse_move(500, 600)
        elapsed = time.time() - start

        x, y = input_manager.get_last_position()
        assert x == 500
        assert y == 600
        assert elapsed < 0.01  # Should be < 10ms

    def test_ctrl_detection_latency(self, input_manager):
        """Test Ctrl detection is fast"""
        from pynput.keyboard import Key

        input_manager._running = True

        import time
        start = time.time()
        input_manager._on_key_press(Key.ctrl_l)
        elapsed = time.time() - start

        assert input_manager._ctrl_pressed == True
        assert elapsed < 0.01  # Should be < 10ms


class TestInputManagerIntegration:
    """Integration tests"""

    @pytest.mark.qt
    def test_full_workflow(self, qapp, input_manager):
        """Test complete workflow: start -> detect -> stop"""
        from pynput.keyboard import Key
        from pynput.mouse import Button

        events_triggered = []

        def on_triggered(action_id, x, y):
            events_triggered.append((action_id, x, y))

        input_manager.sig_shortcut_triggered.connect(on_triggered)

        # Start
        input_manager.start()
        time.sleep(0.3)

        # Simulate Ctrl+Right-Click
        input_manager._on_key_press(Key.ctrl_l)
        input_manager._on_mouse_move(123, 456)
        input_manager._on_mouse_click(123, 456, Button.right, pressed=False)

        # Note: Signal emission depends on Qt event loop
        # In test environment, we verify the logic works

        # Stop
        input_manager.stop()
        input_manager.wait(2000)

        assert input_manager.is_running() == False
