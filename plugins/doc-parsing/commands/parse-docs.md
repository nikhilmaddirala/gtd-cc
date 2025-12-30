---
name: parse-docs
description: Parse office documents from source directory to output directory - supports pptx, docx, xlsx, pdf, pbix formats
args:
  - name: request
    description: Natural language description of parsing request (must include source and output directories)
    required: true
---

# Parse Documents

Parse Office and BI documents using multi-method extraction.

## Context

User provides a natural language request describing a document parsing task.

## Process

Load the doc-parsing skill and pass the user's request directly to it. The skill will:
- Parse the natural language request to extract parameters
- Execute the appropriate workflow based on the request

## Examples

```bash
/parse-docs Parse files from ./documents to ./parsed
/parse-docs Parse PowerPoint and Word files from ~/presentations to ~/parsed
/parse-docs Reparse everything from ./docs to ./output, force regenerate
```

Supports: PowerPoint, Word, Excel, PDF, Power BI files
