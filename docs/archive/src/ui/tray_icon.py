"""
System Tray Icon Integration (F-14)

Manages system tray icon with status indicators and context menu.
Shows application status (Ready, Busy, Error) via icon color.

Features:
  - System tray integration
  - Status indicators (green/yellow/red)
  - Context menu with actions
  - Tooltip with current status
  - Signal emission for menu actions
"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QIcon, QColor, QPixmap
import logging
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)


class TrayStatus(Enum):
    """Tray icon status states"""
    READY = "ready"      # Green
    BUSY = "busy"        # Yellow
    ERROR = "error"      # Red


class TrayIcon(QObject):
    """
    System tray icon manager.

    Manages application tray icon with status indicators and context menu.
    Shows Ready (green), Busy (yellow), or Error (red) status.

    Signals:
        sig_action_triggered: (action_id) when menu item clicked
        sig_status_changed: (status) when status changes

    Usage:
        tray = TrayIcon()
        tray.set_status(TrayStatus.READY)
        tray.add_action("open", "Open Chat")
        tray.show()
    """

    sig_action_triggered = Signal(str)  # action_id
    sig_status_changed = Signal(str)    # status name

    def __init__(self):
        super().__init__()

        app = QApplication.instance()
        if app is None:
            raise RuntimeError("TrayIcon requires QApplication instance")

        self._app = app
        self._tray_icon = QSystemTrayIcon(app)
        self._menu = QMenu()
        self._tray_icon.setContextMenu(self._menu)

        self._status = TrayStatus.READY
        self._actions_map = {}

        # Create menu connections
        self._menu.triggered.connect(self._on_menu_action)

        # Create default icon and tooltip
        self._update_icon()
        self._update_tooltip()

        logger.info("TrayIcon initialized")

    def set_status(self, status: TrayStatus):
        """Set tray icon status (changes color)"""
        if self._status != status:
            self._status = status
            self._update_icon()
            self._update_tooltip()
            self.sig_status_changed.emit(status.value)
            logger.info(f"Tray status: {status.value}")

    def get_status(self) -> TrayStatus:
        """Get current tray status"""
        return self._status

    def _update_icon(self):
        """Update tray icon based on current status"""
        icon = self._create_status_icon(self._status)
        self._tray_icon.setIcon(icon)

    def _create_status_icon(self, status: TrayStatus) -> QIcon:
        """Create icon with status color"""
        # Create 32x32 pixel icon
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)

        # Choose color based on status
        if status == TrayStatus.READY:
            color = QColor(0, 200, 0)  # Green
        elif status == TrayStatus.BUSY:
            color = QColor(255, 200, 0)  # Yellow
        elif status == TrayStatus.ERROR:
            color = QColor(255, 0, 0)  # Red
        else:
            color = QColor(128, 128, 128)  # Gray fallback

        # Fill with color
        pixmap.fill(color)

        return QIcon(pixmap)

    def _update_tooltip(self):
        """Update tooltip text"""
        status_text = {
            TrayStatus.READY: "Quick Shortcut AI - Ready",
            TrayStatus.BUSY: "Quick Shortcut AI - Processing...",
            TrayStatus.ERROR: "Quick Shortcut AI - Error",
        }

        tooltip = status_text.get(self._status, "Quick Shortcut AI")
        self._tray_icon.setToolTip(tooltip)

    def add_action(self, action_id: str, label: str):
        """Add action to tray menu"""
        action = self._menu.addAction(label)
        self._actions_map[action] = action_id
        logger.info(f"Tray action added: {action_id}")

    def add_separator(self):
        """Add separator to tray menu"""
        self._menu.addSeparator()

    def _on_menu_action(self, action):
        """Handle menu action triggered"""
        action_id = self._actions_map.get(action)
        if action_id:
            logger.info(f"Tray action triggered: {action_id}")
            self.sig_action_triggered.emit(action_id)

    def show(self):
        """Show tray icon"""
        self._tray_icon.show()
        logger.info("Tray icon shown")

    def hide(self):
        """Hide tray icon"""
        self._tray_icon.hide()
        logger.info("Tray icon hidden")

    def is_visible(self) -> bool:
        """Check if tray icon is visible"""
        return self._tray_icon.isVisible()

    def close(self):
        """Close tray icon"""
        self._tray_icon.hide()


# Test/Demo
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    # Create and show tray
    tray = TrayIcon()

    # Add actions
    tray.add_action("open", "Open Chat")
    tray.add_action("screenshot", "Take Screenshot")
    tray.add_separator()
    tray.add_action("settings", "Settings")
    tray.add_action("quit", "Quit")

    def on_action(action_id):
        print(f"Action: {action_id}")

    tray.sig_action_triggered.connect(on_action)

    # Show with different statuses
    tray.set_status(TrayStatus.READY)
    tray.show()

    print("TrayIcon demo - Right-click on tray icon to see menu")
    print("Status will cycle: Ready (green) -> Busy (yellow) -> Error (red)")

    # Simulate status changes
    from PySide6.QtCore import QTimer

    def cycle_status():
        if tray.get_status() == TrayStatus.READY:
            tray.set_status(TrayStatus.BUSY)
        elif tray.get_status() == TrayStatus.BUSY:
            tray.set_status(TrayStatus.ERROR)
        else:
            tray.set_status(TrayStatus.READY)

    timer = QTimer()
    timer.timeout.connect(cycle_status)
    timer.start(3000)  # Change every 3 seconds

    sys.exit(app.exec())
