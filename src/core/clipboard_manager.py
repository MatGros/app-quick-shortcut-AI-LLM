"""
Clipboard Manager - Thread-safe clipboard access for text and images.

Provides unified interface for reading/writing clipboard content,
handling Unicode, RTL text, and concurrent access.
"""

import logging
from typing import Optional
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QMimeData, QBuffer, QIODevice
from PySide6.QtGui import QImage

logger = logging.getLogger(__name__)


class ClipboardManager:
    """Thread-safe clipboard access manager."""

    def __init__(self):
        """Initialize clipboard manager."""
        self.app = QApplication.instance()
        if self.app is None:
            raise RuntimeError("ClipboardManager requires QApplication instance")

    def get_text(self) -> Optional[str]:
        """
        Read text from clipboard.

        Returns:
            str: Clipboard text content, or None if clipboard is empty/unavailable
        """
        try:
            clipboard = self.app.clipboard()
            text = clipboard.text()

            if not text or not text.strip():
                logger.warning("Clipboard is empty")
                return None

            logger.info(f"Clipboard text retrieved: {len(text)} characters")
            return text

        except Exception as e:
            logger.error(f"Failed to read clipboard: {e}", exc_info=True)
            return None

    def get_image(self) -> Optional[bytes]:
        """
        Read image from clipboard as PNG bytes.

        Returns:
            bytes: PNG image data, or None if no image in clipboard
        """
        try:
            clipboard = self.app.clipboard()
            mime_data = clipboard.mimeData()

            if not mime_data or not mime_data.hasImage():
                logger.debug("No image in clipboard")
                return None

            image = QImage(mime_data.imageData())

            if image.isNull():
                logger.warning("Clipboard image is null")
                return None

            # Convert to PNG bytes
            png_data = bytearray()
            buffer = QBuffer(png_data)
            buffer.open(QIODevice.WriteOnly)
            image.save(buffer, "PNG")

            logger.info(f"Clipboard image retrieved: {image.width()}x{image.height()}")
            return bytes(png_data)

        except Exception as e:
            logger.error(f"Failed to read clipboard image: {e}", exc_info=True)
            return None

    def set_text(self, text: str) -> bool:
        """
        Write text to clipboard.

        Args:
            text: Text to write

        Returns:
            bool: True if successful, False otherwise
        """
        if not text:
            logger.warning("Attempted to set empty clipboard text")
            return False

        try:
            clipboard = self.app.clipboard()
            clipboard.setText(text)
            logger.info(f"Clipboard text set: {len(text)} characters")
            return True

        except Exception as e:
            logger.error(f"Failed to set clipboard text: {e}", exc_info=True)
            return False

    def set_rich_text(self, html: str) -> bool:
        """
        Write HTML content to clipboard (rich text format).

        Args:
            html: HTML content to write

        Returns:
            bool: True if successful, False otherwise
        """
        if not html:
            logger.warning("Attempted to set empty clipboard HTML")
            return False

        try:
            clipboard = self.app.clipboard()
            mime_data = QMimeData()

            # Set both plain text and HTML
            # Extract plain text from HTML (simple approach)
            plain_text = html.replace("<br>", "\n").replace("<p>", "").replace("</p>", "\n")
            plain_text = plain_text.replace("<div>", "").replace("</div>", "\n")
            plain_text = plain_text.replace("<span>", "").replace("</span>", "")
            # Remove HTML tags
            import re
            plain_text = re.sub(r"<[^>]+>", "", plain_text).strip()

            mime_data.setHtml(html)
            mime_data.setText(plain_text)

            clipboard.setMimeData(mime_data)
            logger.info(f"Clipboard HTML set: {len(html)} characters")
            return True

        except Exception as e:
            logger.error(f"Failed to set clipboard HTML: {e}", exc_info=True)
            return False

    def clear(self) -> bool:
        """
        Clear clipboard content.

        Returns:
            bool: True if successful
        """
        try:
            clipboard = self.app.clipboard()
            clipboard.clear()
            logger.info("Clipboard cleared")
            return True

        except Exception as e:
            logger.error(f"Failed to clear clipboard: {e}", exc_info=True)
            return False

    def copy_response_to_clipboard(self, response: str, is_html: bool = False) -> bool:
        """
        Copy LLM response to clipboard.

        Args:
            response: Response text or HTML
            is_html: If True, treat as HTML content

        Returns:
            bool: True if successful
        """
        if is_html:
            return self.set_rich_text(response)
        else:
            return self.set_text(response)


# Singleton instance (optional)
_instance: Optional[ClipboardManager] = None


def get_clipboard_manager() -> ClipboardManager:
    """Get or create singleton ClipboardManager instance."""
    global _instance
    if _instance is None:
        _instance = ClipboardManager()
    return _instance
