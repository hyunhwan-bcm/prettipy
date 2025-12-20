# Setup Guide for Prettipy

This guide will help you set up Prettipy for development or prepare it for publishing to PyPI.

## 📑 Table of Contents

- [For Users](#for-users)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
- [For Developers](#for-developers)
  - [Initial Setup](#initial-setup)
  - [Project Structure](#project-structure)
  - [Running Tests](#running-tests)
  - [Code Quality](#code-quality)
  - [Testing Locally](#testing-locally)
- [Publishing to PyPI](#publishing-to-pypi)
  - [Prerequisites](#prerequisites)
  - [Build the Package](#build-the-package)
  - [Test on TestPyPI](#test-on-testpypi)
  - [Publish to PyPI](#publish-to-pypi-1)
  - [Post-Publication](#post-publication)
- [Version Management](#version-management)
- [Troubleshooting](#troubleshooting)
  - [Import Errors](#import-errors)
  - [Missing Dependencies](#missing-dependencies)
  - [Build Failures](#build-failures)
- [Resources](#resources)

## For Users

### Installation

```bash
# Install from PyPI (when published)
pip install prettipy

# Install with rich formatting support
pip install prettipy[rich]
```

### Quick Start

```bash
# Convert current directory
prettipy

# Get help
prettipy --help

# Generate sample config
prettipy --init-config
```

## For Developers

### Initial Setup

1. **Clone the repository** (or download your code):
   ```bash
   git clone <your-repo-url>
   cd prettipy
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e ".[dev,rich]"
   ```

### Project Structure

```
prettipy/
├── src/prettipy/          # Source code
│   ├── __init__.py        # Package initialization
│   ├── __main__.py        # Entry point for python -m
│   ├── cli.py             # Command-line interface
│   ├── config.py          # Configuration management
│   ├── core.py            # Core PDF generation
│   ├── formatter.py       # Line wrapping logic
│   ├── styles.py          # PDF styling
│   └── syntax.py          # Syntax highlighting
├── tests/                 # Test files
├── examples/              # Example scripts and configs
├── pyproject.toml         # Package configuration
├── README.md              # Main documentation
└── LICENSE                # MIT License
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=prettipy

# Run specific test file
pytest tests/test_formatter.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code with black
black src/prettipy tests

# Lint with flake8
flake8 src/prettipy tests

# Type check with mypy
mypy src/prettipy
```

### Testing Locally

Before publishing, test the package locally:

```bash
# Install in development mode
pip install -e ".[rich]"

# Test CLI
prettipy --version
prettipy --help
prettipy --init-config

# Test on a sample directory
prettipy ./examples -o test_output.pdf
```

## Publishing to PyPI

### Prerequisites

1. **Create PyPI account**:
   - Create account at [https://pypi.org](https://pypi.org)
   - Create account at [https://test.pypi.org](https://test.pypi.org) for testing

2. **Install build tools**:
   ```bash
   pip install build twine
   ```

3. **Update package information**:
   - Edit `pyproject.toml`:
     - Update `authors` with your name and email
     - Update `urls` with your GitHub repository
     - Verify version number
   - Edit `src/prettipy/__init__.py`:
     - Update `__author__` and `__email__`
   - Edit `README.md`:
     - Update contact information
     - Update repository URLs

### Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distribution packages
python -m build
```

This creates:
- `dist/prettipy-0.1.0-py3-none-any.whl` (wheel)
- `dist/prettipy-0.1.0.tar.gz` (source distribution)

### Test on TestPyPI

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Install from TestPyPI to test
pip install --index-url https://test.pypi.org/simple/ prettipy
```

### Publish to PyPI

When everything works on TestPyPI:

```bash
# Upload to PyPI
twine upload dist/*
```

### Post-Publication

1. **Install from PyPI**:
   ```bash
   pip install prettipy
   ```

2. **Test installation**:
   ```bash
   prettipy --version
   prettipy --help
   ```

3. **Create a git tag**:
   ```bash
   git tag -a v0.1.0 -m "Release version 0.1.0"
   git push origin v0.1.0
   ```

## Version Management

When releasing new versions:

1. Update version in `pyproject.toml`
2. Update version in `src/prettipy/__init__.py`
3. Update CHANGELOG (if you create one)
4. Create git tag
5. Build and publish

## Troubleshooting

### Import Errors

If you get import errors:
```bash
pip install -e .
```

### Missing Dependencies

```bash
pip install -r requirements.txt  # If you create one
# Or:
pip install reportlab pygments rich
```

### Build Failures

```bash
# Clean everything
rm -rf build/ dist/ *.egg-info
pip cache purge

# Rebuild
python -m build
```

## Resources

- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Documentation](https://pypi.org/help/)
- [Twine Documentation](https://twine.readthedocs.io/)
- [setuptools Documentation](https://setuptools.pypa.io/)
