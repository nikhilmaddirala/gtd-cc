---
name: doc-audit
description: Audit documentation health and identify problems and gaps
---

# Documentation Audit

## Overview

This command guides users through the docs-management skill's update.md workflow with audit parameters interactively. CRITICAL: You MUST use the docs-management skill for this task.

## Context

This command defaults to scope=all, type=minor parameters for comprehensive documentation health audit and systematic maintenance. User may provide specific areas to focus on.

## Process

- Load the docs-management skill and its update.md workflow; you MUST do this first.
- Parse the user input to understand if they want to focus on specific areas or do a complete audit.
- Interactively guide the user through the docs-management's update.md workflow with scope=all, type=minor:
  1. Scan all documentation layers for common issues:
     - Outdated information and version mismatches
     - Broken links and dead references
     - Missing documentation for new features
     - Duplicated content across layers
     - Coverage gaps in documentation
  2. Check README length and readability (200-500 line guidelines)
  3. Verify directory READMEs exist and explain local context
  4. Validate /docs folder organization (if Phase 3 project)
  5. Generate comprehensive audit report with recommendations
  6. Prioritize fixes based on impact and effort
- Collect inputs and execute each step with confirmation.