# Plugin Marketplaces

This doc provides an overview of Claude Code plugin marketplaces, what they are, how to build them, best practices etc. based on reference examples.

## Overview

Plugin marketplaces are curated collections of Claude Code plugins that provide users with easy access to specialized tools, skills, agents, and workflows. They serve as centralized repositories where plugin authors can publish their creations and users can discover, install, and manage plugins efficiently.

## Types of Marketplaces

### Skills Marketplaces
Skills marketplaces focus on providing specialized capabilities that extend Claude's functionality for specific tasks. These are typically collections of skills with `SKILL.md` files that contain instructions and metadata.

**Example: Anthropic Agent Skills**
- Contains example skills for creative applications, technical tasks, and enterprise workflows
- Skills are self-contained directories with `SKILL.md` files
- Includes both open-source examples and production document skills

### Plugin Marketplaces
Plugin marketplaces offer comprehensive plugins that may include commands, agents, hooks, and skills. These are more complex and can provide full-featured functionality.

**Example: Claude Code Plugins**
- Bundled plugins including Agent SDK development tools, PR review toolkit, and commit workflows
- Each plugin can contain multiple components (commands, agents, hooks, skills)
- Focused on development productivity and code quality

### Workflow Marketplaces
Workflow marketplaces provide orchestration of multiple plugins and agents to accomplish complex, multi-step processes.

**Example: Claude Code Workflows**
- Production-ready workflow orchestration with 64+ focused plugins
- Optimized for granular installation and minimal token usage
- Covers development, operations, security, and business workflows

## Marketplace Structure

### Core Components

#### marketplace.json
Every marketplace must have a `.claude-plugin/marketplace.json` file that defines the marketplace metadata and plugin catalog.

**Required Fields:**
- `name` - Marketplace identifier (kebab-case, no spaces)
- `owner` - Marketplace owner information with name and optional email/url
- `plugins` - Array of plugin definitions

**Optional Fields:**
- `version` - Marketplace version
- `metadata` - Additional metadata including description, pluginRoot
- `$schema` - JSON schema reference

**Metadata Options:**
- `metadata.description` - Brief marketplace description
- `metadata.version` - Marketplace version string
- `metadata.pluginRoot` - Base path for relative plugin sources

#### Plugin Definitions
Each plugin in marketplace is defined with the following structure:

**Required Fields:**
- `name` - Plugin identifier (kebab-case, no spaces)
- `source` - Where to fetch plugin from (string or object)

**Optional Fields:**
- `description` - Brief plugin description
- `version` - Plugin version string
- `author` - Plugin author information
- `homepage` - Plugin homepage or documentation URL
- `repository` - Source code repository URL
- `license` - SPDX license identifier (e.g., MIT, Apache-2.0)
- `keywords` - Tags for plugin discovery and categorization
- `category` - Plugin category for organization
- `tags` - Tags for searchability
- `strict` - Require plugin.json in plugin folder (default: true)
- `commands` - Custom paths to command files or directories
- `agents` - Custom paths to agent files
- `hooks` - Custom hooks configuration or path to hooks file
- `mcpServers` - MCP server configurations or path to MCP config

**Plugin Sources:**
- **Relative paths**: `"./plugins/my-plugin"` for plugins in same repository
- **GitHub repositories**: `{"source": "github", "repo": "owner/plugin-repo"}`
- **Git repositories**: `{"source": "url", "url": "https://gitlab.com/team/plugin.git"}`

**Example Plugin Entry:**
```json
{
  "name": "plugin-name",
  "description": "Clear description of plugin functionality",
  "version": "1.0.0",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  },
  "category": "development",
  "keywords": ["tag1", "tag2"],
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "license": "MIT",
  "strict": true,
  "commands": ["./commands/command1.md"],
  "agents": ["./agents/agent1.md"],
  "skills": ["./skills/skill1"]
}
```

**Note**: Plugin entries use the plugin manifest schema with all fields made optional, plus marketplace-specific fields (`source`, `strict`, `category`, `tags`). When `strict: false`, the marketplace entry serves as the complete plugin manifest if no `plugin.json` exists.

### Directory Structure

```
marketplace-name/
├── .claude-plugin/
│   └── marketplace.json       # Plugin catalog
├── plugins/                   # Plugin directories (optional)
│   ├── plugin1/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   ├── agents/
│   │   └── skills/
│   └── plugin2/
└── README.md                  # Marketplace documentation
```

## Plugin Types and Components

### Skills
Skills are folders containing instructions, scripts, and resources that Claude loads dynamically. Each skill must contain a `SKILL.md` file with YAML frontmatter.

**Skill Structure:**
```
skill-name/
├── SKILL.md                   # Required skill definition
├── resources/                 # Optional supporting files
└── scripts/                   # Optional automation scripts
```

**SKILL.md Format:**
```markdown
---
name: skill-name
description: What this skill does and when to use it
license: License information
allowed-tools: [tool1, tool2]  # Optional
metadata:                      # Optional
  key: value
---

# Skill Instructions
[Detailed instructions for Claude]
```

### Commands
Commands are reusable instruction sets that can be invoked via slash commands.

**Command Structure:**
```
command-name.md
```

### Agents
Agents are specialized AI assistants with specific expertise and instructions.

**Agent Structure:**
```
agent-name.md
```

### Hooks
Hooks are automated scripts that run at specific events (e.g., session start, pre-commit).

**Hook Structure:**
```
.hooks/
├── hooks.json                 # Hook configuration
└── handlers/
    └── script.sh              # Hook implementation
```

## Best Practices

### Marketplace Design

#### Categorization
Organize plugins into logical categories to help users discover relevant content:
- `development` - Development tools and workflows
- `productivity` - Productivity enhancements
- `security` - Security scanning and compliance
- `documentation` - Documentation generation
- `testing` - Testing automation
- `operations` - DevOps and infrastructure
- `business` - Business and workflow automation

#### Version Management
- Use semantic versioning for plugins
- Include version information in marketplace.json
- Maintain backward compatibility when possible
- Document breaking changes clearly

#### Metadata Quality
- Provide clear, concise descriptions
- Use relevant keywords for discoverability
- Include author contact information
- Specify appropriate licenses

### Plugin Development

#### Modular Design
- Keep plugins focused on specific functionality
- Avoid monolithic plugins that do too much
- Design for granular installation
- Minimize token usage and dependencies

#### Documentation
- Include comprehensive README files
- Provide installation instructions
- Document all commands and features
- Include usage examples

#### Testing
- Test plugins thoroughly before publishing
- Include test cases where applicable
- Validate plugin.json syntax
- Test installation and removal

### Security Considerations

#### Code Safety
- Review all code for security vulnerabilities
- Avoid including secrets or sensitive data
- Use secure coding practices
- Implement proper input validation

#### Access Control
- Use `allowed-tools` restriction where appropriate
- Implement principle of least privilege
- Document any security considerations
- Consider using `strict` mode for enhanced security

## Installation and Usage

### Adding Marketplaces
Users can add marketplaces to Claude Code using multiple source types:

**GitHub repositories:**
```bash
/plugin marketplace add owner/repo
```

**Git repositories:**
```bash
/plugin marketplace add https://gitlab.com/company/plugins.git
```

**Local marketplaces for development:**
```bash
/plugin marketplace add ./my-marketplace
/plugin marketplace add ./path/to/marketplace.json
```

**Remote marketplace.json via URL:**
```bash
/plugin marketplace add https://url.of/marketplace.json
```

### Installing Plugins
After adding a marketplace, users can install specific plugins:

```bash
/plugin install plugin-name@marketplace-name
```

Or browse and install through the interactive interface.

### Plugin Management
- List installed plugins: `/plugin list`
- Remove plugins: `/plugin uninstall plugin-name@marketplace-name`
- Update plugins: `/plugin update plugin-name@marketplace-name`
- Enable disabled plugins: `/plugin enable plugin-name@marketplace-name`
- Disable without uninstalling: `/plugin disable plugin-name@marketplace-name`
- Remove marketplace: `/plugin marketplace remove marketplace-name`

### Marketplace Management
- List known marketplaces: `/plugin marketplace list`
- Update marketplace metadata: `/plugin marketplace update marketplace-name`
- Browse available plugins: `/plugin` (interactive interface)
- Validate marketplace JSON: `claude plugin validate .`

## Reference Examples

### Anthropic Agent Skills
- **Repository:** `anthropic-agent-skills`
- **Focus:** Example skills for learning and inspiration
- **Categories:** Creative, Development, Enterprise
- **Key Features:** Algorithmic art, brand guidelines, document skills

### Superpowers Marketplace
- **Repository:** `obra/superpowers-marketplace`
- **Focus:** Curated productivity tools
- **Categories:** Testing, Debugging, Collaboration
- **Key Features:** Core skills library, writing guidance, development resources

### Claude Code Plugins
- **Repository:** `claude-code-plugins`
- **Focus:** Official Anthropic plugins
- **Categories:** Development, Productivity, Security
- **Key Features:** Agent SDK tools, PR review, commit workflows

### Claude Code Workflows
- **Repository:** `claude-code-workflows`
- **Focus:** Production-ready workflow orchestration
- **Categories:** Development, Operations, Business
- **Key Features:** 64+ plugins, 87+ agents, comprehensive coverage

## Publishing Process

### Preparation
1. Create plugin repository with proper structure
2. Implement plugin functionality
3. Write comprehensive documentation
4. Test thoroughly using local marketplace
5. Choose appropriate license
6. Validate plugin structure: `claude plugin validate .`

### Marketplace Creation
1. Create marketplace repository on GitHub or other git hosting
2. Add `.claude-plugin/marketplace.json` with proper schema
3. Define plugin catalog with complete metadata
4. Write marketplace README with installation instructions
5. Test marketplace installation locally
6. Validate marketplace JSON: `claude plugin validate .`

### Publication
1. Push repositories to GitHub (recommended) or other git hosting
2. Ensure repositories are public or accessible to intended users
3. Test installation commands from fresh environment
4. Announce marketplace availability through appropriate channels
5. Provide support channels (GitHub issues, discussions, etc.)
6. Consider setting up GitHub releases for versioning

### Hosting Options

**GitHub (Recommended):**
- Built-in version control and issue tracking
- Easy team collaboration features
- Simple installation: `/plugin marketplace add owner/repo`

**Other Git Services:**
- GitLab, Bitbucket, or self-hosted git
- Use full repository URL: `/plugin marketplace add https://gitlab.com/company/plugins.git`

**Private/Distribution:**
- Internal git repositories for enterprise
- Require authentication access
- Can be combined with team configuration

## Community and Support

### Contribution Guidelines
- Follow established patterns from reference marketplaces
- Maintain code quality standards
- Provide clear documentation
- Be responsive to issues and feedback

### Support Channels
- GitHub issues for bug reports
- Discussions for feature requests
- Documentation for common questions
- Community forums for general support

### Maintenance
- Regular updates and bug fixes
- Compatibility testing with new Claude Code versions
- Community engagement and feedback incorporation
- Security audits and updates

## Team Configuration

### Repository-Level Plugin Management
Configure plugins at repository level to ensure consistent tooling across teams:

1. Add marketplace and plugin configuration to repository's `.claude/settings.json`
2. Team members trust the repository folder
3. Plugins install automatically for all team members

**Example Team Configuration:**
```json
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    },
    "project-specific": {
      "source": {
        "source": "git",
        "url": "https://git.company.com/project-plugins.git"
      }
    }
  },
  "enabledPlugins": [
    "code-formatter@team-tools",
    "deployment-tools@project-specific"
  ]
}
```

### Development Workflow

**Local Testing Setup:**
```bash
mkdir dev-marketplace
cd dev-marketplace
mkdir my-plugin
# Create plugin structure and marketplace.json
cd ..
claude
/plugin marketplace add ./dev-marketplace
/plugin install my-plugin@dev-marketplace
```

**Iterative Development:**
1. Make changes to plugin code
2. Uninstall current version: `/plugin uninstall my-plugin@dev-marketplace`
3. Reinstall to test changes: `/plugin install my-plugin@dev-marketplace`
4. Repeat development cycle

## Advanced Topics

### Multi-Plugin Workflows
Design plugins that work together seamlessly:
- Standardize data formats between plugins
- Implement consistent command interfaces
- Provide integration examples
- Document workflow patterns

### Performance Optimization
- Minimize plugin startup time
- Reduce memory footprint
- Optimize for token efficiency
- Implement lazy loading where appropriate

### Environment Variables
Use `${CLAUDE_PLUGIN_ROOT}` in plugin configurations:
- Resolves to plugin's installation directory
- Useful for hooks and MCP server configurations
- Enables portable plugin paths

### Internationalization
- Support multiple languages in documentation
- Consider locale-specific functionality
- Use Unicode-compliant practices
- Test with international character sets

## Troubleshooting

### Common Marketplace Issues

**Marketplace not loading:**
- Verify marketplace URL is accessible
- Check that `.claude-plugin/marketplace.json` exists at specified path
- Ensure JSON syntax is valid using `claude plugin validate`
- For private repositories, confirm access permissions

**Plugin installation failures:**
- Verify plugin source URLs are accessible
- Check that plugin directories contain required files
- For GitHub sources, ensure repositories are public or accessible
- Test plugin sources manually by cloning/downloading

### Validation and Testing

**Before publishing:**
```bash
# Validate marketplace JSON syntax
claude plugin validate .

# Add marketplace for testing
/plugin marketplace add ./path/to/marketplace

# Install test plugin
/plugin install test-plugin@marketplace-name
```

**Debugging plugin issues:**
1. Check directory structure (ensure components are at plugin root, not inside `.claude-plugin/`)
2. Test components individually (commands, agents, hooks separately)
3. Use validation tools and check syntax
4. Verify marketplace.json and plugin.json files

## Conclusion

Plugin marketplaces are a powerful mechanism for extending Claude Code's capabilities and building a vibrant ecosystem. By following the patterns and best practices established in the reference examples and official documentation, developers can create high-quality marketplaces that provide value to users while maintaining security, performance, and usability standards.

The key to success is focusing on user needs, maintaining high quality standards, fostering an active community around your marketplace, and leveraging the flexible plugin system to solve real-world problems.

## References

- [Claude Code Plugins Documentation](https://code.claude.com/docs/en/plugins) - Comprehensive guide to plugin development, installation, and management
- [Claude Code Plugin Marketplaces Documentation](https://code.claude.com/docs/en/plugin-marketplaces) - Official documentation for creating and managing plugin marketplaces
- [Plugin Reference](https://code.claude.com/docs/en/plugins-reference) - Complete technical specifications and schemas
- [Agent Skills Documentation](https://code.claude.com/docs/en/skills) - Creating and using Agent Skills
- [Slash Commands](https://code.claude.com/docs/en/slash-commands) - Understanding custom commands
- [Subagents](https://code.claude.com/docs/en/sub-agents) - Creating and using specialized agents
- [Hooks](https://code.claude.com/docs/en/hooks) - Automating workflows with event handlers
- [MCP Integration](https://code.claude.com/docs/en/mcp) - Connecting to external tools and services
- [Settings Configuration](https://code.claude.com/docs/en/settings) - Plugin configuration options
