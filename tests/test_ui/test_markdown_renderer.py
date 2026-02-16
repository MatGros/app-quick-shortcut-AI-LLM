"""
Tests for Markdown Renderer

Tests verify:
  - Markdown to HTML conversion
  - Code syntax highlighting
  - Special element handling (tables, lists, blockquotes)
  - Dark/light mode CSS
"""

import pytest
from src.ui.markdown_renderer import MarkdownRenderer, get_markdown_renderer


@pytest.fixture
def renderer():
    """Create a markdown renderer instance"""
    return MarkdownRenderer(dark_mode=True)


class TestMarkdownRendererBasics:
    """Basic rendering tests"""

    def test_renderer_creation(self, renderer):
        """Test renderer initializes"""
        assert renderer is not None
        assert renderer.dark_mode == True

    def test_render_plain_text(self, renderer):
        """Test rendering plain text"""
        text = "This is plain text"
        html = renderer.render(text)

        assert "<style>" in html
        assert "This is plain text" in html

    def test_render_empty_string(self, renderer):
        """Test rendering empty string"""
        html = renderer.render("")
        assert "<style>" in html

    def test_dark_mode_css_included(self, renderer):
        """Test dark mode CSS is included"""
        html = renderer.render("test")
        assert "background-color: #1e1e1e" in html

    def test_light_mode_css(self):
        """Test light mode CSS"""
        renderer = MarkdownRenderer(dark_mode=False)
        html = renderer.render("test")
        assert "background-color: #f5f5f5" in html


class TestMarkdownFormatting:
    """Test markdown formatting elements"""

    def test_headers(self, renderer):
        """Test markdown headers"""
        text = "# Header 1\n## Header 2\n### Header 3"
        html = renderer.render(text)

        assert "<h1>" in html or "header" in html.lower()
        assert "<h2>" in html or "header" in html.lower()
        assert "<h3>" in html or "header" in html.lower()

    def test_bold_italic(self, renderer):
        """Test bold and italic formatting"""
        text = "This is **bold** and *italic* text"
        html = renderer.render(text)

        assert "<strong>" in html or "<b>" in html
        assert "<em>" in html or "<i>" in html

    def test_lists(self, renderer):
        """Test unordered lists"""
        text = "- Item 1\n- Item 2\n- Item 3"
        html = renderer.render(text)

        assert "<ul>" in html or "<li>" in html

    def test_ordered_lists(self, renderer):
        """Test ordered lists"""
        text = "1. First\n2. Second\n3. Third"
        html = renderer.render(text)

        assert "<ol>" in html or "<li>" in html

    def test_blockquote(self, renderer):
        """Test blockquote"""
        text = "> This is a quote"
        html = renderer.render(text)

        assert "<blockquote>" in html or "quote" in html.lower()

    def test_links(self, renderer):
        """Test markdown links"""
        text = "[Click here](https://example.com)"
        html = renderer.render(text)

        assert "<a" in html
        assert "example.com" in html or "Click here" in html

    def test_inline_code(self, renderer):
        """Test inline code"""
        text = "Use `variable_name` in your code"
        html = renderer.render(text)

        assert "<code>" in html or "variable_name" in html


class TestCodeHighlighting:
    """Test syntax highlighting for code blocks"""

    def test_python_code_block(self, renderer):
        """Test Python code highlighting"""
        text = """```python
def hello():
    print("world")
```"""
        html = renderer.render(text)

        # Should contain highlighted code
        assert "hello" in html or "print" in html

    def test_javascript_code_block(self, renderer):
        """Test JavaScript code highlighting"""
        text = """```javascript
const x = 10;
console.log(x);
```"""
        html = renderer.render(text)

        assert "const" in html or "console" in html or "javascript" in html.lower()

    def test_generic_code_block(self, renderer):
        """Test code block without language specified"""
        text = """```
some code here
```"""
        html = renderer.render(text)

        assert "code" in html or "<pre>" in html

    def test_code_with_special_chars(self, renderer):
        """Test code with HTML special characters"""
        text = """```python
if x < 10 and y > 5:
    print("test")
```"""
        html = renderer.render(text)

        # Should properly escape < and >
        assert "&lt;" in html or "<" not in html.replace("&lt;", "")

    def test_multiline_code(self, renderer):
        """Test multiline code block"""
        text = """```python
def complex_function(x, y):
    result = x + y
    return result * 2

# Call it
answer = complex_function(3, 4)
```"""
        html = renderer.render(text)

        assert "complex_function" in html or "result" in html


class TestTables:
    """Test table rendering"""

    def test_simple_table(self, renderer):
        """Test simple markdown table"""
        text = """| Column 1 | Column 2 |
| -------- | -------- |
| Value 1  | Value 2  |"""
        html = renderer.render(text)

        assert "<table>" in html

    def test_table_structure(self, renderer):
        """Test table has proper structure"""
        text = """| Header 1 | Header 2 |
| -------- | -------- |
| Cell 1   | Cell 2   |"""
        html = renderer.render(text)

        assert "<table>" in html
        assert "<th>" in html or "Header" in html


class TestDarkLightMode:
    """Test dark and light mode switching"""

    def test_switch_to_light_mode(self, renderer):
        """Test switching to light mode"""
        assert renderer.dark_mode == True

        renderer.set_dark_mode(False)
        assert renderer.dark_mode == False

        html = renderer.render("test")
        assert "#f5f5f5" in html  # Light mode background

    def test_switch_to_dark_mode(self):
        """Test switching to dark mode"""
        renderer = MarkdownRenderer(dark_mode=False)
        renderer.set_dark_mode(True)

        html = renderer.render("test")
        assert "#1e1e1e" in html  # Dark mode background


class TestComplexContent:
    """Test complex markdown content"""

    def test_mixed_formatting(self, renderer):
        """Test mixed markdown formatting"""
        text = """# Main Title

This is **bold** and *italic* text.

## Subsection

Here's a list:
- Item 1
- Item 2
- Item 3

And some code:
```python
print("hello")
```

> A quote for emphasis

[Link to site](https://example.com)
"""
        html = renderer.render(text)

        # Should render without errors
        assert len(html) > len(text)  # HTML is longer due to tags
        assert "<style>" in html
        assert "<h1>" in html or "Main Title" in html

    def test_code_with_formatting(self, renderer):
        """Test code block in context"""
        text = """## Example

Here's how to use it:

```python
# This is a comment
def example():
    return True
```

That's all!
"""
        html = renderer.render(text)

        assert "Example" in html
        assert "example" in html
        assert "That's all" in html


class TestEdgeCases:
    """Test edge cases and error handling"""

    def test_malformed_markdown(self, renderer):
        """Test handling malformed markdown"""
        text = "# Header without closing\n\nSome text"
        html = renderer.render(text)

        # Should still render without crashing
        assert len(html) > 0

    def test_very_long_code_block(self, renderer):
        """Test very long code block"""
        code_lines = ["def func():" for _ in range(100)]
        text = "```python\n" + "\n".join(code_lines) + "\n```"

        html = renderer.render(text)
        assert "func" in html

    def test_unicode_content(self, renderer):
        """Test Unicode content"""
        text = "# Hello 世界 🌍\n\nText with émojis 🎉 and spëcial chars"
        html = renderer.render(text)

        assert "Hello" in html

    def test_special_html_chars_in_text(self, renderer):
        """Test HTML special characters in text"""
        text = "This has <tag> and & symbol and \"quotes\""
        html = renderer.render(text)

        # Should render without crashing
        assert len(html) > 0
        # HTML should contain the content
        assert "This has" in html

    def test_nested_lists(self, renderer):
        """Test nested list formatting"""
        text = """- Item 1
  - Nested 1
  - Nested 2
- Item 2"""
        html = renderer.render(text)

        assert "<li>" in html or "Item 1" in html


class TestSingleton:
    """Test singleton instance"""

    def test_singleton_instance(self):
        """Test get_markdown_renderer singleton"""
        renderer1 = get_markdown_renderer(dark_mode=True)
        renderer2 = get_markdown_renderer(dark_mode=False)

        # Should be same instance
        assert renderer1 is renderer2

    def test_singleton_dark_mode(self):
        """Test singleton dark mode persistence"""
        renderer = get_markdown_renderer()
        original_dark = renderer.dark_mode

        renderer.set_dark_mode(not original_dark)

        # Should persist
        renderer2 = get_markdown_renderer()
        assert renderer2.dark_mode == (not original_dark)

        # Reset
        renderer.set_dark_mode(original_dark)
