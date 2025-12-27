#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-pptx>=0.6.21",
#   "markitdown>=0.0.1a2",
#   "Pillow>=10.0.0",
# ]
# ///
"""
Parse PPTX (PowerPoint) files using multiple Python methods.

This script extracts content from Microsoft PowerPoint presentations using four different methods,
each optimized for different use cases: completeness, speed, detailed metadata, or image extraction.

Output structure for each file:
    output_dir/filename.pptx/
    ├── parsing_results.json           # File-level metadata and method results
    ├── python_pptx_basic/            # Method 1 output
    │   ├── content.md                # Text with slide numbers
    │   └── images/                  # Extracted images
    ├── markitdown/                  # Method 2 output
    │   └── content.md              # Text-only extraction
    ├── python_pptx_detailed/         # Method 3 output
    │   ├── content.md              # Text with notes and layout info
    │   └── slides_metadata.json    # Detailed slide metadata
    └── python_pptx_images/           # Method 4 output
        ├── images/                 # All extracted images
        └── images_metadata.json    # Image metadata with dimensions

Methods:

1. python-pptx (basic) - Extract text and images using python-pptx library
   - Basic text extraction with slide numbers
   - Extracts all images from presentation
   - Simple and reliable
   - Output: Markdown text with slide structure + images

   CLI alternative: markitdown CLI (same as Method 2)
   CLI alternative: pptx2md
   - Command: uvx pptx2md "$SOURCE_FILE"
   - Advantages: Preserves formatting, handles tables well, multiple indentation levels
   - Disadvantages: Requires Python 3.10+, outputs to `out.md` and `img/` only

2. markitdown - Extract text using markitdown library
   - Microsoft tool for converting documents to Markdown
   - Fast text-only extraction
   - Maintains document structure (headings, paragraphs)
   - No image extraction
   - Output: Markdown text only

   CLI alternative: markitdown CLI
   - Command: uvx --from 'markitdown[pptx]' markitdown "$SOURCE_FILE" > content.md
   - C library required: nixpkgs#stdenv.cc.cc.lib
   - Advantages: Same as library, faster for batch processing
   - Disadvantages: No image extraction

3. python-pptx (detailed) - Extract with slide notes and layout info
   - Comprehensive extraction with slide metadata
   - Extracts slide layout information
   - Captures speaker notes
   - Preserves shape information
   - Output: Markdown with notes + metadata JSON

   CLI alternative: None (Python library is best option for detailed extraction)

4. python-pptx (images) - Focus on comprehensive image extraction with metadata
   - Extracts all images with detailed metadata
   - Captures image dimensions
   - Tracks slide and shape index for each image
   - Saves images with meaningful filenames
   - Output: Images with metadata JSON

   CLI alternative: None (Python library is best option for comprehensive image extraction)

Usage:
    ./parse_pptx.py <file_path> <output_dir>

Arguments:
    file_path  - Path to PPTX file to parse
    output_dir  - Directory where parsed content will be created

Example:
    ./parse_pptx.py /path/to/presentation.pptx /path/to/output

Dependencies:
    - python-pptx>=0.6.21 - PowerPoint presentation parsing
    - markitdown>=0.0.1a2 - Microsoft document conversion
    - Pillow>=10.0.0 - Image processing for metadata extraction

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

python-pptx (basic):
- Advantages: Extracts text + images, simple structure, reliable
- Disadvantages: No speaker notes, limited layout info
- Best for: General-purpose text and image extraction

markitdown:
- Advantages: Fast, Microsoft-maintained, consistent structure
- Disadvantages: No image extraction, complex animations not preserved
- Best for: Quick text extraction when images aren't needed
- Source: https://github.com/microsoft/markitdown

python-pptx (detailed):
- Advantages: Extracts speaker notes, captures layout info, shape metadata
- Disadvantages: Slower, more complex output
- Best for: Full presentation analysis, notes capture, metadata extraction

python-pptx (images):
- Advantages: Comprehensive image extraction, includes dimensions, tracks source
- Disadvantages: Text-only (no images in output)
- Best for: Image extraction and cataloging, visual asset management

Additional CLI options (via nix):

LibreOffice PDF:
- Command: nix shell nixpkgs#libreoffice --command bash -c "libreoffice --headless --convert-to pdf '$SOURCE_FILE'"
- Creates visual PDF representation
- Preserves original formatting exactly
- Does not produce machine-readable text
- Useful for: Visual reference, maintaining layout
- Source: https://help.libreoffice.org/latest/en-US/text/swriter/guide/convert.html

pptx2md CLI:
- Command: uvx pptx2md "$SOURCE_FILE"
- Preserves formatting: bold, italic, colors, hyperlinks
- Handles tables with merged cells
- Supports multiple indentation levels in lists
- Outputs: out.md and img/ directory
- Source: https://github.com/ssine/pptx2md
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from pptx import Presentation
from markitdown import MarkItDown
from PIL import Image
import io


def parse_method1_python_pptx(source_file, output_dir):
    """
    Method 1: python-pptx library for text and images

    Extracts all text content and images from PPTX file using python-pptx library.
    Organizes text by slide numbers and extracts images to images/ subdirectory.

    Advantages:
    - Extracts both text and images
    - Simple slide-by-slide structure
    - Fast and reliable
    - Well-maintained library

    Disadvantages:
    - No speaker notes extraction
    - Limited layout information
    - No shape type metadata

    When to use:
    - General-purpose text and image extraction
    - When you need both content and images
    - When slide-by-slide structure is sufficient

    Output:
    - content.md: Text content organized by slide number
    - images/: Directory with extracted images (image_001.png, etc.)

    Dependencies: python-pptx>=0.6.21

    CLI alternatives:
    - pptx2md: uvx pptx2md "$SOURCE_FILE" (preserves formatting, tables)
    - markitdown: See Method 2
    """
    print("    Method 1: python-pptx (basic)...")
    method_dir = output_dir / "python_pptx_basic"
    method_dir.mkdir(exist_ok=True)
    images_dir = method_dir / "images"
    images_dir.mkdir(exist_ok=True)

    try:
        prs = Presentation(source_file)

        # Extract text
        text_content = []
        for slide_idx, slide in enumerate(prs.slides, 1):
            text_content.append(f"\n## Slide {slide_idx}\n")
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text.strip():
                    text_content.append(shape.text)

        # Save text content
        with open(method_dir / "content.md", "w") as f:
            f.write("\n\n".join(text_content))

        # Extract images
        img_count = 0
        for slide_idx, slide in enumerate(prs.slides, 1):
            for shape in slide.shapes:
                if hasattr(shape, "image"):
                    img_count += 1
                    ext = shape.image.content_type.split("/")[-1]
                    if ext == "jpeg":
                        ext = "jpg"
                    with open(images_dir / f"image_{img_count:03d}.{ext}", "wb") as f:
                        f.write(shape.image.blob)

        print(
            f"      ✓ Extracted text from {len(prs.slides)} slides and {img_count} images"
        )
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method2_markitdown(source_file, output_dir):
    """
    Method 2: markitdown library

    Extracts text-only content from PPTX file using Microsoft's markitdown library.
    Maintains document structure (headings, paragraphs) but does not extract images.

    Advantages:
    - Fast text extraction
    - Microsoft-maintained tool
    - Maintains document structure
    - Consistent with other format parsers (DOCX, PDF)

    Disadvantages:
    - Does not extract images
    - Charts extracted as images (not underlying data)
    - Complex animations not preserved
    - Table formatting may be simplified

    When to use:
    - Quick text extraction when images aren't needed
    - When document structure is more important than images
    - For consistent processing across multiple formats

    Output:
    - content.md: Markdown text with document structure

    Dependencies: markitdown>=0.0.1a2

    CLI alternative: markitdown CLI
    - Command: uvx --from 'markitdown[pptx]' markitdown "$SOURCE_FILE" > content.md
    - C library required: nixpkgs#stdenv.cc.cc.lib
    - Advantages: Same as library, faster for batch processing
    - Disadvantages: No image extraction
    - Source: https://github.com/microsoft/markitdown
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


def parse_method3_python_pptx_detailed(source_file, output_dir):
    """
    Method 3: python-pptx with detailed metadata including notes and layout

    Extracts comprehensive content from PPTX file using python-pptx library with
    enhanced detail. Captures speaker notes, layout information, and shape metadata.

    Advantages:
    - Extracts speaker notes
    - Captures slide layout information
    - Preserves shape metadata (type, text presence)
    - Detailed JSON metadata for programmatic access
    - Maintains slide order and structure

    Disadvantages:
    - More complex output structure
    - Slower than basic methods
    - Larger metadata files for large presentations

    When to use:
    - Full presentation analysis needed
    - Speaker notes capture required
    - Layout/metadata extraction needed
    - When detailed programmatic access is beneficial

    Output:
    - content.md: Text with notes, organized by slide and layout
    - slides_metadata.json: Detailed metadata for each slide including:
        * slide_number, layout name, shapes list, notes text

    Dependencies: python-pptx>=0.6.21
    """
    print("    Method 3: python-pptx (detailed)...")
    method_dir = output_dir / "python_pptx_detailed"
    method_dir.mkdir(exist_ok=True)

    try:
        prs = Presentation(source_file)

        # Extract detailed slide information
        slides_data = []
        for slide_idx, slide in enumerate(prs.slides, 1):
            slide_info = {
                "slide_number": slide_idx,
                "layout": slide.slide_layout.name
                if hasattr(slide.slide_layout, "name")
                else "Unknown",
                "shapes": [],
                "notes": "",
            }

            # Extract shapes and text
            for shape in slide.shapes:
                shape_info = {
                    "type": shape.shape_type.name
                    if hasattr(shape.shape_type, "name")
                    else str(shape.shape_type),
                    "has_text": hasattr(shape, "text"),
                }
                if hasattr(shape, "text") and shape.text.strip():
                    shape_info["text"] = shape.text
                slide_info["shapes"].append(shape_info)

            # Extract notes
            if hasattr(slide, "notes_slide") and slide.notes_slide:
                try:
                    notes_text = slide.notes_slide.notes_text_frame.text
                    if notes_text.strip():
                        slide_info["notes"] = notes_text
                except:
                    pass

            slides_data.append(slide_info)

        # Save detailed metadata
        with open(method_dir / "slides_metadata.json", "w") as f:
            json.dump(slides_data, f, indent=2)

        # Create markdown with notes
        md_content = []
        for slide_info in slides_data:
            md_content.append(
                f"\n## Slide {slide_info['slide_number']} ({slide_info['layout']})\n"
            )
            for shape in slide_info["shapes"]:
                if "text" in shape:
                    md_content.append(shape["text"])
            if slide_info["notes"]:
                md_content.append(f"\n**Notes:** {slide_info['notes']}\n")

        with open(method_dir / "content.md", "w") as f:
            f.write("\n\n".join(md_content))

        print(f"      ✓ Extracted detailed metadata for {len(slides_data)} slides")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def parse_method4_python_pptx_images(source_file, output_dir):
    """
    Method 4: python-pptx focused on comprehensive image extraction with metadata

    Extracts all images from PPTX file with detailed metadata using python-pptx
    library and Pillow for image processing. Captures dimensions and source information.

    Advantages:
    - Comprehensive image extraction
    - Captures image dimensions
    - Tracks slide and shape index for each image
    - Saves images with meaningful filenames
    - JSON metadata for programmatic access

    Disadvantages:
    - Larger output for image-heavy presentations
    - No text content in this method
    - Requires additional Pillow dependency

    When to use:
    - Image extraction and cataloging needed
    - When image metadata (dimensions, location) is important
    - Visual asset management
    - When text is not the primary concern

    Output:
    - images/: All extracted images with filenames like: slide_01_image_02.png
    - images_metadata.json: Detailed metadata for each image including:
        * filename, slide, shape_index, content_type, width, height, size_bytes

    Dependencies: python-pptx>=0.6.21, Pillow>=10.0.0
    """
    print("    Method 4: python-pptx (images + metadata)...")
    method_dir = output_dir / "python_pptx_images"
    method_dir.mkdir(exist_ok=True)
    images_dir = method_dir / "images"
    images_dir.mkdir(exist_ok=True)

    try:
        prs = Presentation(source_file)

        # Extract all images with detailed metadata
        images_metadata = []
        img_count = 0

        for slide_idx, slide in enumerate(prs.slides, 1):
            for shape_idx, shape in enumerate(slide.shapes):
                if hasattr(shape, "image"):
                    img_count += 1
                    ext = shape.image.content_type.split("/")[-1]
                    if ext == "jpeg":
                        ext = "jpg"

                    image_filename = (
                        f"slide_{slide_idx:02d}_image_{shape_idx:02d}.{ext}"
                    )
                    image_path = images_dir / image_filename

                    # Save image
                    with open(image_path, "wb") as f:
                        f.write(shape.image.blob)

                    # Try to get image dimensions
                    try:
                        img = Image.open(io.BytesIO(shape.image.blob))
                        width, height = img.size
                    except:
                        width, height = None, None

                    # Store metadata
                    images_metadata.append(
                        {
                            "filename": image_filename,
                            "slide": slide_idx,
                            "shape_index": shape_idx,
                            "content_type": shape.image.content_type,
                            "width": width,
                            "height": height,
                            "size_bytes": len(shape.image.blob),
                        }
                    )

        # Save images metadata
        with open(method_dir / "images_metadata.json", "w") as f:
            json.dump(images_metadata, f, indent=2)

        print(f"      ✓ Extracted {img_count} images with metadata")
        return True
    except Exception as e:
        print(f"      ⚠ Failed: {str(e)[:100]}")
        return False


def main():
    if len(sys.argv) != 3:
        print("Usage: ./parse_pptx.py <file_path> <output_dir>")
        sys.exit(1)

    source_file = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])

    if not source_file.exists():
        print(f"Error: File not found: {source_file}")
        sys.exit(1)

    print(f"Parsing PPTX: {source_file.name}")
    print(f"Output directory: {output_dir}")
    print()

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run all parsing methods
    methods_success = {
        "method1_python_pptx_basic": parse_method1_python_pptx(source_file, output_dir),
        "method2_markitdown": parse_method2_markitdown(source_file, output_dir),
        "method3_python_pptx_detailed": parse_method3_python_pptx_detailed(
            source_file, output_dir
        ),
        "method4_python_pptx_images": parse_method4_python_pptx_images(
            source_file, output_dir
        ),
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
