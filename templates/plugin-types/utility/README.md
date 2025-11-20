# Utility Plugin Template

Utility plugins provide reusable tools, capabilities, and helper functions that enhance Claude Code functionality. These plugins offer cross-cutting functionality that other plugins and workflows can leverage.

## Use Cases

Utility plugins are ideal when you need to:

- Provide reusable tools and capabilities
- Offer cross-platform functionality (web scraping, data processing, etc.)
- Create library-like functionality for other plugins to use
- Implement infrastructure and foundational capabilities

## Core Structure

A utility plugin typically includes:

### Commands

Interactive commands for user-facing operations:

- Core utility operations (e.g., `/web-crawl` for website crawling)
- Configuration and setup commands
- Status and information commands

### Agents

Autonomous agents for complex utility operations:

- Multi-step data processing workflows
- Batch operations and bulk processing
- Workflows requiring decision-making and adaptation

### Skills

Comprehensive knowledge about the utility's domain:

- Technical documentation and API reference
- Best practices and patterns
- Use cases and implementation examples
- Integration with other plugins

## Example Structure

```
plugins/my-utility/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── README.md                 # Plugin documentation
├── commands/
│   ├── core-utility.md       # Main utility command
│   ├── configuration.md      # Setup and config
│   └── status.md             # Status/info commands
├── agents/
│   ├── batch-processing.md   # Batch operations agent
│   └── advanced-operations.md # Advanced agent
├── skills/
│   └── utility-knowledge/
│       ├── SKILL.md          # Core skill documentation
│       ├── api-guide.md      # Tool/API documentation
│       └── patterns.md       # Usage patterns
└── references/
    └── troubleshooting.md    # Common issues and solutions
```

## Plugin Manifest

Create `.claude-plugin/plugin.json`:

```json
{
  "name": "my-utility",
  "version": "0.1.0",
  "description": "Utility plugin providing [specific capabilities]",
  "author": "Your Name",
  "homepage": "https://github.com/yourusername/gtd-cc/tree/main/plugins/my-utility",
  "license": "MIT",
  "commands": [
    {
      "name": "core-utility",
      "path": "commands/core-utility.md",
      "description": "Primary utility operation"
    },
    {
      "name": "configuration",
      "path": "commands/configuration.md",
      "description": "Configure utility options"
    }
  ],
  "agents": [
    {
      "name": "batch-processing",
      "path": "agents/batch-processing.md",
      "description": "Autonomous batch processing agent"
    }
  ],
  "skills": [
    {
      "name": "utility-knowledge",
      "path": "skills/utility-knowledge/SKILL.md",
      "description": "Domain expertise and technical documentation"
    }
  ]
}
```

## Key Files to Create

### 1. README.md

Document the utility's purpose, capabilities, installation, and usage.

### 2. Commands

Create commands for:
- Primary utility operations
- Configuration and setup
- Status checks and information

### 3. Agents

Create agents for:
- Batch processing operations
- Complex workflows using the utility
- Operations requiring decision-making

### 4. Skills

Create comprehensive skills covering:
- Technical documentation and APIs
- Best practices and patterns
- Integration with other plugins
- Common use cases and examples
- Troubleshooting and limitations

## Development Workflow

1. Create the plugin directory structure
2. Write the plugin manifest
3. Develop core commands and agents
4. Create comprehensive skills documentation
5. Test all commands and agents locally
6. Validate structure and manifest
7. Submit for review

## Testing Checklist

Before publishing:

- [ ] Core utility operations work correctly
- [ ] All commands execute without errors
- [ ] All agents handle success and error cases
- [ ] Plugin manifest is valid JSON
- [ ] All referenced files exist and are valid
- [ ] Documentation is complete and accurate
- [ ] Examples in documentation are tested
- [ ] Performance is acceptable for expected use cases
- [ ] Error messages are helpful and actionable

## Common Patterns

### Batch Processing

Implement efficient batch operations for processing multiple items.

### Caching

Use caching to improve performance for repeated operations.

### Configuration

Allow users to configure utility behavior and preferences.

### Integration

Design utilities so other plugins can easily use them.

## Utility Best Practices

- Make utilities focused and single-purpose
- Provide clear, intuitive command interfaces
- Document all configuration options
- Handle errors gracefully with helpful messages
- Implement caching when appropriate
- Provide performance metrics and status information
- Support batch/bulk operations
- Design for composability with other plugins
