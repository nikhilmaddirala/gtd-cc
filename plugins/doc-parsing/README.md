# Document Parsing Plugin

Parse proprietary Office and BI file formats into repository-friendly artifacts with multi-method extraction strategies.

## Overview

The doc-parsing plugin transforms binary Office documents (PowerPoint, Word, Excel) and BI files (Power BI, PDF) into structured, versionable content. The plugin provides self-contained Python parsing scripts that can be copied to any project and adapted for project-specific document processing workflows.

Each file type supports multiple parsing methods optimized for different use cases - comprehensive extraction, speed, or detailed analysis.

## Supported File Types

| Type | Extension | Methods | Primary Outputs |
|------|-----------|---------|-----------------|
| PowerPoint | `.pptx` | 4 | Markdown text, images, slide notes |
| Word | `.docx` | 4 | Markdown text, images, tables |
| Excel | `.xlsx` | 4 | CSV files, JSON metadata, formulas |
| PDF | `.pdf` | 4 | Markdown text, tables, layout info |
| Power BI | `.pbix` | 2 | JSON metadata, DAX measures, model structure |

## Installation

Install from gtd-cc marketplace:

```bash
/plugin marketplace add nikhilmaddirala/gtd-cc
/plugin install doc-parsing@gtd-cc
```

## Commands

### /parse-docs

Parse office documents using natural language requests.

**Usage:**

```bash
/parse-docs Parse files from [source-dir] to [output-dir]
```

**Examples:**

```bash
# Parse all supported files
/parse-docs Parse files from ./documents to ./parsed

# Parse specific file types
/parse-docs Parse PowerPoint and Word files from ~/presentations to ~/parsed

# Force reparse everything
/parse-docs Reparse everything from ./docs to ./output, force regenerate

# Parse specific subdirectory
/parse-docs Parse all Excel files in ./data/reports to ./parsed/reports
```

The command intelligently extracts parameters from natural language and:
1. Copies parsing scripts to your project
2. Adapts the orchestrator with your directories
3. Executes the parsing workflow
4. Creates mirrored output structure

## Architecture

```
plugins/doc-parsing/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── commands/
│   └── parse-docs.md            # Natural language command entrypoint
├── skills/
│   └── doc-parsing/
│       ├── SKILL.md             # Comprehensive usage guide
│       └── scripts/             # Self-contained Python scripts
│           ├── parse_pptx.py    # PowerPoint parser (4 methods)
│           ├── parse_docx.py    # Word parser (4 methods)
│           ├── parse_xlsx.py    # Excel parser (4 methods)
│           ├── parse_pdf.py     # PDF parser (4 methods)
│           ├── parse_pbix.py    # Power BI parser (2 methods)
│           └── orchestrate_parsing.py  # Batch orchestrator
└── README.md                    # This file
```

## How It Works

### Multi-Method Extraction

Each file type is processed using all available methods for comprehensive coverage:

- **Comprehensive** - Full content + images + metadata (complex tools)
- **Fast** - Text-only extraction (simple tools)
- **Detailed** - Structure, formatting, and analysis
- **Specialized** - Format-specific features (formulas, DAX, layout)

All methods execute independently - failure in one does not stop others.

### Mirrored Directory Structure

The output directory mirrors source directory structure exactly:

```
output-dir/
├── [source-relative-path]/
│   └── filename.ext/
│       ├── parsing_results.json      # File-level metadata
│       ├── method-1-name/            # First method output
│       │   ├── content.md or *.csv
│       │   └── images/ (if applicable)
│       ├── method-2-name/            # Second method output
│       │   └── ...
│       └── orchestration_metadata.json
└── orchestration_summary.json         # Top-level summary
```

### Incremental Parsing

The plugin uses SHA256 hashing to skip unchanged files:
- Files with matching hash in `parsing_results.json` are skipped
- Only changed files are re-parsed automatically
- Use "force" keyword to re-parse everything

### Self-Contained Scripts

All scripts use uv inline metadata for dependency management:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "python-pptx>=1.0.0",
#   "pandas>=2.0.0",
# ]
# ///
```

Scripts include comprehensive documentation:
- Module docstrings: Overview, methods, dependencies
- Method docstrings: Purpose, advantages, when to use
- Inline comments: Implementation details, CLI alternatives

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

Run orchestrator in automated pipelines for continuous document parsing.

## Environment Requirements

The plugin uses:
- **uv** for Python package management (inline script metadata)
- **Python 3.11+** for script execution
- **nix** (optional) for CLI tools and system libraries

Some parsing methods require C++ standard library. Wrap execution when needed:

```bash
nix shell nixpkgs#stdenv.cc.cc.lib --command bash -c "
  export LD_LIBRARY_PATH=\$(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:\$LD_LIBRARY_PATH &&
  ./scripts/parse_docx.py document.docx output/
"
```

## Troubleshooting

### Script Execution Errors

```bash
# Fix permissions
chmod +x scripts/*.py

# Verify Python version
python --version  # Must be >=3.11
```

### C Library Errors

Some methods (markitdown, pandas with certain features) require system libraries. Use nix shell wrapper as shown above.

### Missing Images

Not all methods extract images. Check method descriptions in parser script docstrings. For images, use:
- **PPTX**: python-pptx-images or python-pptx-detailed methods
- **DOCX**: python-docx-detailed or python-docx-basic methods
- **PDF**: pdfplumber method (limited support)

### Empty CSV Files

For Excel files, verify sheet names exist. Check `metadata.json` in method output directory.

### PBIX Parsing on Linux

Windows-specific Power BI tools are unavailable on Linux. Use:
- **pbixray** method for metadata and measures
- **zipfile** method for raw contents

## Format Notes

- **XLSX**: Multiple sheets output as separate CSV files, formulas in separate JSON
- **PBIX**: Limited on Linux, pbixray provides best metadata extraction
- **Images**: Check method documentation - not all methods extract images
- **Formulas**: Excel formulas preserved in openpyxl-formulas method only
- **Layout**: PDF layout preservation best with pdfminer-layout method

## Documentation

For comprehensive documentation on orchestration patterns, method details, and advanced usage:

- **SKILL.md**: Complete usage guide with workflows and patterns
- **Parser scripts**: Detailed method documentation in script docstrings
- **Command documentation**: See `/parse-docs` command for natural language usage

## License

Part of gtd-cc plugin marketplace.

## Author

Nikhil Maddirala
