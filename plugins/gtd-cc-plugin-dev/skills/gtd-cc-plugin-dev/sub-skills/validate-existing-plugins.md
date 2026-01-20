---
description: Validate gtd-cc patterns by wrapping official plugin-dev skill
---

# Validate existing plugins

## Overview

This sub-skill validates that plugins follow gtd-cc architectural patterns. It wraps the official plugin-dev skill for mechanical validation and adds gtd-cc-specific pattern checks.

CRITICAL: You MUST use the official plugin-dev skill for base validation. Let plugin-dev handle its own internal routing.


## Context

User wants to validate one or more plugins before release or contribution. They may specify a single plugin or request validation of all marketplace plugins.


## Process

1. Run plugin-dev validation
   - Use the official plugin-dev skill
   - Check directory structure, manifests, component registration

2. Check gtd-cc-specific patterns
   - Commands are thin wrappers (reference skills, no inline logic)
   - Agents are thin wrappers (reference skills, no inline logic)
   - Skills have proper structure (Overview, Context, Process, Guidelines)
   - Naming follows gtd-cc conventions (plugin prefix pattern)

3. Check marketplace registration
   - Plugin is registered in `.claude-plugin/marketplace.json`
   - No duplicate plugin names

4. Generate validation report
   - List any violations of gtd-cc patterns
   - Provide specific recommendations for fixes

5. Verification: Confirm all plugins pass both plugin-dev and gtd-cc validation


## Guidelines

- Let plugin-dev handle base validation
- Focus on gtd-cc-specific pattern checks
- Provide actionable recommendations for fixes
- Check thin wrapper pattern compliance
