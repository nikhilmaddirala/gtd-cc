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
Parse PDF files using 4 extraction methods: basic text with metadata, advanced with tables,
fast text-only, and layout-aware extraction.

Usage: ./parse_pdf.py <file_path> <output_dir>
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
    """Basic text extraction with PDF metadata using pypdf."""
    print("    Method 1: pypdf...")
    method_dir = output_dir / "pypdf"
    method_dir.mkdir(exist_ok=True)

    try:
        reader = PdfReader(source_file)

        text_content = []
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                text_content.append(f"\n## Page {page_num}\n\n{text}")

        with open(method_dir / "content.md", "w") as f:
            f.write("\n\n".join(text_content))

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
    """Advanced extraction with table parsing using pdfplumber."""
    print("    Method 2: pdfplumber...")
    method_dir = output_dir / "pdfplumber"
    method_dir.mkdir(exist_ok=True)
    tables_dir = method_dir / "tables"
    tables_dir.mkdir(exist_ok=True)

    try:
        with pdfplumber.open(source_file) as pdf:
            text_content = []
            table_count = 0

            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text and text.strip():
                    text_content.append(f"\n## Page {page_num}\n\n{text}")

                tables = page.extract_tables()
                for table_idx, table in enumerate(tables, 1):
                    table_count += 1
                    table_file = tables_dir / f"page_{page_num}_table_{table_idx}.json"
                    with open(table_file, "w") as f:
                        json.dump(table, f, indent=2)

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
    """Fast text-only extraction using Microsoft's markitdown."""
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
    """Layout-aware text extraction for complex multi-column PDFs."""
    print("    Method 4: pdfminer.six...")
    method_dir = output_dir / "pdfminer"
    method_dir.mkdir(exist_ok=True)

    try:
        output_string = StringIO()

        with open(source_file, "rb") as fin:
            extract_text_to_fp(
                fin, output_string, laparams=LAParams(), output_type="text", codec=None
            )

        text = output_string.getvalue()

        with open(method_dir / "content.txt", "w") as f:
            f.write(text)

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

    output_dir.mkdir(parents=True, exist_ok=True)

    methods_success = {
        "method1_pypdf": parse_method1_pypdf(source_file, output_dir),
        "method2_pdfplumber": parse_method2_pdfplumber(source_file, output_dir),
        "method3_markitdown": parse_method3_markitdown(source_file, output_dir),
        "method4_pdfminer": parse_method4_pdfminer(source_file, output_dir),
    }

    success_count = sum(methods_success.values())
    print(f"\n  ✓ Completed: {success_count}/{len(methods_success)} methods successful")

    results = {
        "timestamp": datetime.now().isoformat(),
        "source_file": str(source_file),
        "output_dir": str(output_dir),
        "methods": methods_success,
        "success_count": success_count,
    }

    with open(output_dir / "parsing_summary.json", "w") as f:
        json.dump(results, f, indent=2)

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
