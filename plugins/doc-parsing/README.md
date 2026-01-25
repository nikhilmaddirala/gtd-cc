# Document Parsing Plugin

Parse Office and BI documents into repository-friendly artifacts using focused single-type skills.

## Supported File Types

| Type | Extension | Skill | Method |
|------|-----------|-------|--------|
| PowerPoint | `.pptx` | pptx-to-markdown | LibreOffice pipeline (PDF to images to markdown) |
| Word | `.docx` | docx-parsing | python-docx with table extraction |
| Excel | `.xlsx` | xlsx-parsing | pandas with CSV exports |
| PDF | `.pdf` | pdf-parsing | Multi-method extraction |
| Power BI | `.pbix` | pbix-parsing | pbixray for metadata |

## Installation

Install from marketplace:

```bash
/plugin marketplace add nikhilmaddirala/gtd-cc
/plugin install doc-parsing@gtd-cc
```

## Usage

### Orchestrate Multiple Files

Use the orchestration command for batch processing:

```bash
/orchestrate-parsing Parse files from ./documents to ./parsed
/orchestrate-parsing Parse PowerPoint and Word from ~/presentations to ~/parsed
/orchestrate-parsing Reparse everything from ./docs to ./output, force regenerate
/orchestrate-parsing Process only Excel files from ./data to ./parsed
```

The orchestration command provides:

- Hash-based incremental parsing (skip unchanged files)
- Mirrored directory structure in output
- Multi-format batch processing
- Runtime overrides (source, output, types, force)
- Comprehensive summary JSON

### Parse Single Files

Invoke individual skills directly:

**PowerPoint:**
```bash
./scripts/convert_pptx_to_markdown.py presentation.pptx output/
```

**Word documents:**
```bash
./scripts/parse_docx.py report.docx output/
```

**Excel spreadsheets:**
```bash
./scripts/parse_xlsx.py data.xlsx output/
```

**PDF documents:**
```bash
./scripts/parse_pdf.py document.pdf output/
```

**Power BI files:**
```bash
./scripts/parse_pbix.py report.pbix output/
```

## Architecture

```
doc-parsing/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   └── orchestrate-parsing.md
├── skills/
│   ├── pptx-to-markdown/
│   ├── docx-parsing/
│   ├── xlsx-parsing/
│   ├── pdf-parsing/
│   └── pbix-parsing/
└── README.md
```

## Output Structure

**Single file (PPTX):**
```
output/
├── presentation.md
├── presentation-text.md
├── pdf/
│   └── presentation.pdf
└── slide-images/
    └── slide-01.jpg ... slide-N.jpg
```

**Orchestrated batch:**
```
output_dir/
├── [mirrored-source-path]/
│   └── filename.ext/
│       ├── parsing_summary.json
│       └── [method_outputs]/
└── parsing_summary.json
```

## NixOS Requirements

Some parsers require system libraries:

```bash
nix shell nixpkgs#stdenv.cc.cc.lib nixpkgs#zlib --command bash -c "
  export LD_LIBRARY_PATH=\$(nix eval --raw nixpkgs#stdenv.cc.cc.lib)/lib:\$(nix eval --raw nixpkgs#zlib)/lib:\$LD_LIBRARY_PATH &&
  rm -rf ~/.cache/uv/environments-v2/parse-* || true &&
  ./scripts/orchestrate_parsing.py
"
```

Required for:
- XLSX files (pandas/numpy)
- PBIX files (apsw/sqlite)
- PDF files (pypdfium2)

PPTX and DOCX files work without nix shell.
