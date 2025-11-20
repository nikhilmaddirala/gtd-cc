# Workflow Plugin Template

Workflow plugins implement process automation and methodology tools. These plugins guide users through structured workflows, best practices, and consistent processes.

## Use Cases

Workflow plugins are ideal when you need to:

- Automate complex business processes or methodologies
- Guide users through structured workflows (GTD, PARA, etc.)
- Implement best practices and standardized approaches
- Coordinate multi-stage operations with human decision points

## Core Structure

A workflow plugin typically includes:

### Commands

Interactive commands that guide users through workflow steps:

- Main workflow commands with step-by-step guidance
- Setup and initialization commands
- Configuration and customization options

### Agents

Autonomous agents for workflow implementation:

- Agents that execute workflow steps autonomously
- Agents that handle data processing and generation
- Agents that coordinate with other plugins

### Skills

Comprehensive knowledge about the methodology and workflow:

- Detailed workflow documentation and sequences
- Best practices and patterns
- Integration with related tools and plugins
- Decision-making guidance

## Example Structure

```
plugins/my-workflow/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── README.md                 # Plugin documentation
├── commands/
│   ├── main-workflow.md      # Primary workflow command
│   ├── setup.md              # Initialization command
│   └── utilities.md          # Utility commands
├── agents/
│   ├── workflow-executor.md  # Autonomous workflow agent
│   └── helper-agent.md       # Supporting agent
├── skills/
│   └── methodology/
│       ├── SKILL.md          # Core skill documentation
│       ├── workflows.md      # Workflow definitions
│       ├── best-practices.md # Guidelines and patterns
│       └── decision-guide.md # Decision-making framework
└── references/
    └── examples.md           # Example implementations
```

## Plugin Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-workflow",
  "version": "0.1.0",
  "description": "Workflow plugin for [process name] methodology",
  "author": "Your Name",
  "homepage": "https://github.com/yourusername/gtd-cc/tree/main/plugins/my-workflow",
  "license": "MIT",
  "commands": [
    {
      "name": "main-workflow",
      "path": "commands/main-workflow.md",
      "description": "Execute the main workflow with step-by-step guidance"
    },
    {
      "name": "setup",
      "path": "commands/setup.md",
      "description": "Initialize workflow environment"
    }
  ],
  "agents": [
    {
      "name": "workflow-executor",
      "path": "agents/workflow-executor.md",
      "description": "Autonomous workflow execution agent"
    }
  ],
  "skills": [
    {
      "name": "methodology",
      "path": "skills/methodology/SKILL.md",
      "description": "Comprehensive methodology and workflow documentation"
    }
  ]
}
```

## Key Files to Create

### 1. README.md

Document the workflow's purpose, methodology, and how to get started.

### 2. Commands

Create commands for:
- Main workflow with guidance and decision points
- Setup and initialization
- Utility operations (status, reset, configuration, etc.)

### 3. Agents

Create agents for:
- Autonomous workflow execution
- Specialized subtasks or phases
- Data generation and artifact creation

### 4. Skills

Create comprehensive skills covering:
- Complete workflow definitions and sequences
- Best practices and decision frameworks
- Integration with other plugins
- Common scenarios and variations
- Troubleshooting and common mistakes

## Development Workflow

1. Document your methodology and workflow clearly
2. Create the plugin directory structure
3. Write the plugin manifest
4. Develop commands to guide users through workflows
5. Create agents for autonomous execution
6. Document workflow logic and best practices in skills
7. Test workflows with example scenarios
8. Validate structure and manifest
9. Submit for review

## Testing Checklist

Before publishing:

- [ ] Main workflow command executes successfully
- [ ] All workflow steps are clear and well-documented
- [ ] Agents handle both success and error cases
- [ ] Decision points are clear with helpful guidance
- [ ] Plugin manifest is valid JSON
- [ ] All referenced files exist and are valid
- [ ] Documentation is complete and accurate
- [ ] Example scenarios are tested and working
- [ ] Workflow can handle variations and edge cases
- [ ] Integration with other plugins works

## Common Patterns

### Multi-Stage Workflows

Design workflows with clear stages and decision points between stages.

### Human Approval Points

Build in review and approval points where humans make decisions.

### Progress Tracking

Provide clear tracking of workflow progress and current state.

### Recovery Paths

Design workflows to handle mistakes and provide recovery options.

## Workflow Best Practices

- Document all workflow stages and transitions clearly
- Provide clear decision-making guidance
- Build in approval and review points for critical decisions
- Allow users to restart or resume workflows
- Implement graceful error handling and recovery
- Track and report workflow progress
- Provide examples and templates
- Keep workflow documentation synchronized with implementation
- Design for variations and edge cases
- Support both guided and automated execution
