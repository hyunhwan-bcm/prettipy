"""Tests for notebook integration in core module."""

import pytest
from pathlib import Path
from prettipy.core import PrettipyConverter
from prettipy.config import PrettipyConfig
import json


class TestNotebookIntegration:
    """Test cases for notebook integration in PrettipyConverter."""

    def test_find_python_files_excludes_ipynb_by_default(self, tmp_path):
        """Test that .ipynb files are excluded by default."""
        # Create test files
        (tmp_path / "script.py").write_text("print('python')")

        notebook_path = tmp_path / "notebook.ipynb"
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [],
                    "source": ["print('notebook')"],
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

        config = PrettipyConfig(include_ipynb=False)
        converter = PrettipyConverter(config)
        files = converter.find_python_files(tmp_path)

        # Should only find the .py file
        assert len(files) == 1
        assert files[0].name == "script.py"

    def test_find_python_files_includes_ipynb_when_enabled(self, tmp_path):
        """Test that .ipynb files are included when enabled."""
        # Create test files
        (tmp_path / "script.py").write_text("print('python')")

        notebook_path = tmp_path / "notebook.ipynb"
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [],
                    "source": ["print('notebook')"],
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

        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)
        files = converter.find_python_files(tmp_path)

        # Should find both files (original .py and converted .ipynb)
        assert len(files) == 2
        file_names = [f.name for f in files]
        assert "script.py" in file_names
        assert "notebook.py" in file_names

    def test_convert_directory_with_ipynb(self, tmp_path):
        """Test converting a directory with .ipynb files."""
        # Create a test notebook
        notebook_path = tmp_path / "test.ipynb"
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [],
                    "source": ["x = 42\n", "print(x)"],
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

        output_pdf = tmp_path / "output.pdf"

        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)
        converter.convert_directory(str(tmp_path), str(output_pdf))

        # Check PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # Check that converted .py file was cleaned up
        converted_py = tmp_path / "test.py"
        assert not converted_py.exists()

    def test_convert_directory_cleanup_on_error(self, tmp_path):
        """Test that converted files are cleaned up even on error."""
        # Create a valid notebook
        notebook_path = tmp_path / "test.ipynb"
        notebook_content = {
            "cells": [
                {
                    "cell_type": "code",
                    "execution_count": 1,
                    "metadata": {},
                    "outputs": [],
                    "source": ["print('test')"],
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

        output_pdf = tmp_path / "output.pdf"

        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)

        # Convert successfully
        converter.convert_directory(str(tmp_path), str(output_pdf))

        # Verify cleanup happened
        converted_py = tmp_path / "test.py"
        assert not converted_py.exists()

    def test_convert_with_multiple_notebooks(self, tmp_path):
        """Test converting multiple notebooks in a directory."""
        # Create multiple notebooks
        for i in range(3):
            notebook_path = tmp_path / f"notebook{i}.ipynb"
            notebook_content = {
                "cells": [
                    {
                        "cell_type": "code",
                        "execution_count": 1,
                        "metadata": {},
                        "outputs": [],
                        "source": [f"print('notebook {i}')"],
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

        output_pdf = tmp_path / "output.pdf"

        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)
        converter.convert_directory(str(tmp_path), str(output_pdf))

        # Check PDF was created
        assert output_pdf.exists()

        # Check all converted files were cleaned up
        for i in range(3):
            converted_py = tmp_path / f"notebook{i}.py"
            assert not converted_py.exists()
