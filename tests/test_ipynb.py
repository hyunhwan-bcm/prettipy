"""Tests for Jupyter notebook (.ipynb) support."""

import pytest
from pathlib import Path
import json
from prettipy.core import PrettipyConverter
from prettipy.config import PrettipyConfig
from prettipy.ipynb_converter import NotebookConverter


class TestNotebookSupport:
    """Test cases for .ipynb file support."""

    def create_sample_notebook(self, path: Path) -> None:
        """Create a minimal valid Jupyter notebook for testing."""
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [],
                    "source": ["print('Hello from notebook')\n", "x = 42\n"],
                },
                {
                    "cell_type": "code",
                    "execution_count": 2,
                    "metadata": {},
                    "outputs": [],
                    "source": ["def add(a, b):\n", "    return a + b\n"],
                },
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": ["# This is a markdown cell\n", "It should not appear in the Python output"],
                },
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "version": "3.8.0"},
            },
            "nbformat": 4,
            "nbformat_minor": 4,
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(notebook_content, f, indent=2)

    def test_notebook_converter_basic(self, tmp_path):
        """Test basic notebook conversion."""
        notebook_path = tmp_path / "test_notebook.ipynb"
        self.create_sample_notebook(notebook_path)

        converter = NotebookConverter(verbose=True)
        python_code = converter.convert_notebook_to_python(notebook_path)

        assert python_code is not None
        assert "print('Hello from notebook')" in python_code
        assert "def add(a, b):" in python_code
        # nbconvert's PythonExporter includes markdown cells as commented lines
        # This is expected behavior - we only exclude outputs, not markdown
        assert "# This is a markdown cell" in python_code

    def test_notebook_converter_temp_file(self, tmp_path):
        """Test creating temporary Python file from notebook."""
        notebook_path = tmp_path / "test_notebook.ipynb"
        self.create_sample_notebook(notebook_path)

        converter = NotebookConverter(verbose=True)
        temp_py_file = converter.create_temp_python_file(notebook_path)

        assert temp_py_file is not None
        assert temp_py_file.exists()
        assert temp_py_file.suffix == ".py"
        # Filename includes hash for uniqueness
        assert temp_py_file.stem.startswith("test_notebook")

        # Check content
        content = temp_py_file.read_text()
        assert "print('Hello from notebook')" in content

    def test_include_ipynb_disabled_by_default(self, tmp_path):
        """Test that .ipynb files are not included by default."""
        # Create a notebook
        notebook_path = tmp_path / "test.ipynb"
        self.create_sample_notebook(notebook_path)

        # Create a regular Python file
        py_path = tmp_path / "test.py"
        py_path.write_text("print('regular python')")

        config = PrettipyConfig(include_ipynb=False)
        converter = PrettipyConverter(config)
        files = converter.find_python_files(tmp_path)

        # Should only find the .py file
        assert len(files) == 1
        assert files[0].name == "test.py"

    def test_include_ipynb_enabled(self, tmp_path):
        """Test that .ipynb files are included when enabled."""
        # Create a notebook
        notebook_path = tmp_path / "test.ipynb"
        self.create_sample_notebook(notebook_path)

        # Create a regular Python file
        py_path = tmp_path / "test.py"
        py_path.write_text("print('regular python')")

        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)
        files = converter.find_python_files(tmp_path)

        # Should find both files (the .py and the converted notebook)
        assert len(files) == 2

        # Check that the mapping was created
        # One of the files should be in the ipynb_to_py_map
        assert len(converter.ipynb_to_py_map) == 1

    def test_convert_directory_with_notebook(self, tmp_path):
        """Test converting a directory with notebooks to PDF."""
        # Create a notebook
        notebook_path = tmp_path / "notebook.ipynb"
        self.create_sample_notebook(notebook_path)

        # Create a regular Python file
        py_path = tmp_path / "script.py"
        py_path.write_text("print('regular python')")

        output_pdf = tmp_path / "output.pdf"

        config = PrettipyConfig(include_ipynb=True, verbose=True)
        converter = PrettipyConverter(config)
        converter.convert_directory(str(tmp_path), str(output_pdf))

        # Check that PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

    def test_invalid_notebook_handling(self, tmp_path):
        """Test that invalid notebooks are handled gracefully."""
        # Create an invalid notebook (not valid JSON)
        bad_notebook = tmp_path / "bad.ipynb"
        bad_notebook.write_text("this is not valid JSON")

        config = PrettipyConfig(include_ipynb=True, verbose=True)
        converter = PrettipyConverter(config)
        files = converter.find_python_files(tmp_path)

        # Should handle the error gracefully and not include the bad notebook
        # (no temp file created for invalid notebook)
        assert len(files) == 0

    def test_notebook_with_directory_tree(self, tmp_path):
        """Test that notebooks appear in directory tree with proper links."""
        # Create a notebook in a subdirectory
        subdir = tmp_path / "notebooks"
        subdir.mkdir()
        notebook_path = subdir / "analysis.ipynb"
        self.create_sample_notebook(notebook_path)

        # Create a regular Python file
        py_path = tmp_path / "script.py"
        py_path.write_text("print('regular python')")

        output_pdf = tmp_path / "with_tree.pdf"

        config = PrettipyConfig(
            include_ipynb=True, 
            show_directory_tree=True, 
            verbose=True
        )
        converter = PrettipyConverter(config)
        converter.convert_directory(str(tmp_path), str(output_pdf))

        # Check that PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # Verify that the ipynb_to_py_map was populated
        assert len(converter.ipynb_to_py_map) == 1
