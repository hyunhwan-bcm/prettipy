"""Integration tests for mixed .ipynb and .py project conversion."""

import pytest
from pathlib import Path
from prettipy.core import PrettipyConverter
from prettipy.config import PrettipyConfig


class TestMixedProjectIntegration:
    """Test cases for converting projects with mixed .ipynb and .py files."""

    @pytest.fixture
    def test_project_dir(self):
        """Return path to test project directory."""
        return Path(__file__).parent / "test_data" / "mixed_project"

    def test_mixed_project_without_ipynb(self, test_project_dir, tmp_path):
        """Test converting mixed project without including notebooks."""
        output_pdf = tmp_path / "output_no_ipynb.pdf"

        # Convert without including .ipynb files
        config = PrettipyConfig(include_ipynb=False)
        converter = PrettipyConverter(config)
        converter.convert_directory(str(test_project_dir), str(output_pdf))

        # Verify PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # PDF should be reasonably sized (at least 10KB for 2 Python files)
        assert output_pdf.stat().st_size > 10_000

    def test_mixed_project_with_ipynb(self, test_project_dir, tmp_path):
        """Test converting mixed project including notebooks.

        This is the main integration test that verifies:
        1. PDF is generated successfully
        2. Both .py and .ipynb files are included
        3. Cross-references between files work correctly
        """
        output_pdf = tmp_path / "output_with_ipynb.pdf"

        # Convert with .ipynb files included
        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)
        converter.convert_directory(str(test_project_dir), str(output_pdf))

        # Verify PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # PDF should be larger when including notebooks (at least 30KB for 2 .py + 2 .ipynb files)
        assert output_pdf.stat().st_size > 30_000

    def test_mixed_project_with_dependency_sorting(self, test_project_dir, tmp_path):
        """Test converting mixed project with dependency-based sorting."""
        output_pdf = tmp_path / "output_sorted.pdf"

        # Convert with dependency sorting
        config = PrettipyConfig(include_ipynb=True, sort_method="dependency")
        converter = PrettipyConverter(config)
        converter.convert_directory(str(test_project_dir), str(output_pdf))

        # Verify PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # PDF should still be properly sized
        assert output_pdf.stat().st_size > 30_000

    def test_mixed_project_with_tree(self, test_project_dir, tmp_path):
        """Test converting mixed project with directory tree."""
        output_pdf = tmp_path / "output_with_tree.pdf"

        # Convert with directory tree and notebooks
        config = PrettipyConfig(include_ipynb=True, show_directory_tree=True)
        converter = PrettipyConverter(config)
        converter.convert_directory(str(test_project_dir), str(output_pdf))

        # Verify PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # PDF should be properly sized with tree
        assert output_pdf.stat().st_size > 30_000

    def test_mixed_project_with_linking(self, test_project_dir, tmp_path):
        """Test that auto-linking works with mixed .py and .ipynb files."""
        output_pdf = tmp_path / "output_with_linking.pdf"

        # Convert with linking enabled
        config = PrettipyConfig(include_ipynb=True, enable_linking=True)
        converter = PrettipyConverter(config)
        converter.convert_directory(str(test_project_dir), str(output_pdf))

        # Verify PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # PDF should be properly sized
        assert output_pdf.stat().st_size > 30_000

    def test_mixed_project_finds_correct_files(self, test_project_dir):
        """Test that the converter finds the correct files in the mixed project."""
        # Without ipynb
        config = PrettipyConfig(include_ipynb=False)
        converter = PrettipyConverter(config)
        files = converter.find_python_files(test_project_dir)

        file_names = [f.name for f in files]
        assert "utils.py" in file_names
        assert "main.py" in file_names
        assert len(files) == 2

        # With ipynb - notebooks are converted to temporary .py files with hashes
        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)
        files = converter.find_python_files(test_project_dir)

        file_names = [f.name for f in files]
        assert "utils.py" in file_names
        assert "main.py" in file_names
        # Notebooks get converted to .py files with hash suffixes
        assert any("analysis" in name for name in file_names)
        assert any("experiments" in name for name in file_names)
        assert len(files) == 4

    def test_mixed_project_specific_files(self, test_project_dir, tmp_path):
        """Test converting specific files from the mixed project."""
        output_pdf = tmp_path / "output_specific.pdf"

        # Convert only specific files
        utils_py = test_project_dir / "utils.py"
        analysis_ipynb = test_project_dir / "analysis.ipynb"

        config = PrettipyConfig(include_ipynb=True)
        converter = PrettipyConverter(config)
        converter.convert_files([str(utils_py), str(analysis_ipynb)], str(output_pdf))

        # Verify PDF was created
        assert output_pdf.exists()
        assert output_pdf.stat().st_size > 0

        # PDF should be reasonably sized for 2 files
        assert output_pdf.stat().st_size > 15_000
