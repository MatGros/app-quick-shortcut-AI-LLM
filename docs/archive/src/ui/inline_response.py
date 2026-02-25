"""
Inline Response Window - Lightweight Floating Display

A small, frameless window that appears near the cursor for quick actions
(Summarize, Translate) instead of opening the full Chat window.
"""

import logging
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTextEdit, QGraphicsDropShadowEffect,
    QPushButton, QHBoxLayout, QLabel
)
from PySide6.QtCore import Qt, QPoint, QPropertyAnimation, QTimer, Signal
from PySide6.QtGui import QColor, QCursor, QFont, QTextCursor

logger = logging.getLogger(__name__)

class InlineResponseWindow(QWidget):
    """
    Lightweight floating window for streaming LLM responses.
    """
    sig_closed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Frameless and Always on Top
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Main container with style
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        
        self.container = QWidget()
        self.container.setObjectName("InlineContainer")
        self.container.setStyleSheet("""
            QWidget#InlineContainer {
                background-color: rgba(30, 30, 30, 240);
                border: 1px solid #555555;
                border-radius: 10px;
            }
        """)
        
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(10, 25, 10, 10)
        self.container_layout.setSpacing(10)
        
        # Header (Draggable area + Close button)
        self.header = QWidget()
        self.header_layout = QHBoxLayout(self.header)
        self.header_layout.setContentsMargins(5, 0, 5, 0)
        
        self.title_label = QLabel("Quick Shortcut AI")
        self.title_label.setStyleSheet("color: #888888; font-size: 10px; font-weight: bold;")
        
        self.close_button = QPushButton("×")
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #888888;
                font-size: 16px;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.1);
                color: #ffffff;
            }
        """)
        self.close_button.clicked.connect(self.hide_window)
        
        self.header_layout.addWidget(self.title_label)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.close_button)
        
        self.container_layout.addWidget(self.header)
        
        # Add spacing between header and text (Fix first line obscured)
        self.container_layout.addSpacing(10)
        
        # Text display
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFrameStyle(0)
        self.text_display.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.text_display.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.text_display.setStyleSheet("background: transparent; color: #e0e0e0; border: none;")
        self.text_display.setFont(QFont("Segoe UI", 10))
        # Ensure some padding inside the text area
        self.text_display.document().setDocumentMargin(8)
        
        self.container_layout.addWidget(self.text_display)
        self.layout.addWidget(self.container)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 180))
        shadow.setOffset(0, 8)
        self.setGraphicsEffect(shadow)
        
        # Animation
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(300)
        
        # Timer for auto-hide
        self.auto_hide_timer = QTimer(self)
        self.auto_hide_timer.setSingleShot(True)
        self.auto_hide_timer.timeout.connect(self.hide_window)
        
        # Dimensions
        self.setMinimumSize(320, 100)
        self.setMaximumSize(550, 450)
        
        # State
        self._is_streaming = False
        self._dragging = False
        self._drag_pos = QPoint()

    def set_text(self, text: str):
        """Set or append text to the display"""
        self.text_display.setPlainText(text)
        self._adjust_size()

    def append_token(self, token: str):
        """Append a token and adjust window size"""
        self._is_streaming = True
        cursor = self.text_display.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(token)
        self.text_display.setTextCursor(cursor)
        self._adjust_size()

    def hide(self):
        logger.debug(f"Inline: hide() called. Visible: {self.isVisible()}")
        super().hide()

    def _adjust_size(self):
        """Auto-adjust window height based on content"""
        doc = self.text_display.document()
        # Account for header (~30px) + spacing (10px) + content margins (~16px) + vertical padding
        height = doc.size().height() + 65 
        width = 450 # Slightly wider for better readability
        
        new_height = min(max(int(height), 120), 450)
        self.resize(width, new_height)

    def show_at_cursor(self):
        """Position near cursor and fade in"""
        logger.debug(f"Inline: show_at_cursor() called. Current Opacity: {self.windowOpacity()}")
        # Stop any pending hide animations
        self.animation.stop()
        try:
            # Only disconnect if there are receivers to avoid RuntimeWarning
            if self.receivers(self.animation.finished) > 0:
                logger.debug("Inline: Disconnecting old animation slots")
                self.animation.finished.disconnect()
            
            # CRITICAL: Specifically disconnect our hide method to prevent the late-hide race condition
            # This is redundant with the generic disconnect() but ensures safety if multiple things were connected.
            try:
                self.animation.finished.disconnect(self.hide)
            except (RuntimeError, TypeError):
                pass
        except (RuntimeError, TypeError):
            pass

        self._is_streaming = True
        self.auto_hide_timer.stop()

        pos = QCursor.pos()
        # Offset to not be directly under the mouse
        self.move(pos.x() + 20, pos.y() + 20)
        
        self.setWindowOpacity(0.0)
        self.show()
        logger.debug("Inline: Window shown (Opacity 0), starting fade-in")
        
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()
        
        # Auto-close timer (optional, or rely on user click?)
        # For now, stay until dismissed or new action starts

    def clear(self):
        """Reset content and stop timers"""
        self._is_streaming = True
        self.auto_hide_timer.stop()
        self.text_display.clear()
        self.resize(450, 120)

    def closeEvent(self, event):
        """Handle manual close request (ALT+F4 or system close)"""
        self.hide_window()
        event.ignore()

    def finish_streaming(self):
        """Called when streaming is complete. Starts auto-hide timer."""
        self._is_streaming = False
        logger.debug("Inline: Streaming finished, starting 30s auto-hide timer")
        # Auto-hide after 30 seconds of showing the result (plenty of time to read)
        self.auto_hide_timer.start(30000)

    def enterEvent(self, event):
        """Pause timer on hover"""
        if self.auto_hide_timer.isActive():
            logger.debug("Inline: Pause auto-hide timer (hover)")
            self.auto_hide_timer.stop()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Resume timer on leave if not streaming"""
        if not self._is_streaming and self.isVisible():
            logger.debug("Inline: Resume auto-hide timer (leave)")
            self.auto_hide_timer.start(15000) # Give 15 more seconds to read result
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Handle dragging or manual close click (if not on close button)"""
        if event.button() == Qt.LeftButton:
            # Check if clicking on header (or just anywhere in container for easy drag)
            if self.header.geometry().contains(self.header.mapFromGlobal(event.globalPos())):
                self._dragging = True
                self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()
                event.accept()
            else:
                # Clicking text area doesn't drag, but stops timer?
                self.auto_hide_timer.stop()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle window dragging"""
        if self._dragging and event.buttons() & Qt.LeftButton:
            self.move(event.globalPos() - self._drag_pos)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Stop dragging"""
        self._dragging = False
        super().mouseReleaseEvent(event)

    def hide_window(self):
        """Manual hide with animation and signaling"""
        if not self.isVisible():
            return
            
        if self.animation.state() == QPropertyAnimation.Running and self.animation.endValue() == 0.0:
            return
        
        logger.debug(f"Inline: Starting hide animation (Opacity: {self.windowOpacity()})")
        self.auto_hide_timer.stop()
        self.animation.stop()
        
        # Emit signal that user manually closed the window
        self.sig_closed.emit()
        
        try:
            if self.receivers(self.animation.finished) > 0:
                self.animation.finished.disconnect()
        except (RuntimeError, TypeError):
            pass
            
        self.animation.setStartValue(self.windowOpacity())
        self.animation.setEndValue(0.0)
        
        # Connect to parent's hide
        self.animation.finished.connect(self.hide)
        self.animation.start()

