---
name: plugin-development-gtd
description: Guide for developing Claude Code plugins following gtd-cc architectural patterns - central skills with workflows, thin wrapper commands and agents.
---

# Plugin Development GTD Skill

This skill provides complete guidance for developing Claude Code plugins following the gtd-cc repository's architectural patterns.

## About This Skill

This skill should be used when developing plugins for the gtd-cc marketplace or creating repository-specific automation. It encompasses all aspects of plugin development from planning through release, following the gtd-cc architecture where skills contain domain expertise, commands are thin wrappers, and agents execute autonomously.

### When to Use This Skill

Use this skill when:
- Creating new plugins for the gtd-cc marketplace
- Updating existing plugins with new components
- Creating repository-specific automation in `.claude/` directories
- Validating plugin structure and consistency
- Learning the gtd-cc architectural patterns

## The gtd-cc Plugin Architecture Pattern

All plugins in this marketplace follow a layered architecture:

**Skills - Foundation Layer**
- Central SKILL.md describes the domain and lists workflows
- Individual workflow files in workflows/ subdirectory contain detailed procedures
- Single source of truth for all domain expertise

**Commands - Interactive Wrappers**
- Thin wrappers (3-6 lines) that reference specific skill workflows
- No inline logic - just pointers to workflows
- Example: "Use the <skill-name> and follow its <workflow-name> exactly as written."

**Agents - Autonomous Executors**
- Configuration plus instructions to execute workflows autonomously
- Maintain context across multi-step processes
- Delegate all procedures to skill workflows

## Plugin Development Workflows

Each workflow provides detailed step-by-step guidance for specific plugin development tasks. Select the workflow that matches your current goal:

### Workflow 1: Create New Plugin
**File**: `workflows/create-new-plugin.md`

Create a brand new plugin in the gtd-cc marketplace with complete directory structure, manifests, initial components, and marketplace registration.

**Use when**: Building a new plugin from scratch for the gtd-cc marketplace

### Workflow 2: Update Existing Plugin
**File**: `workflows/update-existing-plugin.md`

Add new components (commands, agents, skills, workflows) to existing plugins while maintaining consistency and updating manifests.

**Use when**: Extending or modifying an existing gtd-cc marketplace plugin

### Workflow 3: Validate Existing Plugins
**File**: `workflows/validate-existing-plugins.md`

Comprehensive validation of plugin structure, manifests, documentation, and marketplace consistency.

**Use when**: Checking plugin health before releases, contributions, or during development

### Workflow 4: Create Repository-Specific Plugin
**File**: `workflows/create-repo-plugin.md`

Analyze any repository and create custom `.claude/` automation tailored to that repository's specific needs, following gtd-cc patterns.

**Use when**: Adding Claude Code automation to a specific repository with domain-specific operations

## How to Use This Skill

When this skill is referenced by a command or agent:

1. **Select the relevant workflow** based on your current task
2. **Read the workflow file** for detailed step-by-step procedures
3. **Follow the process exactly** as written in the workflow
4. **Execute operations** (bash commands, file creation, validation)
5. **Verify success criteria** to ensure quality

### Workflow Selection Logic

**For gtd-cc marketplace plugins:**
- New plugin → Use `create-new-plugin.md`
- Modifying existing → Use `update-existing-plugin.md`
- Before release → Use `validate-existing-plugins.md`

**For repository-specific automation:**
- Custom `.claude/` setup → Use `create-repo-plugin.md`

**For learning:**
- All workflows demonstrate the gtd-cc pattern in action

## Key Principles

**Single Source of Truth**: Skills contain all logic in workflow files. Commands and agents are thin orchestrators.

**Layered Architecture**: Skills (expertise) → Commands (interactive interface) → Agents (autonomous execution)

**Maintainability**: Update workflow once, affects all commands/agents using it.

**Clarity**: Clean separation between knowledge (skills) and interface (commands/agents).

**Consistency**: All plugins follow the same pattern, making the codebase predictable.

## gtd-cc Repository Conventions

**Naming:**
- Commands: kebab-case with plugin prefix (e.g., `gh-issue`, `doc-audit`, `pl-create`)
- Agents: kebab-case with descriptive suffix (e.g., `gtd-github-agent`)
- Skills: kebab-case directories, uppercase `SKILL.md` files
- Workflows: kebab-case with `.md` extension

**File Organization:**
- Skills: `plugins/<plugin>/skills/<skill-name>/SKILL.md`
- Workflows: `plugins/<plugin>/skills/<skill-name>/workflows/*.md`
- Commands: `plugins/<plugin>/commands/<command-name>.md`
- Agents: `plugins/<plugin>/agents/<agent-name>.md`

**Content Style:**
- SKILL.md: Lean overview, lists workflows, provides selection logic
- Workflows: Detailed step-by-step procedures with bash commands and examples
- Commands: Minimal (3-6 lines) references to workflows
- Agents: Configuration plus autonomous execution instructions

## Examples to Study

**Complex multi-workflow plugin:**
- `plugins/github/` - GitHub workflow automation
- Study `skills/github-gtd/SKILL.md` and its workflows/ directory
- Notice how commands are thin wrappers (1-2 lines each)

**Simple plugin:**
- `plugins/documentation/` - Documentation tools
- Straightforward structure

**Meta-example:**
- `plugins/developing-for-claude-code/` - This plugin
- Demonstrates the pattern it teaches

## Workflow Dependencies

- Workflows are independent and can be used in any order
- `validate-existing-plugins.md` should be run before releases
- `create-repo-plugin.md` is for different use case (repository-specific vs marketplace plugins)

## Reference Files

All detailed procedures are in individual workflow files in the `workflows/` directory. SKILL.md serves as the index and overview - all implementation details live in workflows.
