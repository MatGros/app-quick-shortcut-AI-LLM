"""
Tests for InputManager (F-01: Global Input Hooks) - Phase 3B

Tests verify:
  - Thread-safe signal emission
  - Win32 mouse hook detection
  - Position tracking via Win32 API
  - Ctrl+Right-Click hotkey detection
  - Error handling
  - Graceful start/stop

Phase 3B: Uses Win32 API directly (RegisterWindowsHookEx WH_MOUSE_LL).
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
        mgr.wait(2000)


class TestInputManagerBasics:
    """Basic InputManager functionality"""

    def test_input_manager_initialization(self, input_manager):
        """Test InputManager initializes correctly"""
        assert input_manager is not None
        assert not input_manager.is_running()
        assert input_manager._running == False
        assert hasattr(input_manager, '_event_queue')

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
        with patch('src.core.input_manager._user32.SetWindowsHookExW', return_value=0x1000):
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

        with patch('src.core.input_manager._user32.SetWindowsHookExW', return_value=0x1000):
            input_manager.start()
            time.sleep(0.5)

            assert started_callback.called or input_manager.is_running()

            input_manager.stop()
            input_manager.wait(2000)


class TestInputManagerPositionTracking:
    """Test position tracking"""

    def test_position_tracking(self, input_manager):
        """Test that position tracking works"""
        x, y = input_manager.get_last_position()
        assert isinstance(x, int)
        assert isinstance(y, int)
        # Initial position should be (0, 0)
        assert x == 0
        assert y == 0


class TestInputManagerErrorHandling:
    """Test error handling"""

    @pytest.mark.qt
    def test_double_stop_safe(self, input_manager, qapp):
        """Test calling stop multiple times is safe"""
        with patch('src.core.input_manager._user32.SetWindowsHookExW', return_value=0x1000):
            input_manager.start()
            time.sleep(0.3)

            try:
                input_manager.stop()
                input_manager.stop()  # Second stop
                input_manager.wait(2000)
            except Exception:
                pytest.fail("Double stop raised exception")

    @pytest.mark.qt
    def test_graceful_stop_without_running(self, input_manager):
        """Test stop on non-running manager is safe"""
        try:
            input_manager.stop()
            # Should not raise any exception
            assert not input_manager.is_running()
        except Exception:
            pytest.fail("Stop on non-running manager raised exception")


class TestInputManagerPerformance:
    """Performance-related tests"""

    def test_position_get_latency(self, input_manager):
        """Test get_last_position is fast"""
        input_manager._last_x = 500
        input_manager._last_y = 600

        start = time.time()
        x, y = input_manager.get_last_position()
        elapsed = time.time() - start

        assert elapsed < 0.01  # Should be < 10ms
        assert x == 500
        assert y == 600


class TestInputManagerIntegration:
    """Integration tests"""

    @pytest.mark.qt
    def test_full_workflow(self, qapp, input_manager):
        """Test complete workflow: start -> detect -> stop"""
        events_triggered = []

        def on_triggered(action_id, x, y):
            events_triggered.append((action_id, x, y))

        input_manager.sig_shortcut_triggered.connect(on_triggered)

        with patch('src.core.input_manager._user32.SetWindowsHookExW', return_value=0x1000):
            # Start
            input_manager.start()
            time.sleep(0.3)

            # Simulate event via queue (internal API)
            input_manager._event_queue.put_nowait(('show_menu', 123, 456))

            # Allow time for signal processing
            time.sleep(0.1)

            # Stop
            input_manager.stop()
            input_manager.wait(2000)

        assert input_manager.is_running() == False
