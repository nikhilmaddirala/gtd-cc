---
description: Create repository-specific .claude/ automation by wrapping official plugin-dev skill
---

# Create repo plugin

## Overview

This sub-skill creates repository-specific `.claude/` automation for a given project. It wraps the official plugin-dev skill but targets the repo's `.claude/` directory instead of the gtd-cc marketplace.

CRITICAL: You MUST use the official plugin-dev skill for the mechanical aspects of plugin creation. Let plugin-dev handle its own internal routing.


## Context

User wants to add Claude Code automation to a specific repository. This creates commands, agents, and skills in the repo's `.claude/` directory, not in the gtd-cc marketplace.


## Process

1. Gather repo automation requirements
   - What workflows should be automated
   - What commands/agents are needed
   - What domain expertise the skill should contain

2. Invoke plugin-dev for mechanics
   - Use the official plugin-dev skill
   - Target the repo's `.claude/` directory
   - Let plugin-dev handle structure creation and its own routing

3. Apply gtd-cc patterns
   - Restructure commands as thin wrappers using `../templates/command.md`
   - Restructure agents as thin wrappers using `../templates/agent.md`
   - Ensure skills follow `../templates/skill.md` structure

4. Verification: Confirm repo automation follows gtd-cc thin wrapper architecture


## Guidelines

- This is NOT for gtd-cc marketplace plugins
- Target is the repo's `.claude/` directory
- Same gtd-cc patterns apply (thin wrappers, centralization)
- No marketplace registration needed
- Use templates from `../templates/` directory
