# Document Parsing Plugin

Parse proprietary Office and BI file formats into repository-friendly artifacts with multi-method extraction strategies.

## Overview

The doc-parsing plugin transforms binary Office documents (PowerPoint, Word, Excel) and BI files (Power BI, PDF) into structured, versionable content. Each file type supports multiple parsing methods optimized for different use cases - comprehensive extraction, speed, or visual fidelity.

## Supported File Types

- **PowerPoint (.pptx)** - 4 methods: python-pptx basic, markitdown, python-pptx detailed, python-pptx images
- **Word (.docx)** - 4 methods: python-docx basic, markitdown, python-docx detailed, docx2txt
- **Excel (.xlsx)** - 4 methods: pandas basic, openpyxl structure, pandas detailed, openpyxl formulas
- **PDF (.pdf)** - 4 methods: pypdf, pdfplumber, markitdown, pdfminer layout
- **Power BI (.pbix)** - 2 methods: pbixray metadata, zipfile extraction

## Installation

Install from gtd-cc marketplace:

```bash
/plugin marketplace add nikhilmaddirala/gtd-cc
/plugin install doc-parsing@gtd-cc
```

## Commands

### /parse-docs

Parse office documents from a source directory to a mirrored output directory.

**Required arguments:**
- `source_dir` - Directory containing files to parse
- `output_dir` - Directory where parsed content will be created

**Optional arguments:**
- `force` - Re-parse all files regardless of hash match (default: false)
- `types` - Specific file types to process (default: all supported types)
- `dry_run` - Preview what would be parsed without executing (default: false)

**Examples:**

```bash
# Parse all supported files
/parse-docs source_dir:/home/user/documents output_dir:/home/user/parsed

# Re-parse all files (force)
/parse-docs source_dir:./docs output_dir:./parsed force:true

# Parse only PowerPoint and Word files
/parse-docs source_dir:./docs output_dir:./parsed types:pptx,docx

# Preview parsing without executing
/parse-docs source_dir:./docs output_dir:./parsed dry_run:true
```

## How It Works

### Script Architecture

The plugin provides self-contained Python scripts in the `scripts/` directory. Orchestrators should:

1. **Copy all scripts to project directory:**
   ```bash
   cp -r /path/to/doc-parsing/scripts/* /your/project/
   ```

2. **Adapt orchestrate_parsing.py with project-specific context:**
   - Set `DEFAULT_SOURCE_DIR` to your source documents directory
   - Set `DEFAULT_OUTPUT_DIR` to your target output directory
   - Adjust `DEFAULT_FILE_TYPES` if you only need specific types
   - Set `DEFAULT_FORCE_REPARSE` to True if you want to always re-parse files

3. **Run the orchestrator:**
   ```bash
   cd /your/project/scripts/
   ./orchestrate_parsing.py
   ```

   Or with command-line arguments:
   ```bash
   ./orchestrate_parsing.py /custom/source /custom/output --force --types=pptx,docx
   ```

### Multi-Method Strategy

Each file type is processed using all available methods:
- **Comprehensive** - Extract all content including text, data, and images
- **Fast** - Quick text-only extraction using simple tools
- **Detailed** - Metadata, structure, and analysis
- **Visuals** - Preserve layout fidelity via PDF/HTML conversion (where applicable)

### Mirrored Directory Structure

The output directory mirrors source directory structure exactly:

```
output/
├── parsed_data/
│   └── [source-relative-path]/
│       └── filename.ext/
│           ├── parsing_results.json     # File-level metadata
│           ├── method1_name/         # First method output
│           │   ├── content.md or *.csv
│           │   ├── images/ or data/
│           │   └── metadata.json
│           ├── method2_name/         # Second method output
│           │   └── ...
│           └── orchestration_metadata.json # Orchestration tracking
└── orchestration_summary.json       # Top-level summary
```

### Incremental Parsing

The plugin uses SHA256 hashing to skip unchanged files on subsequent runs. Each parsed file includes a hash in its `parsing_results.json`, enabling efficient incremental updates.

### Documentation

Each parsing script includes comprehensive documentation:

- **Module docstrings**: Overview of file type, methods, dependencies, CLI alternatives
- **Method docstrings**: Detailed information for each method (purpose, advantages, when to use)
- **Inline comments**: Implementation details, C library requirements, CLI alternatives

See individual parser scripts for detailed documentation about each method.

## Core Principles

**Hybrid Artifacts**: Extract text/data (MD/JSON/CSV) + images (PNG/JPG) without duplication

**Mirror Structure**: Output directory mirrors source directory structure exactly for easy navigation

**Incremental Parsing**: Skip unchanged files by comparing SHA256 hashes for efficiency

**Multi-Method**: Apply all methods for comprehensive coverage and redundancy

**Error Handling**: Log errors but never halt orchestration on single file failures

**Documentation First**: Generate metadata files for each parsed file and top-level summary

## Common Use Cases

### Version Control for Office Documents

Convert binary Office files to text-based formats (Markdown, CSV, JSON) that work well with git and code review tools.

### Document Archive Migration

Extract content from legacy Office documents for migration to modern formats or search indexing.

### BI Report Analysis

Parse Power BI files to extract DAX measures, table schemas, and relationships for documentation.

### Batch Processing

Process entire directories of Office documents with automatic incremental updates.

### CI/CD Integration

Use scripts in automated pipelines - execute `orchestrate_parsing.py` independently of agent.

## Environment Requirements

The plugin uses:
- **uv** for Python package management (inline script metadata)
- **nix** for CLI tools (no installation required)
- **System libraries** (C++ standard library) for some Python packages

Some parsing methods require C library support. Individual scripts document these requirements in their comments and docstrings.

Scripts use uv inline metadata for self-contained execution - no Python environment setup required:

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

## Orchestration Patterns

### For Orchestrators

The `orchestrate_parsing.py` script implements:

- **Mirror Structure Preservation**: Output mirrors source directory structure
- **Hash-Based Incremental Parsing**: Skip unchanged files unless `--force` specified
- **Complete Method Execution**: Run all methods for each file, log errors, continue
- **Error Handling**: Log errors but never halt orchestration
- **Documentation First**: Generate metadata files and summary reports

See `SKILL.md` for detailed orchestration patterns and common code snippets.

## Using Individual Parser Scripts

After copying scripts to your project, you can run parsers individually:

```bash
# Parse a single PPTX file
cd /your/project/scripts/
./parse_pptx.py /path/to/presentation.pptx /path/to/output

# Parse a single DOCX file
./parse_docx.py /path/to/document.docx /path/to/output

# Parse a single XLSX file
./parse_xlsx.py /path/to/spreadsheet.xlsx /path/to/output

# Parse a single PDF file
./parse_pdf.py /path/to/document.pdf /path/to/output

# Parse a single PBIX file
./parse_pbix.py /path/to/report.pbix /path/to/output
```

Each script includes usage examples and detailed documentation about each method.

## Troubleshooting

### Script Execution Errors

**Missing dependencies**:
- Scripts use inline metadata - uv handles dependency installation automatically
- Ensure uv is installed and accessible
- Check Python version meets requirement: `>=3.11`

**Execute permissions**:
```bash
chmod +x scripts/*.py
```

**Path issues**:
- Use absolute paths when running scripts directly
- Ensure source and output directories exist

### C Library Errors

Some tools require system libraries. Individual scripts document these in comments.

Example for markitdown/docling:
```bash
nix shell nixpkgs#stdenv.cc.cc.lib --command bash -c "
  export LD_LIBRARY_PATH=$(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:$LD_LIBRARY_PATH &&
  uvx --from 'markitdown[pdf]' markitdown '$SOURCE_FILE'
"
```

### Missing Images

Not all parsing methods extract images. Check individual script documentation for method capabilities.

### Empty CSV Files

For Excel files, verify sheet names exist or check metadata files for table information.

### PBIX Parsing on Linux

Windows-specific Power BI tools are unavailable on Linux. Use pbixray or zipfile methods instead.

See `scripts/parse_pbix.py` for Linux limitations and recommended approaches.

## Format Notes

**XLSX**: CSV primary output, multiple sheets = multiple CSV files, formulas extracted separately
**PBIX**: Linux-limited, pbixray extracts tables/measures/metadata, zipfile gets raw contents
**Images**: Not all methods extract images (check script documentation)
**Formulas**: Preserved in openpyxl formulas method, evaluated as values in pandas methods

## Script Reference

All scripts are self-contained with comprehensive documentation:

- `scripts/parse_pptx.py` - PowerPoint parser with 4 methods
- `scripts/parse_docx.py` - Word document parser with 4 methods
- `scripts/parse_xlsx.py` - Excel spreadsheet parser with 4 methods
- `scripts/parse_pdf.py` - PDF parser with 4 methods
- `scripts/parse_pbix.py` - Power BI parser with 2 methods
- `scripts/orchestrate_parsing.py` - Main orchestration script

Each script includes:
- Module-level documentation with overview and usage
- Method-level docstrings with advantages, disadvantages, when to use
- Inline comments for implementation details and CLI alternatives
- C library requirement notes (where applicable)

## Architecture

```
plugins/doc-parsing/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── parse-docs.md
├── skills/
│   └── doc-parsing/
│       ├── SKILL.md                 # Comprehensive documentation with orchestration patterns
│       └── scripts/                # Self-contained Python scripts
│           ├── parse_pptx.py       # PPTX parser (4 methods)
│           ├── parse_docx.py       # DOCX parser (4 methods)
│           ├── parse_xlsx.py       # XLSX parser (4 methods)
│           ├── parse_pdf.py        # PDF parser (4 methods)
│           ├── parse_pbix.py       # PBIX parser (2 methods)
│           └── orchestrate_parsing.py  # Orchestrator
└── README.md
```

**Removed in refactoring**:
- `workflows/` directory - Information now embedded in scripts
- `resources/templates/` directory - No longer using Jinja2 templates
- Script generation workflow - Scripts are self-contained, no generation needed

## License

Part of gtd-cc plugin marketplace.

## Author

Nikhil Maddirala
