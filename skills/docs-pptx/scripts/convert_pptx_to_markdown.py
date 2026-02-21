#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "markitdown[pptx]>=0.0.1a2",
# ]
# ///

"""
PPTX to Markdown Conversion Script

Converts PowerPoint presentations to markdown format with inline slide images.
Handles all deterministic steps: PPTX→PDF→Images→Text→Markdown assembly.

Usage:
    ./convert_pptx_to_markdown.py <input.pptx> <output_dir>

Example:
    ./convert_pptx_to_markdown.py source/presentation.pptx output/

Requirements:
    - LibreOffice (soffice command)
    - poppler-utils (pdftoppm command)
    - Python 3.11+ with uv

Output:
    output_dir/
    ├── presentation.md              # Final markdown with inline images
    ├── presentation-text.md         # Extracted text (intermediate)
    ├── pdf/
    │   └── presentation.pdf         # Generated PDF (intermediate)
    └── slide-images/
        └── slide-*.jpg              # Exported slide images

Note:
    See references/troubleshooting.md for OS-specific installation instructions
    and handling system library dependencies for markitdown.
"""

import sys
import subprocess
import re
import argparse
from pathlib import Path


def check_command(cmd, install_hint):
    """Check if a command is available, provide install hint if not."""
    try:
        # Try --version first, fall back to -h if that fails
        result = subprocess.run([cmd, "--version"], capture_output=True)
        if result.returncode != 0:
            result = subprocess.run([cmd, "-h"], capture_output=True)
        return True
    except FileNotFoundError:
        print(f"❌ Error: {cmd} not found. {install_hint}", file=sys.stderr)
        return False


def run_command(cmd, description, check=True):
    """Run a shell command with progress output."""
    print(f"→ {description}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        if result.returncode == 0:
            print(f"  ✓ {description} complete")
            return result.stdout
        else:
            print(f"  ✗ {description} failed", file=sys.stderr)
            if result.stderr:
                print(f"  Error: {result.stderr}", file=sys.stderr)
            return None
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {description} failed: {e}", file=sys.stderr)
        if e.stderr:
            print(f"  Error: {e.stderr}", file=sys.stderr)
        return None


def convert_pptx_to_pdf(pptx_path, pdf_dir):
    """Convert PPTX to PDF using LibreOffice."""
    pdf_dir.mkdir(parents=True, exist_ok=True)
    cmd = f'soffice --headless --convert-to pdf "{pptx_path}" --outdir "{pdf_dir}"'
    result = run_command(cmd, "Converting PPTX to PDF (LibreOffice)")

    if result is None:
        return None

    # Find the generated PDF
    pdf_name = pptx_path.stem + ".pdf"
    pdf_path = pdf_dir / pdf_name

    if pdf_path.exists():
        return pdf_path
    else:
        print(f"  ✗ Expected PDF not found: {pdf_path}", file=sys.stderr)
        return None


def convert_pdf_to_images(pdf_path, images_dir, dpi=150):
    """Convert PDF pages to JPEG images using poppler-utils."""
    images_dir.mkdir(parents=True, exist_ok=True)
    output_prefix = images_dir / "slide"

    cmd = f'pdftoppm -jpeg -r {dpi} "{pdf_path}" "{output_prefix}"'
    result = run_command(cmd, f"Converting PDF to JPEG images ({dpi} DPI)")

    if result is None:
        return None

    # Check if images were created
    image_files = sorted(images_dir.glob("slide-*.jpg"))
    if image_files:
        print(f"  Generated {len(image_files)} slide images")
        return image_files
    else:
        print(f"  ✗ No slide images found in {images_dir}", file=sys.stderr)
        return None


def extract_text(pptx_path, output_file):
    """Extract text from PPTX using markitdown."""
    output_file.parent.mkdir(parents=True, exist_ok=True)

    cmd = f"python -m markitdown '{pptx_path}' > '{output_file}'"
    result = run_command(cmd, "Extracting text with markitdown", check=False)

    if output_file.exists() and output_file.stat().st_size > 0:
        return output_file
    else:
        print(f"  ✗ Text extraction failed or produced empty file", file=sys.stderr)
        return None


def extract_title_from_content(content):
    """Extract presentation title from content."""
    # Try to find first heading
    heading_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if heading_match:
        title = heading_match.group(1).strip()
        # Remove common artifacts
        title = re.sub(r'\s{2,}', ' ', title)
        return title

    # Try first non-empty line after first slide
    first_slide = re.search(r'<!-- Slide number: 1 -->\s*\n(.+)', content)
    if first_slide:
        first_line = first_slide.group(1).strip()
        first_line = re.sub(r'\s{2,}', ' ', first_line)
        if 5 < len(first_line) < 100:
            return first_line

    return "Presentation"


def split_into_slides(content):
    """Split content by slide number markers."""
    parts = re.split(r'<!-- Slide number: (\d+) -->', content)

    slides = []
    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            slide_num = parts[i]
            slide_content = parts[i + 1].strip()
            slides.append((slide_num, slide_content))

    return slides


def assemble_markdown(text_file, output_file, images_dir_rel, title=None):
    """Assemble final markdown from extracted text and slide images."""
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract title if not provided
    if not title:
        title = extract_title_from_content(content)

    # Split into slides
    slides = split_into_slides(content)

    if not slides:
        print("  ✗ No slide markers found in extracted text", file=sys.stderr)
        print("     Expected markers like: <!-- Slide number: 1 -->", file=sys.stderr)
        return None

    # Generate markdown
    output = []
    output.append(f"# {title}\n\n")
    output.append("---\n\n")
    output.append("**Note:** For detailed alt-text descriptions of all slides, see [alt-texts.md](alt-texts.md)\n\n")
    output.append("---\n\n")

    for slide_num, slide_content in slides:
        output.append(f"## Slide {slide_num}\n\n")

        # Add image reference
        img_path = f"{images_dir_rel}/slide-{slide_num.zfill(2)}.jpg"
        output.append(f"![Slide {slide_num}]({img_path})\n\n")

        # Add slide content
        if slide_content:
            slide_content = re.sub(r'\n{3,}', '\n\n', slide_content)
            output.append(slide_content)
            output.append("\n\n")

        output.append("---\n\n")

    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(output))

    print(f"  ✓ Assembled markdown with {len(slides)} slides")
    return output_file


def main():
    parser = argparse.ArgumentParser(
        description="Convert PowerPoint presentations to markdown with inline images"
    )
    parser.add_argument("input", help="Input PPTX file path")
    parser.add_argument("output_dir", help="Output directory path")
    parser.add_argument("--dpi", type=int, default=150, help="Image DPI (default: 150)")
    parser.add_argument("--title", help="Presentation title (auto-detected if not provided)")

    args = parser.parse_args()

    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"❌ Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if not input_path.suffix.lower() == '.pptx':
        print(f"❌ Error: Input file must be .pptx format", file=sys.stderr)
        sys.exit(1)

    # Setup output directories
    output_dir = Path(args.output_dir)
    pdf_dir = output_dir / "pdf"
    images_dir = output_dir / "slide-images"
    text_file = output_dir / f"{input_path.stem}-text.md"
    final_md = output_dir / f"{input_path.stem}.md"

    print(f"\n🔄 Converting: {input_path.name}")
    print(f"📁 Output: {output_dir}/\n")

    # Check dependencies
    if not check_command("soffice", "Install LibreOffice"):
        sys.exit(1)

    if not check_command("pdftoppm", "Install poppler-utils (see references/troubleshooting.md)"):
        sys.exit(1)

    # Step 1: PPTX → PDF
    pdf_path = convert_pptx_to_pdf(input_path, pdf_dir)
    if not pdf_path:
        sys.exit(1)

    # Step 2: PDF → Images
    image_files = convert_pdf_to_images(pdf_path, images_dir, args.dpi)
    if not image_files:
        sys.exit(1)

    # Step 3: Extract text
    text_path = extract_text(input_path, text_file)
    if not text_path:
        sys.exit(1)

    # Step 4: Assemble markdown
    result = assemble_markdown(
        text_file,
        final_md,
        "slide-images",  # Relative path from output_dir
        args.title
    )

    if not result:
        sys.exit(1)

    print(f"\n✅ Conversion complete!")
    print(f"📄 Markdown: {final_md}")
    print(f"🖼️  Images: {images_dir}/ ({len(image_files)} files)")
    print(f"\n💡 Next step: Generate alt-texts using AI")
    print(f"   Read slide images and create detailed descriptions in alt-texts.md")


if __name__ == "__main__":
    main()
