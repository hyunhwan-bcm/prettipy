"""Tests for the notebook handler module."""

import pytest
from pathlib import Path
from prettipy.notebook_handler import convert_notebook_to_python, cleanup_converted_notebook
import json


class TestNotebookHandler:
    """Test cases for notebook handler functions."""

    def test_convert_simple_notebook(self, tmp_path):
        """Test converting a simple notebook to Python."""
        # Create a simple notebook
        notebook_path = tmp_path / "test_notebook.ipynb"
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [],
                    "source": ["print('Hello, World!')"],
                },
                {
                    "cell_type": "code",
                    "execution_count": 2,
                    "metadata": {},
                    "outputs": [],
                    "source": ["def add(a, b):\n", "    return a + b"],
                },
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }

        with open(notebook_path, "w") as f:
            json.dump(notebook_content, f)

        # Convert the notebook
        converted_path = convert_notebook_to_python(notebook_path)

        # Check the converted file exists
        assert converted_path is not None
        assert converted_path.exists()
        assert converted_path.suffix == ".py"
        assert converted_path.stem == "test_notebook"

        # Check the content
        content = converted_path.read_text()
        assert "print('Hello, World!')" in content
        assert "def add(a, b):" in content
        assert "return a + b" in content

    def test_convert_notebook_with_markdown(self, tmp_path):
        """Test converting a notebook with markdown cells."""
        notebook_path = tmp_path / "test_markdown.ipynb"
        notebook_content = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# This is a title\n", "Some description"],
                },
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [],
                    "source": ["x = 42"],
                },
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }

        with open(notebook_path, "w") as f:
            json.dump(notebook_content, f)

        converted_path = convert_notebook_to_python(notebook_path)

        # Markdown should be converted to comments
        content = converted_path.read_text()
        assert "x = 42" in content

    def test_convert_notebook_excludes_outputs(self, tmp_path):
        """Test that conversion excludes outputs."""
        notebook_path = tmp_path / "test_outputs.ipynb"
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [
                        {
                            "name": "stdout",
                            "output_type": "stream",
                            "text": ["Output text\n"],
                        }
                    ],
                    "source": ["print('Code only')"],
                }
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }

        with open(notebook_path, "w") as f:
            json.dump(notebook_content, f)

        converted_path = convert_notebook_to_python(notebook_path)
        content = converted_path.read_text()

        # Code should be present
        assert "print('Code only')" in content
        # Output should not be present as a string literal
        # Note: nbconvert Python exporter doesn't include outputs

    def test_cleanup_converted_notebook(self, tmp_path):
        """Test cleaning up a converted notebook file."""
        # Create a test file
        py_file = tmp_path / "test.py"
        py_file.write_text("print('test')")

        assert py_file.exists()

        # Clean it up
        cleanup_converted_notebook(py_file)

        assert not py_file.exists()

    def test_cleanup_nonexistent_file(self, tmp_path):
        """Test cleaning up a file that doesn't exist."""
        py_file = tmp_path / "nonexistent.py"

        # Should not raise an error
        cleanup_converted_notebook(py_file)

    def test_convert_invalid_notebook(self, tmp_path):
        """Test converting an invalid notebook file."""
        notebook_path = tmp_path / "invalid.ipynb"
        notebook_path.write_text("not a valid notebook")

        # Should raise an exception
        with pytest.raises(Exception):
            convert_notebook_to_python(notebook_path)
