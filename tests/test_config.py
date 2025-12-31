"""Tests for the configuration module."""

import pytest
import json
from pathlib import Path
from prettipy.config import PrettipyConfig


class TestPrettipyConfig:
    """Test cases for PrettipyConfig class."""

    def test_default_config(self):
        """Test default configuration."""
        config = PrettipyConfig()
        assert config.max_line_width == 79
        assert config.page_size == "letter"
        assert "venv" in config.exclude_dirs
        assert "__pycache__" in config.exclude_dirs

    def test_custom_config(self):
        """Test custom configuration."""
        config = PrettipyConfig(max_line_width=100, page_size="a4", verbose=True)
        assert config.max_line_width == 100
        assert config.page_size == "a4"
        assert config.verbose is True

    def test_should_exclude_path(self):
        """Test path exclusion logic."""
        config = PrettipyConfig()

        # Should exclude
        assert config.should_exclude_path(Path("venv/lib/python"))
        assert config.should_exclude_path(Path("project/__pycache__/file.pyc"))
        assert config.should_exclude_path(Path(".git/config"))

        # Should not exclude
        assert not config.should_exclude_path(Path("src/main.py"))
        assert not config.should_exclude_path(Path("utils/helper.py"))

    def test_save_and_load_config(self, tmp_path):
        """Test saving and loading configuration from file."""
        config_file = tmp_path / "test_config.json"

        # Create and save config
        original_config = PrettipyConfig(max_line_width=100, page_size="a4", title="Test Project")
        original_config.to_file(config_file)

        # Load config
        loaded_config = PrettipyConfig.from_file(config_file)

        assert loaded_config.max_line_width == 100
        assert loaded_config.page_size == "a4"
        assert loaded_config.title == "Test Project"

    def test_exclude_patterns(self):
        """Test exclude patterns functionality."""
        config = PrettipyConfig(exclude_patterns=["*_test.py"])
        assert config.should_exclude_path(Path("tests/example_test.py"))

    def test_source_url_config(self):
        """Test source_url configuration field."""
        # Test default value
        config = PrettipyConfig()
        assert config.source_url is None
        
        # Test custom value
        github_url = "https://github.com/hyunhwan-bcm/prettipy"
        config = PrettipyConfig(source_url=github_url)
        assert config.source_url == github_url

    def test_save_and_load_config_with_source_url(self, tmp_path):
        """Test saving and loading configuration with source_url from file."""
        config_file = tmp_path / "test_config_with_url.json"
        
        # Create and save config with source_url
        github_url = "https://github.com/hyunhwan-bcm/prettipy"
        original_config = PrettipyConfig(
            max_line_width=100, 
            source_url=github_url,
            title="Test Project"
        )
        original_config.to_file(config_file)
        
        # Load config
        loaded_config = PrettipyConfig.from_file(config_file)
        
        assert loaded_config.max_line_width == 100
        assert loaded_config.source_url == github_url
        assert loaded_config.title == "Test Project"
