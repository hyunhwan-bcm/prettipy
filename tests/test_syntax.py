"""Tests for the syntax highlighting module."""

import pytest
from prettipy.syntax import SyntaxHighlighter


class TestSyntaxHighlighter:
    """Test cases for SyntaxHighlighter class."""

    def test_empty_line(self):
        """Test highlighting of empty lines."""
        highlighter = SyntaxHighlighter()
        result = highlighter.highlight_line("")
        assert result == "<br/>"

    def test_simple_assignment(self):
        """Test highlighting of simple assignment."""
        highlighter = SyntaxHighlighter()
        result = highlighter.highlight_line("x = 1")
        assert "font" in result or "nbsp" in result
        assert isinstance(result, str)

    def test_function_definition(self):
        """Test highlighting of function definition."""
        highlighter = SyntaxHighlighter()
        result = highlighter.highlight_line("def hello():")
        assert "font" in result
        assert "color" in result
        assert isinstance(result, str)

    def test_comment(self):
        """Test highlighting of comments."""
        highlighter = SyntaxHighlighter()
        result = highlighter.highlight_line("# This is a comment")
        assert "font" in result
        assert "color" in result

    def test_preserve_spaces(self):
        """Test that spaces are preserved."""
        highlighter = SyntaxHighlighter()
        result = highlighter.highlight_line("    indented")
        assert "nbsp" in result

    def test_highlight_code_multiline(self):
        """Test highlighting of multiple lines."""
        highlighter = SyntaxHighlighter()
        code = "def hello():\n    print('world')"
        result = highlighter.highlight_code(code)
        assert "<br/>" in result
        assert "font" in result

    def test_multiline_docstring_double_quotes(self):
        """Test highlighting of triple-double-quoted docstrings."""
        highlighter = SyntaxHighlighter()
        code = '"""\nThis is a docstring.\nIt spans multiple lines.\n"""'
        lines = highlighter.highlight_code_multiline_aware(code)

        # All lines should contain string color
        string_color = "#4070a0"
        assert string_color in lines[0], "Opening quotes should be highlighted"
        assert string_color in lines[1], "First line of content should be highlighted as string"
        assert string_color in lines[2], "Second line of content should be highlighted as string"
        assert string_color in lines[3], "Closing quotes should be highlighted"

    def test_multiline_docstring_single_quotes(self):
        """Test highlighting of triple-single-quoted strings."""
        highlighter = SyntaxHighlighter()
        code = "'''\nMultiline string\nwith single quotes\n'''"
        lines = highlighter.highlight_code_multiline_aware(code)

        # All lines should contain string color
        string_color = "#4070a0"
        assert string_color in lines[0], "Opening quotes should be highlighted"
        assert string_color in lines[1], "First line of content should be highlighted as string"
        assert string_color in lines[2], "Second line of content should be highlighted as string"
        assert string_color in lines[3], "Closing quotes should be highlighted"

    def test_multiline_string_in_function(self):
        """Test multiline string inside a function definition."""
        highlighter = SyntaxHighlighter()
        code = '''def example():
    """
    This is a function docstring.
    It explains what the function does.
    """
    pass'''
        lines = highlighter.highlight_code_multiline_aware(code)

        # Check that docstring lines are highlighted as strings
        string_color = "#4070a0"
        assert string_color in lines[1], "Opening docstring quotes should be highlighted"
        assert string_color in lines[2], "Docstring content should be highlighted as string"
        assert string_color in lines[3], "Docstring content should be highlighted as string"
        assert string_color in lines[4], "Closing docstring quotes should be highlighted"

    def test_empty_code(self):
        """Test highlighting of empty code."""
        highlighter = SyntaxHighlighter()
        lines = highlighter.highlight_code_multiline_aware("")
        assert lines == []

    def test_mixed_strings_and_code(self):
        """Test file with both multiline strings and regular code."""
        highlighter = SyntaxHighlighter()
        code = '''"""Module docstring"""

def func():
    x = 1
    return x'''
        lines = highlighter.highlight_code_multiline_aware(code)

        # First line should have string highlighting
        assert "#4070a0" in lines[0]
        # Empty line
        assert lines[1] == "<br/>"
        # Function definition should have keyword highlighting
        assert "#007020" in lines[2]  # 'def' keyword color

    def test_wrapped_comment_highlighting(self):
        """Test that wrapped comment lines maintain comment color."""
        from prettipy.formatter import CodeFormatter

        highlighter = SyntaxHighlighter()
        formatter = CodeFormatter(max_width=50)

        # Long comment that will be wrapped
        line = "# We can also plot average attention across all heads and layers"
        wrapped_lines = formatter.wrap_line(line)

        # Highlight each wrapped line
        for wrapped_line in wrapped_lines:
            highlighted = highlighter.highlight_line(wrapped_line)
            # All wrapped comment lines should have comment color
            assert "#60a0b0" in highlighted, f"Comment color missing in: {wrapped_line}"

    def test_wrapped_inline_comment_highlighting(self):
        """Test that wrapped inline comments maintain comment color on continuation."""
        from prettipy.formatter import CodeFormatter

        highlighter = SyntaxHighlighter()
        formatter = CodeFormatter(max_width=50)

        # Inline comment that will be wrapped
        line = "x = 1  # This is a very long inline comment that should wrap"
        wrapped_lines = formatter.wrap_line(line)

        # Should have multiple lines
        assert len(wrapped_lines) > 1

        # All lines with comments should have comment color
        for i, wrapped_line in enumerate(wrapped_lines):
            if "#" in wrapped_line:
                highlighted = highlighter.highlight_line(wrapped_line)
                assert "#60a0b0" in highlighted, f"Comment color missing in line {i}: {wrapped_line}"
