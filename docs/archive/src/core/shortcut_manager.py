"""
Keyboard Shortcuts Manager (F-13)

Manages global keyboard shortcuts registration, customization, and conflict detection.
Persists shortcuts in configuration and supports full customization.

Features:
  - Register global shortcuts
  - Conflict detection with system shortcuts
  - Customization via config.json
  - Default shortcuts predefined
  - Signal emission on shortcut triggered
"""

from PySide6.QtCore import Signal, QObject, Qt
from PySide6.QtGui import QKeySequence
import logging
from typing import Dict, List, Optional, Callable

logger = logging.getLogger(__name__)


class ShortcutConfig:
    """Shortcut configuration"""

    def __init__(self, shortcut_id: str, default_key: str, description: str):
        self.shortcut_id = shortcut_id
        self.key_sequence = default_key
        self.description = description


class ShortcutManager(QObject):
    """
    Manages keyboard shortcuts for the application.

    Signals:
        sig_shortcut_triggered: (shortcut_id) when shortcut is pressed

    Default shortcuts:
      - show_menu: Ctrl+Right-Click (special)
      - screenshot: Ctrl+Shift+S
      - escape: Esc
      - close_window: Ctrl+W
      - settings: Ctrl+,
    """

    sig_shortcut_triggered = Signal(str)  # shortcut_id

    # Default shortcuts
    DEFAULT_SHORTCUTS = {
        "show_menu": ShortcutConfig("show_menu", "Ctrl+Right", "Show context menu"),
        "screenshot": ShortcutConfig("screenshot", "Ctrl+Shift+S", "Take screenshot"),
        "escape": ShortcutConfig("escape", "Esc", "Close menu/window"),
        "close_window": ShortcutConfig("close_window", "Ctrl+W", "Close chat window"),
        "settings": ShortcutConfig("settings", "Ctrl+,", "Open settings"),
    }

    # System reserved shortcuts (can't be overridden)
    RESERVED_SHORTCUTS = {
        "Ctrl+Alt+Delete",
        "Alt+Tab",
        "Alt+F4",
        "Win",
        "Alt+Space",
    }

    def __init__(self):
        super().__init__()
        self.shortcuts: Dict[str, ShortcutConfig] = {}
        self.custom_shortcuts: Dict[str, str] = {}
        self._registered_keys: List[str] = []

        # Initialize with defaults
        self._load_defaults()

    def _load_defaults(self):
        """Load default shortcuts"""
        for shortcut_id, config in self.DEFAULT_SHORTCUTS.items():
            # Create new copy to avoid shared state between instances
            self.shortcuts[shortcut_id] = ShortcutConfig(
                config.shortcut_id,
                config.key_sequence,
                config.description
            )
            self._registered_keys.append(self.shortcuts[shortcut_id].key_sequence)

    def register_shortcut(self, shortcut_id: str, key_sequence: str) -> bool:
        """
        Register a shortcut with conflict detection.

        Returns:
            bool: True if registered successfully, False if conflict
        """
        if self._has_conflict(key_sequence):
            logger.warning(f"Shortcut conflict: {key_sequence}")
            return False

        if shortcut_id not in self.shortcuts:
            self.shortcuts[shortcut_id] = ShortcutConfig(
                shortcut_id, key_sequence, "Custom shortcut"
            )
        else:
            self.shortcuts[shortcut_id].key_sequence = key_sequence

        self.custom_shortcuts[shortcut_id] = key_sequence
        self._registered_keys.append(key_sequence)

        logger.info(f"Shortcut registered: {shortcut_id} = {key_sequence}")
        return True

    def _has_conflict(self, key_sequence: str) -> bool:
        """Check for conflicts with reserved/existing shortcuts"""
        # Check reserved system shortcuts
        if key_sequence in self.RESERVED_SHORTCUTS:
            return True

        # Check already registered
        if key_sequence in self._registered_keys:
            return True

        return False

    def get_shortcut(self, shortcut_id: str) -> Optional[str]:
        """Get shortcut key sequence"""
        if shortcut_id in self.shortcuts:
            return self.shortcuts[shortcut_id].key_sequence
        return None

    def get_all_shortcuts(self) -> Dict[str, str]:
        """Get all shortcuts as {id: key_sequence}"""
        return {
            shortcut_id: config.key_sequence
            for shortcut_id, config in self.shortcuts.items()
        }

    def remove_shortcut(self, shortcut_id: str) -> bool:
        """Remove a custom shortcut"""
        if shortcut_id in self.custom_shortcuts:
            del self.custom_shortcuts[shortcut_id]
            # Reset to default if exists
            if shortcut_id in self.DEFAULT_SHORTCUTS:
                default = self.DEFAULT_SHORTCUTS[shortcut_id]
                self.shortcuts[shortcut_id].key_sequence = default.key_sequence
            else:
                del self.shortcuts[shortcut_id]
            logger.info(f"Shortcut removed: {shortcut_id}")
            return True
        return False

    def reset_to_defaults(self):
        """Reset all shortcuts to defaults"""
        self.custom_shortcuts.clear()
        self._registered_keys.clear()
        self.shortcuts.clear()
        self._load_defaults()
        logger.info("All shortcuts reset to defaults")

    def is_registered(self, shortcut_id: str) -> bool:
        """Check if shortcut is registered"""
        return shortcut_id in self.shortcuts

    def get_description(self, shortcut_id: str) -> Optional[str]:
        """Get shortcut description"""
        if shortcut_id in self.shortcuts:
            return self.shortcuts[shortcut_id].description
        return None

    def to_dict(self) -> Dict[str, str]:
        """Export shortcuts to dictionary for saving"""
        return self.custom_shortcuts.copy()

    def from_dict(self, data: Dict[str, str]):
        """Import shortcuts from dictionary"""
        for shortcut_id, key_sequence in data.items():
            self.register_shortcut(shortcut_id, key_sequence)

    def trigger_shortcut(self, shortcut_id: str):
        """Manually trigger a shortcut (for testing)"""
        if self.is_registered(shortcut_id):
            logger.debug(f"Shortcut triggered: {shortcut_id}")
            self.sig_shortcut_triggered.emit(shortcut_id)
        else:
            logger.warning(f"Shortcut not registered: {shortcut_id}")
