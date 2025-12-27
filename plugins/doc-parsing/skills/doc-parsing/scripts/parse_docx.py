#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-docx>=1.1.0",
#   "markitdown>=0.0.1a2",
#   "docx2txt>=0.8",
# ]
# ///
"""
Parse DOCX (Word) files using multiple Python methods.

This script extracts content from Microsoft Word documents using four different methods,
each optimized for different use cases: completeness, speed, detailed structure, or simplicity.

Output structure for each file:
    output_dir/filename.docx/
    ├── parsing_results.json           # File-level metadata and method results
    ├── python_docx_basic/            # Method 1 output
    │   ├── content.md                # Text content
    │   ├── images/                  # Extracted images
    │   └── (no readme needed - content is self-documenting)
    ├── markitdown/                  # Method 2 output
    │   └── content.md              # Text-only extraction
    ├── python_docx_detailed/         # Method 3 output
    │   ├── content.md              # Text with structure
    │   ├── table_1.json           # Tables as JSON
    │   ├── metadata.json           # Document metadata
    │   └── table_N.json
    ├── docx2txt/                  # Method 4 output
    │   ├── content.txt             # Plain text
    │   └── images/                # Extracted images

Methods:

1. python-docx (basic) - Extract text and images using python-docx library
   - Comprehensive extraction with text and images
   - Preserves paragraph structure
   - Fast and reliable
   - Output: Markdown text + images in images/ subdirectory

   CLI alternative: pandoc
   - Command: nix run nixpkgs#pandoc -- pandoc "$SOURCE_FILE" -t markdown --extract-media=./images -o content.md
   - Advantages: Better table handling, more formatting options
   - Disadvantages: Requires nix, more complex setup

2. markitdown - Extract text using markitdown library
   - Microsoft tool for converting documents to Markdown
   - Fast text-only extraction
   - Maintains document structure (headings, paragraphs)
   - Output: Markdown text only (no images)

   CLI alternative: markitdown CLI
   - Command: uvx --from 'markitdown[docx]' markitdown "$SOURCE_FILE" > content.md
   - C library required: nixpkgs#stdenv.cc.cc.lib
   - Advantages: Same as library, faster for batch processing
   - Disadvantages: No image extraction

3. python-docx (detailed) - Extract with tables, headers, and formatting
   - Most comprehensive Python-based extraction
   - Preserves heading structure and styles
   - Extracts tables as JSON for programmatic access
   - Captures document metadata (author, title, created/modified dates)
   - Output: Markdown with tables, table JSON files, metadata.json

   CLI alternative: None (Python library is best option for detailed extraction)

4. docx2txt - Simple text extraction with image links
   - Pure Python library for DOCX parsing
   - Extracts text and images
   - Outputs plain text (not Markdown-formatted)
   - Images saved to specified directory
   - Lightweight and fast
   - Output: Plain text + images

   CLI alternative: docx2txt CLI
   - Command: uvx --from docx2txt docx2txt -i ./images "$SOURCE_FILE" > content.txt
   - Advantages: Same as library, faster for batch processing
   - Disadvantages: No Markdown formatting

Usage:
    ./parse_docx.py <file_path> <output_dir>

Arguments:
    file_path  - Path to DOCX file to parse
    output_dir  - Directory where parsed content will be created

Example:
    ./parse_docx.py /path/to/document.docx /path/to/output

Dependencies:
    - python-docx>=1.1.0 - Word document parsing
    - markitdown>=0.0.1a2 - Microsoft document conversion
    - docx2txt>=0.8 - Simple DOCX text extraction

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

python-docx (basic):
- Advantages: Extracts text + images, preserves structure, fast
- Disadvantages: Limited table formatting, no document metadata
- Best for: General-purpose text and image extraction

markitdown:
- Advantages: Fast, Microsoft-maintained, consistent structure
- Disadvantages: No image extraction, simplified table formatting
- Best for: Quick text extraction when images aren't needed
- Source: https://github.com/microsoft/markitdown

python-docx (detailed):
- Advantages: Most comprehensive, preserves headings/tables, captures metadata
- Disadvantages: Slower than other methods, more complex output
- Best for: Full document analysis, table data extraction, metadata capture

docx2txt:
- Advantages: Lightweight, extracts images, plain text output
- Disadvantages: No Markdown formatting, simplified structure
- Best for: Simple text analysis, when formatting isn't critical
- Source: https://github.com/ankushshah89/python-docx2txt

CLI alternatives (via nix):

LibreOffice PDF:
- Command: nix shell nixpkgs#libreoffice --command bash -c "libreoffice --headless --convert-to pdf '$SOURCE_FILE'"
- Creates visual PDF representation
- Preserves original formatting exactly
- Does not produce machine-readable text
- Useful for: Visual reference, maintaining layout
- Source: https://help.libreoffice.org/latest/en-US/text/swriter/guide/convert.html
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from docx import Document
from markitdown import MarkItDown
import docx2txt


def parse_method1_python_docx(source_file, output_dir):
    """
    Method 1: python-docx library for text and images

    Extracts all text content and images from DOCX file using python-docx library.
    Preserves paragraph structure and extracts images to images/ subdirectory.

    Advantages:
    - Extracts both text and images
    - Preserves paragraph structure
    - Fast and reliable
    - Well-maintained library

    Disadvantages:
    - Limited table formatting
    - Does not capture document metadata
    - No heading style preservation

    When to use:
    - General-purpose text and image extraction
    - When you need both content and images
    - When paragraph structure is sufficient

    Output:
    - content.md: Text content with paragraph structure
    - images/: Directory with extracted images (image_001.png, etc.)

    Dependencies: python-docx>=1.1.0

    CLI alternative: pandoc
    Command: nix run nixpkgs#pandoc -- pandoc "$SOURCE_FILE" -t markdown --extract-media=./images -o content.md
    """
    print("    Method 1: python-docx (basic)...")
    method_dir = output_dir / "python_docx_basic"
    method_dir.mkdir(exist_ok=True)
    images_dir = method_dir / "images"
    images_dir.mkdir(exist_ok=True)

    try:
        doc = Document(source_file)

        # Extract text
        text_content = []
        for para in doc.paragraphs:
            if para.text.strip():
                text_content.append(para.text)

        # Save text content
        with open(method_dir / "content.md", "w") as f:
            f.write("\n\n".join(text_content))

        # Extract images
        img_count = 0
        for rel in doc.part.rels.values():
            if "image" in rel.target_ref:
                img_count += 1
                img_data = rel.target_part.blob
                ext = rel.target_ref.split(".")[-1]
                with open(images_dir / f"image_{img_count:03d}.{ext}", "wb") as f:
                    f.write(img_data)

        print(
            f"      ✓ Extracted {len(doc.paragraphs)} paragraphs and {img_count} images"
        )
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method2_markitdown(source_file, output_dir):
    """
    Method 2: markitdown library

    Extracts text-only content from DOCX file using Microsoft's markitdown library.
    Maintains document structure (headings, paragraphs) but does not extract images.

    Advantages:
    - Fast text extraction
    - Microsoft-maintained tool
    - Maintains document structure
    - Consistent with other format parsers (PPTX, PDF)

    Disadvantages:
    - Does not extract images
    - Table formatting may be simplified
    - Limited customization options

    When to use:
    - Quick text extraction when images aren't needed
    - When document structure is more important than images
    - For consistent processing across multiple formats

    Output:
    - content.md: Markdown text with document structure

    Dependencies: markitdown>=0.0.1a2

    CLI alternative: markitdown CLI
    Command: uvx --from 'markitdown[docx]' markitdown "$SOURCE_FILE" > content.md
    C library required: nixpkgs#stdenv.cc.cc.lib
    Source: https://github.com/microsoft/markitdown
    """
    print("    Method 2: markitdown...")
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


def parse_method3_python_docx_detailed(source_file, output_dir):
    """
    Method 3: python-docx with detailed extraction including tables

    Extracts comprehensive content from DOCX file using python-docx library with
    enhanced detail. Captures headings, tables, and document metadata.

    Advantages:
    - Most comprehensive Python-based extraction
    - Preserves heading structure and styles
    - Extracts tables as JSON for programmatic access
    - Captures document metadata (author, title, dates)
    - Maintains table structure in Markdown

    Disadvantages:
    - Slower than other methods
    - More complex output structure
    - May struggle with complex merged cells in tables

    When to use:
    - Full document analysis needed
    - Table data extraction required
    - Document metadata capture needed
    - When heading structure is important

    Output:
    - content.md: Text with headings (preserved as Markdown #) and tables
    - table_1.json, table_2.json, ...: Tables as JSON arrays
    - metadata.json: Document metadata (author, title, created, modified, paragraph/table counts)

    Dependencies: python-docx>=1.1.0
    """
    print("    Method 3: python-docx (detailed)...")
    method_dir = output_dir / "python_docx_detailed"
    method_dir.mkdir(exist_ok=True)

    try:
        doc = Document(source_file)

        # Extract document metadata
        metadata = {
            "paragraphs": len(doc.paragraphs),
            "tables": len(doc.tables),
            "sections": len(doc.sections),
        }

        # Try to extract core properties
        if hasattr(doc, "core_properties"):
            core_props = doc.core_properties
            core_props_data = {}
            if hasattr(core_props, "author"):
                core_props_data["author"] = core_props.author
            if hasattr(core_props, "title"):
                core_props_data["title"] = core_props.title
            if hasattr(core_props, "created"):
                core_props_data["created"] = str(core_props.created)
            if hasattr(core_props, "modified"):
                core_props_data["modified"] = str(core_props.modified)
            metadata["core_properties"] = core_props_data

        with open(method_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

        # Extract content with structure
        content = []

        # Extract paragraphs with style information
        for para in doc.paragraphs:
            if para.text.strip():
                style = para.style.name if para.style else "Normal"
                if "Heading" in style:
                    level = style.replace("Heading ", "").strip()
                    try:
                        heading_level = int(level)
                        content.append(f"{'#' * heading_level} {para.text}")
                    except:
                        content.append(f"## {para.text}")
                else:
                    content.append(para.text)

        # Extract tables
        for table_idx, table in enumerate(doc.tables, 1):
            content.append(f"\n### Table {table_idx}\n")
            table_data = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_data.append(row_data)

            # Save table as JSON
            with open(method_dir / f"table_{table_idx}.json", "w") as f:
                json.dump(table_data, f, indent=2)

            # Add table to markdown (simple format)
            if table_data:
                content.append("| " + " | ".join(table_data[0]) + " |")
                content.append("|" + "---|" * len(table_data[0]))
                for row in table_data[1:]:
                    content.append("| " + " | ".join(row) + " |")

        with open(method_dir / "content.md", "w") as f:
            f.write("\n\n".join(content))

        print(
            f"      ✓ Extracted {len(doc.paragraphs)} paragraphs and {len(doc.tables)} tables"
        )
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method4_docx2txt(source_file, output_dir):
    """
    Method 4: docx2txt for simple text extraction

    Extracts text and images using the docx2txt Python library.
    Outputs plain text (not Markdown-formatted) with images saved to subdirectory.

    Advantages:
    - Lightweight and fast
    - Extracts text and images
    - Simple output format
    - Pure Python (no C dependencies)

    Disadvantages:
    - Outputs plain text (no Markdown formatting)
    - Simplified structure
    - No heading preservation
    - No table structure capture

    When to use:
    - Simple text analysis
    - When formatting isn't critical
    - When you need images but plain text is sufficient
    - Lightweight extraction for large documents

    Output:
    - content.txt: Plain text content
    - images/: Directory with extracted images

    Dependencies: docx2txt>=0.8

    CLI alternative: docx2txt CLI
    Command: uvx --from docx2txt docx2txt -i ./images "$SOURCE_FILE" > content.txt
    Advantages: Same as library, faster for batch processing
    Disadvantages: No Markdown formatting
    Source: https://github.com/ankushshah89/python-docx2txt
    """
    print("    Method 4: docx2txt...")
    method_dir = output_dir / "docx2txt"
    method_dir.mkdir(exist_ok=True)
    images_dir = method_dir / "images"
    images_dir.mkdir(exist_ok=True)

    try:
        # Extract text with images
        text = docx2txt.process(str(source_file), str(images_dir))

        # Save text content
        with open(method_dir / "content.txt", "w") as f:
            f.write(text)

        # Count extracted images
        img_count = len(list(images_dir.glob("*")))

        print(f"      ✓ Extracted text and {img_count} images")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def main():
    if len(sys.argv) != 3:
        print("Usage: ./parse_docx.py <file_path> <output_dir>")
        sys.exit(1)

    source_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not source_file.exists():
        print(f"Error: File not found: {source_file}")
        sys.exit(1)

    print(f"Parsing DOCX: {source_file.name}")
    print(f"Output directory: {output_dir}")
    print()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run all parsing methods
    methods_success = {
        "method1_python_docx_basic": parse_method1_python_docx(source_file, output_dir),
        "method2_markitdown": parse_method2_markitdown(source_file, output_dir),
        "method3_python_docx_detailed": parse_method3_python_docx_detailed(
            source_file, output_dir
        ),
        "method4_docx2txt": parse_method4_docx2txt(source_file, output_dir),
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
