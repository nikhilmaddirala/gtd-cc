#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Orchestrate document parsing across all file types.

This is the main orchestration script for batch processing, incremental parsing,
and state management of office documents. Orchestrators should copy this script to
their project directory and adapt the configuration at the top of the file.

**ORCHESTRATOR USAGE:**

To use this orchestrator for your project:

1. Copy this script and all parse_*.py scripts to your project directory:
   cp -r /path/to/doc-parsing/scripts/* /your/project/scripts/

2. Adapt this script with project-specific context:
   - Set `DEFAULT_SOURCE_DIR` to your source documents directory
   - Set `DEFAULT_OUTPUT_DIR` to your target output directory
   - Adjust `DEFAULT_FILE_TYPES` if you only need specific types
   - Set `DEFAULT_FORCE_REPARSE` to True if you want to re-parse all files

3. Run the orchestrator:
   ./orchestrate_parsing.py

   Or with command-line arguments:
   ./orchestrate_parsing.py /custom/source /custom/output --force --types=pptx,docx

Supported file types: pptx, docx, xlsx, pdf, pbix

**CORE ORCHESTRATION PRINCIPLES:**

Mirror Structure Preservation:
- Output directory mirrors source directory structure exactly
- Preserve subdirectory organization and file relationships
- Example: source/decks/Q4/deck.pptx → output/decks/Q4/deck.pptx/

Hash-Based Incremental Parsing:
- Compare source file SHA256 with existing parsing_results.json hash
- Skip unchanged files unless --force specified
- Re-parse files with hash mismatches

Complete Method Execution:
- For each file, run ALL methods defined in its parser script
- Methods are independent - failure in one does not stop others
- Log all errors, continue execution

Error Handling:
- Log errors in file's parsing_results.json with context
- Continue with next method if one fails
- Continue with next file if parsing partially succeeds
- Never halt orchestration due to single file errors

Documentation First:
- Generate parsing_results.json for every parsed file (even partial failures)
- Create top-level orchestration_summary.json summarizing all operations

**PATTERNS AND COMMON CODE:**

Hash Calculation:
```python
import hashlib

def calculate_hash(file_path: Path) -> str:
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()
```

Directory Mirroring:
```python
from pathlib import Path

source_dir = Path('/home/user/docs')
source_file = Path('/home/user/docs/decks/Q4/deck.pptx')
rel_path = source_file.relative_to(source_dir)
output_dir = Path('/home/user/parsed')
file_output_dir = output_dir / rel_path
file_output_dir.mkdir(parents=True, exist_ok=True)
```

Subprocess Execution with Error Handling:
```python
import subprocess

def parse_file(source_file, output_dir, parser_script):
    try:
        result = subprocess.run(
            [str(parser_script), str(source_file), str(output_dir)],
            capture_output=True,
            text=True,
            timeout=600
        )
        return {'success': result.returncode == 0, 'returncode': result.returncode}
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'timeout'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

C Library Wrapping (when needed):
```bash
# For tools requiring C++ standard library (markitdown, docling, pandas)
nix shell nixpkgs#stdenv.cc.cc.lib --command bash -c "
  export LD_LIBRARY_PATH=\$(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:\$LD_LIBRARY_PATH &&
  uvx --from 'markitdown[pdf]' markitdown '$SOURCE_FILE'
"
```

**DECISION POINTS:**

Hash Comparison Strategy:
- Skip unchanged files (default) - saves time
- Always re-parse (--force) - ensures consistency
- Default: Skip unchanged, use --force when methods or file content changed

Error Handling Severity:
- Log and continue (recommended) - maximizes coverage
- Stop on first error (fail-fast) - limits wasted time
- Default: Log and continue, use fail-fast if first file errors indicate systemic issues

**COMMAND LINE ARGUMENTS:**

Usage:
    ./orchestrate_parsing.py [source_dir] [output_dir] [options]

Arguments:
    source_dir  - Source directory containing files to parse (optional if DEFAULT_SOURCE_DIR set)
    output_dir  - Output directory for parsed content (optional if DEFAULT_OUTPUT_DIR set)

Options:
    --force        - Re-parse all files regardless of hash match
    --types=TYPE   - Specific file types to process (comma-separated, default: all)
    --help         - Show this help message

Examples:
    # Use default directories configured below
    ./orchestrate_parsing.py

    # Specify directories on command line
    ./orchestrate_parsing.py /home/user/docs /home/user/parsed

    # Force reparse all files
    ./orchestrate_parsing.py --force

    # Parse only specific file types
    ./orchestrate_parsing.py --types=pptx,docx

    # Combine options
    ./orchestrate_parsing.py /data/docs /data/parsed --force --types=pdf
"""

import sys
import subprocess
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

# ========================================
# ORCHESTRATOR CONFIGURATION
# Adapt these for your project
# ========================================

DEFAULT_SOURCE_DIR = None  # Set to your source directory, e.g., Path("/home/user/docs")
DEFAULT_OUTPUT_DIR = (
    None  # Set to your output directory, e.g., Path("/home/user/parsed")
)
DEFAULT_FILE_TYPES = (
    None  # Set to None for all types, or specific types like ["pptx", "docx"]
)
DEFAULT_FORCE_REPARSE = False  # Set to True to always re-parse all files

# File type to parser mapping
PARSERS = {
    "pptx": "parse_pptx.py",
    "docx": "parse_docx.py",
    "xlsx": "parse_xlsx.py",
    "pdf": "parse_pdf.py",
    "pbix": "parse_pbix.py",
}


def calculate_hash(file_path: Path) -> str:
    """Calculate SHA256 hash of file for incremental parsing."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def discover_files(source_dir: Path, file_types: Set[str]) -> Dict[str, List[Path]]:
    """Discover all files of specified types in source directory."""
    files_by_type = {ft: [] for ft in file_types}

    for file_type in file_types:
        pattern = f"**/*.{file_type}"
        for file_path in source_dir.glob(pattern):
            if file_path.is_file():
                files_by_type[file_type].append(file_path)

    return files_by_type


def should_parse_file(source_file: Path, output_dir: Path, force: bool) -> bool:
    """Determine if file should be parsed based on hash comparison."""
    if force:
        return True

    # Check if results file exists
    results_file = output_dir / "parsing_results.json"
    if not results_file.exists():
        return True

    try:
        with open(results_file, "r") as f:
            results = json.load(f)

        # Compare hashes
        current_hash = calculate_hash(source_file)
        previous_hash = results.get("file_hash")

        return current_hash != previous_hash
    except:
        return True


def parse_file(source_file: Path, output_dir: Path, parser_script: Path) -> Dict:
    """Parse a single file using the appropriate parser."""
    print(f"\n  Parsing: {source_file.name}")
    print(f"  Output: {output_dir}")

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Run parser
    try:
        result = subprocess.run(
            [str(parser_script), str(source_file), str(output_dir)],
            capture_output=True,
            text=True,
            timeout=600,
        )

        success = result.returncode == 0

        if success:
            print(f"  ✓ Parsing completed")
        else:
            print(f"  ⚠ Parsing failed (exit code: {result.returncode})")
            if result.stderr:
                print(f"  Error: {result.stderr[:200]}")

        return {
            "success": success,
            "returncode": result.returncode,
            "stdout": result.stdout if not success else "",
            "stderr": result.stderr if not success else "",
        }
    except subprocess.TimeoutExpired:
        print(f"  ⚠ Parsing timed out")
        return {"success": False, "error": "timeout"}
    except Exception as e:
        print(f"  ⚠ Parsing failed: {str(e)}")
        return {"success": False, "error": str(e)}


def main():
    # Parse command-line arguments
    source_dir = DEFAULT_SOURCE_DIR
    output_dir = DEFAULT_OUTPUT_DIR
    file_types = (
        set(PARSERS.keys()) if DEFAULT_FILE_TYPES is None else set(DEFAULT_FILE_TYPES)
    )
    force = DEFAULT_FORCE_REPARSE

    # Parse optional arguments
    args = sys.argv[1:]
    positional_args = []

    while args:
        arg = args.pop(0)

        if arg.startswith("--"):
            # Handle flags
            if arg == "--force":
                force = True
            elif arg.startswith("--types="):
                types_str = arg.split("=", 1)[1]
                file_types = set(t.strip().lower() for t in types_str.split(","))
                invalid_types = file_types - set(PARSERS.keys())
                if invalid_types:
                    print(f"Error: Invalid file types: {', '.join(invalid_types)}")
                    print(f"Supported types: {', '.join(PARSERS.keys())}")
                    sys.exit(1)
            elif arg == "--help":
                print(__doc__)
                sys.exit(0)
            else:
                print(f"Error: Unknown option {arg}")
                print("Use --help for usage information")
                sys.exit(1)
        else:
            # Positional arguments
            positional_args.append(arg)

    # Set source/output from positional args
    if len(positional_args) >= 1:
        source_dir = Path(positional_args[0])
    if len(positional_args) >= 2:
        output_dir = Path(positional_args[1])
    if len(positional_args) > 2:
        print(f"Error: Too many positional arguments")
        print("Use --help for usage information")
        sys.exit(1)

    # Validate directories
    if source_dir is None:
        print("Error: Source directory not specified")
        print("Use --help for usage information")
        sys.exit(1)

    if output_dir is None:
        print("Error: Output directory not specified")
        print("Use --help for usage information")
        sys.exit(1)

    if not source_dir.exists():
        print(f"Error: Source directory not found: {source_dir}")
        sys.exit(1)

    if not source_dir.is_dir():
        print(f"Error: Source path is not a directory: {source_dir}")
    sys.exit(1)

    # Get script directory
    script_dir = Path(__file__).parent

    # Start processing
    start_time = datetime.now()

    print("=" * 80)
    print("DOCUMENT PARSING ORCHESTRATION")
    print("=" * 80)
    print(f"Start time: {start_time.isoformat()}")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print(f"Force reparse: {force}")
    print(f"File types: {', '.join(sorted(file_types))}")
    print()

    # Discover files
    print("Discovering files...")
    files_by_type = discover_files(source_dir, file_types)

    total_files = sum(len(files) for files in files_by_type.values())
    print(f"\nFound {total_files} files:")
    for file_type, files in sorted(files_by_type.items()):
        print(f"  {file_type.upper()}: {len(files)} files")
    print()

    if total_files == 0:
        print("No files found to parse.")
        return 0

    # Create output base directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Process each file
    results = {}
    processed_count = 0
    skipped_count = 0
    error_count = 0

    for file_type, files in files_by_type.items():
        if not files:
            continue

        parser_script = script_dir / PARSERS[file_type]
        if not parser_script.exists():
            print(f"⚠ Parser not found: {parser_script}")
            continue

        print(f"\n{'=' * 80}")
        print(f"Processing {file_type.upper()} files ({len(files)} files)")
        print(f"{'=' * 80}")

        for source_file in files:
            # Calculate relative path from source_dir
            rel_path = source_file.relative_to(source_dir)

            # Create mirrored output directory
            file_output_dir = output_dir / rel_path

            # Check if we should parse
            if not force and not should_parse_file(source_file, file_output_dir, force):
                print(f"\n  Skipping: {source_file.name} (unchanged)")
                skipped_count += 1
                continue

            # Parse file
            parse_result = parse_file(source_file, file_output_dir, parser_script)

            # Store file hash in results
            file_hash = calculate_hash(source_file)

            # Update results file
            results_data = {
                "timestamp": datetime.now().isoformat(),
                "source_file": str(source_file),
                "file_hash": file_hash,
                "relative_path": str(rel_path),
                "file_type": file_type,
                "parse_result": parse_result,
            }

            results_file = file_output_dir / "orchestration_metadata.json"
            file_output_dir.mkdir(parents=True, exist_ok=True)
            with open(results_file, "w") as f:
                json.dump(results_data, f, indent=2)

            # Track results
            results[str(rel_path)] = parse_result

            if parse_result["success"]:
                processed_count += 1
            else:
                error_count += 1

    # Generate summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"Total files discovered: {total_files}")
    print(f"Successfully parsed: {processed_count}")
    print(f"Skipped (unchanged): {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Duration: {duration:.2f} seconds")
    print()

    # Save orchestration summary
    summary = {
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "duration_seconds": duration,
        "source_dir": str(source_dir),
        "output_dir": str(output_dir),
        "force": force,
        "file_types": list(file_types),
        "total_files": total_files,
        "processed": processed_count,
        "skipped": skipped_count,
        "errors": error_count,
        "files_by_type": {k: len(v) for k, v in files_by_type.items()},
        "results": results,
    }

    summary_file = output_dir / "orchestration_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Summary saved to: {summary_file}")
    print("=" * 80)

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
