# Plugin Development Templates

This directory contains comprehensive templates and tools for developing plugins for the gtd-cc marketplace.

## Quick Navigation

New to plugin development? Start here:

1. [DEVELOPMENT.md](../DEVELOPMENT.md) - Complete development guide
2. [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution workflow
3. This directory - Templates and tools

## What's in This Directory

### Component Templates

Standard templates for creating plugin components:

- **Command Template** (`components/command-template.md`): Interactive user-facing workflows
- **Agent Template** (`components/agent-template.md`): Autonomous decision-making workflows
- **Skill Template** (`components/skill-template.md`): Domain expertise and reference documentation

Each template includes:
- Complete structure and sections
- Explanatory comments
- Best practices
- Examples and patterns

### Plugin Type Templates

Pre-built structures for different plugin categories:

#### Integration Plugins (`plugin-types/integration/`)

Connect Claude Code with external services and APIs (GitHub, Obsidian, etc.)

- `README.md`: Overview and best practices
- `plugin.json.template`: Manifest template

Use when: Building integrations with external platforms

#### Utility Plugins (`plugin-types/utility/`)

Provide reusable tools and cross-cutting functionality (data processing, web crawling, etc.)

- `README.md`: Overview and best practices
- `plugin.json.template`: Manifest template

Use when: Creating reusable tools or capabilities

#### Workflow Plugins (`plugin-types/workflow/`)

Implement process automation and methodology tools (GTD, documentation workflows, etc.)

- `README.md`: Overview and best practices
- `plugin.json.template`: Manifest template

Use when: Automating specific processes or methodologies

#### Data Plugins (`plugin-types/data/`)

Handle data processing, transformation, and management

- `README.md`: Overview and best practices
- `plugin.json.template`: Manifest template

Use when: Building data processing or transformation tools

### Development Tools

Guides and references for plugin development:

- **VALIDATION-GUIDE.md** (`tools/`): Complete validation checklist and rules
- **COMPONENT-GENERATOR.md** (`tools/`): Step-by-step guide for creating components

## Quick Start

### 1. Choose Your Plugin Type

Determine which plugin type fits your needs:

```
Integration: External service connectivity
Utility: Reusable tools and functions
Workflow: Process automation
Data: Data processing and transformation
```

Review the appropriate template in `plugin-types/<type>/README.md`

### 2. Use Component Templates

When creating components, use the appropriate template:

- Commands: `components/command-template.md`
- Agents: `components/agent-template.md`
- Skills: `components/skill-template.md`

### 3. Follow the Development Guide

Read [DEVELOPMENT.md](../DEVELOPMENT.md) for:

- Complete step-by-step instructions
- Best practices and patterns
- Integration guidance
- Troubleshooting

### 4. Validate Your Work

Use [VALIDATION-GUIDE.md](tools/VALIDATION-GUIDE.md) to ensure quality:

- Structure validation
- Content validation
- Link validation
- Pre-submission checklist

## Template Usage Workflow

### Creating a Command

```
1. Read plugin type guide (plugin-types/<type>/README.md)
2. Copy command template: templates/components/command-template.md
3. Fill in YAML frontmatter and sections
4. Add to plugin manifest
5. Validate using VALIDATION-GUIDE.md
6. Submit pull request
```

### Creating an Agent

```
1. Read plugin type guide (plugin-types/<type>/README.md)
2. Copy agent template: templates/components/agent-template.md
3. Define autonomy scope and workflows
4. Fill in all required sections
5. Add to plugin manifest
6. Validate using VALIDATION-GUIDE.md
7. Submit pull request
```

### Creating a Skill

```
1. Read plugin type guide (plugin-types/<type>/README.md)
2. Copy skill template: templates/components/skill-template.md
3. Document domain, concepts, and workflows
4. Create supporting documentation if needed
5. Add to plugin manifest
6. Validate using VALIDATION-GUIDE.md
7. Submit pull request
```

### Creating a New Plugin

```
1. Choose plugin type
2. Copy plugin.json.template from plugin-types/<type>/
3. Create plugin directory structure
4. Create plugin README.md
5. Create initial components using templates
6. Update root marketplace.json
7. Validate all files
8. Submit pull request
```

## File Organization

After using templates, your plugin structure should look like:

```
plugins/your-plugin/
├── .claude-plugin/
│   └── plugin.json              # Copy from template, customize
├── README.md                    # Plugin documentation
├── commands/
│   ├── command-1.md             # Based on command-template.md
│   └── command-2.md
├── agents/
│   ├── agent-1.md               # Based on agent-template.md
│   └── agent-2.md
└── skills/
    └── skill-name/
        ├── SKILL.md             # Based on skill-template.md
        ├── api-reference.md     # Supporting documentation
        └── patterns.md
```

## Key Sections in Templates

### Command Template Sections

- Overview: What the command does
- Required Information: Input parameters
- Prerequisites: Setup requirements
- Process: Step-by-step workflow
- Expected Outputs: Deliverables
- Common Issues & Solutions: Troubleshooting
- Integration: Related components

### Agent Template Sections

- Overview: Agent purpose
- Autonomy Scope: Autonomous vs. human decisions
- Prerequisites: Setup requirements
- Workflow and Logic: Detailed execution phases
- Error Handling and Recovery: Error scenarios
- Decision Points and Logic: Decision frameworks
- Integration Points: Related components
- Examples and Use Cases: Concrete examples
- Testing and Validation: How to test

### Skill Template Sections

- Overview: Domain explanation
- Core Capabilities: Main capabilities
- Key Concepts: Fundamental concepts
- Workflows and Patterns: Detailed workflows
- Integration Points: Component connections
- Examples and Use Cases: Real-world examples
- Maintenance Notes: Update frequency
- Troubleshooting: Common problems and solutions

## Best Practices

### When Using Templates

1. **Don't use placeholders**: Replace all `[bracket text]` with actual content
2. **Be specific**: Customize every section for your use case
3. **Test examples**: Verify all examples work as documented
4. **Keep formatting**: Maintain markdown structure and style
5. **Complete all sections**: Don't skip sections marked as required

### Naming Conventions

- Plugin directories: `kebab-case` (my-plugin)
- Command files: `kebab-case` (my-command.md)
- Agent files: `kebab-case` (my-agent.md)
- Skill directories: `kebab-case` (skill-name)

### Documentation Quality

- Write clearly and concisely
- Provide context and background
- Include practical examples
- Document error cases
- Keep documentation in sync with code

## Common Patterns

### Command Patterns

- **Setup Command**: Initialize or configure (e.g., `/gh-repo`)
- **Workflow Command**: Guide through multi-step process (e.g., `/gh-issue`)
- **Utility Command**: Quick single operation (e.g., `/plugin-validate`)

### Agent Patterns

- **Orchestration**: Coordinate multiple steps or components
- **Processing**: Handle bulk processing with adaptation
- **Integration**: Coordinate with external systems

### Skill Patterns

- **API Reference**: Document external service APIs
- **Pattern Library**: Collect design patterns and best practices
- **Workflow Guide**: Detailed workflow documentation
- **Concept Reference**: Domain terminology and concepts

## Validation

Before submitting, validate your plugin:

Use [VALIDATION-GUIDE.md](tools/VALIDATION-GUIDE.md) for:

- Structure validation checklist
- JSON manifest validation
- Component validation rules
- Content quality standards
- Pre-submission checklist

Quick validation commands:

```bash
# Validate JSON
jq . plugins/your-plugin/.claude-plugin/plugin.json

# Check structure
find plugins/your-plugin/ -type f -name "*.md" | head -20

# Verify references
grep -r "\.\./" plugins/your-plugin/ | head -10
```

## Examples

Study existing plugins for reference:

- `plugins/github/`: Integration plugin with full workflow
- `plugins/documentation/`: Workflow plugin for documentation
- `plugins/obsidian/`: Integration plugin with PARA methodology
- `plugins/web-research/`: Utility plugin for web operations

## Getting Help

If you're unsure:

1. Check [DEVELOPMENT.md](../DEVELOPMENT.md) for detailed guidance
2. Review [COMPONENT-GENERATOR.md](tools/COMPONENT-GENERATOR.md) for step-by-step processes
3. Study existing plugins for patterns
4. Check [VALIDATION-GUIDE.md](tools/VALIDATION-GUIDE.md) for common issues
5. Look at plugin type README for your specific type

## Tools in This Directory

### VALIDATION-GUIDE.md

Comprehensive guide for validating plugins:

- Structure validation rules
- JSON manifest validation
- Component validation requirements
- Content quality standards
- Common issues and fixes
- Pre-submission checklist

### COMPONENT-GENERATOR.md

Step-by-step guide for creating components:

- Creating commands
- Creating agents
- Creating skills
- Naming conventions
- Common patterns
- Integration patterns
- Testing guidelines

## Version History

Templates and tools are regularly updated to reflect best practices. Check commit history for changes.

## Contributing to Templates

If you improve the templates or tools:

1. Update the relevant template or tool file
2. Document your changes
3. Update examples if needed
4. Submit PR with explanation

## Related Documentation

- [DEVELOPMENT.md](../DEVELOPMENT.md): Complete development guide
- [CONTRIBUTING.md](../CONTRIBUTING.md): Contribution workflow
- [CLAUDE.md](../CLAUDE.md): Project conventions

## See Also

- gtd-cc README: Project overview
- Plugin Marketplace documentation
- Individual plugin READMEs: Study existing implementations
