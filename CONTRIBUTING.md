# Contributing to Prettipy

Thank you for your interest in contributing to Prettipy! This document provides guidelines and instructions for contributing.

## Code of Conduct

Be respectful, inclusive, and professional in all interactions. We're all here to make Prettipy better!

## How to Contribute

### Reporting Bugs

If you find a bug:

1. Check if it's already reported in [Issues](https://github.com/yourusername/prettipy/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Code samples or screenshots if applicable

### Suggesting Features

We welcome feature suggestions! Please:

1. Check existing issues first
2. Create a new issue describing:
   - The feature and its benefits
   - Use cases
   - Possible implementation approaches

### Pull Requests

1. **Fork the repository**

2. **Create a branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write clean, readable code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

4. **Set up pre-commit hooks** (recommended):
   ```bash
   pip install pre-commit
   pre-commit install
   ```
   This will automatically run black formatting and pytest before each commit.

5. **Test your changes**:
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Check code formatting
   black --check .
   
   # Or run all pre-commit hooks manually
   pre-commit run --all-files
   ```

6. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description"
   ```
   Use clear, descriptive commit messages.
   
   **Note:** If you've installed pre-commit hooks, they will run automatically before the commit.
   - **Black** will check code formatting (commits are rejected if code isn't formatted)
   - **Pytest** will run all tests (commits are rejected if tests fail)
   
   If hooks fail, fix the issues and try committing again.

7. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**:
   - Provide a clear title and description
   - Reference any related issues
   - Explain what changed and why
   
   **Note:** GitHub Actions CI will automatically run when you create a PR:
   - Tests will run on Python 3.8-3.12
   - Black formatting will be checked
   - PRs cannot be merged if CI checks fail

## Development Setup

See [SETUP.md](SETUP.md) for detailed setup instructions.

Quick start:
```bash
git clone <your-fork>
cd prettipy
python -m venv venv
source venv/bin/activate
pip install -e ".[dev,rich]"
pytest
```

### Pre-commit Hooks Setup

Pre-commit hooks help catch issues before they're committed:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hooks
pre-commit install

# (Optional) Run hooks on all files
pre-commit run --all-files
```

Once installed, hooks will automatically run on each commit:
- **Black**: Ensures code is properly formatted
- **Pytest**: Runs all tests to prevent broken code from being committed

If a hook fails, the commit is rejected. Fix the issues and try again.

### Continuous Integration (CI)

GitHub Actions automatically runs checks on all pushes and pull requests:

1. **Test Job**: Runs pytest on Python 3.8, 3.9, 3.10, 3.11, and 3.12
2. **Lint Job**: Validates code formatting with black

All CI checks must pass before a PR can be merged. You can view CI results in the "Checks" tab of your PR.

## Coding Guidelines

### Style

- Follow PEP 8
- Use `black` for formatting (line length: 100)
- Use type hints where appropriate
- Write docstrings for public functions/classes

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for good test coverage
- Use pytest fixtures for reusable test data

### Documentation

- Update README.md if adding features
- Add docstrings to new functions/classes
- Update SETUP.md if changing setup process
- Include examples for new features

## Project Structure

```
src/prettipy/
├── __init__.py     # Package initialization
├── cli.py          # Command-line interface
├── config.py       # Configuration management
├── core.py         # Main PDF generation logic
├── formatter.py    # Code formatting/wrapping
├── styles.py       # PDF styling
└── syntax.py       # Syntax highlighting
```

## Areas for Contribution

### Easy (Good First Issues)

- Add more color themes
- Improve error messages
- Add more examples
- Documentation improvements
- Add more tests

### Medium

- Add line numbering feature
- Support for more file types
- Table of contents generation
- Additional configuration options

### Advanced

- PDF bookmarks/navigation
- Custom syntax highlighting rules
- Performance optimizations
- Export to other formats (HTML, etc.)

## Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Once approved, your PR will be merged
4. Your contribution will be in the next release!

## Questions?

- Open an issue for questions
- Discussion section for general topics
- Check existing documentation first

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to Prettipy!
