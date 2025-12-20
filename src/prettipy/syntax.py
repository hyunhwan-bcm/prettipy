"""
Syntax highlighting for Python code.

This module handles syntax highlighting using Pygments,
converting tokens to HTML with appropriate colors.
"""

import html
from typing import List, Tuple, Dict
from pygments import lex
from pygments.lexers import PythonLexer
from pygments.token import Token


class SyntaxHighlighter:
    """Handles syntax highlighting for Python code."""

    # Default color scheme (GitHub-like)
    DEFAULT_COLORS = {
        Token.Keyword: '#007020',
        Token.Name.Builtin: '#007020',
        Token.Name.Function: '#06287e',
        Token.Name.Class: '#0e7c7b',
        Token.Name.Decorator: '#aa22ff',
        Token.String: '#4070a0',
        Token.Number: '#40a070',
        Token.Comment: '#60a0b0',
        Token.Comment.Single: '#60a0b0',
        Token.Comment.Multiline: '#60a0b0',
        Token.Operator: '#666666',
    }

    def __init__(self, color_scheme: Dict = None):
        """
        Initialize the syntax highlighter.

        Args:
            color_scheme: Optional custom color scheme dictionary.
                         If None, uses DEFAULT_COLORS.
        """
        self.lexer = PythonLexer()
        self.color_scheme = color_scheme or self.DEFAULT_COLORS

    def highlight_line(self, line: str) -> str:
        """
        Highlight a single line of Python code.

        Args:
            line: Line of Python code to highlight

        Returns:
            HTML string with syntax highlighting
        """
        if not line.strip():
            return '<br/>'

        tokens = list(lex(line, self.lexer))
        colored_parts = []

        for token_type, token_value in tokens:
            colored_parts.append(self._colorize_token(token_type, token_value))

        return ''.join(colored_parts)

    def _colorize_token(self, token_type: Token, token_value: str) -> str:
        """
        Apply color to a single token.

        Args:
            token_type: Pygments token type
            token_value: The actual text of the token

        Returns:
            HTML string with color formatting
        """
        # Escape HTML special characters
        escaped = html.escape(token_value)
        # Preserve spaces and tabs
        escaped = escaped.replace(' ', '&nbsp;')
        escaped = escaped.replace('\t', '&nbsp;&nbsp;&nbsp;&nbsp;')

        # Find matching color
        color = self._get_token_color(token_type)

        if color and token_value.strip():
            return f'<font color="{color}">{escaped}</font>'
        return escaped

    def _get_token_color(self, token_type: Token) -> str:
        """
        Get the color for a given token type.

        Args:
            token_type: Pygments token type

        Returns:
            Hex color string or None
        """
        for ttype, color in self.color_scheme.items():
            if token_type in ttype:
                return color
        return None

    def highlight_code(self, code: str, lines: List[str] = None) -> str:
        """
        Highlight an entire code block.

        Args:
            code: Full code string
            lines: Optional pre-split lines (if already processed)

        Returns:
            HTML string with all lines highlighted
        """
        if lines is None:
            lines = code.split('\n')

        highlighted_lines = [self.highlight_line(line) for line in lines]
        return '<br/>'.join(highlighted_lines)

    def highlight_code_multiline_aware(self, code: str) -> List[str]:
        """
        Highlight code with proper multiline string support.
        
        This method processes the entire code block to correctly identify
        multiline strings and other constructs that span multiple lines,
        then returns a list of highlighted HTML strings for each line.

        Args:
            code: Full code string to highlight

        Returns:
            List of HTML strings, one per line
        """
        if not code:
            return []
        
        # Tokenize the entire code block
        tokens = list(lex(code, self.lexer))
        
        # Split code into lines to track line boundaries
        lines = code.split('\n')
        
        # Build highlighted HTML for each line
        highlighted_lines = [''] * len(lines)
        current_line = 0
        
        for token_type, token_value in tokens:
            # Split token value by newlines to handle multiline tokens
            token_lines = token_value.split('\n')
            
            for i, line_part in enumerate(token_lines):
                if i > 0:
                    # New line boundary
                    current_line += 1
                
                if current_line >= len(lines):
                    break
                    
                if line_part:
                    # Colorize the entire line part as one unit
                    highlighted_part = self._colorize_token(token_type, line_part)
                    highlighted_lines[current_line] += highlighted_part
        
        # Convert empty lines to <br/>
        return [line if line else '<br/>' for line in highlighted_lines]
