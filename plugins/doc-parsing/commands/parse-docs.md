---
name: parse-docs
description: Parse office documents using natural language - provide source and output directories
args:
  - name: request
    description: Natural language description of what to parse (must include source and output directories)
    required: true
---

# Parse Documents

Parse office and BI documents by extracting source_dir and output_dir from your natural language request.

## How It Works

This command parses your natural language request to identify:
- Source directory (where files are)
- Output directory (where parsed content goes)
- File types to process (optional - defaults to all supported)
- Force reparse flag (optional - defaults to skip unchanged)
- Dry run mode (optional - defaults to execute)

After extracting parameters, it invokes the doc-parsing skill orchestration workflow.

## Parameter Extraction

The command looks for these patterns in your request:

**Directory paths:**
- Absolute paths: `/home/user/documents`, `/data/docs`
- Relative paths: `./docs`, `~/documents`, `../my-files`
- Patterns: "from X to Y", "X to Y", "in X", "output to X"

**File type keywords:**
- PowerPoint: pptx, presentations, slides
- Word: docx, documents, word
- Excel: xlsx, spreadsheets, excel
- PDF: pdf, documents
- Power BI: pbix, power bi, reports
- "only [types]" or "just [types]"

**Option keywords:**
- Force reparse: "force", "reparse everything", "ignore cache", "regenerate", "skip hash"
- Dry run: "preview", "dry run", "show me what would happen", "what if"

**Examples:**

| User request | Extracted parameters |
|------------|-------------------|
| "Parse files from /data/docs to /data/output" | source_dir=/data/docs, output_dir=/data/output |
| "Parse ./docs to ./parsed" | source_dir=./docs, output_dir=./parsed |
| "Parse all PowerPoint files from ~/docs to ~/parsed" | source_dir=~/docs, output_dir=~/parsed, types=[pptx] |
| "Parse just PDFs and Excel files to output" | source_dir=./ (current), output_dir=output, types=[pdf,xlsx] |
| "Reparse everything from docs to parsed" | source_dir=docs, output_dir=parsed, force=true |
| "Preview what would be parsed from ./source" | source_dir=./source, output_dir=./ (default), dry_run=true |

## Clarification

If your request is ambiguous or missing required information, the command will ask:
- "What is the source directory?"
- "Where should I output the parsed content?"
- "Which file types should I process?" (if ambiguous)

## Supported File Types

- `.pptx` - PowerPoint
- `.docx` - Word
- `.xlsx` - Excel
- `.pdf` - PDF
- `.pbix` - Power BI

## Next Steps

After extracting parameters, the command will invoke the doc-parsing orchestration workflow which:
- Copies scripts to your project
- Applies all parsing methods for each file
- Creates mirrored directory structure
- Generates summary reports

For comprehensive documentation on orchestration principles, method details, and CLI alternatives, see: `doc-parsing/SKILL.md`
