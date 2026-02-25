"""
Floating Context Menu - Modern Frameless UI Component

A sleek, modern context menu that appears at cursor position with animations,
keyboard navigation, and smart positioning to avoid going off-screen.

Features:
  - Frameless design with rounded corners and shadow
  - Fade-in animation (200ms)
  - Keyboard navigation (arrow keys, Enter, Esc)
  - Smart positioning (multi-monitor aware)
  - Custom actions with icons
  - Accessible and responsive
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QGraphicsDropShadowEffect,
    QApplication
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, Signal, QRect, QSize
from PySide6.QtGui import QColor, QFont, QPalette, QIcon, QCursor, QScreen
import logging
from typing import List, Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class MenuAction:
    """Represents a menu action/item"""

    def __init__(self, action_id: str, label: str, icon: Optional[QIcon] = None):
        self.action_id = action_id
        self.label = label
        self.icon = icon


class MenuItem(QLabel):
    """Individual menu item widget - fully clickable"""

    clicked = Signal()  # Emitted when item is clicked

    def __init__(self, action: MenuAction, parent=None):
        super().__init__(parent)
        self.action = action
        self.is_selected = False

        # Text setup
        self.setText(f"  {action.label}")
        self.setMinimumHeight(40)
        self.setCursor(Qt.PointingHandCursor)

        # Enable mouse events
        self.setAttribute(Qt.WA_Hover)

        # Font
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        # Colors
        self._update_colors()

    def _update_colors(self):
        """Update colors based on selection state"""
        if self.is_selected:
            # Highlight color when selected - bright blue background, white text
            self.setStyleSheet("""
                MenuItem {
                    background-color: #0066ff;
                    color: #ffffff;
                    padding: 8px 12px;
                    border-radius: 4px;
                    font-weight: bold;
                }
            """)
        else:
            # Normal text color - light gray on dark background
            self.setStyleSheet("""
                MenuItem {
                    background-color: transparent;
                    color: #e0e0e0;
                    padding: 8px 12px;
                    border-radius: 4px;
                }
            """)

    def set_selected(self, selected: bool):
        """Set selection state"""
        self.is_selected = selected
        self._update_colors()

    def mousePressEvent(self, event):
        """Handle click event"""
        if event.button() == Qt.LeftButton:
            logger.debug(f"MenuItem clicked: {self.action.label}")
            self.clicked.emit()
            event.accept() # Stop propagation to parent
        super().mousePressEvent(event)

    def enterEvent(self, event):
        """Handle mouse hover"""
        self.set_selected(True)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handle mouse leave"""
        self.set_selected(False)
        super().leaveEvent(event)


class FloatingMenu(QWidget):
    """
    Modern frameless context menu.

    Shows at cursor position with smooth animations and keyboard navigation.

    Signals:
        sig_action_selected: (action_id) when user selects an action

    Usage:
        menu = FloatingMenu()
        menu.add_action("summarize", "Summarize Text")
        menu.add_action("translate", "Translate to French")
        menu.sig_action_selected.connect(on_action_selected)
        menu.show_at_cursor()
    """

    sig_action_selected = Signal(str)  # action_id
    sig_closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.actions: List[MenuAction] = []
        self.menu_items: List[MenuItem] = []
        self.current_selection = -1

        # Frameless window setup
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)

        # Apply stylesheet for rounding and proper opacity
        self.setStyleSheet("""
            QWidget#FloatingMenuContainer {
                background-color: rgba(35, 35, 35, 245); 
                border: 1px solid #444444;
                border-radius: 8px;
            }
        """)

        # Main container to handle transparency/rounding better
        self.container = QWidget(self)
        self.container.setObjectName("FloatingMenuContainer")
        self.container_layout = QVBoxLayout(self)
        self.container_layout.setContentsMargins(2, 2, 2, 2)
        self.container_layout.addWidget(self.container)

        # Layout inside container
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(4, 4, 4, 4)
        self.layout.setSpacing(2)
        
        self.setMinimumWidth(220)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 150))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)
 
        # Animation setup
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
 
        self.setWindowOpacity(0)

    def add_action(self, action_id: str, label: str, icon: Optional[QIcon] = None):
        """Add an action to the menu"""
        action = MenuAction(action_id, label, icon)
        self.actions.append(action)

        # Create and add menu item
        item = MenuItem(action, self)
        self.menu_items.append(item)
        # Connect item click to action trigger (bind action_id securely)
        item.clicked.connect(lambda a=action_id: self.action_triggered(a))
        self.layout.addWidget(item)

    def show_at_cursor(self):
        """Show menu at current cursor position with animation"""
        cursor_pos = QCursor.pos()
        logger.info(f"FloatingMenu: Showing at {cursor_pos}")

        # Position menu smartly
        self._position_smart(cursor_pos)
        
        # Show and animate
        self.show()
        self.raise_()
        self.activateWindow()
        self.setFocus()
        self.animation.start()

    def focusOutEvent(self, event):
        """Close menu when it loses focus (clicking outside)"""
        logger.debug(f"FloatingMenu: focusOutEvent triggered, reason: {event.reason()}")
        super().focusOutEvent(event)
        # Small delay to allow click on items to register first
        QTimer.singleShot(250, self.close_if_not_active)

    def close_if_not_active(self):
        """Check if we should really close"""
        if not self.isActiveWindow() and self.isVisible():
            logger.info("FloatingMenu: Auto-closing due to focus loss")
            self.close_menu()

    def _position_smart(self, pos: QPoint):
        """
        Smart positioning - avoid going off-screen.

        Considers screen geometry and adjusts menu position if needed.
        """
        # Get menu size
        self.adjustSize()
        menu_size = self.size()

        # Get screen containing the cursor
        screen = self._get_screen_at_point(pos)
        if screen:
            screen_geom = screen.geometry()
        else:
            # Fallback to primary screen
            app = QApplication.instance()
            screen_geom = app.primaryScreen().geometry()

        # Calculate position
        x = pos.x()
        y = pos.y() + 20  # Offset below cursor

        # Adjust if menu goes off right edge
        if x + menu_size.width() > screen_geom.right():
            x = screen_geom.right() - menu_size.width() - 10

        # Adjust if menu goes off bottom
        if y + menu_size.height() > screen_geom.bottom():
            y = screen_geom.bottom() - menu_size.height() - 10

        # Adjust if menu goes off left edge
        if x < screen_geom.left():
            x = screen_geom.left() + 10

        # Adjust if menu goes off top
        if y < screen_geom.top():
            y = screen_geom.top() + 10

        self.move(QPoint(x, y))

    @staticmethod
    def _get_screen_at_point(pos: QPoint) -> Optional[QScreen]:
        """Get screen containing the point"""
        app = QApplication.instance()
        for screen in app.screens():
            if screen.geometry().contains(pos):
                return screen
        return None

    def keyPressEvent(self, event):
        """Handle keyboard navigation"""
        if event.key() == Qt.Key_Escape:
            self.close_menu()

        elif event.key() == Qt.Key_Up:
            self.select_previous()

        elif event.key() == Qt.Key_Down:
            self.select_next()

        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if 0 <= self.current_selection < len(self.actions):
                action_id = self.actions[self.current_selection].action_id
                self.action_triggered(action_id)

        else:
            # Check for letter shortcuts (first letter of action)
            key_text = event.text().upper()
            for i, action in enumerate(self.actions):
                if action.label and action.label[0].upper() == key_text:
                    self.current_selection = i
                    self.update_selection_display()
                    self.action_triggered(action.action_id)
                    return

            super().keyPressEvent(event)

    # mouseMoveEvent and mousePressEvent were redundant and removed to prevent double triggers.
    # Individual MenuItem objects handle their own hover and click events.

    def select_next(self):
        """Select next menu item"""
        if not self.menu_items:
            return

        self.current_selection = (self.current_selection + 1) % len(self.menu_items)
        self.update_selection_display()

    def select_previous(self):
        """Select previous menu item"""
        if not self.menu_items:
            return

        self.current_selection = (self.current_selection - 1) % len(self.menu_items)
        self.update_selection_display()

    def update_selection_display(self):
        """Update visual selection"""
        for i, item in enumerate(self.menu_items):
            item.set_selected(i == self.current_selection)

    def action_triggered(self, action_id: str):
        """Called when an action is selected"""
        logger.info(f"FloatingMenu action triggered: {action_id}")
        self.sig_action_selected.emit(action_id)
        self.close_menu()

    def close_menu(self):
        """Close menu with fade-out"""
        self.hide()
        self.setWindowOpacity(0)
        self.current_selection = -1
        self.update_selection_display()
        self.sig_closed.emit()

    def closeEvent(self, event):
        """Handle window close - hide instead of closing app"""
        logger.debug("FloatingMenu close requested - hiding instead")
        self.close_menu()
        event.ignore()  # Don't close, just hide


# Test/Demo
if __name__ == "__main__":
    app = QApplication([])

    # Create and test menu
    menu = FloatingMenu()

    # Add actions
    menu.add_action("summarize", "Summarize Text")
    menu.add_action("translate", "Translate")
    menu.add_action("explain", "Explain This")
    menu.add_action("code", "Generate Code")
    menu.add_action("screenshot", "Screenshot")
    menu.add_action("chat", "Open Chat")

    def on_action(action_id):
        print(f"Action selected: {action_id}")

    menu.sig_action_selected.connect(on_action)

    # Show at center of screen
    screen = app.primaryScreen()
    center = screen.geometry().center()
    menu.move(center.x() - 75, center.y() - 100)
    menu.show()
    menu.animation.start()

    print("FloatingMenu demo - Use arrow keys to navigate, Enter to select, Esc to close")

    import sys
    sys.exit(app.exec())
