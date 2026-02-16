"""
Markdown Renderer - Convert markdown text to styled HTML

Converts markdown responses to HTML with:
- Code syntax highlighting (Pygments)
- Proper formatting (headers, bold, italic, lists, tables)
- Dark mode compatible CSS
"""

import logging
import re
from typing import Optional
from markdown import markdown
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

logger = logging.getLogger(__name__)


class MarkdownRenderer:
    """Render markdown to HTML with syntax highlighting."""

    # CSS for code blocks (dark mode friendly)
    DARK_CODE_CSS = """
    <style>
    pre {
        background-color: #1e1e1e;
        border: 1px solid #444;
        border-radius: 4px;
        padding: 12px;
        overflow-x: auto;
        margin: 8px 0;
    }
    code {
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 12px;
    }
    .codehilite {
        background-color: #1e1e1e;
    }
    .codehilite pre {
        background-color: transparent;
        border: none;
        padding: 0;
        margin: 0;
    }
    h1, h2, h3, h4, h5, h6 {
        margin-top: 12px;
        margin-bottom: 6px;
        font-weight: 600;
    }
    h1 { font-size: 24px; }
    h2 { font-size: 20px; }
    h3 { font-size: 18px; }
    h4 { font-size: 16px; }
    ul, ol {
        margin: 8px 0;
        padding-left: 24px;
    }
    li {
        margin: 4px 0;
    }
    blockquote {
        border-left: 3px solid #0066ff;
        margin: 8px 0;
        padding-left: 12px;
        color: #999;
    }
    table {
        border-collapse: collapse;
        margin: 8px 0;
        width: 100%;
    }
    table th, table td {
        border: 1px solid #444;
        padding: 8px;
        text-align: left;
    }
    table th {
        background-color: #2d2d2d;
        font-weight: 600;
    }
    a {
        color: #0066ff;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """

    LIGHT_CODE_CSS = """
    <style>
    pre {
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 12px;
        overflow-x: auto;
        margin: 8px 0;
    }
    code {
        font-family: 'Fira Code', 'Courier New', monospace;
        font-size: 12px;
    }
    .codehilite {
        background-color: #f5f5f5;
    }
    .codehilite pre {
        background-color: transparent;
        border: none;
        padding: 0;
        margin: 0;
    }
    h1, h2, h3, h4, h5, h6 {
        margin-top: 12px;
        margin-bottom: 6px;
        font-weight: 600;
        color: #1a1a1a;
    }
    h1 { font-size: 24px; }
    h2 { font-size: 20px; }
    h3 { font-size: 18px; }
    h4 { font-size: 16px; }
    ul, ol {
        margin: 8px 0;
        padding-left: 24px;
    }
    li {
        margin: 4px 0;
    }
    blockquote {
        border-left: 3px solid #0066ff;
        margin: 8px 0;
        padding-left: 12px;
        color: #666;
    }
    table {
        border-collapse: collapse;
        margin: 8px 0;
        width: 100%;
    }
    table th, table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    table th {
        background-color: #f0f0f0;
        font-weight: 600;
    }
    a {
        color: #0066ff;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """

    def __init__(self, dark_mode: bool = True):
        """
        Initialize markdown renderer.

        Args:
            dark_mode: If True, use dark mode CSS. Else light mode.
        """
        self.dark_mode = dark_mode
        self.css = self.DARK_CODE_CSS if dark_mode else self.LIGHT_CODE_CSS

    def render(self, text: str) -> str:
        """
        Render markdown text to HTML with syntax highlighting.

        Args:
            text: Markdown text

        Returns:
            HTML string with CSS and syntax-highlighted code blocks
        """
        try:
            # Convert markdown to HTML
            html = markdown(
                text,
                extensions=[
                    "fenced_code",
                    "tables",
                    "nl2br",
                    "toc",
                ],
            )

            # Process code blocks for syntax highlighting
            html = self._highlight_code_blocks(html)

            # Wrap in HTML with CSS
            return f"{self.css}\n{html}"

        except Exception as e:
            logger.error(f"Markdown rendering failed: {e}", exc_info=True)
            # Fallback: return as plain text wrapped in pre
            return f"{self.css}\n<pre>{self._escape_html(text)}</pre>"

    def _highlight_code_blocks(self, html: str) -> str:
        """
        Find and syntax-highlight code blocks in HTML.

        Args:
            html: HTML with <pre><code> blocks

        Returns:
            HTML with syntax-highlighted code blocks
        """
        # Pattern to find <pre><code class="language-xxx">...code...</code></pre>
        pattern = r'<pre><code class="language-(\w+)">(.+?)</code></pre>'

        def replace_code_block(match):
            language = match.group(1)
            code = match.group(2)

            # Unescape HTML entities
            code = code.replace("&lt;", "<")
            code = code.replace("&gt;", ">")
            code = code.replace("&amp;", "&")

            return self._highlight_code(code, language)

        html = re.sub(pattern, replace_code_block, html, flags=re.DOTALL)

        # Also handle generic <pre><code> without language
        pattern_generic = r'<pre><code>(.+?)</code></pre>'

        def replace_generic_code(match):
            code = match.group(1)
            code = code.replace("&lt;", "<")
            code = code.replace("&gt;", ">")
            code = code.replace("&amp;", "&")
            return self._highlight_code(code, None)

        html = re.sub(pattern_generic, replace_generic_code, html, flags=re.DOTALL)

        return html

    def _highlight_code(self, code: str, language: Optional[str] = None) -> str:
        """
        Highlight code block using Pygments.

        Args:
            code: Code to highlight
            language: Programming language (e.g., 'python', 'javascript')

        Returns:
            HTML with syntax highlighting
        """
        try:
            # Try to get lexer by language
            if language:
                try:
                    lexer = get_lexer_by_name(language)
                except ClassNotFound:
                    logger.warning(f"Lexer not found for language: {language}, guessing...")
                    lexer = guess_lexer(code)
            else:
                lexer = guess_lexer(code)

            # Highlight code
            formatter = HtmlFormatter(
                style="monokai" if self.dark_mode else "default",
                noclasses=False,
                wrapcode=True,
            )

            highlighted = highlight(code, lexer, formatter)
            return f"<pre>{highlighted}</pre>"

        except Exception as e:
            logger.debug(f"Syntax highlighting failed: {e}")
            # Fallback: return as plain code
            return f"<pre><code>{self._escape_html(code)}</code></pre>"

    @staticmethod
    def _escape_html(text: str) -> str:
        """Escape HTML special characters."""
        return (
            text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
            .replace("'", "&#39;")
        )

    def set_dark_mode(self, dark_mode: bool):
        """Switch between dark and light mode."""
        self.dark_mode = dark_mode
        self.css = self.DARK_CODE_CSS if dark_mode else self.LIGHT_CODE_CSS


# Singleton instance
_instance: Optional[MarkdownRenderer] = None


def get_markdown_renderer(dark_mode: bool = True) -> MarkdownRenderer:
    """Get or create markdown renderer instance."""
    global _instance
    if _instance is None:
        _instance = MarkdownRenderer(dark_mode=dark_mode)
    return _instance
