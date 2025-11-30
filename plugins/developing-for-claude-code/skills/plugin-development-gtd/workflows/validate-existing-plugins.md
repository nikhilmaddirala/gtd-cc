---
description: Validate all plugins for structure, manifests, and documentation
---

# Validate Existing Plugins Workflow

## Overview

This workflow provides comprehensive validation of all plugins in the gtd-cc marketplace including structure, manifests, documentation completeness, and marketplace consistency. Commands and agents should reference this workflow directly and follow the process exactly as written.

## Context

User specifies whether to validate all plugins or specific target plugins. This workflow scans the marketplace manifest and validates each registered plugin against gtd-cc standards and requirements.

## Guidelines

Follow these general guidelines when executing this workflow:

- Always validate JSON manifests using `jq .` before processing
- Use absolute paths for all file operations to avoid ambiguity
- Generate clear, actionable validation reports for any issues found
- Test plugin discovery and installation when possible
- Follow gtd-cc validation criteria consistently across all plugins
- **Reference validation patterns from `../references/common-patterns.md`** for detailed checks

## Process

### 1. Scan marketplace and identify plugins

- Access marketplace manifest from `.claude-plugin/marketplace.json`
- Verify marketplace file exists and is valid JSON
- List all registered plugins with their paths
- Count total plugins for validation scope

### 2. Validate each plugin structure and manifests

For each plugin, validate using patterns from `../references/common-patterns.md`:

- Check plugin directory exists and is accessible
- Validate plugin manifest using JSON validation commands
- Verify README.md exists for documentation completeness
- Check for required subdirectories (commands, agents, skills)
- Validate plugin name follows kebab-case conventions

### 3. Check component registration consistency

Validate that all registered components exist and are properly referenced:
- Use component discovery patterns to check file existence
- Validate command file paths match registered components
- Validate agent file paths match registered components
- Validate skill file paths match registered components
- Ensure all paths are relative to plugin root

### 4. Validate marketplace consistency

- Check for duplicate plugin names across marketplace
- Validate marketplace manifest JSON structure and syntax
- Verify all plugin paths are accessible and correct
- Check marketplace follows gtd-cc naming conventions

### 5. Generate validation report

- Generate clear, actionable validation summary
- Count successful validations vs. errors found
- Provide specific recommendations for fixing issues
- Use validation report patterns from `../references/common-patterns.md`
- Return appropriate exit codes based on validation results

## Final Review

Verify that the plugin validation workflow completed successfully:

- [ ] Marketplace manifest scanned successfully
- [ ] All registered plugins found and accessible
- [ ] Plugin directory structure validated for each plugin
- [ ] Plugin manifests are valid JSON with required fields
- [ ] Component registration consistency verified
- [ ] README files exist for all plugins
- [ ] Marketplace consistency checked (no duplicates, valid JSON)
- [ ] Validation report generated with clear actionable items
- [ ] All naming conventions followed consistently
- [ ] Plugin discovery tested where possible