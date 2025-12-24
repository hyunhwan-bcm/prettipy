"""
Core PDF generation logic.

This module contains the main converter class that orchestrates
the entire PDF generation process.
"""

import html
from pathlib import Path
from typing import List, Optional, Dict
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors

from .config import PrettipyConfig
from .formatter import CodeFormatter
from .syntax import SyntaxHighlighter
from .styles import StyleManager
from .sorting import sort_files
from .tree import DirectoryTreeGenerator
from .ipynb_converter import NotebookConverter


class PrettipyConverter:
    """Main converter class for Python code to PDF."""

    def __init__(self, config: Optional[PrettipyConfig] = None):
        """
        Initialize the converter.

        Args:
            config: Optional configuration object. If None, uses defaults.
        """
        self.config = config or PrettipyConfig()
        self.formatter = CodeFormatter(max_width=self.config.max_line_width)
        self.highlighter = SyntaxHighlighter(enable_linking=self.config.enable_linking)
        self.style_manager = StyleManager(theme=self.config.theme)
        self.styles = self.style_manager.get_styles()
        self.notebook_converter = NotebookConverter(verbose=self.config.verbose)
        # Maps converted .py file paths to original .ipynb file paths
        self.ipynb_to_py_map: Dict[Path, Path] = {}

    def find_python_files(self, directory: Path) -> List[Path]:
        """
        Find all Python files in a directory, respecting exclusion rules.
        If include_ipynb is enabled, also converts .ipynb files to temporary .py files.

        Args:
            directory: Root directory to search

        Returns:
            List of Path objects for Python files (including converted notebooks), sorted according to config
        """
        py_files = []

        for pattern in self.config.include_patterns:
            for file_path in directory.rglob(pattern):
                if not self.config.should_exclude_path(file_path):
                    py_files.append(file_path)

        # If include_ipynb is enabled, also find and convert notebooks
        if self.config.include_ipynb:
            for ipynb_path in directory.rglob("*.ipynb"):
                if not self.config.should_exclude_path(ipynb_path):
                    # Convert notebook to temporary Python file
                    temp_py_file = self.notebook_converter.create_temp_python_file(ipynb_path)
                    if temp_py_file:
                        # Store the mapping for later use in PDF generation
                        self.ipynb_to_py_map[temp_py_file] = ipynb_path
                        py_files.append(temp_py_file)
                        if self.config.verbose:
                            print(f"Converted {ipynb_path.name} to temporary Python file")
                    else:
                        if self.config.verbose:
                            print(f"Warning: Failed to convert notebook {ipynb_path}")

        # Apply sorting based on configuration
        try:
            sorted_files = sort_files(
                py_files, method=self.config.sort_method, reverse_deps=self.config.reverse_deps
            )
            return sorted_files
        except ValueError as e:
            # If dependency sorting fails (e.g., circular dependencies),
            # fall back to lexicographic sorting
            if self.config.verbose:
                print(f"Warning: {e}")
                print("Falling back to lexicographic sorting")
            return sort_files(py_files, method="lexicographic")

    def convert_directory(self, directory: str = ".", output: Optional[str] = None):
        """
        Convert all Python files in a directory to PDF.

        Args:
            directory: Directory path to scan for Python files
            output: Output PDF file path (overrides config)

        Raises:
            FileNotFoundError: If directory doesn't exist
            PermissionError: If unable to write output file
        """
        root = Path(directory).resolve()

        if not root.exists():
            raise FileNotFoundError(f"Directory not found: {root}")

        if not root.is_dir():
            raise NotADirectoryError(f"Not a directory: {root}")

        output_path = output or self.config.output_file
        py_files = self.find_python_files(root)

        if not py_files:
            print(f"No Python files found in {root}")
            return

        if self.config.verbose:
            print(f"Found {len(py_files)} Python files")
            for f in py_files:
                # For converted notebooks, show the original path
                if f in self.ipynb_to_py_map:
                    display_f = self.ipynb_to_py_map[f]
                    try:
                        print(f"  - {display_f.relative_to(root)} (from .ipynb)")
                    except ValueError:
                        print(f"  - {display_f} (from .ipynb)")
                else:
                    try:
                        print(f"  - {f.relative_to(root)}")
                    except ValueError:
                        print(f"  - {f}")

        self._generate_pdf(root, py_files, output_path)

    def convert_files(self, files: List[str], output: Optional[str] = None):
        """
        Convert specific Python files to PDF.

        Args:
            files: List of file paths to convert
            output: Output PDF file path (overrides config)

        Raises:
            FileNotFoundError: If any file doesn't exist
        """
        file_paths = []
        for f in files:
            path = Path(f)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")
            file_paths.append(path)

        output_path = output or self.config.output_file

        # Use common parent as root
        root = Path.cwd()

        self._generate_pdf(root, file_paths, output_path)

    def _create_code_block(self, highlighted_lines: List[str]) -> List:
        """
        Create a code block from highlighted lines.
        
        This method creates individual Paragraph elements for each line
        to ensure proper line spacing and prevent overlapping text.
        
        Args:
            highlighted_lines: List of HTML-highlighted code lines
            
        Returns:
            List of flowable elements to add to the story
        """
        # Create a table with one column to simulate a bordered code block
        # Each row contains one line of code
        table_data = []
        for line in highlighted_lines:
            # Create a paragraph for each line with no vertical spacing
            para = Paragraph(line, self.styles["code_line"])
            table_data.append([para])
        
        # Create the table
        code_table = Table(
            table_data,
            colWidths=[None],  # Auto width
        )
        
        # Apply table styling to create the code block appearance
        code_table.setStyle(
            TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8f8f8")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#e0e0e0")),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ])
        )
        
        return [code_table, Spacer(1, 10)]

    def _generate_pdf(self, root: Path, files: List[Path], output_path: str):
        """
        Generate the PDF document.

        Args:
            root: Root directory for relative path calculation
            files: List of Python files to include
            output_path: Output PDF file path
        """
        # Page size
        page_size = A4 if self.config.page_size.lower() == "a4" else letter

        # Create document
        margins = self.style_manager.get_page_margins()
        doc = SimpleDocTemplate(
            output_path,
            pagesize=page_size,
            topMargin=margins[0],
            bottomMargin=margins[1],
            leftMargin=margins[2],
            rightMargin=margins[3],
        )

        story = []

        # Pre-analyze all files for linking if enabled
        if self.config.enable_linking:
            for file_path in files:
                try:
                    code = file_path.read_text(encoding="utf-8")
                    # Wrap lines before analyzing for linking
                    # This ensures symbol tracking matches what will be highlighted
                    lines = code.split("\n")
                    wrapped_lines = [wrapped_line for line in lines for wrapped_line in self.formatter.wrap_line(line)]
                    wrapped_code = "\n".join(wrapped_lines)
                    self.highlighter.prepare_for_linking(wrapped_code, clear_existing=False)
                except Exception:
                    continue
            # Reset anchors so they can be created during the actual highlighting phase
            self.highlighter.reset_anchors()

        # Title page
        title = self.config.title or f"Python Scripts from {root.name}/"
        story.append(Paragraph(html.escape(title), self.styles["title"]))
        story.append(Paragraph(f"<b>Total files:</b> {len(files)}", self.styles["info"]))
        story.append(
            Paragraph(f"<b>Generated from:</b> {html.escape(str(root))}", self.styles["info"])
        )
        story.append(Spacer(1, 0.3 * 72))  # 0.3 inch

        # Create anchor mapping for directory tree links
        file_to_anchor = {}
        tree_anchor_name = "directory_tree"
        tree_anchor_exists = False

        # Add directory tree if enabled
        if self.config.show_directory_tree:
            tree_generator = DirectoryTreeGenerator(max_depth=self.config.directory_tree_max_depth)

            try:
                # For the tree, we need to map display paths (original .ipynb) to their anchors
                # Create a list of display files for the tree
                display_files = []
                for f in files:
                    if f in self.ipynb_to_py_map:
                        # Use the original .ipynb path for display
                        display_files.append(self.ipynb_to_py_map[f])
                    else:
                        display_files.append(f)
                
                # Generate tree with links to file pages
                tree_html, file_to_anchor = tree_generator.generate_linked_tree_html(
                    root, display_files, self.config.exclude_dirs
                )

                # Add tree heading
                story.append(
                    Paragraph(
                        f'<a name="{tree_anchor_name}"/><b>📂 Directory Structure</b>',
                        self.styles["info"],
                    )
                )
                story.append(Spacer(1, 0.1 * 72))
                tree_anchor_exists = True

                # Add the tree
                story.append(Paragraph(tree_html, self.styles["tree"]))
                story.append(Spacer(1, 0.2 * 72))

            except Exception as e:
                if self.config.verbose:
                    print(f"Warning: Failed to generate directory tree: {e}")

        # If linking is enabled, mark all known definitions as having anchors
        # This allows forward references (linking to a class defined later)
        if self.config.enable_linking and self.highlighter.symbol_tracker:
            for symbol in self.highlighter.symbol_tracker.definitions.keys():
                self.highlighter.symbol_tracker.mark_anchor_created(symbol)

        # Process each file
        for idx, file_path in enumerate(files):
            if idx > 0:
                story.append(PageBreak())

            # Check if this is a converted notebook file
            original_ipynb_path = self.ipynb_to_py_map.get(file_path)
            
            # Determine the display path and file to read from
            if original_ipynb_path:
                # For converted notebooks, show the original .ipynb name in PDF
                try:
                    display_path = original_ipynb_path.relative_to(root)
                except ValueError:
                    display_path = original_ipynb_path
                # Use a notebook emoji for .ipynb files
                file_emoji = "📓"
            else:
                # For regular .py files
                try:
                    display_path = file_path.relative_to(root)
                except ValueError:
                    display_path = file_path
                file_emoji = "📄"

            # Get anchor for this file if directory tree is enabled
            anchor_name = (
                file_to_anchor.get(str(display_path), "") if self.config.show_directory_tree else ""
            )

            back_link_html = ""
            if tree_anchor_exists:
                back_link_html = f' <font size="9"><a href="#{tree_anchor_name}" color="blue"><u>← Back</u></a></font>'

            # File header with emoji, anchor, and back link
            if anchor_name:
                # Add anchor to the file header so links from tree work
                file_header_html = f'<a name="{anchor_name}"/>{file_emoji} {html.escape(str(display_path))}'
            else:
                file_header_html = f"{file_emoji} {html.escape(str(display_path))}"

            if back_link_html:
                file_header_html = f"{file_header_html}{back_link_html}"

            story.append(Paragraph(file_header_html, self.styles["file_header"]))

            # Process file content
            try:
                code = file_path.read_text(encoding="utf-8")

                # Split into lines and wrap long lines before highlighting
                # This prevents ReportLab from wrapping HTML-laden text incorrectly
                lines = code.split("\n")
                wrapped_lines = [wrapped_line for line in lines for wrapped_line in self.formatter.wrap_line(line)]
                
                # Join back into code string
                wrapped_code = "\n".join(wrapped_lines)

                # Highlight with multiline awareness
                # This correctly handles triple-quoted strings and other multiline constructs
                highlighted_lines = self.highlighter.highlight_code_multiline_aware(wrapped_code)

                # Create code block using individual paragraphs for each line
                # This prevents line overlapping issues that occur with <br/> tags
                code_elements = self._create_code_block(highlighted_lines)
                story.extend(code_elements)

            except Exception as e:
                error_msg = f"Error reading file: {html.escape(str(e))}"
                story.append(Paragraph(f"<i>{error_msg}</i>", self.styles["error"]))

        # Build PDF
        doc.build(story)

        print(f"✓ Created {output_path} with {len(files)} files")
