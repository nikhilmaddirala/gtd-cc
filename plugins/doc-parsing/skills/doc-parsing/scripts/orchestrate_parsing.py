#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
Orchestrate document parsing across all file types with incremental hash-based processing.

Adapt this script by setting DEFAULT_SOURCE_DIR and DEFAULT_OUTPUT_DIR below.

Usage:
    ./orchestrate_parsing.py [source_dir] [output_dir] [options]

Options:
    --force        - Re-parse all files regardless of hash match
    --types=TYPE   - Specific file types (comma-separated, default: all)
    --help         - Show this help

Examples:
    ./orchestrate_parsing.py
    ./orchestrate_parsing.py /data/docs /data/parsed --force --types=pptx,docx

Supported file types: pptx, docx, xlsx, pdf, pbix
"""

import sys
import subprocess
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

DEFAULT_SOURCE_DIR = None
DEFAULT_OUTPUT_DIR = None
DEFAULT_FILE_TYPES = None
DEFAULT_FORCE_REPARSE = False

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
    """Check if file needs reparsing based on hash comparison."""
    if force:
        return True

    results_file = output_dir / "parsing_results.json"
    if not results_file.exists():
        return True

    try:
        with open(results_file, "r") as f:
            results = json.load(f)
        current_hash = calculate_hash(source_file)
        previous_hash = results.get("file_hash")
        return current_hash != previous_hash
    except:
        return True


def parse_file(source_file: Path, output_dir: Path, parser_script: Path) -> Dict:
    """Execute parser script for a single file."""
    print(f"\n  Parsing: {source_file.name}")
    print(f"  Output: {output_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

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
    source_dir = DEFAULT_SOURCE_DIR
    output_dir = DEFAULT_OUTPUT_DIR
    file_types = (
        set(PARSERS.keys()) if DEFAULT_FILE_TYPES is None else set(DEFAULT_FILE_TYPES)
    )
    force = DEFAULT_FORCE_REPARSE

    args = sys.argv[1:]
    positional_args = []

    while args:
        arg = args.pop(0)

        if arg.startswith("--"):
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
            positional_args.append(arg)

    if len(positional_args) >= 1:
        source_dir = Path(positional_args[0])
    if len(positional_args) >= 2:
        output_dir = Path(positional_args[1])
    if len(positional_args) > 2:
        print(f"Error: Too many positional arguments")
        print("Use --help for usage information")
        sys.exit(1)

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

    script_dir = Path(__file__).parent
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

    output_dir.mkdir(parents=True, exist_ok=True)

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
            rel_path = source_file.relative_to(source_dir)
            file_output_dir = output_dir / rel_path

            if not force and not should_parse_file(source_file, file_output_dir, force):
                print(f"\n  Skipping: {source_file.name} (unchanged)")
                skipped_count += 1
                continue

            parse_result = parse_file(source_file, file_output_dir, parser_script)
            file_hash = calculate_hash(source_file)

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

            results[str(rel_path)] = parse_result

            if parse_result["success"]:
                processed_count += 1
            else:
                error_count += 1

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
