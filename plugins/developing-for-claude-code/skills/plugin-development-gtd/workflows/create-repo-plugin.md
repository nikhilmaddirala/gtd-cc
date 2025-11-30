---
description: Create repository-specific automation following gtd-cc patterns
---

# Create Repository-Specific Plugin Workflow

## Overview

This workflow analyzes a repository and creates custom `.claude/` automation tailored to that repository's specific needs, following gtd-cc architectural patterns. Commands and agents should reference this workflow directly and follow the process exactly as written.

## Context

User provides information about the repository's domain, technologies, and common automation needs. This workflow analyzes the repository structure and creates custom skills, commands, and agents that address the repository's specific workflows.

## Guidelines

Follow these general guidelines when executing this workflow:

- Always analyze the repository thoroughly before creating automation
- Use absolute paths for all file operations to avoid ambiguity
- Validate all JSON manifests using `jq .` before proceeding
- Focus on repository-specific needs, not generic functionality
- Follow gtd-cc naming conventions (kebab-case for all components)
- **Use templates from `../templates/` directory** - don't duplicate template content in workflows
- **Reference common patterns from `../references/common-patterns.md`** for registration and validation

## Process

### 1. Analyze repository structure and domain

- Verify git repository and analyze current structure
- Check for existing .claude/ automation structure
- Analyze repository domain and technology stack
- Identify common patterns and repetitive operations
- Detect automation opportunities (build, docs, deployment, etc.)

### 2. Identify automation opportunities

- Look for common file types that indicate build processes
- Check for package files and build scripts
- Identify documentation management needs
- Recognize CI/CD configuration files
- Note any repetitive manual processes

### 3. Design domain-specific skill

Create ONE skill with MULTIPLE workflows tailored to repository:
- Determine skill name based on repository (usually `${REPO_NAME}-automation`)
- Use template from `../templates/SKILL.md` for skill structure
- Create skill directory with required subdirectories (workflows, scripts, references, assets)
- Customize skill content for repository-specific domain

### 4. Create focused workflows

Design 2-3 specific workflows based on repository needs:
- Use template from `../templates/workflow.md` for each workflow
- Focus on repository-specific operations (build-test-deploy, docs, analysis, etc.)
- Customize workflow content for repository domain
- Reference common patterns from `../references/common-patterns.md`

### 5. Create thin wrapper commands and agents

- Use templates from `../templates/command.md` and `../templates/agent.md`
- Create commands that orchestrate the repository workflows
- Create agents for autonomous execution where appropriate
- Customize to reference specific repository workflows

### 6. Create .claude/ manifest and validate

- Create `.claude-plugin/plugin.json` for repository-specific automation
- Use manifest patterns from `../references/common-patterns.md`
- Validate JSON structure using validation commands
- Ensure component paths are relative and correct

### 7. Test repository automation

- Test that automation works in repository context
- Verify commands are discoverable immediately
- Test skill discovery and agent functionality
- Confirm automation provides value for repository workflows

## Final Review

Verify that the repository plugin creation workflow completed successfully:

- [ ] Repository structure analyzed and understood
- [ ] Domain-specific automation opportunities identified
- [ ] Single skill created with multiple focused workflows
- [ ] Workflows tailored to repository-specific needs
- [ ] Thin wrapper commands created to orchestrate workflows
- [ ] Autonomous agents created where appropriate
- [ ] .claude/ manifest created and validated
- [ ] All components use gtd-cc architectural patterns
- [ ] All naming conventions followed consistently
- [ ] Repository automation tested in context
- [ ] Automation provides real value for repository workflows