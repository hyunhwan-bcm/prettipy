"""
Jupyter Notebook to Python converter.

This module handles conversion of .ipynb files to .py files using nbconvert.
"""

import tempfile
from pathlib import Path
from typing import Optional
import json


class NotebookConverter:
    """Converts Jupyter notebooks to Python scripts."""

    def __init__(self, verbose: bool = False):
        """
        Initialize the notebook converter.

        Args:
            verbose: Enable verbose output
        """
        self.verbose = verbose

    def convert_notebook_to_python(self, notebook_path: Path) -> Optional[str]:
        """
        Convert a Jupyter notebook to Python code using nbconvert.

        Args:
            notebook_path: Path to the .ipynb file

        Returns:
            Python code as a string, or None if conversion fails

        Raises:
            ImportError: If nbconvert is not installed
            ValueError: If the notebook file is invalid
        """
        try:
            from nbconvert import PythonExporter
        except ImportError:
            raise ImportError(
                "nbconvert is required for .ipynb support. "
                "Install it with: pip install nbconvert"
            )

        try:
            # Read the notebook
            with open(notebook_path, "r", encoding="utf-8") as f:
                notebook_content = f.read()

            # Validate that it's a valid JSON notebook
            try:
                json.loads(notebook_content)
            except json.JSONDecodeError as e:
                if self.verbose:
                    print(f"Warning: Invalid JSON in notebook {notebook_path}: {e}")
                return None

            # Create a PythonExporter
            # script exports only code cells, no outputs or metadata
            exporter = PythonExporter()

            # Convert the notebook
            (body, resources) = exporter.from_filename(str(notebook_path))

            return body

        except Exception as e:
            if self.verbose:
                print(f"Warning: Failed to convert notebook {notebook_path}: {e}")
            return None

    def create_temp_python_file(self, notebook_path: Path) -> Optional[Path]:
        """
        Convert a notebook and save it as a temporary Python file.

        Args:
            notebook_path: Path to the .ipynb file

        Returns:
            Path to the temporary .py file, or None if conversion fails
        """
        python_code = self.convert_notebook_to_python(notebook_path)

        if python_code is None:
            return None

        # Create a temporary file with a unique name to avoid conflicts
        # Include a hash of the absolute path to ensure uniqueness
        import hashlib

        path_hash = hashlib.md5(str(notebook_path.absolute()).encode()).hexdigest()[:8]
        temp_dir = Path(tempfile.gettempdir()) / "prettipy_notebooks"
        temp_dir.mkdir(exist_ok=True)

        # Use base name with path hash to ensure uniqueness
        base_name = notebook_path.stem
        temp_py_file = temp_dir / f"{base_name}_{path_hash}.py"

        # Write the Python code
        temp_py_file.write_text(python_code, encoding="utf-8")

        return temp_py_file
