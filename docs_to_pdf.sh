#!/bin/bash
# Script to convert Prettipy documentation to PDF format
# Requires: pandoc and pdflatex (texlive)

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored messages
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    print_error "pandoc is not installed. Please install it first:"
    echo ""
    echo "  macOS:     brew install pandoc"
    echo "  Ubuntu:    sudo apt-get install pandoc texlive-latex-base texlive-latex-recommended"
    echo "  Windows:   Download from https://pandoc.org/installing.html"
    echo ""
    exit 1
fi

print_info "pandoc found: $(pandoc --version | head -1)"

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    print_warning "pdflatex not found. PDF output quality may be reduced."
    print_warning "Consider installing: texlive-latex-base texlive-latex-recommended"
    PDF_ENGINE=""
else
    print_info "pdflatex found: $(pdflatex --version | head -1)"
    PDF_ENGINE="--pdf-engine=pdflatex"
fi

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Output directory
OUTPUT_DIR="${SCRIPT_DIR}/pdf_docs"
mkdir -p "$OUTPUT_DIR"

print_info "Output directory: $OUTPUT_DIR"
echo ""

# Convert individual files
print_info "Converting individual documentation files..."

for file in README.md QUICKSTART.md SETUP.md CONTRIBUTING.md; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        output="${OUTPUT_DIR}/${file%.md}.pdf"
        print_info "Converting $file -> ${file%.md}.pdf"
        pandoc "$SCRIPT_DIR/$file" \
            -o "$output" \
            --toc \
            --toc-depth=3 \
            $PDF_ENGINE \
            -V geometry:margin=1in \
            -V fontsize=11pt \
            -V documentclass=article \
            2>&1 | grep -v "Missing character" || true
    else
        print_warning "$file not found, skipping..."
    fi
done

echo ""
print_info "Creating complete documentation bundle..."

# Build list of files that exist
DOCS_TO_COMBINE=()
for file in README.md QUICKSTART.md SETUP.md CONTRIBUTING.md; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        DOCS_TO_COMBINE+=("$SCRIPT_DIR/$file")
    else
        print_warning "$file not found, excluding from bundle..."
    fi
done

# Only create combined PDF if we have at least one file
if [ ${#DOCS_TO_COMBINE[@]} -gt 0 ]; then
    pandoc "${DOCS_TO_COMBINE[@]}" \
        -o "$OUTPUT_DIR/prettipy-complete-documentation.pdf" \
        --toc \
        --toc-depth=3 \
        $PDF_ENGINE \
        -V geometry:margin=1in \
        -V fontsize=11pt \
        -V documentclass=article \
        -V title="Prettipy Complete Documentation" \
        -V author="Prettipy Project" \
        2>&1 | grep -v "Missing character" || true
else
    print_error "No documentation files found to combine!"
    exit 1
fi

echo ""
print_info "✅ Documentation conversion complete!"
echo ""
print_info "Generated files:"
ls -lh "$OUTPUT_DIR"/*.pdf 2>/dev/null | awk '{print "  - " $9 " (" $5 ")"}'
echo ""
print_info "PDF files saved in: $OUTPUT_DIR"
