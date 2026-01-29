---
description: Validate that plugins follow gtd-cc architectural patterns
---

# Validate existing plugins

## Process

- Run plugin-dev validation (directory structure, manifests, component registration)
- Check gtd-cc-specific patterns:
  - Commands/agents are thin wrappers (no inline logic, reference skills)
  - Skills have proper structure (Overview, Context, Process, Guidelines)
  - Naming follows plugin prefix conventions
  - Marketplace registration exists (if marketplace plugin)
- Generate validation report listing violations with specific fix recommendations
