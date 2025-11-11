# Contributing to cc-gtd

Thank you for your interest in contributing to the cc-gtd project! This guide explains the project structure, development workflow, and how to add new components.

## Project Structure

```
cc-gtd/
├── .claude-plugin/                 # Marketplace configuration
│   ├── marketplace.json            # Lists all plugins in this marketplace
│   └── plugin.json                 # Marketplace-level plugin manifest
│
├── plugins/                        # Individual plugin directories
│   ├── github-code/               # GitHub workflow automation plugin
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
│   └── obsidian-workflow/         # Obsidian integration plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/              # (future)
│       ├── agents/                # (future)
│       ├── skills/
│       │   └── obsidian-workflow/
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

The cc-gtd project follows a 7-stage workflow. Each plugin component contributes to specific stages:

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

### Adding a New Command

1. Identify which plugin it belongs to (or create new plugin)
2. Create command file: `plugins/<plugin-name>/commands/<name>.md`
3. Add it to the plugin manifest: `.claude-plugin/plugin.json`
4. Update the plugin README.md
5. Test locally with `/command-name`
6. Create PR with changes

### Adding a New Skill

1. Create skill directory: `plugins/<plugin-name>/skills/<skill-name>/`
2. Create comprehensive `SKILL.md` documentation
3. Add skill to plugin manifest if needed
4. Update plugin README to reference the skill
5. Create PR with changes

### Adding a New Agent

1. Create agent file: `plugins/<plugin-name>/agents/<name>.md`
2. Add it to the plugin manifest: `.claude-plugin/plugin.json`
3. Document autonomy requirements and error handling
4. Update plugin README.md
5. Create PR with changes

### Creating a New Plugin

1. Create plugin directory: `plugins/<new-plugin-name>/`
2. Create structure:
   ```bash
   mkdir -p plugins/<new-plugin-name>/{.claude-plugin,commands,agents,skills}
   ```
3. Create plugin manifest: `.claude-plugin/plugin.json`
4. Create plugin README.md
5. Add plugin to root `.claude-plugin/marketplace.json`
6. Implement initial components (skills, commands, agents)
7. Create PR with complete plugin

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

## Testing Your Changes

Before submitting a PR:

1. Validate JSON files:
   ```bash
   jq . .claude-plugin/marketplace.json
   jq . plugins/<plugin>/.claude-plugin/plugin.json
   ```

2. Verify directory structure is complete
3. Test commands/agents locally if possible
4. Check that all links and references are valid
5. Ensure documentation is clear and complete

## Pull Request Guidelines

When submitting a PR:

1. **Title:** Use conventional format: `feat:`, `fix:`, `docs:`, etc.
2. **Description:** Explain what components were added/modified and why
3. **Changes:** Keep PRs focused on specific features
4. **Testing:** Describe how changes were tested
5. **Documentation:** Update README/CONTRIBUTING if structure changed

Example PR:
```
feat: add obsidian-capture command to obsidian-workflow plugin

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

Thank you for contributing to cc-gtd!
