# Contributing to gtd-cc

Thank you for your interest in contributing to the gtd-cc project! This guide explains the project structure, development workflow, and how to add new components.

## Project Structure

```
gtd-cc/
├── .claude-plugin/                 # Marketplace configuration
│   ├── marketplace.json            # Lists all plugins in this marketplace
│   └── plugin.json                 # Marketplace-level plugin manifest
│
├── plugins/                        # Individual plugin directories
│   ├── github/               # GitHub workflow automation plugin
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json        # Plugin manifest with components
│   │   ├── commands/              # Interactive slash commands
│   │   │   ├── gh-repo.md
│   │   │   ├── gh-issue.md
│   │   │   ├── gh-plan.md
│   │   │   ├── gh-build.md
│   │   │   └── gh-commit.md
│   │   ├── agents/                # Autonomous agents
│   │   │   ├── gh-build.md        # Code building agent
│   │   │   ├── gh-merge.md        # Merge and cleanup agent
│   │   │   └── gh-maintenance.md  # Repository health monitoring
│   │   ├── skills/                # Foundation skills
│   │   │   ├── github-workflow/   # GitHub operations expertise
│   │   │   │   └── SKILL.md
│   │   │   └── implementation/    # Code implementation patterns
│   │   │       └── SKILL.md
│   │   └── README.md
│   │
│   └── obsidian/         # Obsidian integration plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/              # (future)
│       ├── agents/                # (future)
│       ├── skills/
│       │   └── obsidian/
│       │       └── SKILL.md
│       └── README.md
│
├── references/                     # Reference documentation
│   └── docs/
│       ├── plugin-marketplaces.md
│       ├── ai-agents-README.md
│       └── Github-projects-ai-workflow.md
│
├── README.md                       # Project overview
├── CONTRIBUTING.md                # This file
└── .claude-plugin/marketplace.json # Root marketplace config

```

## Component Types

### Skills

Skills contain reusable domain expertise and form the foundation layer. They should be self-contained with clear responsibilities.

**Location:** `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`

**Purpose:**
- Provide detailed knowledge about a domain (GitHub operations, implementation patterns, etc.)
- Document patterns, best practices, and common workflows
- Serve as reference for commands and agents
- Be framework-independent

**Creating a Skill:**
1. Create directory: `plugins/<plugin-name>/skills/<skill-name>/`
2. Create `SKILL.md` with:
   - Overview section describing the skill domain
   - Core capabilities list
   - Key patterns and examples
   - Integration points with other components

### Commands

Commands are interactive workflows triggered by slash commands (`/command-name`). They provide user guidance and accept input.

**Location:** `plugins/<plugin-name>/commands/<command-name>.md`

**Purpose:**
- Provide interactive workflows with human input
- Guide users through complex processes
- Accept arguments and options
- Maintain context across user interactions

**Creating a Command:**
1. Create file: `plugins/<plugin-name>/commands/<command-name>.md`
2. Add YAML frontmatter:
   ```yaml
   ---
   name: command-name
   description: Brief description of what the command does
   ---
   ```
3. Document context, process, and expected interactions

### Agents

Agents are autonomous workers that run without human interaction between approval gates.

**Location:** `plugins/<plugin-name>/agents/<agent-name>.md`

**Purpose:**
- Execute complex, multi-step workflows autonomously
- Make decisions based on data and patterns
- Handle errors gracefully
- Report status and outcomes

**Creating an Agent:**
1. Create file: `plugins/<plugin-name>/agents/<agent-name>.md`
2. Add YAML frontmatter with name and description
3. Document:
   - Purpose and role in the workflow
   - Process and decision points
   - Error handling and recovery
   - Success criteria

## 7-Stage Workflow Integration

The gtd-cc project follows a 7-stage workflow. Each plugin component contributes to specific stages:

| Stage | Description | Components |
|-------|-------------|-----------|
| 1. Create Repo | Repository initialization | `/gh-repo` command |
| 2. Create Issue | Issue creation with planning | `/gh-issue` command |
| 3. Plan | Detailed implementation planning | `/gh-plan` command |
| 4. Implement | Autonomous code building | `gh-build` agent |
| 5. AI Review | Automated code quality checks | (via tests/linting) |
| 6. Human Review | Manual code review | `/gh-review` command |
| 7. Merge & Cleanup | Final merge and cleanup | `gh-merge` agent |

Plus continuous monitoring with `gh-maintenance` agent.

## Development Workflow

### Plugin Development Process

For comprehensive guidance on all aspects of plugin development, see [DEVELOPMENT.md](DEVELOPMENT.md):

- Choosing a plugin type (Integration, Utility, Workflow, or Data)
- Creating components using templates
- Testing and validation
- Best practices and integration patterns
- Troubleshooting common issues

### Quick Start: Adding a New Command

1. Identify which plugin it belongs to (or create new plugin)
2. Use the command template: `templates/components/command-template.md`
3. Create command file: `plugins/<plugin-name>/commands/<name>.md`
4. Add it to the plugin manifest: `.claude-plugin/plugin.json`
5. Update the plugin README.md
6. Test locally with `/command-name`
7. Run validation checks (see Validation section below)
8. Create PR with changes

### Quick Start: Adding a New Skill

1. Create skill directory: `plugins/<plugin-name>/skills/<skill-name>/`
2. Use the skill template: `templates/components/skill-template.md`
3. Create comprehensive `SKILL.md` documentation
4. Add skill to plugin manifest if needed
5. Update plugin README to reference the skill
6. Run validation checks
7. Create PR with changes

### Quick Start: Adding a New Agent

1. Use the agent template: `templates/components/agent-template.md`
2. Create agent file: `plugins/<plugin-name>/agents/<name>.md`
3. Add it to the plugin manifest: `.claude-plugin/plugin.json`
4. Document autonomy requirements and error handling
5. Update plugin README.md
6. Run validation checks
7. Create PR with changes

### Creating a New Plugin

1. Choose a plugin type: Integration, Utility, Workflow, or Data
2. Review the plugin type template in `templates/plugin-types/<type>/`
3. Create plugin directory: `plugins/<new-plugin-name>/`
4. Create structure:
   ```bash
   mkdir -p plugins/<new-plugin-name>/{.claude-plugin,commands,agents,skills}
   ```
5. Create plugin manifest: `.claude-plugin/plugin.json` (use template)
6. Create plugin README.md
7. Add plugin to root `.claude-plugin/marketplace.json`
8. Implement initial components using templates
9. Run validation checks
10. Create PR with complete plugin

## Conventions

### Naming Conventions

- **Commands:** kebab-case, prefixed by plugin (e.g., `gh-issue`, `ob-capture`)
- **Agents:** kebab-case with `-agent` suffix (e.g., `gh-build-agent`)
- **Skills:** kebab-case directories with uppercase `SKILL.md` files
- **Plugins:** kebab-case directories

### File Format

All markdown files should:
- Use YAML frontmatter for metadata
- Include comprehensive documentation
- Provide examples where applicable
- Link to related resources
- Be focused and concise

### JSON Manifests

Plugin manifests should:
- Be valid JSON
- List all components clearly
- Follow consistent formatting
- Include version and description

## Testing and Validation

### Validation Checklist

Before submitting a PR, ensure your changes pass all validation checks:

See [templates/tools/VALIDATION-GUIDE.md](templates/tools/VALIDATION-GUIDE.md) for comprehensive validation rules covering:

- Plugin structure validation
- JSON manifest validation
- Component (command, agent, skill) validation
- Link validation
- Content quality checks
- Pre-submission checklist

### Quick Validation

Before submitting a PR:

1. Validate JSON files:
   ```bash
   jq . .claude-plugin/marketplace.json
   jq . plugins/<plugin>/.claude-plugin/plugin.json
   ```

2. Verify directory structure is complete:
   ```bash
   # Check plugin has required structure
   ls -la plugins/<plugin-name>/
   ```

3. Check all referenced files exist:
   ```bash
   # Verify manifest references are correct
   find plugins/<plugin-name>/ -type f -name "*.md"
   ```

4. Test commands/agents locally if possible
5. Validate all links and references are valid
6. Ensure documentation is clear, complete, and has no placeholder text
7. Verify no syntax errors in YAML frontmatter
8. Run the full validation checklist from VALIDATION-GUIDE.md

### Using Templates

Use the provided templates to ensure consistency:

- **Command Template**: `templates/components/command-template.md`
- **Agent Template**: `templates/components/agent-template.md`
- **Skill Template**: `templates/components/skill-template.md`
- **Plugin Type Templates**: `templates/plugin-types/<type>/plugin.json.template`

### Common Issues

See [DEVELOPMENT.md - Troubleshooting](DEVELOPMENT.md#troubleshooting) for solutions to common problems during development.

## Pull Request Guidelines

When submitting a PR:

1. **Title:** Use conventional format: `feat:`, `fix:`, `docs:`, etc.
2. **Description:** Explain what components were added/modified and why
3. **Changes:** Keep PRs focused on specific features
4. **Testing:** Describe how changes were tested
5. **Documentation:** Update README/CONTRIBUTING if structure changed

Example PR:
```
feat: add obsidian-capture command to obsidian plugin

- Added `/ob-capture` command for capturing web content to Obsidian
- Created obsidian-integration skill with note creation patterns
- Updated plugin manifest and README documentation
- Tested command with sample article capture
```

## Questions or Need Help?

- Check the reference documentation in `references/docs/`
- Review existing plugins for patterns to follow
- Open an issue for clarification or suggestions
- Look at recent commits for current conventions

Thank you for contributing to gtd-cc!
