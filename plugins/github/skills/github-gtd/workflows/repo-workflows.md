---
description: Set up repo specific claude code workflows 
---

## Overview

Analyze a specific repository to understand its domain, technologies, and common development operations. Based on this analysis, propose ONE domain-specific skill (following the github-gtd pattern) that contains multiple workflows specific to this repository's needs. Then propose lightweight commands and agents that orchestrate different workflows within that skill. For example, a package manager repository might create one "package-management-skill" with workflows for versioning, publishing, and changelog management—then create commands like "/version-bump", "/publish-package", and "/update-changelog" that each reference different workflows. A documentation site might create "documentation-skill" with workflows for content creation, deployment, and SEO optimization—then create commands like "/add-doc-page" and "/deploy-docs" that orchestrate those workflows.

## Context

You are analyzing the repository in the current working directory. Check the existing state of the .claude/ directory infrastructure:

```bash
# Check current repository
echo "Repository: $(pwd)"
echo "Current branch: $(git branch --show-current 2>/dev/null || echo 'No branch')"

# Check existing .claude/ structure
echo -e "\n=== Existing .claude/ Structure ==="
if [ -d ".claude" ]; then
  find .claude -type f -name "*.md" | sort
else
  echo "No .claude/ directory found - first time setup"
fi

# Check key repository files
echo -e "\n=== Repository Files ==="
ls -la README.md CONTRIBUTING.md package.json Cargo.toml requirements.txt 2>/dev/null | awk '{print $NF}' || echo "Some key files not found"

# Check CI/CD workflows
echo -e "\n=== CI/CD Workflows ==="
if [ -d ".github/workflows" ]; then
  ls -la .github/workflows/ | grep -E "\.yml|\.yaml" | wc -l
else
  echo "No .github/workflows/ found"
fi
```

## Your Task

Goal: Analyze the current repository's domain, technologies, and workflows to generate a comprehensive set of recommendations for custom .claude/ directory components (skills, commands, and agents) tailored to this project's specific needs.

Target: The repository in the current working directory (cwd).

Supports both scenarios:
- **First-time setup**: Create .claude/ directory structure and initialize with recommendations
- **Updating existing setup**: Add to or modify existing .claude/ structure with new recommendations

Role: This is a standalone workflow that establishes or evolves repository-specific automation infrastructure. Run once during initial setup or periodically (e.g., quarterly) to identify new automation opportunities as the project evolves.

### Process

1. **Understand Repository Domain and Technologies**
   - Verify this is a git repository (check .git directory exists)
   - Determine the repository type (library, application, tool, framework, monorepo, etc.)
   - Identify primary technologies, languages, and frameworks
   - Review README.md and CONTRIBUTING.md to understand project goals and development model
   - Examine package.json, Cargo.toml, requirements.txt, or equivalent dependency files
   - Understand the build, test, and deployment architecture

2. **Analyze Common Operations and Workflows**
   - Review recent commit history to identify patterns in common tasks developers perform
   - Examine CI/CD pipeline configuration (.github/workflows/, .gitlab-ci.yml, etc.) to understand automated processes
   - Look for operations mentioned in README or CONTRIBUTING that are manual or repetitive
   - Identify domain-specific concepts unique to this project (e.g., package versioning, schema migrations, content publishing)
   - Check for existing .claude/ directory content to understand current automation

3. **Identify Workflow Gaps and Opportunities**
   - Compare against operations that are typically automated in similar projects
   - Find repetitive developer tasks that could benefit from automation
   - Identify operations that are documented but require multiple manual steps
   - Recognize domain-specific workflows that would benefit from Claude Code support
   - Assess which gaps would provide the most value for development velocity

4. **Design Skills-First Architecture**

   Follow the core architecture principle: Skills contain the logic and workflows. Commands and agents are thin orchestrators that reference skills.

   a. **Create ONE Domain-Specific Skill (Foundation Layer)**
      - What is the primary domain or purpose of this repository? (e.g., plugin development, API management, documentation)
      - Create ONE skill named after that domain (e.g., "plugin-development-skill", "api-management-skill", "docs-authoring-skill")
      - This ONE skill contains ALL domain-specific workflows in its `workflows/` subdirectory
      - Each workflow is a separate file: workflows/scaffolding-workflow.md, workflows/validation-workflow.md, workflows/release-workflow.md, etc.
      - Skills contain: comprehensive procedures, bash commands, guidelines, examples, success criteria, and templates
      - Structure pattern: `.claude/skills/[domain-skill-name]/SKILL.md` + `workflows/[workflow-name].md` (multiple workflow files)
      - Example model: `plugins/github/skills/github-gtd/` is ONE skill with workflows/ directory:
        - workflows/issue-creation-workflow.md
        - workflows/plan-workflow.md
        - workflows/commit-workflow.md
        - workflows/review-workflow.md
        - workflows/approval-workflow.md
      - The SKILL.md file describes the skill's purpose and lists all available workflows

   b. **Design Multiple Thin Orchestrators Around the ONE Skill (Orchestration Layer)**
      - Create MULTIPLE commands and/or agents, each referencing a different workflow from your ONE domain skill
      - **Commands**: Create 3-6 line interactive orchestrators (one per workflow, or per user scenario)
        - Format: Minimal YAML frontmatter + single instruction to invoke a specific skill workflow
        - Pattern: "Use the {domain-skill-name} skill and follow its {workflow-name} exactly as written"
        - Each command orchestrates ONE workflow from the skill
        - Adds interactivity and context injection, but all logic lives in the skill
        - Example mapping:
          - `/create-plugin` → invokes plugin-development-skill's scaffolding-workflow
          - `/validate-plugin` → invokes plugin-development-skill's validation-workflow
          - `/release-plugin` → invokes plugin-development-skill's release-workflow

      - **Agents**: Create autonomous orchestrators (can be longer than commands)
        - Each agent orchestrates one or more workflows from the skill
        - Include role context and guidance for autonomous decision-making
        - Example: An agent that autonomously manages the entire plugin workflow chain could reference multiple workflows
        - Delegate all detailed procedures to the skill rather than containing logic itself
        - Example: `plugins/obsidian/agents/options-analysis-agent.md` references skill workflows

   c. **Validate Architecture Alignment**
      - [ ] Are you proposing ONE domain-specific skill (not multiple skills)?
      - [ ] Does that ONE skill contain all the workflows (not scattered across multiple skills)?
      - [ ] Are each proposed command/agent 3-6 lines that just reference ONE specific workflow from the skill?
      - [ ] Do commands/agents reference the skill and add interactivity but delegate all logic to the skill?
      - [ ] Do you have multiple commands/agents, each orchestrating a different workflow from the ONE skill?
      - [ ] Have you shown examples that follow the github-gtd pattern (ONE skill → MULTIPLE commands)?
      - If any checkbox is unchecked, revise your approach before proceeding

5. **Present Analysis to User via Chat**

   Output your analysis directly in chat, structured as follows:

   - **Repository Analysis Summary**: Type, primary technologies, identified workflow gaps and opportunities

   - **Proposed ONE Domain-Specific Skill**: Explain:
     - What domain expertise and workflows this ONE skill would provide
     - The skill name (should be domain-focused)
     - All the workflows it would contain (e.g., workflows/scaffolding.md, workflows/validation.md, workflows/release.md)
     - Why this single consolidated skill is better than multiple skills

   - **Proposed Commands**: Show the set of commands that orchestrate different workflows from the ONE skill
     - For each command, show:
       - The actual thin format (3-6 lines, similar to gh-issue.md)
       - Which specific workflow from the skill it orchestrates
       - What user interaction it enables
     - Group them to show how they coordinate around the one skill
     - Example:
       ```
       /create-plugin → uses plugin-development-skill's scaffolding-workflow
       /validate-plugin → uses plugin-development-skill's validation-workflow
       /release-plugin → uses plugin-development-skill's release-workflow
       ```

   - **Proposed Agents** (if any): Show how they orchestrate workflows from the ONE skill
     - For each agent, explain:
       - What autonomous capability it provides
       - Which workflow(s) from the skill it orchestrates

   - **Priority Tiers**: Group commands/agents into High/Medium/Low impact categories with rationale

   **Important: No file creation at this stage**
   - Do not create .claude/ directory or subdirectories yet
   - Do not create recommendation documents
   - Focus on interactive discussion of the proposed architecture

   **After presenting analysis:**
   - Ask the user which components they would like to implement first
   - Offer to provide implementation guidance for any approved component
   - Be ready to refine the architecture based on user feedback

### Guidelines

- Focus on repository-specific operations, not generic GitHub workflows already covered by github-gtd (issues, PRs, merges, releases)
- Look for operations mentioned in README, CONTRIBUTING, or documentation that are manual or multi-step
- Consider the repository's domain and development patterns when proposing components
- Ensure proposed components complement github-gtd, not duplicate it
- Prioritize high-impact, low-effort automation opportunities
- Balance automation with maintainability - don't over-engineer simple tasks
- Document assumptions about the repository's structure and workflows
- If no unique patterns are found, document that github-gtd workflows alone may be sufficient
- **Non-destructive approach**: Never overwrite existing .claude/ customizations without user approval
- **Support both scenarios**: Handle first-time setup (create structure) and updates (enhance existing) gracefully
- **Idempotent workflow**: This workflow should be safe to run multiple times without causing problems

## Success Criteria

Your work is complete when:
- ✅ Verified this is a git repository in the current working directory
- ✅ Checked existing .claude/ structure (first-time or update scenario identified)
- ✅ Repository type, domain, and primary technologies are clearly identified
- ✅ Common development operations and workflows are catalogued
- ✅ Repository-specific automation gaps are identified and documented
- ✅ Skills-first architecture is proposed where:
  - ONE domain-specific skill is proposed (not multiple skills)
  - That ONE skill contains MULTIPLE workflows (scaffolding, validation, release, etc.)
  - MULTIPLE commands are proposed, each orchestrating a different workflow from the ONE skill
  - Each command is 3-6 lines that reference the skill (thin orchestrators)
  - Agents (if any) orchestrate workflows from the ONE skill while adding autonomous decision-making
- ✅ Clear visual examples show the ONE-skill-to-MULTIPLE-commands relationship (like github-gtd pattern)
- ✅ Implementation effort and impact prioritization is provided for all commands/agents
- ✅ Analysis is presented to user in chat (not as a file)
- ✅ User is asked which components they would like to implement first
- ✅ No .claude/ files or directories have been created yet

## Error Handling

If you encounter the following issues, address them as indicated:

**Issue: Not in a git repository**
- Solution: Cannot proceed - stop and inform user they must run this workflow from within a git repository root
- Guide user to navigate to the repository directory (cd /path/to/repo) and run the workflow again
- Verify the current directory has a .git folder

**Issue: Insufficient information to analyze repository**
- Solution: Document what files/information were accessible and what was not
- Make recommendations based on available information
- Note assumptions in the generated recommendations document
- Suggest the user review for accuracy

**Issue: No unique patterns or specialized workflows identified**
- Solution: Document that the repository appears to follow standard development practices
- Recommend that generic github-gtd workflows are sufficient for this project
- Suggest revisiting periodically as the project evolves
- Note specific areas where repo-specific automation could be added in the future

**Issue: Repository is too simple or follows standard conventions exactly**
- Solution: This is valid - document that existing plugins and generic workflows provide sufficient automation
- Recommend standard development practices from github-gtd

**Issue: Overwriting existing .claude/ customizations**
- Solution: Never overwrite existing .claude/ files without explicit user approval
- Review existing components and propose additions/modifications that respect current setup
- If updating, clearly mark what's new vs. what's being modified
- Suggest user review changes before implementation

## Architecture Examples to Reference

When presenting your analysis and during implementation, refer users to these examples that demonstrate the skills-first architecture:

### Example 1: Skill Structure (Foundation Layer)

Location: `plugins/github/skills/github-gtd/`

Structure:
```
skills/github-gtd/
├── SKILL.md (overview of the skill, available workflows)
└── workflows/
    ├── issue-creation-workflow.md (detailed procedure)
    ├── plan-workflow.md (detailed procedure)
    ├── commit-workflow.md (detailed procedure)
    └── [other domain-specific workflows]
```

Content characteristics:
- SKILL.md: Overview, when to use this skill, list of available workflow files
- Workflow files: Detailed step-by-step procedures with bash commands, guidelines, success criteria

### Example 2: Thin Command Orchestration (Orchestration Layer)

Location: `plugins/github/commands/gh-issue.md`

Content pattern (3-6 lines total):
```markdown
---
description: Create a GitHub issue for this repo using templates and conventions
---

Use the github-gtd skill and follow its issue-creation-workflow exactly as written.
```

Key characteristics:
- Minimal YAML frontmatter
- Single clear instruction to invoke a skill workflow
- No procedural logic in the command file itself
- References the specific workflow file in the skill's workflows/ directory

### Example 3: ONE Skill → MULTIPLE Commands Pattern

Directory structure showing the correct relationship:
```
.claude/
├── skills/
│   └── plugin-development-skill/          ← ONE SKILL
│       ├── SKILL.md                       (describes skill, lists workflows)
│       └── workflows/
│           ├── scaffolding-workflow.md
│           ├── validation-workflow.md
│           ├── release-workflow.md
│           └── documentation-workflow.md
│
└── commands/
    ├── create-plugin.md                   ← MULTIPLE COMMANDS
    │   └── "Use plugin-development-skill's scaffolding-workflow"
    ├── validate-plugin.md
    │   └── "Use plugin-development-skill's validation-workflow"
    ├── release-plugin.md
    │   └── "Use plugin-development-skill's release-workflow"
    └── generate-plugin-docs.md
        └── "Use plugin-development-skill's documentation-workflow"
```

**Pattern**: ONE skill with multiple workflows → MULTIPLE thin commands that each reference ONE workflow

Real example from the codebase:
```
plugins/github/
├── skills/github-gtd/                    ← ONE SKILL
│   ├── SKILL.md
│   └── workflows/
│       ├── issue-creation-workflow.md
│       ├── plan-workflow.md
│       ├── commit-workflow.md
│       ├── review-workflow.md
│       └── [other workflows]
│
└── commands/                             ← MULTIPLE COMMANDS
    ├── gh-issue.md → github-gtd's issue-creation-workflow
    ├── gh-plan.md → github-gtd's plan-workflow
    ├── gh-commit.md → github-gtd's commit-workflow
    ├── gh-review.md → github-gtd's review-workflow
    └── [more commands]
```

### Example 4: Agent Orchestration

Location: `plugins/obsidian/agents/options-analysis-agent.md`

Characteristics:
- Longer than commands (includes autonomous role context and decision-making guidance)
- Still delegates detailed methodology and procedures to skills
- References the skills it orchestrates and the specific workflows they provide

### When Presenting Your Recommendations

Follow this structure when presenting to the user:

**THE ONE DOMAIN-SPECIFIC SKILL:**
- Skill name (e.g., "plugin-development-skill", "api-management-skill")
- What domain expertise it provides
- ALL the workflows it would contain (list them all, e.g., scaffolding-workflow, validation-workflow, release-workflow, documentation-workflow)
- A brief description of each workflow and what problem it solves
- Why this single consolidated skill is better than multiple separate skills

**THE MULTIPLE COMMANDS (organized by workflow they orchestrate):**

For each command, show:
```markdown
### /create-plugin
Orchestrates: `plugin-development-skill`'s `scaffolding-workflow`
Use the plugin-development-skill and follow its scaffolding-workflow exactly as written.
```

- The actual 3-6 line thin format
- Which workflow from the ONE skill it orchestrates
- What user interaction/interactivity it enables
- Low effort estimate (these are thin orchestrators)

Group them to visually show how multiple commands coordinate around the one skill.

**AGENTS (if any):**
- What autonomous capability each provides
- Which workflows from the ONE skill it orchestrates
- Effort estimate

**VISUAL: Show the architecture**
- Include a diagram or ASCII art showing: ONE SKILL → MULTIPLE COMMANDS

After presenting all components with this structure, ask the user which they would like to implement first, and be ready to help with implementation for any approved component.
