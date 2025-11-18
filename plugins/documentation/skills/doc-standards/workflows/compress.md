---
description: Compress documentation in-place to improve clarity while preserving critical information
---

## Compress Documentation Workflow

Compress lengthy documentation in-place to improve clarity and reduce noise while preserving critical information.

## Overview

This workflow guides you through systematically compressing a document in-place. The goal is to reduce length while preserving critical information that matters for your use case and audience. The improved document replaces the original.

## Context

Before starting:

- You have a lengthy document to compress in-place
- You understand what information is critical vs. supplementary
- You know your target audience and their needs
- You're ready to improve the document's clarity by removing noise

## Your Task

- Goal: Compress documentation in-place to improve clarity
- Target: Remove noise while preserving all critical information
- Role: Technical editor improving the document through careful compression

### Step 1: Identify the Document and Target Compression

```bash
# Locate the file to compress
ls -la /path/to/file

# Check file size
wc -l /path/to/file
wc -w /path/to/file

# Review current length against guidelines in SKILL.md
```

Decide on target compression:

- **Light compression** (2-3×) - Remove examples and explanations, keep structure and details
- **Medium compression** (5-8×) - Remove verbose explanations, keep decisions and critical details
- **Heavy compression** (10×+) - Keep only essential details, API contracts, thresholds, decisions

Choose based on:

- Document type (API reference compresses more than tutorials)
- Audience (expert teams can compress more heavily)
- Use case (quick lookup vs. learning reference)
- Detail preservation needs

### Step 2: Understand What's Critical

Identify what your audience *must* have for their use case:

```bash
# For API reference: function signatures, parameters, error codes
# For guides: key decisions, critical steps, caveats
# For architecture: components, data flow, deployment topology
# For configuration: all options, defaults, constraints
```

Ask:

- What would break if removed?
- What prevents errors or misunderstanding?
- What numbers/thresholds are non-obvious?
- What gotchas does my audience need to know?

### Step 3: Extract Critical Elements

Systematically identify what to keep:

```bash
# Scan for key terms and concepts
grep -E "^##? |^###? " /path/to/file

# Find defined terms
grep -E "\*\*.*\*\*|__.*__" /path/to/file

# Find numbers and constraints
grep -E "[0-9]+" /path/to/file

# Find decisions and recommendations
grep -E "should|must|always|never|use when|avoid" /path/to/file

# Find warnings and caveats
grep -E "important|note|caveat|gotcha|careful|watch out|exception" /path/to/file
```

Preserve:

- Definitions of concepts
- Key decisions and their rationale
- Numbers, thresholds, constraints, SLAs
- Caveats, gotchas, limitations
- API contracts and function signatures
- Configuration options and defaults

Remove:

- Verbose explanations (condense to essentials)
- Repeated information (keep once, link elsewhere)
- Examples (unless essential for understanding)
- Marketing language and motivation
- Detailed walkthroughs (replace with quick reference)

### Step 4: Choose Your Format

The SKILL.md defines acceptable document types and their length guidelines. Choose a format that:

- Matches your document type
- Meets length targets
- Preserves critical information
- Is scannable for your audience

Options:

- Dense bullet points
- Structured sections (definitions, decisions, details, caveats)
- Quick reference tables
- Glossary/term definitions
- API contracts only
- Checklist format
- Other formats your team prefers

### Step 5: Compress the Document In-Place

Rewrite your document using your chosen format, replacing the original:

```bash
# You will be editing the original document directly
# Preserve the filename - this becomes the improved version
# /path/to/file.md (not a new file)
```

Include only:

- What your audience needs for their use case
- Critical details, numbers, constraints
- Key decisions and gotchas
- Skip: verbose explanations, repeated content, examples (unless essential)

Guidelines:

- Use short, direct sentences
- Preserve all terminology and variable names exactly
- Keep all numbers, thresholds, and constraints
- Make it scannable
- Use formatting (bold, tables, bullets) to aid scanning

### Step 6: Measure Compression

After completing your edits, calculate the compression achieved:

```bash
# You can use git to see the before/after stats
# git diff will show the reduction in lines and content
git diff /path/to/file.md

# Or manually count if the file is not yet committed
# Before: (your original line/word count from Step 1)
# After: run the commands from Step 1 again to see new stats
wc -l /path/to/file.md
wc -w /path/to/file.md
```

Compare the achieved compression to your target compression level from Step 1.

### Step 7: Verify Accuracy of Compressed Content

Before committing, verify the compressed document:

- Do all numbers match the source materials exactly?
- Have you changed any terminology or simplified it incorrectly?
- Are all critical decisions captured?
- Are important caveats included?
- Do all internal cross-references still work?
- Is the format consistent with SKILL.md guidelines?
- Is the document scannable and well-organized?

### Step 8: Summarize What Was Removed

Document what was removed and why, for your commit message:

- Removed verbose explanations → kept essential details
- Removed examples → focus on core concepts
- Removed background context → preserved key decisions
- Removed repeated information → consolidated to single mentions
- Other removals: [specify based on your document]

This summary will help reviewers understand the intent of your compression.

### Step 9: Save the Compressed Document

Since you're compressing in-place, the filename remains the same:

```bash
# The original document has been replaced with the compressed version
# Filename stays the same:
# README.md (now compressed)
# docs/api-reference.md (now compressed)
# docs/architecture.md (now compressed)

# Save your changes using your editor
```

### Step 10: Commit the Compressed Document

Commit your in-place compression changes:

```bash
git add /path/to/file.md
git commit -m "docs: compress [document name]

- Original: X lines/words
- Compressed: Y lines/words (~1:[ratio]× compression)
- Compression level: [light/medium/heavy]
- Removed: [summarize what was removed and why]
- Preserved: [summarize critical content kept]"
```

The commit message should focus on what was removed and why, since the reader can see the actual changes in the diff.

## Examples

### Example 1: API Reference (Medium Compression)

Compress docs/api-reference.md in-place:
- Before: 800 lines
- After: 100-150 lines (5-8× compression)
- Format: Function signatures + critical details in tables
- Removed: Verbose explanations, basic examples, introductory content

### Example 2: Architecture Document (Light Compression)

Compress docs/architecture.md in-place:
- Before: 600 lines
- After: 200-300 lines (2-3× compression)
- Format: Components + data flow + deployment, with essential details preserved
- Removed: Historical context, detailed walkthroughs, background explanations

### Example 3: Configuration Reference (Heavy Compression)

Compress docs/configuration.md in-place:
- Before: 400 lines
- After: 40-50 lines (8-10× compression)
- Format: Table of options, defaults, constraints only
- Removed: Use case examples, detailed descriptions, troubleshooting guides

## Guidelines

- **Choose compression level consciously** - Match to your audience's needs
- **Preserve critical information** - Never compress away gotchas, constraints, or decisions
- **Keep exact terminology** - No simplification or substitution
- **Keep all numbers** - Don't round or approximate
- **Make it scannable** - Use formatting to aid quick lookup
- **Document removals** - Note what was condensed and why
- **Verify accuracy** - Cross-check every detail against source
- **Follow SKILL.md guidelines** - Respect length targets for your document type

## Success Criteria

- ✅ Target compression level achieved
- ✅ All critical information preserved for your audience
- ✅ All numbers, constraints, and decisions included exactly
- ✅ Format appropriate for document type
- ✅ Document is scannable and well-organized
- ✅ Terminology preserved exactly as in original
- ✅ All internal cross-references still work
- ✅ Removals documented in commit message (what was removed and why)
- ✅ Compressed document committed with clear commit message
