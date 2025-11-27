# Create Repository-Specific Plugin Workflow

This workflow guides you through analyzing a repository and creating a custom `.claude/` plugin tailored to that repository's specific needs, following gtd-cc architectural patterns.

## Overview

When working on any repository, you can create custom Claude Code automation by:
1. Analyzing the repository's domain, technologies, and common workflows
2. Designing ONE domain-specific skill containing MULTIPLE workflows
3. Creating MULTIPLE thin wrapper commands/agents that orchestrate those workflows
4. Implementing the approved components in the repository's `.claude/` directory

This workflow teaches the gtd-cc pattern by applying it to create repository-specific automation.

## When to Use This Workflow

Use this workflow when:
- You want to add Claude Code automation to a specific repository
- The repository has domain-specific operations not covered by generic plugins
- You want to teach others the gtd-cc plugin development pattern
- You need to create custom workflows tailored to a project's needs

## Process

### Step 1: Verify Repository Context

First, confirm you're in a git repository and check for existing `.claude/` structure:

```bash
# Verify git repository
if [ ! -d ".git" ]; then
  echo "ERROR: Not in a git repository. Please cd to repository root."
  exit 1
fi

echo "Repository: $(pwd)"
echo "Current branch: $(git branch --show-current 2>/dev/null || echo 'No branch')"

# Check existing .claude/ structure
echo -e "\n=== Existing .claude/ Structure ==="
if [ -d ".claude" ]; then
  find .claude -type f -name "*.md" | sort
  echo "Status: Updating existing setup"
else
  echo "Status: First-time setup - will create .claude/ directory"
fi
```

### Step 2: Analyze Repository Domain and Technologies

Understand what the repository does and how it works:

**Identify Repository Type:**
```bash
# Check key repository files
echo -e "\n=== Repository Files ===="
ls -la README.md CONTRIBUTING.md package.json Cargo.toml requirements.txt setup.py go.mod 2>/dev/null | awk '{print $NF}' || echo "Some key files not found"

# Check CI/CD workflows
echo -e "\n=== CI/CD Workflows ===="
if [ -d ".github/workflows" ]; then
  ls .github/workflows/
else
  echo "No .github/workflows/ found"
fi
```

**Questions to answer:**
- What type of project is this? (library, application, tool, framework, monorepo, documentation site, etc.)
- What are the primary technologies and languages?
- What build/test/deployment tools are used?
- What does the README say about project goals?
- What does CONTRIBUTING.md say about development workflows?

### Step 3: Identify Common Operations and Workflow Gaps

Analyze what developers actually do in this repository:

**Review recent commits:**
```bash
git log --oneline -20 --no-merges
```

Look for patterns:
- Are there repetitive commit message patterns? (e.g., "bump version", "update changelog", "regenerate docs")
- What operations are frequently performed together?
- What manual steps are documented in CONTRIBUTING.md?

**Identify workflow gaps:**
- Operations mentioned in docs but requiring multiple manual steps
- Repetitive tasks developers perform frequently
- Domain-specific operations unique to this project
- Opportunities for automation that would improve development velocity

### Step 4: Design ONE Domain-Specific Skill

Following the gtd-cc pattern, create ONE skill containing ALL domain-specific workflows.

**Architecture Principle:**
**Skills contain logic. Commands/agents are thin orchestrators.**

**Skill Design Questions:**
1. What is the primary domain of this repository? (e.g., "plugin development", "API management", "documentation authoring", "package publishing")
2. What workflows belong in this domain? (e.g., for plugin development: scaffolding, validation, testing, release)
3. What's the skill name? (Format: `<domain>-skill`, e.g., `plugin-development-skill`, `api-management-skill`)

**Example Skill Structure:**
```
.claude/
└── skills/
    └── <domain>-skill/
        ├── SKILL.md                    # Overview, lists all workflows
        └── workflows/
            ├── workflow-1.md          # Detailed procedure for operation 1
            ├── workflow-2.md          # Detailed procedure for operation 2
            └── workflow-3.md          # Detailed procedure for operation 3
```

**Each workflow file should contain:**
- Purpose statement
- Prerequisites
- Step-by-step bash commands and procedures
- Success criteria
- Error handling
- Examples

### Step 5: Design MULTIPLE Thin Wrapper Commands

For each workflow in your skill, create thin wrapper commands that orchestrate them.

**Command Design Pattern:**
```markdown
---
description: Brief description of what this does
---

Use the <domain>-skill and follow its <workflow-name> exactly as written.
```

**That's it!** Just 3-6 lines total. All logic lives in the skill.

**Example Mapping:**
```
ONE SKILL: plugin-development-skill
├── workflows/scaffolding-workflow.md
├── workflows/validation-workflow.md
└── workflows/release-workflow.md

MULTIPLE COMMANDS:
├── /create-plugin → orchestrates scaffolding-workflow
├── /validate-plugin → orchestrates validation-workflow
└── /release-plugin → orchestrates release-workflow
```

### Step 6: Design Agents (Optional)

If you need autonomous execution, create agents that orchestrate one or more workflows.

**Agent Design Pattern:**
```markdown
---
name: agent-name
description: When to use this agent with specific examples
---

You are the <Agent Name>, an autonomous expert in <domain> using the <domain>-skill.

Your core responsibilities:
- Execute <domain> workflows autonomously
- Follow exact instructions from the skill
- Maintain context throughout execution
- Handle errors gracefully

[Additional autonomous operation guidance]
```

Agents are longer than commands but still delegate all procedures to the skill.

### Step 7: Present Analysis to User

**Present your recommendations in this format:**

**THE ONE DOMAIN-SPECIFIC SKILL:**
- Skill name: `<domain>-skill`
- Domain expertise it provides
- ALL workflows it contains (list each one):
  - `workflows/workflow-1.md` - What it does
  - `workflows/workflow-2.md` - What it does
  - `workflows/workflow-3.md` - What it does
- Why one consolidated skill is better than multiple skills

**THE MULTIPLE COMMANDS:**

For each command, show:
```markdown
### /<command-name>
Orchestrates: `<domain>-skill`'s `<workflow-name>`

---
description: Brief description
---

Use the <domain>-skill and follow its <workflow-name> exactly as written.
```

**VISUAL ARCHITECTURE:**
```
.claude/
├── skills/
│   └── <domain>-skill/          ← ONE SKILL
│       ├── SKILL.md
│       └── workflows/
│           ├── workflow-1.md
│           ├── workflow-2.md
│           └── workflow-3.md
│
└── commands/
    ├── command-1.md             ← MULTIPLE COMMANDS
    ├── command-2.md
    └── command-3.md
```

**Ask the user:**
- Which components should be implemented first?
- Are there any additional workflows needed?
- Any concerns about the proposed architecture?

### Step 8: Implement Approved Components

Once the user approves, implement the components:

**Create directory structure:**
```bash
mkdir -p .claude/skills/<domain>-skill/workflows
mkdir -p .claude/commands
mkdir -p .claude/agents  # if needed
```

**Implement the skill:**
1. Create `SKILL.md` with:
   - YAML frontmatter (name, description)
   - Overview of the domain
   - List of all workflows with when-to-use guidance
   - How to use this skill
   - Key principles

2. Create each workflow file in `workflows/`:
   - Detailed step-by-step procedures
   - Bash commands and examples
   - Success criteria
   - Error handling

**Implement commands:**
Create each command file as a thin wrapper (3-6 lines):
```markdown
---
description: <what it does>
---

Use the <domain>-skill and follow its <workflow-name> exactly as written.
```

**Implement agents (if approved):**
Create agent files with configuration and autonomous execution instructions.

**Test the implementation:**
- Try each command
- Verify workflows execute correctly
- Check that all bash commands work
- Validate success criteria are met

## Guidelines

**Focus on repository-specific operations:**
- Don't duplicate generic GitHub workflows (issues, PRs) - use github-gtd plugin instead
- Look for operations mentioned in README/CONTRIBUTING that are manual
- Consider the repository's unique domain and development patterns

**Follow gtd-cc architecture strictly:**
- ONE skill containing ALL domain workflows
- MULTIPLE thin commands orchestrating individual workflows
- No logic in commands - just references to skill workflows
- All procedures, bash commands, and logic in skill workflows

**Balance automation with maintainability:**
- Don't over-engineer simple tasks
- Prioritize high-impact, low-effort automation
- Document assumptions clearly
- Make it easy to understand and modify

**Non-destructive approach:**
- Never overwrite existing `.claude/` files without approval
- When updating, respect current customizations
- Present recommendations before implementing
- This workflow can be run multiple times safely

## Success Criteria

Your analysis and implementation is complete when:

- ✅ Verified git repository in current directory
- ✅ Checked existing `.claude/` structure
- ✅ Repository type, domain, and technologies identified
- ✅ Common operations and workflow gaps catalogued
- ✅ Proposed ONE domain-specific skill with MULTIPLE workflows
- ✅ Proposed MULTIPLE thin commands orchestrating those workflows
- ✅ Showed visual architecture (ONE skill → MULTIPLE commands)
- ✅ Presented recommendations to user in chat
- ✅ User approved which components to implement
- ✅ Implemented approved components following gtd-cc patterns
- ✅ Tested that commands work and workflows execute correctly

## Error Handling

**Not in a git repository:**
- Stop and inform user
- Guide them to navigate to repository root
- Verify `.git` directory exists

**Insufficient information:**
- Document what files were accessible
- Make recommendations based on available info
- Note assumptions
- Suggest user review for accuracy

**No unique patterns identified:**
- Document that standard development practices are sufficient
- Recommend github-gtd plugin alone may be enough
- Suggest revisiting as project evolves

**Existing .claude/ customizations:**
- Never overwrite without approval
- Review existing components
- Propose additions that respect current setup
- Clearly mark new vs modified

## Architecture Examples

Study these examples to understand the gtd-cc pattern:

**Example: github-gtd (Complex Multi-Workflow)**
```
plugins/github/
├── skills/github-gtd/                ← ONE SKILL
│   ├── SKILL.md
│   └── workflows/
│       ├── issue-creation.md
│       ├── plan.md
│       ├── implementation.md
│       ├── review.md
│       └── merge.md
│
└── commands/                         ← MULTIPLE COMMANDS
    ├── gh-issue.md → issue-creation workflow
    ├── gh-plan.md → plan workflow
    ├── gh-build.md → implementation workflow
    ├── gh-review.md → review workflow
    └── gh-merge.md → merge workflow
```

**Pattern:** ONE skill with 5+ workflows → 5+ thin commands, each orchestrating one workflow

**Key Insight:** All logic is in the skill workflows. Commands are just 3-6 line pointers.

## Teaching Tip

When teaching this pattern to others, emphasize:
1. **Centralization**: All logic in ONE skill with MULTIPLE workflows
2. **Thin Wrappers**: Commands are just 3-6 lines referencing workflows
3. **Maintainability**: Update workflow once, affects all commands using it
4. **Clarity**: Clean separation between knowledge (skill) and interface (commands)
5. **Reusability**: Multiple commands can reference the same workflow

This workflow itself demonstrates the pattern - it's teaching you to build plugins the same way gtd-cc plugins are built!
