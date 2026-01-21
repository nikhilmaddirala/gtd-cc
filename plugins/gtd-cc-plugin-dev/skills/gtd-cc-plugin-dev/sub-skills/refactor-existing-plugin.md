---
description: Refactor existing plugin to follow gtd-cc patterns while preserving core functionality
---

# Refactor existing plugin

## Overview

This sub-skill refactors an existing Claude Code plugin to follow gtd-cc architectural patterns. It wraps the official plugin-dev skill for validation and mechanics, then systematically transforms components to follow the thin wrapper pattern while preserving all functionality.

CRITICAL: You MUST use the official plugin-dev skill for validation and mechanics. Let plugin-dev handle its own internal routing.


## Context

User wants to migrate an existing plugin to gtd-cc standards. The plugin may have:
- Commands with inline logic (should become thin wrappers)
- Agents with inline logic (should become thin wrappers)
- Skills missing standard structure (Overview, Context, Process, Guidelines)
- Naming that doesn't follow prefix conventions
- Missing or incomplete manifest entries


## Process

1. Validate current plugin state
   - Use the official plugin-dev skill to assess current structure
   - Use the validate-existing-plugins sub-skill to identify gtd-cc pattern violations
   - Document all issues found: inline logic, missing structure, naming violations

2. Create refactoring plan
   - For each command with inline logic: identify what skill should be created/used
   - For each agent with inline logic: identify what skill should be created/used
   - For skills missing structure: note which sections need to be added
   - Present plan to user for approval before making changes

3. Extract logic to skills
   - For each command/agent with inline logic:
     - Create a new skill (or identify existing skill to use)
     - Move domain logic from command/agent into the skill
     - Structure skill with: Overview, Context, Process, Guidelines
   - Use templates from `../templates/` for new skills

4. Convert commands to thin wrappers
   - Replace command body with skill reference
   - Pattern: "Use [skill-name] for this task. CRITICAL: You MUST invoke [skill-name]."
   - Preserve $ARGUMENTS passthrough for user context
   - Use template from `../templates/command.md`

5. Convert agents to thin wrappers
   - Replace agent body with skill reference
   - Pattern: "Use [skill-name] for this task. CRITICAL: You MUST invoke [skill-name]."
   - Preserve agent-specific context passing
   - Use template from `../templates/agent.md`

6. Apply naming conventions
   - Rename components to follow plugin prefix pattern
   - Plugin: `example` → Components: `ex-*`
   - Update all internal references to new names

7. Update manifests
   - Add any new skills to plugin.json
   - Update command/agent paths if renamed
   - Bump minor version number (e.g., 1.0.0 → 1.1.0)

8. Re-validate
   - Use the official plugin-dev skill to confirm structure is correct
   - Use validate-existing-plugins to confirm gtd-cc patterns are followed
   - Fix any remaining issues

9. Verification: Confirm all components follow gtd-cc thin wrapper pattern and functionality is preserved


## Guidelines

- Always validate before and after refactoring
- Create skills BEFORE converting commands/agents to thin wrappers
- Preserve all original functionality - refactoring changes structure, not behavior
- Use templates from `../templates/` directory for consistency
- Get user approval before making destructive changes
- One component at a time - complete each conversion fully before moving to next
- If a command/agent already references a skill correctly, skip it
