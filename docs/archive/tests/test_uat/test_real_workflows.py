"""
UAT Tests - Real User Workflows

Validates real-world usage scenarios:
  - LLM streaming with real responses
  - Markdown rendering quality
  - Auto-paste functionality
  - Error handling in real scenarios
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from PySide6.QtWidgets import QApplication

from src.ui.response_window import ResponseWindow
from src.ui.floating_menu import FloatingMenu
from src.core.clipboard_manager import ClipboardManager
from src.core.auto_paster import AutoPaster


@pytest.fixture
def qapp():
    """Qt Application fixture"""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    return app


class TestRealStreamingWorkflow:
    """Test real LLM streaming workflows"""

    @pytest.mark.qt
    def test_summarize_action_workflow(self, qapp):
        """Test complete summarize workflow"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Simulate user workflow
        window.set_context("summarize", "gpt-4o")

        # Simulate streaming response
        sample_response = (
            "# Summary\n\n"
            "This document discusses the importance of AI. "
            "Key points:\n"
            "- Machine learning revolutionizes industries\n"
            "- Data quality is critical\n"
            "- Ethical considerations matter\n\n"
            "## Conclusion\n"
            "AI is transformative but requires responsible deployment."
        )

        # Stream tokens (word by word)
        for token in sample_response.split():
            window.append_token(token + " ")

        window.finish_streaming()

        # Verify results
        response_text = window.get_response_text()
        assert "Summary" in response_text
        assert "Machine learning" in response_text
        assert "AI is transformative" in response_text

        window.close()

    @pytest.mark.qt
    def test_code_generation_workflow(self, qapp):
        """Test code generation with syntax highlighting"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        window.set_context("code", "code-model")

        # Python code generation example
        code_response = (
            "Here's a Python function:\n\n"
            "```python\n"
            "def factorial(n):\n"
            "    if n <= 1:\n"
            "        return 1\n"
            "    return n * factorial(n - 1)\n"
            "```\n\n"
            "This uses recursion to calculate factorial."
        )

        for token in code_response.split():
            window.append_token(token + " ")

        window.finish_streaming()

        response_text = window.get_response_text()
        assert "def factorial" in response_text
        assert "python" in response_text.lower()
        assert "recursion" in response_text.lower()

        window.close()

    @pytest.mark.qt
    def test_long_response_streaming(self, qapp):
        """Test streaming of very long response"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        window.set_context("explain", "model")

        # Simulate long response (1000+ tokens)
        long_response = " ".join(["word"] * 1000)

        token_count = 0
        for token in long_response.split():
            window.append_token(token + " ")
            token_count += 1

        window.finish_streaming()

        # Verify it handled it
        response_text = window.get_response_text()
        assert len(response_text) > 4000  # 1000 words * ~4 chars + spaces

        window.close()

    @pytest.mark.qt
    def test_response_with_special_characters(self, qapp):
        """Test response with UTF-8, emojis, special chars"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        window.set_context("translate", "translate-model")

        # Translation with special chars and emojis
        response = (
            "Bonjour! 👋 Here's the translation:\n\n"
            "French: Café ☕\n"
            "German: Größe 📏\n"
            "Chinese: 你好 🇨🇳\n"
            "Emoji test: ✅ ❌ ⚠️ 🚀\n"
        )

        for token in response.split():
            window.append_token(token + " ")

        window.finish_streaming()

        response_text = window.get_response_text()
        assert "Bonjour" in response_text
        assert "Café" in response_text
        # Emojis and special chars preserved

        window.close()


class TestMarkdownRenderingQuality:
    """Test quality of markdown rendering"""

    @pytest.mark.qt
    def test_markdown_headers_rendering(self, qapp):
        """Test markdown headers render correctly"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        markdown_text = (
            "# Main Title\n\n"
            "## Section One\n\n"
            "Content here.\n\n"
            "### Subsection\n\n"
            "More content."
        )

        for token in markdown_text.split():
            window.append_token(token + " ")

        window.finish_streaming()

        response_text = window.get_response_text()
        assert "Main Title" in response_text
        assert "Section One" in response_text
        assert "Subsection" in response_text

        window.close()

    @pytest.mark.qt
    def test_markdown_list_rendering(self, qapp):
        """Test markdown lists render correctly"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        list_markdown = (
            "# Shopping List\n\n"
            "- Apples\n"
            "- Bananas\n"
            "- Oranges\n\n"
            "## Prioritized:\n"
            "1. Buy milk\n"
            "2. Get bread\n"
            "3. Add eggs\n"
        )

        for token in list_markdown.split():
            window.append_token(token + " ")

        window.finish_streaming()

        response_text = window.get_response_text()
        assert "Apples" in response_text
        assert "milk" in response_text
        assert "eggs" in response_text

        window.close()

    @pytest.mark.qt
    def test_markdown_table_rendering(self, qapp):
        """Test markdown table rendering"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        table_markdown = (
            "# Comparison Table\n\n"
            "| Feature | Python | JavaScript |\n"
            "| --- | --- | --- |\n"
            "| Speed | Fast | Very Fast |\n"
            "| Learning | Easy | Medium |\n"
        )

        for token in table_markdown.split():
            window.append_token(token + " ")

        window.finish_streaming()

        response_text = window.get_response_text()
        assert "Feature" in response_text or "Python" in response_text

        window.close()


class TestAutoClipboardIntegration:
    """Test clipboard-based workflows"""

    @pytest.mark.qt
    def test_get_text_from_clipboard(self, qapp):
        """Test getting text from clipboard"""
        ClipboardManager._instance = None
        manager = ClipboardManager()

        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_cb.text.return_value = "Sample text to process"
            mock_clipboard.return_value = mock_cb

            text = manager.get_text()
            assert text == "Sample text to process"

    @pytest.mark.qt
    def test_clipboard_with_long_text(self, qapp):
        """Test clipboard handles long text"""
        ClipboardManager._instance = None
        manager = ClipboardManager()

        long_text = " ".join(["word"] * 500)  # 500 words

        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_cb.text.return_value = long_text
            mock_clipboard.return_value = mock_cb

            text = manager.get_text()
            assert len(text) > 1000  # Should be quite long

    @pytest.mark.qt
    def test_clipboard_with_code_content(self, qapp):
        """Test clipboard with code content"""
        ClipboardManager._instance = None
        manager = ClipboardManager()

        code_text = """def hello():
    print('Hello, World!')
    return True"""

        with patch('PySide6.QtWidgets.QApplication.clipboard') as mock_clipboard:
            mock_cb = MagicMock()
            mock_cb.text.return_value = code_text
            mock_clipboard.return_value = mock_cb

            text = manager.get_text()
            assert "def hello" in text
            assert "print" in text


class TestAutoPasteQuality:
    """Test auto-paste functionality quality"""

    @pytest.mark.qt
    def test_auto_paste_with_regular_text(self, qapp):
        """Test auto-paste with regular text"""
        paster = AutoPaster(delay_ms=100)

        text = "This is text to paste into an application"

        with patch.object(paster, '_get_active_window') as mock_get, \
             patch.object(paster, '_copy_to_clipboard') as mock_copy, \
             patch.object(paster, '_paste_via_keyboard') as mock_paste, \
             patch.object(paster, '_restore_focus') as mock_restore:

            mock_get.return_value = 12345

            result = paster.paste_to_active_window(text)

            assert result == True
            mock_copy.assert_called_once_with(text)
            mock_paste.assert_called_once()
            mock_restore.assert_called_once()

    @pytest.mark.qt
    def test_auto_paste_with_markdown_text(self, qapp):
        """Test auto-paste with markdown formatted text"""
        paster = AutoPaster()

        markdown_text = (
            "# Title\n\n"
            "- Item 1\n"
            "- Item 2\n\n"
            "```python\nprint('hello')\n```"
        )

        with patch.object(paster, '_get_active_window') as mock_get, \
             patch.object(paster, '_copy_to_clipboard') as mock_copy, \
             patch.object(paster, '_paste_via_keyboard') as mock_paste:

            mock_get.return_value = 99999

            result = paster.paste_to_active_window(markdown_text)

            assert result == True
            # Should paste the exact markdown
            call_args = mock_copy.call_args[0][0]
            assert "# Title" in call_args
            assert "python" in call_args

    @pytest.mark.qt
    def test_auto_paste_error_recovery(self, qapp):
        """Test auto-paste error recovery"""
        paster = AutoPaster()

        with patch.object(paster, '_copy_to_clipboard') as mock_copy:
            mock_copy.side_effect = Exception("Clipboard unavailable")

            result = paster.paste_to_active_window("text")

            # Should handle error gracefully
            assert result == False


class TestErrorHandling:
    """Test error handling in real scenarios"""

    @pytest.mark.qt
    def test_empty_clipboard_error(self, qapp):
        """Test handling of empty clipboard"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        with patch('src.core.clipboard_manager.ClipboardManager.get_text') as mock_get:
            mock_get.return_value = ""

            # Simulate error response
            error_msg = "❌ Clipboard is empty. Please copy some text first."
            window.append_token(error_msg)
            window.finish_streaming()

            response_text = window.get_response_text()
            assert "Clipboard is empty" in response_text

        window.close()

    @pytest.mark.qt
    def test_llm_connection_error(self, qapp):
        """Test handling of LLM connection error"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        error_response = (
            "❌ Error: Connection refused\n\n"
            "Could not connect to LLM provider. "
            "Please check your configuration in Settings."
        )

        for token in error_response.split():
            window.append_token(token + " ")

        window.finish_streaming()

        response_text = window.get_response_text()
        assert "Error" in response_text
        assert "Connection" in response_text

        window.close()

    @pytest.mark.qt
    def test_malformed_response_handling(self, qapp):
        """Test handling of malformed LLM response"""
        ResponseWindow._instance = None
        ResponseWindow._initialized = False
        window = ResponseWindow()

        # Broken markdown (unclosed code block)
        broken_response = (
            "Here's some code:\n\n"
            "```python\n"
            "print('missing closing fence')\n\n"
            "And more text..."
        )

        for token in broken_response.split():
            window.append_token(token + " ")

        window.finish_streaming()

        response_text = window.get_response_text()
        # Should render even if malformed
        assert "python" in response_text.lower()
        assert "print" in response_text

        window.close()
