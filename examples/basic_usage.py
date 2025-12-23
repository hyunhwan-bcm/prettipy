"""
Example: Basic usage of Prettipy API

This script demonstrates how to use Prettipy programmatically
to convert Python files to PDF.
"""

from prettipy import PrettipyConverter, PrettipyConfig

# Example 1: Basic usage with defaults
print("Example 1: Converting current directory with defaults...")
converter = PrettipyConverter()
converter.convert_directory(".", output="example1_output.pdf")

# Example 2: Custom configuration
print("\nExample 2: Converting with custom configuration...")
config = PrettipyConfig(
    max_line_width=100,
    page_size="a4",
    title="My Python Project Documentation",
    verbose=True,
    exclude_dirs={"venv", "__pycache__", ".git", "tests"},  # Also exclude tests for this example
)

converter = PrettipyConverter(config)
converter.convert_directory("./src", output="example2_custom.pdf")

# Example 3: Convert specific files
print("\nExample 3: Converting specific files...")
converter = PrettipyConverter()
converter.convert_files(files=["examples/basic_usage.py"], output="example3_single_file.pdf")

# Example 4: Load configuration from file
print("\nExample 4: Using configuration file...")
config = PrettipyConfig.from_file("examples/example-config.json")
converter = PrettipyConverter(config)
converter.convert_directory("./src", output="example4_from_config.pdf")

print("\nAll examples completed!")
