# 📄 Prettipy

**Beautiful Python Code to PDF Converter**

Transform your Python source code into professionally formatted, syntax-highlighted PDF documents with ease.

[![PyPI version](https://badge.fury.io/py/prettipy.svg)](https://badge.fury.io/py/prettipy)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📑 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
  - [Installation](#installation)
  - [Basic Usage](#basic-usage)
- [📖 Detailed Usage](#-detailed-usage)
  - [Command Line Interface](#command-line-interface)
  - [Examples](#examples)
  - [Python API](#python-api)
- [⚙️ Configuration](#️-configuration)
  - [Configuration File](#configuration-file)
  - [Configuration Options](#configuration-options)
- [🎨 Themes](#-themes)
- [🛠️ Development](#️-development)
  - [Setup Development Environment](#setup-development-environment)
  - [Run Tests](#run-tests)
  - [Code Quality](#code-quality)
- [📦 Building and Publishing](#-building-and-publishing)
  - [Build Package](#build-package)
  - [Publish to PyPI](#publish-to-pypi)
- [🤝 Contributing](#-contributing)
- [📋 Roadmap](#-roadmap)
- [📄 License](#-license)
- [🙏 Acknowledgments](#-acknowledgments)
- [📬 Contact](#-contact)
- [📚 Documentation as PDF](#-documentation-as-pdf)

## ✨ Features

- 🎨 **Syntax Highlighting**: Beautiful, GitHub-style syntax highlighting using Pygments
- 📦 **Smart Line Wrapping**: Intelligently wraps long lines at natural break points
- 🎯 **Multiple Input Modes**: Convert entire directories or specific files
- ⚙️ **Highly Configurable**: Customize colors, fonts, page size, and more
- 🚀 **CLI & Python API**: Use from command line or integrate into your projects
- 📋 **Rich Output**: Beautiful progress bars and formatted output (when `rich` is installed)
- 🔍 **Smart Filtering**: Automatically excludes common directories like `venv`, `__pycache__`, etc.
- 📄 **Professional Layout**: Clean, readable formatting with proper spacing and margins

## 🚀 Quick Start

### Installation

```bash
# Basic installation
pip install prettipy

# With rich formatting (recommended)
pip install prettipy[rich]
```

### Basic Usage

```bash
# Convert current directory
prettipy

# Convert specific directory
prettipy /path/to/your/project

# Convert specific files
prettipy -f script1.py script2.py utils.py

# Specify output file
prettipy -o my_code.pdf

# Custom line width
prettipy -w 100
```

## 📖 Detailed Usage

### Command Line Interface

```bash
usage: prettipy [-h] [-o OUTPUT] [-f FILES [FILES ...]] [-w WIDTH]
                [--config CONFIG] [-t TITLE] [--theme {default}]
                [--page-size {letter,a4}] [-v] [--version] [--init-config]
                [directory]

Convert Python code to beautifully formatted PDFs

positional arguments:
  directory             Directory to scan for Python files (default: current)

optional arguments:
  -h, --help            Show this help message and exit
  -o, --output OUTPUT   Output PDF file path (default: output.pdf)
  -f, --files FILES     Specific Python files to convert
  -w, --width WIDTH     Maximum line width before wrapping (default: 90)
  --config CONFIG       Path to configuration JSON file
  -t, --title TITLE     Custom title for the PDF document
  --theme {default}     Color theme to use
  --page-size {letter,a4}
                        PDF page size (default: letter)
  -v, --verbose         Enable verbose output
  --version             Show program's version number and exit
  --init-config         Generate a sample configuration file
```

### Examples

#### Convert Current Directory

```bash
prettipy
```

This will create `output.pdf` with all Python files from the current directory.

#### Convert With Custom Settings

```bash
prettipy /path/to/project \
  -o project_code.pdf \
  -w 100 \
  --title "My Awesome Project" \
  --page-size a4
```

#### Convert Specific Files

```bash
prettipy -f main.py utils.py models.py -o core_files.pdf
```

#### Use Configuration File

```bash
# Generate sample config
prettipy --init-config

# Edit prettipy-config.json, then use it
prettipy --config prettipy-config.json
```

### Python API

You can also use Prettipy programmatically in your Python code:

```python
from prettipy import PrettipyConverter, PrettipyConfig

# Basic usage with defaults
converter = PrettipyConverter()
converter.convert_directory("./my_project", output="project.pdf")

# Custom configuration
config = PrettipyConfig(
    max_line_width=100,
    page_size='a4',
    title='My Project Documentation',
    verbose=True
)

converter = PrettipyConverter(config)
converter.convert_directory("./src")

# Convert specific files
converter.convert_files(
    files=['main.py', 'utils.py', 'models.py'],
    output='core.pdf'
)
```

## ⚙️ Configuration

### Configuration File

Generate a sample configuration file:

```bash
prettipy --init-config
```

This creates `prettipy-config.json`:

```json
{
  "exclude_dirs": [
    ".git",
    "venv",
    "__pycache__",
    "node_modules"
  ],
  "exclude_patterns": [],
  "include_patterns": ["*.py"],
  "max_line_width": 90,
  "font_size": 9,
  "line_spacing": 14,
  "page_size": "letter",
  "title": null,
  "show_line_numbers": false,
  "theme": "default",
  "output_file": "output.pdf",
  "verbose": false
}
```

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `exclude_dirs` | list | See config | Directories to exclude |
| `exclude_patterns` | list | `[]` | File patterns to exclude |
| `include_patterns` | list | `["*.py"]` | File patterns to include |
| `max_line_width` | int | `90` | Max characters before wrapping |
| `font_size` | int | `9` | Font size for code |
| `line_spacing` | int | `14` | Line spacing in points |
| `page_size` | string | `"letter"` | Page size (letter/a4) |
| `title` | string | `null` | PDF title |
| `show_line_numbers` | bool | `false` | Show line numbers (future) |
| `theme` | string | `"default"` | Color theme |
| `output_file` | string | `"output.pdf"` | Default output path |
| `verbose` | bool | `false` | Verbose output |

## 🎨 Themes

Currently, Prettipy includes a beautiful default theme with GitHub-style syntax highlighting:

- **Keywords**: Green (`#007020`)
- **Functions**: Dark Blue (`#06287e`)
- **Classes**: Teal (`#0e7c7b`)
- **Strings**: Blue (`#4070a0`)
- **Numbers**: Green (`#40a070`)
- **Comments**: Gray-Blue (`#60a0b0`)

More themes coming soon!

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/prettipy.git
cd prettipy

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev,rich]"
```

### Run Tests

```bash
pytest
pytest --cov=prettipy  # With coverage
```

### Code Quality

```bash
# Format code
black src/prettipy

# Lint
flake8 src/prettipy

# Type checking
mypy src/prettipy
```

## 📦 Building and Publishing

### Build Package

```bash
# Install build tools
pip install build twine

# Build distribution
python -m build
```

This creates files in `dist/`:
- `prettipy-0.1.0-py3-none-any.whl`
- `prettipy-0.1.0.tar.gz`

### Publish to PyPI

```bash
# Test on TestPyPI first
twine upload --repository testpypi dist/*

# Then publish to PyPI
twine upload dist/*
```

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📋 Roadmap

- [ ] Additional color themes (Monokai, Solarized, etc.)
- [ ] Line numbering option
- [ ] Table of contents generation
- [ ] Support for more file types (JavaScript, Java, etc.)
- [ ] Customizable syntax highlighting rules
- [ ] PDF bookmarks for easy navigation
- [ ] Export to other formats (HTML, Markdown)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[ReportLab](https://www.reportlab.com/)** - PDF generation library
- **[Pygments](https://pygments.org/)** - Syntax highlighting
- **[Rich](https://rich.readthedocs.io/)** - Beautiful terminal output

## 📬 Contact

- **Author**: Hyun-Hwan Jeong
- **Email**: hyun-hwan.jeong@bcm.edu
- **GitHub**: [@hyunhwan-bcm](https://github.com/hyunhwan-bcm)

## 📚 Documentation as PDF

### Viewing Documentation as PDF

You can convert any of the project documentation files (README.md, QUICKSTART.md, SETUP.md, CONTRIBUTING.md) to PDF format using various tools:

#### Option 1: Using Pandoc (Recommended)

[Pandoc](https://pandoc.org/) is a universal document converter that produces high-quality PDFs:

```bash
# Install pandoc (macOS)
brew install pandoc

# Install pandoc (Ubuntu/Debian)
sudo apt-get install pandoc texlive-latex-base texlive-latex-recommended

# Install pandoc (Windows)
# Download from https://pandoc.org/installing.html

# Convert README to PDF
pandoc README.md -o README.pdf --pdf-engine=pdflatex

# Convert with table of contents
pandoc README.md -o README.pdf --toc --pdf-engine=pdflatex

# Convert all documentation files
pandoc README.md QUICKSTART.md SETUP.md CONTRIBUTING.md \
  -o prettipy-documentation.pdf --toc --pdf-engine=pdflatex
```

#### Option 2: Using grip (GitHub-style rendering)

```bash
# Install grip
pip install grip

# Render README as GitHub would (opens in browser)
grip README.md

# Then use your browser's "Print to PDF" feature
```

#### Option 3: Using markdown-pdf (Node.js)

```bash
# Install markdown-pdf
npm install -g markdown-pdf

# Convert to PDF
markdown-pdf README.md

# Convert all documentation
markdown-pdf README.md QUICKSTART.md SETUP.md CONTRIBUTING.md
```

#### Option 4: Online Converters

You can also use online Markdown to PDF converters:
- [Markdown to PDF](https://www.markdowntopdf.com/)
- [CloudConvert](https://cloudconvert.com/md-to-pdf)
- [Dillinger](https://dillinger.io/) (with export option)

### Complete Documentation Bundle

To create a complete PDF bundle of all documentation:

```bash
# Using Pandoc with custom styling
pandoc README.md QUICKSTART.md SETUP.md CONTRIBUTING.md \
  -o prettipy-complete-docs.pdf \
  --toc \
  --toc-depth=3 \
  --pdf-engine=pdflatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article
```

---

Made with ❤️ by developers, for developers.
