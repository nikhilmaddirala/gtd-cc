---
name: get-docs
description: Extract structured documentation from websites using content-extraction skill. Handles documentation platforms like Docusaurus, GitBook, ReadTheDocs, and Sphinx.
---

# Get Documentation

## Overview

This command guides you through extracting structured documentation from documentation sites. Automatically detects documentation platform type and applies appropriate extraction patterns.

## Context

User provides documentation URL to extract. The command identifies documentation platform (Docusaurus, GitBook, ReadTheDocs, Sphinx, or generic) and uses optimized extraction strategies.

## Process

### Step 1: Ask for Documentation URL

Request the documentation URL:
```
Enter the documentation URL to extract:
```

### Step 2: Determine Extraction Scope

Ask about extraction preferences:
```
What do you want to extract?

1. Single documentation page
2. Complete documentation site
3. Specific section (e.g., API docs, tutorials)
```

### Step 3: Detect Documentation Platform

Analyze URL and identify documentation platform:
```bash
# Check for platform indicators
# - Docusaurus: /docs/, versioned URLs
# - GitBook: docs.gitbook.com structure
# - ReadTheDocs: readthedocs.io, /en/latest/
# - Sphinx: /_static/, generic structure
```

### Step 4: Execute Extraction

**Option 1: Single Page**

Use crawl4ai-toolkit with platform-specific selectors:
```bash
# Extract single page
python skills/crawl4ai-toolkit/scripts/basic_crawler.py [URL]

# Save with appropriate filename
```

**Option 2: Complete Documentation Site**

Use site-crawling with content-extraction patterns:
```bash
# Crawl entire documentation
python skills/site-crawling/examples/intelligent-crawler.py [URL]

# Apply documentation-specific filtering (from content-extraction skill)
# - Focus on /docs/, /api/, /guide/ paths
# - Exclude navigation, footer, sidebar
# - Preserve code blocks and examples
```

**Option 3: Specific Section**

Use targeted crawling:
```bash
# Crawl specific documentation section
uvx crawl4ai crawl \
  --url "[BASE_URL]/[SECTION]" \
  --output-dir "docs/[section-name]" \
  --max-depth 3
```

### Step 5: Structure Output

Organize extracted documentation:
```
docs/
├── README.md              # Table of contents
├── getting-started.md     # Getting started section
├── api/                  # API documentation
│   ├── authentication.md
│   ├── endpoints.md
│   └── examples.md
├── guides/               # Guides and tutorials
│   └── ...
└── reference/            # Reference materials
```

### Step 6: Generate Table of Contents

Create navigation structure:
```bash
# Generate TOC from extracted content
# Use patterns from content-extraction skill
# - Detect heading hierarchy
# - Create cross-references
# - Preserve documentation structure
```

### Step 7: Verify Extraction

Check that documentation was extracted correctly:
```bash
# Verify all sections present
ls -lh docs/

# Check code blocks preserved
grep -c '```' docs/*.md

# Verify links work
grep -c '\[.*\](.*\.md)' docs/*.md
```

## Common Use Cases

### API Documentation
```bash
# Extract API docs from Docusaurus site
python skills/crawl4ai-toolkit/scripts/basic_crawler.py \
  https://api.example.com/docs

# Use platform-specific CSS selectors
css_selector="article, .markdown, .theme-doc-markdown"
```

### User Guides
```bash
# Extract user guides from GitBook
uvx crawl4ai crawl \
  --url "https://docs.gitbook.com/product" \
  --output-dir "docs/user-guides" \
  --max-depth 3
```

### Technical Reference
```bash
# Extract technical reference (Sphinx-based)
python skills/content-extraction/examples/api-docs-extraction.py \
  https://ref.example.com
```

## Skills Used

- content-extraction - For documentation platform detection and specialized extraction
- crawl4ai-toolkit - For core crawling functionality
- site-crawling - For multi-page documentation crawling

## Platform-Specific Tips

### Docusaurus Sites
- Use `.theme-doc-markdown` CSS selector
- Exclude `.pagination`, `.table-of-contents`
- Preserve versioned navigation

### GitBook Sites
- Use `.gitbook-root`, `.page-body` CSS selector
- Exclude `.sidebar`, `.navigation`
- Handle search and filters

### ReadTheDocs Sites
- Use `.document`, `.bd-content` CSS selector
- Exclude `.sidebar`, `.toctree-wrapper`
- Handle version dropdowns

### Sphinx Sites
- Use `.document`, `.body` CSS selector
- Exclude `.sphinxsidebar`, `.related-topics`
- Preserve code blocks and examples

## Tips

- Start with single page to test extraction
- Check platform detection results
- Preserve heading hierarchy for navigation
- Verify code examples are intact
- Test internal links after extraction
