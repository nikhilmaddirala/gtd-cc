---
name: get-docs
description: Interactive guide for extracting structured documentation from websites
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion]
argument-hint: [URL] - the documentation site to extract from
---

# Extract Documentation

This command guides you through extracting structured documentation from various platforms using the documentation-extraction skill. It handles API docs, tutorials, reference guides, and knowledge bases.

## Interactive Documentation Extraction

### Step 1: Documentation Site Analysis
**Provide the documentation site URL you want to extract.**

I'll identify the documentation platform and ask about:
- **Platform type** (Docusaurus, GitBook, ReadTheDocs, Sphinx, etc.)
- **Content scope** (entire docs site, specific sections, or API reference only)
- **Output organization** (single file, structured sections, or by topic)

### Step 2: Extraction Configuration

Based on the platform and your needs:
- **Platform detection** and specialized extraction
- **Table of contents** discovery and navigation
- **Code example** preservation and formatting
- **Cross-reference** and link handling

### Step 3: Processing and Organization

I'll help you:
- **Section organization** by hierarchy and topic
- **Code block** preservation with syntax highlighting
- **Navigation structure** extraction
- **Multi-page** documentation consolidation

## Documentation Platform Support

### Docusaurus Sites
```
Patterns: .theme-doc-markdown, article selectors
Features: React-based docs with versioning
Content: Markdown with frontmatter
Navigation: Sidebar and version switching
```

### GitBook Sites
```
Patterns: .gitbook-root, page-body selectors
Features: Collaborative documentation platform
Content: Rich text with embedded media
Navigation: Book-style organization
```

### ReadTheDocs/Sphinx
```
Patterns: .document, .bd-content selectors
Features: Python documentation standard
Content: reStructuredText conversion
Navigation: ToC trees and cross-references
```

### Custom Documentation
```
Patterns: Generic article and content selectors
Features: Adaptive extraction based on structure
Content: HTML with semantic markup
Navigation: Custom navigation elements
```

## Extraction Strategies

### Complete Documentation Set
```
Purpose: Extract entire documentation site
Scope: All pages and sections
Organization: Hierarchical structure
Output: Structured markdown with TOC
```

### API Reference Only
```
Purpose: Extract API documentation specifically
Scope: Endpoints, parameters, examples
Organization: By API version or module
Output: Structured JSON with code examples
```

### Tutorial Extraction
```
Purpose: Extract step-by-step tutorials
Scope: How-to guides and tutorials
Organization: By difficulty or topic
Output: Sequential instruction sets
```

### Knowledge Base Consolidation
```
Purpose: Merge scattered documentation
Scope: Multiple related pages
Organization: By topic or category
Output: Single searchable document
```

## Content Processing Features

### Structure Preservation
- **Heading hierarchy** maintenance
- **Table of contents** generation
- **Section numbering** preservation
- **Cross-reference** link handling

### Code Example Handling
- **Syntax highlighting** preservation
- **Code block** identification
- **Inline code** formatting
- **Example output** capture

### Media and Assets
- **Image alt text** preservation
- **Diagram descriptions** when available
- **Embedded content** references
- **Link validation** and updating

## Output Formats

### Structured Markdown
```
# Documentation Title
[Auto-generated TOC]
## Section 1
### Subsection 1.1
[Content with preserved formatting]
```

### JSON Structure
```
{
  "metadata": {...},
  "sections": [...],
  "api_reference": {...},
  "tutorials": [...]
}
```

### Single File Export
```
Complete documentation consolidated into
single searchable markdown file with
navigation and cross-references
```

## Quality Enhancements

### Content Cleaning
- **Navigation removal** (keep only content)
- **Footer/header** cleanup
- **Advertisement** filtering
- **Redundant content** removal

### Link Processing
- **Internal links** converted to anchors
- **External links** preserved and validated
- **Cross-references** maintained
- **Dead link** identification

### Format Optimization
- **Code blocks** properly fenced
- **Tables** formatted correctly
- **Lists** structured consistently
- **Emphasis** normalized

## Common Use Cases

### API Documentation Migration
```
URL: https://api.example.com/docs
Goal: Migrate to new documentation system
Strategy: API reference extraction
Output: Structured API docs with examples
```

### Knowledge Base Creation
```
URL: https://help.example.com
Goal: Create internal knowledge base
Strategy: Complete documentation extraction
Output: Consolidated markdown knowledge base
```

### Tutorial Compilation
```
URL: https://learn.example.com
Goal: Create offline tutorial package
Strategy: Tutorial-focused extraction
Output: Sequential learning materials
```

### Documentation Backup
```
URL: https://docs.example.com
Goal: Create local backup of documentation
Strategy: Complete site extraction
Output: Full documentation archive
```

## Advanced Features

### Multi-Version Documentation
- **Version detection** and separation
- **Cross-version** comparison
- **Migration path** identification

### Interactive Elements
- **Code playgrounds** preservation
- **Interactive demos** references
- **Sample data** extraction

### Localization Support
- **Language detection**
- **Multi-language** documentation
- **Translation** workflow support

## Getting Started

Provide the documentation URL you want to extract, and I'll guide you through the optimal extraction strategy for that platform and your specific needs!