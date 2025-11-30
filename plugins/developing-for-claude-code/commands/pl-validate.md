---
name: pl-validate
description: Validate all plugins for structure, manifests, and documentation
---

# Validate existing plugins

## Overview

This command guides you through validating plugins in the marketplace for proper structure, manifest correctness, naming conventions, and documentation completeness. It's essential before releasing updates or submitting contributions.

## Context

You provide:
- Plugin directory or plugin name to validate
- Validation scope (structure only, full validation including tests, or specific aspects)

The command automatically checks against gtd-cc architectural patterns and conventions.

## Process

Follow the plugin-development-gtd skill and execute the validate-existing-plugins workflow exactly as written. The workflow will:

- Validate plugin directory structure
- Verify manifest JSON syntax and required fields
- Check component naming conventions
- Validate all referenced file paths exist
- Confirm all required documentation files present
- Check for broken references or circular dependencies
- Generate validation report with any issues found
- Provide recommendations for fixes
