# Integration Plugin Template

Integration plugins provide tools and automations for working with external services and APIs. These plugins bridge Claude Code with external platforms like GitHub, Obsidian, or web services.

## Use Cases

Integration plugins are ideal when you need to:

- Connect Claude Code with external services (GitHub, Jira, Slack, etc.)
- Automate workflows across multiple platforms
- Synchronize data between Claude Code and external systems
- Provide rich integrations with established tools

## Core Structure

An integration plugin typically includes:

### Commands

Interactive commands that guide users through workflows with the external service:

- Main workflow commands (e.g., `/gh-issue` for creating GitHub issues)
- Setup and configuration commands (e.g., `/gh-repo` for initialization)
- Utility commands for common operations

### Agents

Autonomous agents that execute complex multi-step workflows:

- Long-running workflows that don't require human intervention
- Decision-making and error recovery capabilities
- Integration with external API calls and service interactions

### Skills

Domain expertise about the external service and workflow patterns:

- How to use the external service's API
- Best practices and patterns for workflows
- Integration patterns and common scenarios
- Troubleshooting and error handling

## Example Structure

```
plugins/my-integration/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── README.md                 # Plugin documentation
├── commands/
│   ├── integration-setup.md   # Initial setup command
│   ├── main-workflow.md       # Primary workflow
│   └── utility-command.md     # Utility commands
├── agents/
│   ├── autonomous-workflow.md # Main autonomous agent
│   └── error-recovery.md      # Error handling agent
├── skills/
│   └── service-integration/
│       ├── SKILL.md           # Core skill documentation
│       ├── api-reference.md   # API documentation
│       └── patterns.md        # Workflow patterns
└── references/
    └── configuration.md       # Setup and config guide
```

## Plugin Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-integration",
  "version": "0.1.0",
  "description": "Integration with [External Service] for [specific workflows]",
  "author": "Your Name",
  "homepage": "https://github.com/yourusername/gtd-cc/tree/main/plugins/my-integration",
  "license": "MIT",
  "commands": [
    {
      "name": "integration-setup",
      "path": "commands/integration-setup.md",
      "description": "Set up integration with [Service]"
    },
    {
      "name": "main-workflow",
      "path": "commands/main-workflow.md",
      "description": "Execute main workflow"
    }
  ],
  "agents": [
    {
      "name": "autonomous-workflow",
      "path": "agents/autonomous-workflow.md",
      "description": "Autonomous workflow agent"
    }
  ],
  "skills": [
    {
      "name": "service-integration",
      "path": "skills/service-integration/SKILL.md",
      "description": "Domain expertise for [Service] integration"
    }
  ]
}
```

## Key Files to Create

### 1. README.md

Document the plugin's purpose, installation, and basic usage.

### 2. Commands

Create commands for:
- Initial setup and configuration
- Primary workflows users will follow
- Utility operations (list, status, delete, etc.)

### 3. Agents

Create agents for:
- Complex, multi-stage workflows
- Operations requiring decision-making
- Long-running processes

### 4. Skills

Create comprehensive skills covering:
- External service API and capabilities
- Workflow patterns and best practices
- Integration with other gtd-cc plugins
- Troubleshooting and error scenarios

## Development Workflow

1. Create the plugin directory structure
2. Write the plugin manifest
3. Develop commands and agents using templates
4. Create comprehensive skills documentation
5. Test all commands and agents locally
6. Validate structure and manifest
7. Submit for review

## Testing Checklist

Before publishing:

- [ ] All commands execute without errors
- [ ] All agents handle success and error cases
- [ ] External API integration works correctly
- [ ] Plugin manifest is valid JSON
- [ ] All referenced files exist and are valid
- [ ] Documentation is complete and accurate
- [ ] Examples in documentation are tested
- [ ] Error messages are helpful and actionable

## Common Patterns

### API Authentication

Store credentials securely and provide clear setup instructions.

### Error Handling

Implement graceful degradation and helpful error messages for API failures.

### State Management

Track plugin state appropriately for resuming interrupted workflows.

### Rate Limiting

Handle API rate limits with appropriate delays and user notifications.

## Integration Best Practices

- Document all external API endpoints and requirements
- Provide clear setup and authentication instructions
- Handle API errors gracefully with helpful messages
- Test integration thoroughly before release
- Keep API integration isolated in skills
- Document breaking changes from external service updates
