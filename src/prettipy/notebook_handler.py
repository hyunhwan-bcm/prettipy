"""
Notebook handler for converting Jupyter notebooks to Python scripts.

This module handles the conversion of .ipynb files to .py files using nbconvert.
"""

from pathlib import Path
from typing import Optional
import tempfile
import shutil


def convert_notebook_to_python(notebook_path: Path, verbose: bool = False) -> Optional[Path]:
    """
    Convert a Jupyter notebook to a Python script.

    Args:
        notebook_path: Path to the .ipynb file
        verbose: Whether to print verbose output

    Returns:
        Path to the converted .py file, or None if conversion fails

    Raises:
        ImportError: If nbconvert is not installed
        Exception: If conversion fails
    """
    try:
        from nbconvert import PythonExporter
    except ImportError:
        raise ImportError(
            "nbconvert is required for notebook conversion. "
            "Install it with: pip install nbconvert"
        )

    try:
        if verbose:
            print(f"Converting notebook: {notebook_path}")

        # Create a Python exporter
        exporter = PythonExporter()
        # Configure to exclude outputs and metadata
        exporter.exclude_output = True
        exporter.exclude_output_prompt = True
        exporter.exclude_input_prompt = True

        # Convert to Python script
        (body, resources) = exporter.from_filename(str(notebook_path))

        # Create output path with .py extension
        output_path = notebook_path.with_suffix(".py")

        # Write the converted Python code
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(body)

        if verbose:
            print(f"Converted to: {output_path}")

        return output_path

    except Exception as e:
        if verbose:
            print(f"Failed to convert {notebook_path}: {e}")
        raise


def cleanup_converted_notebook(py_path: Path, verbose: bool = False):
    """
    Remove a converted Python file.

    Args:
        py_path: Path to the converted .py file
        verbose: Whether to print verbose output
    """
    try:
        if py_path.exists():
            py_path.unlink()
            if verbose:
                print(f"Cleaned up: {py_path}")
    except Exception as e:
        if verbose:
            print(f"Failed to cleanup {py_path}: {e}")
