# 📄 Prettipy

**Beautiful Python Code to PDF Converter**

Transform your Python source code into professionally formatted, syntax-highlighted PDF documents with ease.

[![PyPI version](https://badge.fury.io/py/prettipy.svg)](https://badge.fury.io/py/prettipy)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

- 🎨 **Syntax Highlighting**: Beautiful, GitHub-style syntax highlighting using Pygments
- 📦 **Smart Line Wrapping**: Intelligently wraps long lines at natural break points
- 🎯 **Multiple Input Modes**: Convert entire directories or specific files
- ⚙️ **Highly Configurable**: Customize colors, fonts, page size, and more
- 🚀 **CLI & Python API**: Use from command line or integrate into your projects
- 📋 **Rich Output**: Beautiful progress bars and formatted output (when `rich` is installed)
- 🔍 **Smart Filtering**: Automatically excludes common directories like `venv`, `__pycache__`, etc.
- 📄 **Professional Layout**: Clean, readable formatting with proper spacing and margins
- 📧 **Kindle Delivery**: Send generated PDFs directly to your Kindle device via email

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

## 📧 Send to Kindle

Prettipy includes a convenient feature to send generated PDFs directly to your Kindle device or app.

### Setup

1. **Find Your Kindle Email Address**
   - Go to [Amazon Account Settings](https://www.amazon.com/hz/mycd/digital-console/contentlist/)
   - Navigate to "Preferences" > "Personal Document Settings"
   - Your Kindle email will be something like `yourname@kindle.com`

2. **Approve Your Sender Email**
   - In the same settings page, find "Approved Personal Document E-mail List"
   - Add the email address you'll send from (e.g., your Gmail address)

3. **Set Up SMTP Credentials**
   - For Gmail, create an [App Password](https://myaccount.google.com/apppasswords)
   - Set environment variables:
     ```bash
     export KINDLE_EMAIL="yourname@kindle.com"
     export SMTP_USER="your.email@gmail.com"
     export SMTP_PASS="your-app-password"
     ```

### Usage

```python
from prettipy import PrettipyConverter, send_to_kindle

# Generate a PDF
converter = PrettipyConverter()
converter.convert_directory("./my_project", output="project.pdf")

# Send to Kindle using environment variables
send_to_kindle("project.pdf")

# Or provide credentials explicitly
send_to_kindle(
    pdf_path="project.pdf",
    kindle_email="yourname@kindle.com",
    smtp_user="your.email@gmail.com",
    smtp_pass="your-app-password",
    subject="My Python Project"
)

# Use custom SMTP server
send_to_kindle(
    pdf_path="project.pdf",
    kindle_email="yourname@kindle.com",
    smtp_user="user@custom.com",
    smtp_pass="password",
    smtp_host="smtp.custom.com",
    smtp_port=587
)
```

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `KINDLE_EMAIL` | Your Kindle email address | `yourname@kindle.com` |
| `SMTP_USER` | SMTP username (your email) | `your.email@gmail.com` |
| `SMTP_PASS` | SMTP password or app password | `your-app-password` |

### Notes

- PDFs typically appear in your Kindle library within a few minutes
- Maximum file size is 50MB per document
- The default SMTP server is Gmail (`smtp.gmail.com:587`)
- For Gmail, you must use an app-specific password if 2FA is enabled
- The sender email must be approved in your Amazon account settings

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

---

Made with ❤️ by developers, for developers.
