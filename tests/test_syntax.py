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
