---
name: doc-parsing
description: Guide for parsing proprietary Office and BI file formats (pptx, docx, xlsx, pbix, pdf) into repo-friendly artifacts. Works with any directory structure and mirrors source to output directory.
---

# Document Parsing Skill

## Overview

Extract content from proprietary Office and BI files into structured, versionable artifacts. Each format has 3-4 parsing methods optimized for speed, completeness, or visual fidelity.

This skill works with any source directory and creates a mirrored output directory with parsed content. It is not tied to any specific project structure.

**Architecture**: Self-contained Python scripts in `scripts/` directory. Orchestrators copy and adapt these scripts to their project directories.

## Supported File Types

| Type | Extension | Methods | Notes |
|------|------------|----------|-------|
| PowerPoint | `.pptx` | 4 | python-pptx, markitdown, detailed extraction, images |
| Word | `.docx` | 4 | python-docx, markitdown, detailed with tables, docx2txt |
| Excel | `.xlsx` | 4 | pandas (basic), openpyxl structure, pandas detailed, openpyxl formulas |
| PDF | `.pdf` | 4 | pypdf, pdfplumber, markitdown, pdfminer layout |
| Power BI | `.pbix` | 2 | pbixray metadata, zipfile extraction |

## Core Principles

**Hybrid Artifacts**: Extract text/data (MD/JSON/CSV) + images (PNG/JPG) without duplication

**Multi-Method Strategy**: Apply all methods for each file type:
- Comprehensive → All content + images (complex tools)
- Fast → Text-only (simple tools)
- Detailed → Metadata, structure, and analysis
- Visuals → PDF/HTML (layout fidelity, optional)

**Mirror Structure**: Output directory mirrors source directory structure exactly
- Source: `source/decks/Q4/presentation.pptx`
- Output: `output/decks/Q4/presentation.pptx/`

**Incremental Parsing**: Skip unchanged files by comparing SHA256 hashes

**Error Handling**: Log errors but never halt orchestration on single file failures

**Documentation First**: Generate metadata files for each parsed file and top-level summary

## Orchestration Workflow

### Orchestrator Implementation

Orchestrators should follow this pattern:

1. **Copy Scripts to Project**: Copy all scripts from `plugins/doc-parsing/skills/doc-parsing/scripts/` to project directory
2. **Adapt Scripts**: Modify `orchestrate_parsing.py` with project-specific context:
   - Set `source_dir` to your source documents directory
   - Set `output_dir` to your target output directory
   - Adjust file type filters if needed
   - Configure force reparse flag
3. **Execute**: Run the adapted `orchestrate_parsing.py` script

### Orchestration Principles

**Mirror Structure Preservation**
- Output directory mirrors source directory structure exactly
- Preserve subdirectory organization and file relationships
- Example: `source/decks/Q4/deck.pptx` → `output/decks/Q4/deck.pptx/`

**Hash-Based Incremental Parsing**
- Compare source file SHA256 with existing `parsing_results.json` hash
- Skip unchanged files unless `--force` specified
- Re-parse files with hash mismatches

**Complete Method Execution**
- For each file, run ALL methods defined in its parser script
- Methods are independent - failure in one does not stop others
- Log all errors, continue execution

**Error Handling Philosophy**
- Log errors in file's `parsing_results.json` with context
- Continue with next method if one fails
- Continue with next file if parsing partially succeeds
- Never halt orchestration due to single file errors

**Documentation Standards**
- Each parsed file gets `parsing_results.json` with metadata
- Top-level `orchestration_summary.json` summarizes all operations
- Include success/failure status for each method

### Common Patterns

**Hash Calculation**
```python
import hashlib

def calculate_hash(file_path):
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()
```

**Directory Mirroring**
```python
from pathlib import Path

# Calculate relative path from source_dir to file
source_dir = Path('/home/user/docs')
source_file = Path('/home/user/docs/decks/Q4/deck.pptx')
rel_path = source_file.relative_to(source_dir)  # 'decks/Q4/deck.pptx'

# Append to output_dir
output_dir = Path('/home/user/parsed')
file_output_dir = output_dir / rel_path  # '/home/user/parsed/decks/Q4/deck.pptx'
file_output_dir.mkdir(parents=True, exist_ok=True)
```

**Subprocess Execution with Error Handling**
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

        success = result.returncode == 0
        if success:
            print(f"✓ Parsing completed")
        else:
            print(f"⚠ Parsing failed (exit code: {result.returncode})")
            if result.stderr:
                print(f"Error: {result.stderr[:200]}")

        return {
            'success': success,
            'returncode': result.returncode,
            'stderr': result.stderr if not success else '',
        }
    except subprocess.TimeoutExpired:
        print(f"⚠ Parsing timed out")
        return {'success': False, 'error': 'timeout'}
    except Exception as e:
        print(f"⚠ Parsing failed: {str(e)}")
        return {'success': False, 'error': str(e)}
```

**C Library Wrapping (when needed)**
```bash
# For tools requiring C++ standard library (markitdown, docling, pandas)
nix shell nixpkgs#stdenv.cc.cc.lib --command bash -c "
  export LD_LIBRARY_PATH=\$(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:\$LD_LIBRARY_PATH &&
  uvx --from 'markitdown[pdf]' markitdown '$SOURCE_FILE'
"
```

### Decision Points

**Hash Comparison Strategy**
- Skip unchanged files (default) - saves time
- Always re-parse (`--force`) - ensures consistency
- Default: Skip unchanged, use `--force` when methods or file content changed

**Error Handling Severity**
- Log and continue (recommended) - maximizes coverage
- Stop on first error (fail-fast) - limits wasted time
- Default: Log and continue, use fail-fast if first file errors indicate systemic issues

**C Library Detection**
- Auto-detect from command patterns (recommended)
- Always wrap (overkill but safe)
- Default: Auto-detect based on presence of `uvx` or Python execution

## Output Structure

```
$OUTPUT_DIR/
├── [source-relative-path]/
│   └── $FILENAME/
│       ├── parsing_results.json         # File-level metadata and results
│       ├── [method_dir_1]/           # First method output
│       │   ├── content.md or out.md
│       │   ├── images/ or *.csv
│       │   └── metadata.json (optional)
│       ├── [method_dir_2]/           # Second method output
│       │   └── ...
│       └── orchestration_metadata.json # Orchestration tracking
└── orchestration_summary.json         # Top-level summary of all files
```

## Parser Script Structure

Each parser script (`parse_*.py`) follows this pattern:

1. **Module docstring**: Overview of file type, methods, dependencies
2. **Method functions**: Each method gets a function with:
   - Docstring explaining purpose, advantages, when to use
   - Implementation using Python libraries
   - Comments noting CLI alternatives
   - Error handling with graceful failure
3. **Main function**:
   - Parse command-line arguments (file_path, output_dir)
   - Execute all methods sequentially
   - Generate `parsing_results.json` with metadata
   - Return exit code based on success count

## Tool Installation Patterns

| Tool Type | Install | Usage Pattern |
|-----------|---------|---------------|
| Python | `uvx --from <package>` or inline dependencies | Self-contained scripts with uv metadata |
| CLI | `nix run nixpkgs#<tool>` | Direct execution without installation |
| C libraries | `nix shell nixpkgs#stdenv.cc.cc.lib --command bash` | Required for markitdown/docling/pandas |

**System libraries**: `nixpkgs#stdenv.cc.cc.lib` (C++), `nixpkgs#zlib`, `nixpkgs#openssl`

**Inline Script Metadata**:
```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-docx>=1.1.0",
#   "markitdown>=0.0.1a2",
# ]
# ///
```

## Usage Example

### For Orchestrators

```bash
# 1. Copy scripts to your project
cp -r /path/to/gtd-cc/plugins/doc-parsing/skills/doc-parsing/scripts/ /your/project/

# 2. Adapt orchestrate_parsing.py
cd /your/project/scripts/
# Edit orchestrate_parsing.py to set:
#   - source_dir = Path('/your/source/docs')
#   - output_dir = Path('/your/output/parsed')

# 3. Run orchestration
./orchestrate_parsing.py

# 4. Force reparse all files
./orchestrate_parsing.py --force

# 5. Parse only specific types
./orchestrate_parsing.py --types=pptx,docx
```

### For Manual Parsing

```bash
# Parse a single file
cd /your/project/scripts/
./parse_pptx.py /path/to/presentation.pptx /path/to/output

# Parse with all methods
./parse_docx.py /path/to/document.docx /path/to/output

# Parse Excel file
./parse_xlsx.py /path/to/spreadsheet.xlsx /path/to/output
```

## Method Descriptions

### PPTX Methods
1. **python-pptx (basic)** - Extract text and images using python-pptx library
2. **markitdown** - Extract text using markitdown library
3. **python-pptx (detailed)** - Extract with slide notes and layout info
4. **python-pptx (images)** - Focus on comprehensive image extraction with metadata

### DOCX Methods
1. **python-docx (basic)** - Extract text and images using python-docx library
2. **markitdown** - Extract text using markitdown library
3. **python-docx (detailed)** - Extract with tables, headers, and formatting
4. **docx2txt** - Simple text extraction with image links

### XLSX Methods
1. **pandas (basic)** - Extract all sheets as CSV files with metadata
2. **openpyxl (structure)** - Extract sheets with formatting and structure info
3. **pandas (detailed)** - Extract with data types and statistics
4. **openpyxl (formulas)** - Extract formulas and calculated values

### PDF Methods
1. **pypdf** - Extract text using pypdf library
2. **pdfplumber** - Extract text and tables using pdfplumber
3. **markitdown** - Extract text using markitdown library
4. **pdfminer.six** - Layout-aware text extraction

### PBIX Methods
1. **pbixray** - Extract model metadata, tables, measures, and relationships
2. **zipfile** - Extract raw PBIX contents (PBIX files are ZIP archives)

## Common Issues

| Issue | Solution |
|--------|----------|
| C library errors | Use `nix shell nixpkgs#stdenv.cc.cc.lib --command bash -c "export LD_LIBRARY_PATH=... && <command>"` |
| Missing images | Check method - not all extract images (see method descriptions) |
| Empty CSV | Verify sheet name exists or check metadata.json for sheet info |
| PBIX fails on Linux | Use pbixray/zipfile methods; Windows tools unavailable |
| Hash comparison fails | Check parsing_results.json format and hash value |
| Scripts won't execute | Check execute permissions: `chmod +x scripts/*.py` |
| Python version | Ensure Python >=3.11 is available |

## Format Notes

**XLSX**: CSV primary output, multiple sheets = multiple CSV files, formulas extracted separately
**PBIX**: Linux-limited, pbixray extracts tables/measures/metadata, zipfile gets raw contents
**Images**: Not all methods extract images (check method docstrings)
**Formulas**: Preserved in openpyxl formulas method, lost in basic pandas methods

## Scripts Reference

All scripts are self-contained with inline metadata. No Python environment setup required.

- `scripts/parse_pptx.py` - PowerPoint parser with 4 methods
- `scripts/parse_docx.py` - Word document parser with 4 methods
- `scripts/parse_xlsx.py` - Excel spreadsheet parser with 4 methods
- `scripts/parse_pdf.py` - PDF parser with 4 methods
- `scripts/parse_pbix.py` - Power BI parser with 2 methods
- `scripts/orchestrate_parsing.py` - Main orchestration script

Each script includes comprehensive documentation in docstrings and comments explaining:
- What each method does
- When to use it
- Advantages and disadvantages
- Tool requirements
- Output structure
- CLI alternatives (when applicable)
