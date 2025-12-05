---
name: doc-compress
description: Create condensed versions of documentation for quick reference and lookup
---

# Documentation Compression

## Overview

This command guides users through the docs-management skill's compress.md workflow interactively. CRITICAL: You MUST use the docs-management skill for this task.

## Context

User may provide target documents or areas to compress. This command should parse input and guide users through reducing documentation bloat while preserving critical information.

## Process

- Load the docs-management skill and its compress.md workflow; you MUST do this first.
- Parse the user input to understand which documents need compression or if they want a comprehensive compression process.
- Interactively guide the user through the docs-management's compress.md workflow step by step:
  1. Identify bloated documentation (READMEs >500 lines, verbose sections)
  2. Analyze content for essential vs. nice-to-have information
  3. Guide through creating condensed versions:
     - Extract key facts and critical information
     - Remove redundant explanations and verbose descriptions
     - Create quick reference guides and cheat sheets
     - Maintain links to detailed content in /docs
  4. Generate compressed output formats:
     - Quick reference cards
     - FAQ sections
     - TL;DR summaries
     - Essential command lists
  5. Verify critical information is preserved and accessible
- Collect inputs and execute each step with confirmation.