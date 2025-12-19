# Prettipy - Quick Start Guide

Your Python code to PDF converter is ready! Here's how to get started.

## What You Have Now

A complete, professional Python package with:
- ✅ Modular, well-documented code
- ✅ Beautiful CLI with progress bars
- ✅ Comprehensive tests
- ✅ Configuration system
- ✅ Ready for PyPI publication

## Immediate Next Steps

### 1. Customize Your Information

Update these files with your details:

**`pyproject.toml`**:
```toml
[project]
authors = [
    {name = "Your Name", email = "your.email@example.com"}  # Change this
]

[project.urls]
Homepage = "https://github.com/yourusername/prettipy"      # Change this
Repository = "https://github.com/yourusername/prettipy.git" # Change this
```

**`src/prettipy/__init__.py`**:
```python
__author__ = "Your Name"        # Change this
__email__ = "your.email@example.com"  # Change this
```

**`README.md`**:
- Update the repository URLs
- Update contact information at the bottom

**`LICENSE`**:
- Update the copyright year and name

### 2. Install and Test Locally

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[rich]"

# Test the CLI
prettipy --version
prettipy --help

# Try it out!
prettipy . -o test_output.pdf
```

### 3. Run Tests

```bash
# Install dev dependencies
pip install -e ".[dev,rich]"

# Run tests
pytest

# Run with coverage
pytest --cov=prettipy
```

## Publishing to PyPI

### Before Publishing

1. **Test everything works**:
   ```bash
   prettipy ./examples -o test.pdf
   python examples/basic_usage.py
   ```

2. **Update your information** (see step 1 above)

3. **Create GitHub repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/prettipy.git
   git push -u origin main
   ```

### Publish to PyPI

1. **Install build tools**:
   ```bash
   pip install build twine
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```

3. **Test on TestPyPI first** (recommended):
   ```bash
   twine upload --repository testpypi dist/*
   ```

4. **Publish to real PyPI**:
   ```bash
   twine upload dist/*
   ```

5. **Install from PyPI**:
   ```bash
   pip install prettipy
   ```

See [SETUP.md](SETUP.md) for detailed publishing instructions.

## Using Your Package

### Command Line

```bash
# Convert current directory
prettipy

# Convert specific directory
prettipy /path/to/project -o project.pdf

# Convert specific files
prettipy -f main.py utils.py -o core.pdf

# Use custom settings
prettipy --width 100 --page-size a4 --title "My Project"

# Generate config file
prettipy --init-config
prettipy --config prettipy-config.json
```

### Python API

```python
from prettipy import PrettipyConverter, PrettipyConfig

# Basic usage
converter = PrettipyConverter()
converter.convert_directory("./src", "output.pdf")

# With custom config
config = PrettipyConfig(
    max_line_width=100,
    page_size='a4',
    title='My Project'
)
converter = PrettipyConverter(config)
converter.convert_directory("./src")
```

## Project Structure

```
prettipy/
├── src/prettipy/           # Source code
│   ├── __init__.py         # Package initialization
│   ├── __main__.py         # python -m prettipy
│   ├── cli.py              # Command-line interface
│   ├── config.py           # Configuration
│   ├── core.py             # PDF generation
│   ├── formatter.py        # Line wrapping
│   ├── styles.py           # PDF styling
│   └── syntax.py           # Syntax highlighting
├── tests/                  # Test suite
├── examples/               # Usage examples
├── pyproject.toml          # Package config
├── README.md               # Documentation
├── LICENSE                 # MIT License
├── SETUP.md                # Setup guide
├── CONTRIBUTING.md         # Contribution guide
└── QUICKSTART.md           # This file
```

## Features

- 🎨 GitHub-style syntax highlighting
- 📦 Smart line wrapping at natural break points
- 🎯 Convert directories or specific files
- ⚙️ Highly configurable (colors, fonts, page size)
- 🚀 Beautiful CLI with rich formatting
- 📋 Progress indicators
- 🔍 Smart directory filtering (excludes venv, __pycache__, etc.)
- 📄 Professional PDF layout

## Next Steps

1. ✅ Test locally
2. ✅ Update your information
3. ✅ Create GitHub repository
4. ✅ Publish to TestPyPI
5. ✅ Publish to PyPI
6. ✅ Share with the world!

## Need Help?

- See [README.md](README.md) for full documentation
- See [SETUP.md](SETUP.md) for publishing guide
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
- Check the [examples/](examples/) directory for usage examples

## What Makes This Special

Your package is:
- **Modular**: Clean separation of concerns
- **Well-documented**: Docstrings, README, guides
- **Tested**: Comprehensive test suite
- **Professional**: Follows Python packaging best practices
- **User-friendly**: Beautiful CLI and clear error messages
- **Configurable**: JSON config files and CLI options
- **Modern**: Uses pyproject.toml, type hints, modern tools

Enjoy your new package! 🎉
