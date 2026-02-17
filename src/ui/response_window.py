"""
Response Window - Chat Streaming Display

A singleton window for displaying LLM responses with streaming tokens,
markdown rendering, and auto-scrolling.

Features:
  - Singleton pattern (one instance reused)
  - Real-time token streaming with buffering
  - Auto-scrolling with user scroll detection
  - Auto-expanding input area
  - Markdown rendering support
  - Stop button for cancellation
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QPushButton, QLabel, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, Signal, QSize, QRect
from PySide6.QtGui import QFont, QColor, QPalette
import logging
from typing import Optional, Iterator

from src.ui.markdown_renderer import get_markdown_renderer
from src.core.auto_paster import get_auto_paster

logger = logging.getLogger(__name__)


class AutoExpandingTextEdit(QTextEdit):
    """
    Text edit that auto-expands based on content.

    Min height: 40px, Max height: 200px
    Supports Ctrl+Enter to submit.
    """

    sig_send_requested = Signal()  # Emitted when Ctrl+Enter pressed

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(40)
        self.setMaximumHeight(200)

        # Auto-expand on text change
        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        """Auto-expand when text changes"""
        # Get document height
        doc = self.document()
        height = doc.size().height()

        # Add some padding
        height = min(int(height) + 10, 200)
        height = max(height, 40)

        self.setMinimumHeight(height)

    def sizeHint(self) -> QSize:
        """Return appropriate size hint"""
        return QSize(400, min(int(self.document().size().height()) + 10, 200))

    def keyPressEvent(self, event):
        """Handle key press - Ctrl+Enter or Shift+Enter to send"""
        # Check for Ctrl+Enter or Shift+Enter
        if event.key() == Qt.Key_Return:
            # Ctrl+Return sends message
            if event.modifiers() & Qt.ControlModifier:
                self.sig_send_requested.emit()
                event.accept()
                return
            # Shift+Return also sends (alternative if Ctrl doesn't work)
            elif event.modifiers() & Qt.ShiftModifier:
                self.sig_send_requested.emit()
                event.accept()
                return

        # Default behavior for other keys (normal Return = newline)
        super().keyPressEvent(event)


class ResponseWindow(QMainWindow):
    """
    Singleton window for displaying streamed LLM responses.

    Signals:
        sig_stop_requested: Emitted when user clicks Stop button

    Usage:
        window = ResponseWindow()
        window.set_context("summarize", "gpt-4o")

        # Stream tokens
        for token in llm_provider.stream_chat(...):
            window.append_token(token)

        window.show()
    """

    _instance = None
    _initialized = False

    sig_stop_requested = Signal()
    sig_input_submitted = Signal(str)  # user message text

    def __new__(cls):
        """Singleton pattern"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize ResponseWindow (called only once)"""
        if ResponseWindow._initialized:
            return

        super().__init__()
        ResponseWindow._initialized = True

        self.setWindowTitle("Quick Shortcut AI - Chat")
        self.setGeometry(100, 100, 800, 600)

        # Dark theme
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(30, 30, 30))
        palette.setColor(QPalette.WindowText, QColor(200, 200, 200))
        self.setPalette(palette)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Context info bar (top)
        context_layout = QHBoxLayout()
        self.label_context = QLabel("Chat")
        self.label_context.setStyleSheet("color: #0066ff; font-weight: bold;")
        self.btn_stop = QPushButton("Stop")
        self.btn_stop.clicked.connect(self._on_stop_clicked)
        self.btn_stop.setMaximumWidth(100)
        self.btn_stop.setEnabled(False)

        context_layout.addWidget(self.label_context)
        context_layout.addStretch()
        context_layout.addWidget(self.btn_stop)
        layout.addLayout(context_layout)

        # Response display area
        self.text_response = QTextEdit()
        self.text_response.setReadOnly(True)
        self.text_response.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #d0d0d0;
                border: 1px solid #333;
                padding: 10px;
            }
        """)
        font = QFont("Consolas", 10)
        self.text_response.setFont(font)
        layout.addWidget(self.text_response)

        # Input area (expandable)
        self.text_input = AutoExpandingTextEdit()
        self.text_input.setPlaceholderText("Type message... (Ctrl+Enter or Shift+Enter to send, or click Send)")
        self.text_input.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a1a;
                color: #d0d0d0;
                border: 1px solid #333;
                padding: 5px;
            }
        """)
        # Connect Ctrl+Enter to send
        self.text_input.sig_send_requested.connect(self._on_send_clicked)
        layout.addWidget(self.text_input)

        # Button bar (bottom)
        button_layout = QHBoxLayout()
        self.btn_send = QPushButton("Send")
        self.btn_send.clicked.connect(self._on_send_clicked)
        self.btn_copy = QPushButton("Copy")
        self.btn_copy.clicked.connect(self._on_copy_clicked)
        self.btn_auto_paste = QPushButton("Auto-Paste")
        self.btn_auto_paste.clicked.connect(self._on_auto_paste_clicked)
        self.btn_auto_paste.setEnabled(False)

        button_layout.addWidget(self.btn_send)
        button_layout.addWidget(self.btn_copy)
        button_layout.addWidget(self.btn_auto_paste)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        # Streaming state
        self._is_streaming = False
        self._token_buffer = ""
        self._buffer_timer = QTimer()
        self._buffer_timer.timeout.connect(self._flush_buffer)
        self._buffer_timer.setInterval(50)  # 50ms buffer window

        # Auto-scroll state
        self._user_scrolled_up = False
        self.text_response.verticalScrollBar().valueChanged.connect(
            self._on_scroll_changed
        )

    def _on_scroll_changed(self):
        """Detect if user scrolled up"""
        scrollbar = self.text_response.verticalScrollBar()
        # If not at bottom, user scrolled up
        self._user_scrolled_up = scrollbar.value() < scrollbar.maximum()

    def set_context(self, action: str, model: str):
        """Set context information"""
        self.label_context.setText(f"{action.title()} • {model}")

    def append_token(self, token: str):
        """Add token to buffer for streaming"""
        if not self._is_streaming:
            self._is_streaming = True
            self.btn_stop.setEnabled(True)
            self._buffer_timer.start()

        self._token_buffer += token

    def _flush_buffer(self):
        """Flush buffered tokens to display"""
        if self._token_buffer:
            self.text_response.insertPlainText(self._token_buffer)
            self._token_buffer = ""

            # Auto-scroll if user didn't scroll up
            if not self._user_scrolled_up:
                scrollbar = self.text_response.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())

    def finish_streaming(self):
        """Called when streaming is complete"""
        self._flush_buffer()
        self._buffer_timer.stop()
        self._is_streaming = False
        self.btn_stop.setEnabled(False)

        # Enable auto-paste if we have content
        if self.text_response.toPlainText().strip():
            self.btn_auto_paste.setEnabled(True)

        # Render markdown after streaming completes
        self._render_markdown_response()

    def _on_stop_clicked(self):
        """Stop button clicked"""
        logger.info("Stop requested")
        self.finish_streaming()
        self.sig_stop_requested.emit()

    def _on_send_clicked(self):
        """Send button clicked"""
        text = self.text_input.toPlainText().strip()
        if text:
            self.sig_input_submitted.emit(text)
            self.text_input.clear()

    def _on_copy_clicked(self):
        """Copy button clicked"""
        from PySide6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_response.toPlainText())
        logger.info("Response copied to clipboard")

    def closeEvent(self, event):
        """Handle window close event - hide instead of closing"""
        logger.debug("ResponseWindow close requested - hiding instead")
        self.hide()
        event.ignore()  # Don't actually close, just hide

    def _on_auto_paste_clicked(self):
        """Auto-Paste button clicked"""
        text = self.text_response.toPlainText()
        if not text.strip():
            logger.warning("No text to paste")
            return

        paster = get_auto_paster()
        success = paster.paste_to_active_window(text)

        if success:
            logger.info("Auto-paste completed successfully")
        else:
            logger.error("Auto-paste failed")

    def clear_response(self):
        """Clear response text"""
        self.text_response.clear()
        self._token_buffer = ""
        self._user_scrolled_up = False
        self.btn_auto_paste.setEnabled(False)

    def get_response_text(self) -> str:
        """Get current response text"""
        return self.text_response.toPlainText()

    def get_input_text(self) -> str:
        """Get current input text"""
        return self.text_input.toPlainText()

    def _render_markdown_response(self):
        """Render accumulated response as markdown HTML"""
        try:
            # Get the plain text response
            plain_text = self.text_response.toPlainText()

            if not plain_text.strip():
                return  # Nothing to render

            # Render markdown to HTML
            renderer = get_markdown_renderer()
            html = renderer.render(plain_text)

            # Display HTML in the widget
            self.text_response.setHtml(html)

            logger.info("Markdown rendering applied to response")
        except Exception as e:
            logger.error(f"Markdown rendering failed: {e}", exc_info=True)
            # Keep the plain text if rendering fails

    def is_streaming(self) -> bool:
        """Check if currently streaming"""
        return self._is_streaming


# Test/Demo
if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication([])

    window = ResponseWindow()
    window.set_context("summarize", "gpt-4o")
    window.show()

    # Simulate streaming
    def simulate_stream():
        tokens = "This is a simulated response from the LLM. ".split()
        for token in tokens:
            window.append_token(token + " ")

        window.finish_streaming()

    # Start simulation after 1 second
    from PySide6.QtCore import QTimer
    QTimer.singleShot(1000, simulate_stream)

    print("ResponseWindow demo - Text should stream in...")

    sys.exit(app.exec())
