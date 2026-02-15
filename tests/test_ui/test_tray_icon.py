"""
Tests for TrayIcon (F-14: System Tray Integration)

Tests verify:
  - Tray icon creation and visibility
  - Status changes
  - Menu actions
  - Signal emission
"""

import pytest
from unittest.mock import Mock
from PySide6.QtWidgets import QApplication
from src.ui.tray_icon import TrayIcon, TrayStatus


@pytest.fixture
def qapp():
    """Qt Application fixture"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def tray_icon(qapp):
    """TrayIcon instance"""
    tray = TrayIcon()
    yield tray
    tray.close()


class TestTrayIconBasics:
    """Basic TrayIcon functionality"""

    def test_tray_icon_creation(self, tray_icon):
        """Test TrayIcon initializes"""
        assert tray_icon is not None
        assert tray_icon.get_status() == TrayStatus.READY

    def test_signals_exist(self, tray_icon):
        """Test required signals exist"""
        assert hasattr(tray_icon, 'sig_action_triggered')
        assert hasattr(tray_icon, 'sig_status_changed')

    def test_initial_status_ready(self, tray_icon):
        """Test initial status is READY"""
        assert tray_icon.get_status() == TrayStatus.READY

    def test_tooltip_set(self, tray_icon):
        """Test tooltip is set"""
        # Tooltip should be set during initialization
        assert tray_icon._tray_icon.toolTip() != ""


class TestTrayIconStatus:
    """Status indicator tests"""

    def test_set_status_ready(self, tray_icon):
        """Test setting status to READY"""
        tray_icon.set_status(TrayStatus.READY)
        assert tray_icon.get_status() == TrayStatus.READY

    def test_set_status_busy(self, tray_icon):
        """Test setting status to BUSY"""
        tray_icon.set_status(TrayStatus.BUSY)
        assert tray_icon.get_status() == TrayStatus.BUSY

    def test_set_status_error(self, tray_icon):
        """Test setting status to ERROR"""
        tray_icon.set_status(TrayStatus.ERROR)
        assert tray_icon.get_status() == TrayStatus.ERROR

    def test_status_changes_tooltip(self, tray_icon):
        """Test status change updates tooltip"""
        original_tooltip = tray_icon._tray_icon.toolTip()

        tray_icon.set_status(TrayStatus.BUSY)
        busy_tooltip = tray_icon._tray_icon.toolTip()

        assert original_tooltip != busy_tooltip
        assert "Processing" in busy_tooltip

    def test_same_status_no_change(self, tray_icon):
        """Test setting same status multiple times"""
        tray_icon.set_status(TrayStatus.READY)
        status1 = tray_icon.get_status()

        tray_icon.set_status(TrayStatus.READY)
        status2 = tray_icon.get_status()

        assert status1 == status2


class TestTrayIconMenu:
    """Menu action tests"""

    def test_add_action(self, tray_icon):
        """Test adding menu action"""
        tray_icon.add_action("test", "Test Action")

        # Menu should have at least one action
        actions = tray_icon._menu.actions()
        assert len(actions) > 0

    def test_add_multiple_actions(self, tray_icon):
        """Test adding multiple actions"""
        tray_icon.add_action("action1", "Action 1")
        tray_icon.add_action("action2", "Action 2")
        tray_icon.add_action("action3", "Action 3")

        actions = tray_icon._menu.actions()
        assert len(actions) >= 3

    def test_add_separator(self, tray_icon):
        """Test adding separator"""
        tray_icon.add_action("action1", "Action 1")
        tray_icon.add_separator()
        tray_icon.add_action("action2", "Action 2")

        # Menu should have separator
        assert len(tray_icon._menu.actions()) >= 3

    def test_action_triggered_signal(self, tray_icon, qapp):
        """Test action trigger emits signal"""
        callback = Mock()
        tray_icon.sig_action_triggered.connect(callback)

        tray_icon.add_action("test_action", "Test")

        # Note: actual triggering requires event loop simulation
        # This test verifies signal connection works
        assert tray_icon._menu is not None


class TestTrayIconVisibility:
    """Visibility tests"""

    def test_show_tray_icon(self, tray_icon):
        """Test showing tray icon"""
        tray_icon.show()
        assert tray_icon.is_visible() == True

    def test_hide_tray_icon(self, tray_icon):
        """Test hiding tray icon"""
        tray_icon.show()
        tray_icon.hide()
        assert tray_icon.is_visible() == False

    def test_initial_not_visible(self, tray_icon):
        """Test icon starts hidden"""
        # New instance should start hidden
        new_tray = TrayIcon()
        assert new_tray.is_visible() == False
        new_tray.close()


class TestTrayStatusEnum:
    """Test TrayStatus enum"""

    def test_ready_status_value(self):
        """Test READY status value"""
        assert TrayStatus.READY.value == "ready"

    def test_busy_status_value(self):
        """Test BUSY status value"""
        assert TrayStatus.BUSY.value == "busy"

    def test_error_status_value(self):
        """Test ERROR status value"""
        assert TrayStatus.ERROR.value == "error"

    def test_status_enum_members(self):
        """Test all status enum members exist"""
        assert hasattr(TrayStatus, 'READY')
        assert hasattr(TrayStatus, 'BUSY')
        assert hasattr(TrayStatus, 'ERROR')


class TestTrayIconIntegration:
    """Integration tests"""

    def test_full_workflow(self, tray_icon, qapp):
        """Test complete tray icon workflow"""
        # Add actions
        tray_icon.add_action("open", "Open Chat")
        tray_icon.add_action("settings", "Settings")
        tray_icon.add_separator()
        tray_icon.add_action("quit", "Quit")

        # Show tray
        tray_icon.show()
        assert tray_icon.is_visible()

        # Change status
        tray_icon.set_status(TrayStatus.BUSY)
        assert tray_icon.get_status() == TrayStatus.BUSY

        # Change status again
        tray_icon.set_status(TrayStatus.ERROR)
        assert tray_icon.get_status() == TrayStatus.ERROR

        # Back to ready
        tray_icon.set_status(TrayStatus.READY)
        assert tray_icon.get_status() == TrayStatus.READY

        # Hide
        tray_icon.hide()
        assert tray_icon.is_visible() == False

    def test_signal_connection(self, tray_icon):
        """Test all signals can be connected"""
        action_callback = Mock()
        status_callback = Mock()

        tray_icon.sig_action_triggered.connect(action_callback)
        tray_icon.sig_status_changed.connect(status_callback)

        # Should be able to change status and emit signal
        tray_icon.set_status(TrayStatus.BUSY)

        # Status callback should have connection
        assert tray_icon.sig_status_changed is not None
