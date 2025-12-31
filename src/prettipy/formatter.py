"""
Code formatting and line wrapping utilities.

This module handles intelligent line wrapping for Python code,
preserving comment structure and breaking at natural points.
"""

import re
from typing import List


class CodeFormatter:
    """Handles formatting and wrapping of Python code lines."""

    def __init__(self, max_width: int = 90):
        """
        Initialize the code formatter.

        Args:
            max_width: Maximum character width before wrapping (default: 90)
        """
        self.max_width = max_width
        self.break_chars = [
            ", ",
            " + ",
            " - ",
            " * ",
            " / ",
            " = ",
            " and ",
            " or ",
            " if ",
            " else ",
            " (",
            " [",
        ]

    def wrap_line(self, line: str) -> List[str]:
        """
        Wrap a long line at natural break points, preserving comment structure.

        Args:
            line: The line of code to wrap

        Returns:
            List of wrapped lines
        """
        if len(line) <= self.max_width:
            return [line]

        # Check if line has a comment
        comment_match = re.search(r"#.*", line)
        if comment_match:
            return self._wrap_line_with_comment(line, comment_match)

        # No comment - wrap at natural break points
        return self._wrap_plain_line(line)

    def _wrap_line_with_comment(self, line: str, comment_match: re.Match) -> List[str]:
        """
        Wrap a line that contains a comment.

        Args:
            line: The full line of code
            comment_match: Regex match object for the comment

        Returns:
            List of wrapped lines
        """
        code_part = line[: comment_match.start()].rstrip()
        comment_part = line[comment_match.start() :]

        # If code part fits, just wrap the comment
        if len(code_part) <= self.max_width:
            # Check if the full line fits
            if len(code_part + " " + comment_part) <= self.max_width:
                return [code_part + " " + comment_part if code_part else comment_part]

            # Need to wrap the comment - use word boundary wrapping
            lines = []
            indent = len(line) - len(line.lstrip())
            base_indent = " " * indent
            continuation_indent = indent + 4

            # First line: code + start of comment
            remaining = comment_part
            if code_part:
                # There's code before the comment
                available = self.max_width - len(code_part) - 1  # -1 for space
                if available > 10:  # Only include comment if reasonable space
                    # Find word boundary in comment
                    break_pos = self._find_comment_break(remaining, available)
                    if break_pos > 0:
                        lines.append(code_part + " " + remaining[:break_pos].rstrip())
                        remaining = remaining[break_pos:].lstrip()
                        # Remove leading # from remaining since we'll add it back
                        if remaining.startswith("#"):
                            remaining = remaining[1:].lstrip()
                    else:
                        # Can't fit any comment, put code on its own line
                        lines.append(code_part)
                else:
                    # Not enough space for comment, code on its own line
                    lines.append(code_part)
            else:
                # Pure comment line - wrap it, preserving base indentation
                available = self.max_width - indent
                break_pos = self._find_comment_break(remaining, available)
                if break_pos > 0:
                    lines.append(base_indent + remaining[:break_pos].rstrip())
                    remaining = remaining[break_pos:].lstrip()
                    # Remove leading # from remaining since we'll add it back
                    if remaining.startswith("#"):
                        remaining = remaining[1:].lstrip()
                else:
                    # Can't find good break, break at available space
                    lines.append(base_indent + remaining[:available].rstrip())
                    remaining = remaining[available:].lstrip()
                    if remaining.startswith("#"):
                        remaining = remaining[1:].lstrip()

            # Wrap remaining comment text with proper indentation and # prefix
            while remaining:
                # Add # prefix for continuation
                line_text = "# " + remaining
                available = self.max_width - continuation_indent

                if len(line_text) <= available:
                    # Remaining text fits
                    lines.append(" " * continuation_indent + line_text)
                    break
                else:
                    # Need to wrap further - find word boundary
                    # Look for break in the comment text (after "# ")
                    break_pos = self._find_comment_break(line_text, available)
                    if break_pos > 2:  # Must be after "# "
                        lines.append(" " * continuation_indent + line_text[:break_pos].rstrip())
                        remaining = line_text[break_pos:].lstrip()
                        # Remove # if present since we'll add it back
                        if remaining.startswith("#"):
                            remaining = remaining[1:].lstrip()
                    else:
                        # No good break found, break at available space
                        lines.append(" " * continuation_indent + line_text[:available].rstrip())
                        remaining = line_text[available:].lstrip()
                        if remaining.startswith("#"):
                            remaining = remaining[1:].lstrip()

            return lines

        # Code part is too long, wrap it first
        return self._wrap_plain_line(line)

    def _find_comment_break(self, text: str, max_len: int) -> int:
        """
        Find a good break point in comment text at a word boundary.

        Args:
            text: The comment text to break
            max_len: Maximum length for the segment (must be > 0)

        Returns:
            Position to break at (at or before max_len), or -1 if no good break point found.
            Returns len(text) if text fits within max_len.
        """
        if not text or max_len <= 0:
            return -1

        if len(text) <= max_len:
            return len(text)

        # Look for space at or before max_len
        # We search backwards from max_len to find the last space that fits
        for i in range(max_len, 0, -1):
            if text[i - 1] == " ":
                return i

        return -1

    def _wrap_plain_line(self, line: str) -> List[str]:
        """
        Wrap a line without comments at natural break points.

        Args:
            line: The line of code to wrap

        Returns:
            List of wrapped lines
        """
        lines = []
        current = line
        indent = len(line) - len(line.lstrip())
        continuation_indent = indent + 4

        while len(current) > self.max_width:
            # Find the best break point
            best_break = self._find_break_point(current, indent)

            if best_break == -1 or best_break <= indent:
                # No good break point found, break at max_width
                best_break = self.max_width

            lines.append(current[:best_break].rstrip())
            current = " " * continuation_indent + current[best_break:].lstrip()

        if current.strip():
            lines.append(current)

        return lines if lines else [line]

    def _find_break_point(self, line: str, min_pos: int) -> int:
        """
        Find the best position to break a line.

        Args:
            line: The line to analyze
            min_pos: Minimum position for the break (usually the indentation)

        Returns:
            Position to break at, or -1 if no good break point found
        """
        best_break = -1
        for char in self.break_chars:
            pos = line.rfind(char, 0, self.max_width)
            if pos > best_break and pos > min_pos:
                potential_break = pos + len(char)
                # Ensure we don't exceed max_width
                if potential_break <= self.max_width:
                    best_break = potential_break
        return best_break
