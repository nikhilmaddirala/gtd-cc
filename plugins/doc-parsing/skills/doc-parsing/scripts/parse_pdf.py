#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pypdf>=4.0.0",
#   "pdfplumber>=0.11.0",
#   "markitdown>=0.0.1a2",
#   "pdfminer.six>=20221105",
# ]
# ///
"""
Parse PDF (Portable Document Format) files using multiple Python methods.

This script extracts content from PDF files using four different methods, each
optimized for different use cases: basic text, table extraction, consistency with other
formats, or layout-aware extraction.

Output structure for each file:
    output_dir/filename.pdf/
    ├── parsing_results.json           # File-level metadata and method results    ├── pypdf/                     # Method 1 output
    │   ├── content.md                # Text with page numbers    │   └── metadata.json          # PDF metadata (pages, metadata)    ├── pdfplumber/                 # Method 2 output
    │   ├── content.md              # Text with page numbers    │   ├── tables/                # Extracted tables as JSON
    │   │   ├── page_1_table_1.json
    │   │   ├── page_2_table_1.json
    │   │   └── ...
    │   └── (tables included in content.md)    ├── markitdown/                 # Method 3 output
    │   └── content.md              # Text-only extraction
    └── pdfminer/                   # Method 4 output        └── content.txt             # Layout-aware text extraction

Methods:

1. pypdf - Extract text using pypdf library
   - Basic text extraction with page numbering
   - Extracts PDF metadata
   - Simple and reliable
   - Output: Markdown text with page structure + metadata.json

   CLI alternative: Pandoc
   - Command: nix run nixpkgs#pandoc -- pandoc "$SOURCE_FILE" -t markdown -o content.md
   - Advantages: Fast conversion, multiple output formats
   - Disadvantages: Limited PDF support, may struggle with complex layouts

2. pdfplumber - Extract text and tables using pdfplumber
   - Advanced PDF parsing with table extraction
   - Extracts tables as JSON for programmatic access
   - Maintains text structure
   - Output: Markdown text + tables as JSON files

   CLI alternative: None (Python library is best option for table extraction)

3. markitdown - Extract text using markitdown library
   - Microsoft tool for converting documents to Markdown
   - Fast text-only extraction
   - Maintains document structure (headings, paragraphs)
   - No image extraction
   - Output: Markdown text only

   CLI alternative: markitdown CLI
   - Command: uvx --from 'markitdown[pdf]' markitdown "$SOURCE_FILE" > content.md
   - C library required: nixpkgs#stdenv.cc.cc.lib
   - Advantages: Same as library, faster for batch processing
   - Disadvantages: No image extraction

4. pdfminer.six - Layout-aware text extraction
   - PDFMiner for layout-conscious text extraction
   - Handles complex PDFs with multiple columns
   - Configurable layout analysis
   - Output: Plain text with layout preserved

   CLI alternative: LibreOffice HTML
   - Command: nix shell nixpkgs#libreoffice --command bash -c "libreoffice --headless --convert-to html:HTML '$SOURCE_FILE'"
   - Advantages: Creates visual HTML representation, preserves formatting well
   - Disadvantages: HTML output, no direct image extraction
   - HTML to Markdown: Use pandoc: pandoc $FILENAME_NOEXT.html -t markdown -o content.md

Usage:
    ./parse_pdf.py <file_path> <output_dir>

Arguments:
    file_path  - Path to PDF file to parse
    output_dir  - Directory where parsed content will be created

Example:
    ./parse_pdf.py /path/to/document.pdf /path/to/output

Dependencies:
    - pypdf>=4.0.0 - Basic PDF text extraction
    - pdfplumber>=0.11.0 - Advanced PDF parsing with table extraction
    - markitdown>=0.0.1a2 - Microsoft document conversion
    - pdfminer.six>=20221105 - Layout-aware PDF text extraction

All dependencies are specified in inline metadata above. Use `uv` to install automatically.

Output Metadata:
    Creates parsing_results.json in output directory with:
    - timestamp: ISO timestamp of parsing
    - source_file: Absolute path to source file
    - output_dir: Output directory path
    - methods: Dict of method_name -> success (bool)
    - success_count: Number of successful methods

Notes:

Method comparison:

pypdf:
- Advantages: Simple, reliable, includes metadata
- Disadvantages: Limited table support, basic text extraction
- Best for: General-purpose text extraction from simple PDFs
- Source: https://pypdf.readthedocs.io/

pdfplumber:
- Advantages: Table extraction, handles complex layouts, detailed text
- Disadvantages: Slower than pypdf, more complex
- Best for: PDFs with tables, complex layouts
- Source: https://github.com/jsvine/pdfplumber

markitdown:
- Advantages: Fast, Microsoft-maintained, consistent with other formats
- Disadvantages: No image extraction, simplified table formatting
- Best for: Quick text extraction, consistent cross-format processing
- Source: https://github.com/microsoft/markitdown

pdfminer.six:
- Advantages: Layout-aware, handles complex PDFs, configurable
- Disadvantages: More complex setup, slower
- Best for: Complex PDFs with multiple columns, non-standard layouts
- Source: https://pdfminer.six.readthedocs.io/

CLI alternatives (via nix) detailed:

Pandoc:
- Command: nix run nixpkgs#pandoc -- pandoc "$SOURCE_FILE" -t markdown -o content.md
- Basic PDF to Markdown conversion
- With custom formatting: pandoc "$SOURCE_FILE" -t gfm --markdown-headings=atx --wrap=none -o content.md
- Advantages: Fast, multiple output formats, cross-platform
- Disadvantages: Limited PDF support, may struggle with complex layouts or images
- Best for: Clean, text-based PDFs
- Source: https://pandoc.org/MANUAL.html

Docling CLI:
- Command: nix shell nixpkgs#stdenv.cc.cc.lib --command bash -c "export LD_LIBRARY_PATH=$(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:$LD_LIBRARY_PATH && uvx --from docling docling '$SOURCE_FILE' --to md --output ./"
- Comprehensive PDF to Markdown conversion with image extraction using IBM's Docling library
- Without OCR (faster for text-based PDFs): Add --no-ocr flag
- Advantages: Excellent for PDFs with complex layouts, extracts text/tables/images, supports OCR for scanned documents
- Disadvantages: Requires heavy dependencies (PyTorch), slower
- Best for: Complex PDFs, best quality extraction
- C library required: nixpkgs#stdenv.cc.cc.lib
- Source: https://github.com/docling-project/docling

LibreOffice HTML:
- Command: nix shell nixpkgs#libreoffice --command bash -c "libreoffice --headless --convert-to html:HTML '$SOURCE_FILE'"
- Creates visual HTML representation with structured content
- Convert HTML to Markdown: pandoc $FILENAME_NOEXT.html -t markdown -o content.md
- Advantages: Preserves formatting well, HTML can be further processed to Markdown
- Disadvantages: HTML output (not direct Markdown), no direct image extraction as files
- Best for: Visual reference and maintaining layout
- Source: https://help.libreoffice.org/latest/en-US/text/swriter/guide/convert.html

OCR Considerations:
Some PDFs are scanned images requiring OCR (Optical Character Recognition):
- Docling (Method 2 CLI alternative) supports OCR with multiple engines (tesseract, rapidocr, etc.)
- For OCR-enabled extraction, Docling is the recommended method
- Other methods (pypdf, pdfplumber, markitdown, pdfminer) work best with text-based PDFs
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from pypdf import PdfReader
import pdfplumber
from markitdown import MarkItDown
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO


def parse_method1_pypdf(source_file, output_dir):
    """
    Method 1: pypdf for text extraction

    Extracts text from PDF file using pypdf library with page numbering.
    Captures PDF metadata including number of pages and document metadata.

    Advantages:
    - Simple and reliable
    - Includes PDF metadata
    - Page-by-page structure
    - Lightweight

    Disadvantages:
    - Limited table support
    - Basic text extraction
    - May struggle with complex layouts

    When to use:
    - General-purpose text extraction
    - Simple PDFs without complex layouts
    - When PDF metadata is needed
    - When page numbering is sufficient

    Output:
    - content.md: Text content organized by page number
    - metadata.json: PDF metadata including pages count and document metadata

    Dependencies: pypdf>=4.0.0

    CLI alternative: Pandoc
    - Command: nix run nixpkgs#pandoc -- pandoc "$SOURCE_FILE" -t markdown -o content.md
    - Advantages: Fast, multiple output formats
    - Disadvantages: Limited PDF support
    """
    print("    Method 1: pypdf...")
    method_dir = output_dir / "pypdf"
    method_dir.mkdir(exist_ok=True)

    try:
        reader = PdfReader(source_file)

        # Extract text from all pages
        text_content = []
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                text_content.append(f"\n## Page {page_num}\n\n{text}")

        # Save text content
        with open(method_dir / "content.md", "w") as f:
            f.write("\n\n".join(text_content))

        # Save metadata
        metadata = {
            "pages": len(reader.pages),
            "metadata": {k: str(v) for k, v in reader.metadata.items()}
            if reader.metadata
            else {},
        }

        with open(method_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        print(f"      ✓ Extracted text from {len(reader.pages)} pages")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method2_pdfplumber(source_file, output_dir):
    """
    Method 2: pdfplumber for text and tables

    Extracts text and tables from PDF file using pdfplumber library.
    Handles tables well and extracts them as JSON for programmatic access.

    Advantages:
    - Advanced PDF parsing
    - Excellent table extraction
    - Handles complex layouts
    - Tables extracted as JSON

    Disadvantages:
    - Slower than pypdf
    - More complex
    - Higher memory usage

    When to use:
    - PDFs with tables
    - Complex layouts
    - When table data needs programmatic access
    - When detailed text extraction is required

    Output:
    - content.md: Text content organized by page number
    - tables/: Directory with tables as JSON (page_N_table_M.json)
      Each table JSON is an array of arrays (rows and cells)

    Dependencies: pdfplumber>=0.11.0
    """
    print("    Method 2: pdfplumber...")
    method_dir = output_dir / "pdfplumber"
    method_dir.mkdir(exist_ok=True)
    tables_dir = method_dir / "tables"
    tables_dir.mkdir(exist_ok=True)

    try:
        with pdfplumber.open(source_file) as pdf:
            # Extract text from all pages
            text_content = []
            table_count = 0

            for page_num, page in enumerate(pdf.pages, 1):
                # Extract text
                text = page.extract_text()
                if text and text.strip():
                    text_content.append(f"\n## Page {page_num}\n\n{text}")

                # Extract tables
                tables = page.extract_tables()
                for table_idx, table in enumerate(tables, 1):
                    table_count += 1
                    table_file = tables_dir / f"page_{page_num}_table_{table_idx}.json"
                    with open(table_file, "w") as f:
                        json.dump(table, f, indent=2)

            # Save text content
            with open(method_dir / "content.md", "w") as f:
                f.write("\n\n".join(text_content))

            print(
                f"      ✓ Extracted text from {len(pdf.pages)} pages and {table_count} tables"
            )
            return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method3_markitdown(source_file, output_dir):
    """
    Method 3: markitdown library

    Extracts text-only content from PDF file using Microsoft's markitdown library.
    Maintains document structure (headings, paragraphs) but does not extract images.

    Advantages:
    - Fast text extraction
    - Microsoft-maintained tool
    - Maintains document structure
    - Consistent with other format parsers (PPTX, DOCX)
    - Good for scanned PDFs (with OCR)

    Disadvantages:
    - Does not extract images
    - Table formatting may be simplified
    - Limited customization options

    When to use:
    - Quick text extraction when images aren't needed
    - When document structure is more important than images
    - For consistent processing across multiple formats
    - For scanned PDFs requiring OCR

    Output:
    - content.md: Markdown text with document structure

    Dependencies: markitdown>=0.0.1a2

    CLI alternative: markitdown CLI
    - Command: uvx --from 'markitdown[pdf]' markitdown "$SOURCE_FILE" > content.md
    - C library required: nixpkgs#stdenv.cc.cc.lib
    - Advantages: Same as library, faster for batch processing
    - Disadvantages: No image extraction
    - Source: https://github.com/microsoft/markitdown
    """
    print("    Method 3: markitdown...")
    method_dir = output_dir / "markitdown"
    method_dir.mkdir(exist_ok=True)

    try:
        md = MarkItDown()
        result = md.convert(str(source_file))

        with open(method_dir / "content.md", "w") as f:
            f.write(result.text_content)

        print(f"      ✓ Text extracted")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method4_pdfminer(source_file, output_dir):
    """
    Method 4: pdfminer.six for layout-aware text extraction

    Extracts text from PDF file using pdfminer.six with layout analysis.
    Handles complex PDFs with multiple columns and non-standard layouts.

    Advantages:
    - Layout-aware text extraction
    - Handles complex PDFs well
    - Configurable layout analysis
    - Preserves reading order

    Disadvantages:
    - More complex setup
    - Slower than simpler methods
    - Higher memory usage
    - Output is plain text (not Markdown)

    When to use:
    - Complex PDFs with multiple columns
    - Non-standard layouts
    - When reading order preservation is important
    - When simple text extraction fails

    Output:
    - content.txt: Plain text with layout preserved
    - Page count approximated from form feed characters

    Dependencies: pdfminer.six>=20221105
    """
    print("    Method 4: pdfminer.six...")
    method_dir = output_dir / "pdfminer"
    method_dir.mkdir(exist_ok=True)

    try:
        output_string = StringIO()

        with open(source_file, "rb") as fin:
            # Extract text with layout parameters
            extract_text_to_fp(
                fin, output_string, laparams=LAParams(), output_type="text", codec=None
            )

        text = output_string.getvalue()

        # Save text content
        with open(method_dir / "content.txt", "w") as f:
            f.write(text)

        # Count pages (approximate)
        page_count = text.count("\f") + 1 if text else 0

        print(f"      ✓ Extracted layout-aware text (approx. {page_count} pages)")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def main():
    if len(sys.argv) != 3:
        print("Usage: ./parse_pdf.py <file_path> <output_dir>")
        sys.exit(1)

    source_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not source_file.exists():
        print(f"Error: File not found: {source_file}")
        sys.exit(1)

    print(f"Parsing PDF: {source_file.name}")
    print(f"Output directory: {output_dir}")
    print()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run all parsing methods
    methods_success = {
        "method1_pypdf": parse_method1_pypdf(source_file, output_dir),
        "method2_pdfplumber": parse_method2_pdfplumber(source_file, output_dir),
        "method3_markitdown": parse_method3_markitdown(source_file, output_dir),
        "method4_pdfminer": parse_method4_pdfminer(source_file, output_dir),
    }

    success_count = sum(methods_success.values())
    print(f"\n  ✓ Completed: {success_count}/{len(methods_success)} methods successful")

    # Save results
    results = {
        "timestamp": datetime.now().isoformat(),
        "source_file": str(source_file),
        "output_dir": str(output_dir),
        "methods": methods_success,
        "success_count": success_count,
    }

    with open(output_dir / "parsing_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
