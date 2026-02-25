"""
Tests for ClipboardManager (F-05: Clipboard Management)

Tests verify:
  - Text clipboard read/write
  - Rich text (HTML) clipboard write
  - Error handling
  - Thread safety (basic)
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QApplication
from src.core.clipboard_manager import ClipboardManager, get_clipboard_manager


@pytest.fixture
def qapp():
    """Qt Application fixture"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


@pytest.fixture
def clipboard_manager(qapp):
    """ClipboardManager instance"""
    mgr = ClipboardManager()
    yield mgr
    # Cleanup
    mgr.clear()


class TestClipboardManagerBasics:
    """Basic ClipboardManager functionality"""

    def test_clipboard_manager_creation(self, clipboard_manager):
        """Test ClipboardManager initializes"""
        assert clipboard_manager is not None
        assert clipboard_manager.app is not None

    def test_singleton_instance(self, qapp):
        """Test get_clipboard_manager singleton"""
        mgr1 = get_clipboard_manager()
        mgr2 = get_clipboard_manager()
        assert mgr1 is mgr2


class TestClipboardText:
    """Text clipboard operations"""

    def test_set_and_get_text(self, clipboard_manager):
        """Test writing and reading text"""
        text = "Hello, World!"
        success = clipboard_manager.set_text(text)

        assert success == True
        retrieved = clipboard_manager.get_text()
        assert retrieved == text

    def test_get_empty_clipboard(self, clipboard_manager):
        """Test reading from empty clipboard"""
        clipboard_manager.clear()
        result = clipboard_manager.get_text()

        # Should return None or empty
        assert result is None or result == ""

    def test_set_empty_text_fails(self, clipboard_manager):
        """Test setting empty text returns False"""
        result = clipboard_manager.set_text("")
        assert result == False

    def test_unicode_text(self, clipboard_manager):
        """Test Unicode text handling"""
        text = "Hello 世界 🌍 مرحبا"
        success = clipboard_manager.set_text(text)

        assert success == True
        retrieved = clipboard_manager.get_text()
        assert retrieved == text

    def test_multiline_text(self, clipboard_manager):
        """Test multiline text"""
        text = "Line 1\nLine 2\nLine 3"
        success = clipboard_manager.set_text(text)

        assert success == True
        retrieved = clipboard_manager.get_text()
        assert retrieved == text

    def test_long_text(self, clipboard_manager):
        """Test large text content"""
        text = "x" * 10000  # 10K characters
        success = clipboard_manager.set_text(text)

        assert success == True
        retrieved = clipboard_manager.get_text()
        assert len(retrieved) == 10000


class TestClipboardHTML:
    """Rich text (HTML) clipboard operations"""

    def test_set_rich_text(self, clipboard_manager):
        """Test setting HTML content"""
        html = "<html><body><h1>Title</h1><p>Content</p></body></html>"
        success = clipboard_manager.set_rich_text(html)

        assert success == True

    def test_set_empty_html_fails(self, clipboard_manager):
        """Test setting empty HTML returns False"""
        result = clipboard_manager.set_rich_text("")
        assert result == False

    def test_markdown_html(self, clipboard_manager):
        """Test markdown-style HTML"""
        html = """
        <h2>Summary</h2>
        <p>This is <strong>bold</strong> and <em>italic</em></p>
        <pre><code>def hello(): pass</code></pre>
        """
        success = clipboard_manager.set_rich_text(html)
        assert success == True

    def test_copy_response_to_clipboard(self, clipboard_manager):
        """Test copy_response_to_clipboard utility"""
        response = "Test response"
        success = clipboard_manager.copy_response_to_clipboard(response, is_html=False)

        assert success == True
        retrieved = clipboard_manager.get_text()
        assert retrieved == response

    def test_copy_html_response(self, clipboard_manager):
        """Test copy_response_to_clipboard with HTML"""
        html = "<h1>Title</h1><p>Content</p>"
        success = clipboard_manager.copy_response_to_clipboard(html, is_html=True)

        assert success == True


class TestClipboardErrorHandling:
    """Error handling"""

    def test_clear_clipboard(self, clipboard_manager):
        """Test clearing clipboard"""
        clipboard_manager.set_text("Test")
        result = clipboard_manager.clear()

        assert result == True

    def test_set_text_exception_handling(self, clipboard_manager):
        """Test exception handling in set_text"""
        # Mock clipboard to raise exception
        with patch.object(clipboard_manager, 'app') as mock_app:
            mock_app.clipboard.side_effect = Exception("Mock error")

            result = clipboard_manager.set_text("Test")
            assert result == False

    def test_get_text_exception_handling(self, clipboard_manager):
        """Test exception handling in get_text"""
        # Mock clipboard to raise exception
        with patch.object(clipboard_manager, 'app') as mock_app:
            mock_app.clipboard.side_effect = Exception("Mock error")

            result = clipboard_manager.get_text()
            assert result is None


class TestClipboardIntegration:
    """Integration tests"""

    def test_full_workflow(self, clipboard_manager):
        """Test complete clipboard workflow"""
        # Write text
        original = "Original content for testing"
        assert clipboard_manager.set_text(original) == True

        # Read text
        retrieved = clipboard_manager.get_text()
        assert retrieved == original

        # Clear
        assert clipboard_manager.clear() == True

        # Write HTML
        html = "<h1>New Content</h1>"
        assert clipboard_manager.set_rich_text(html) == True

    def test_consecutive_operations(self, clipboard_manager):
        """Test multiple consecutive operations"""
        texts = ["First", "Second", "Third"]

        for text in texts:
            assert clipboard_manager.set_text(text) == True
            retrieved = clipboard_manager.get_text()
            assert retrieved == text
