---
name: orchestrate-parsing
description: Orchestrate document parsing across all file types with incremental hash-based processing. Supports pptx, docx, xlsx, pdf, pbix formats.
---

# Orchestrate Document Parsing

Orchestrate batch document parsing with incremental hash-based processing.

## Context

User provides a natural language request describing a batch document parsing task.

## Process

### Step 1: Parse user request

Extract parameters from the natural language request:

**Required:**
- **Source directory**: Look for paths after "from", "in", or standalone directory paths

**Optional:**
- **Output directory**: Look for paths after "to", "output to", "save to". Default to `./parsed_data`
- **File types**: Look for format keywords (pptx, docx, xlsx, pdf, pbix, "all"). Default to all
- **Force reparse**: Check for "force", "regenerate", "reparse all" keywords. Default to False

**Example parsing:**
- "Parse files from ./documents to ./parsed" → source=./documents, output=./parsed
- "Parse PowerPoint files from ~/presentations" → source=~/presentations, output=(ask), types=[pptx]
- "Reparse everything from ./docs" → source=./docs, force=True

### Step 2: Copy scripts to project

Create `scripts/` directory in the project and copy:
- `orchestrate_parsing.py` - Main orchestration script
- Individual parser scripts for each file type:
  - `parse_pptx.py` (from pptx-to-markdown skill)
  - `parse_docx.py` (from docx-parsing skill)
  - `parse_xlsx.py` (from xlsx-parsing skill)
  - `parse_pdf.py` (from pdf-parsing skill)
  - `parse_pbix.py` (from pbix-parsing skill)

Make all scripts executable.

### Step 3: Adapt orchestrate_parsing.py

Edit the DEFAULT_* variables in `orchestrate_parsing.py`:

```python
DEFAULT_SOURCE_DIR = Path("./documents")  # From user request
DEFAULT_OUTPUT_DIR = Path("./parsed")     # From user request
DEFAULT_FILE_TYPES = ["pptx", "docx"]     # From user request or None for all
DEFAULT_FORCE_REPARSE = False             # From user request
```

### Step 4: Execute orchestration

Run the orchestrator:

```bash
cd scripts/
./orchestrate_parsing.py
```

Or use runtime overrides:

```bash
# Override directories
./orchestrate_parsing.py /custom/source /custom/output

# Force reparse all
./orchestrate_parsing.py --force

# Process specific file types only
./orchestrate_parsing.py --types=pptx,docx
```

### Step 5: Report results

Check `parsing_summary.json` in the output directory and report:
- Total files discovered
- Successfully parsed count
- Skipped (unchanged) count
- Errors with troubleshooting guidance

## Examples

```bash
/orchestrate-parsing Parse files from ./documents to ./parsed
/orchestrate-parsing Parse PowerPoint and Word from ~/presentations to ~/parsed
/orchestrate-parsing Reparse everything from ./docs to ./output, force regenerate
/orchestrate-parsing Process only Excel files from ./data to ./parsed
```

## Output Structure

```
output_dir/
├── [mirrored-source-path]/
│   └── filename.ext/
│       ├── parsing_summary.json
│       ├── [method_outputs]/
│       └── ...
└── parsing_summary.json
```

## Parser Details

Each file type uses a specialized parser:
- **pptx**: LibreOffice pipeline (PDF → images → markdown)
- **docx**: python-docx with table extraction
- **xlsx**: pandas with CSV exports
- **pdf**: Multi-method extraction
- **pbix**: pbixray for metadata
