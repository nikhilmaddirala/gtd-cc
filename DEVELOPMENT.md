# Plugin Development Guide

This comprehensive guide covers everything needed to develop plugins for the gtd-cc marketplace. Whether you're creating a new plugin from scratch or extending an existing one, this guide provides step-by-step processes, templates, and best practices.

## Table of Contents

1. Getting Started
2. Plugin Types and Architecture
3. Component Development
4. Testing and Validation
5. Best Practices
6. Troubleshooting
7. Integration Patterns

## Getting Started

### Prerequisites

- Access to the gtd-cc repository
- Familiarity with Claude Code and slash commands
- Markdown knowledge for documentation
- Understanding of JSON (for manifests)

### Plugin Development Workflow

```
1. Plan your plugin
2. Choose a plugin type
3. Create plugin structure
4. Develop components (commands, agents, skills)
5. Test locally
6. Validate structure and content
7. Create pull request
8. Address review feedback
9. Merge and publish
```

## Plugin Types and Architecture

The gtd-cc marketplace supports four plugin types, each with different purposes:

### 1. Integration Plugins

Connect Claude Code with external services and APIs.

**Examples**:
- GitHub integration (GitHub, pull requests, issues, workflows)
- Obsidian integration (note-taking, vault synchronization)
- Web research (website crawling, content analysis)

**Use When**:
- You want to automate workflows with external services
- You need to synchronize data between systems
- You want to provide rich integrations with established tools

**Structure**:
- Commands for user-facing workflows
- Agents for complex multi-step operations
- Skills documenting the external service's API and patterns

See: `templates/plugin-types/integration/README.md`

### 2. Utility Plugins

Provide reusable tools and cross-cutting functionality.

**Examples**:
- Data processing tools
- Content transformation utilities
- General-purpose helpers

**Use When**:
- You want to provide reusable tools
- You want to offer functionality that benefits multiple use cases
- You want infrastructure-like capabilities

**Structure**:
- Commands for core utility operations
- Agents for batch processing and complex workflows
- Skills providing technical documentation and patterns

See: `templates/plugin-types/utility/README.md`

### 3. Workflow Plugins

Implement process automation and methodology tools.

**Examples**:
- Getting Things Done (GTD) workflow
- Documentation and publishing workflows
- Project management methodologies

**Use When**:
- You want to guide users through structured processes
- You want to implement a specific methodology
- You want to ensure consistent, best-practice workflows

**Structure**:
- Commands guiding users through workflow steps
- Agents for autonomous workflow execution
- Skills explaining the methodology and decision frameworks

See: `templates/plugin-types/workflow/README.md`

### 4. Data Plugins

Handle data processing, transformation, and management.

**Examples**:
- Data format conversion (CSV, JSON, etc.)
- Data pipeline orchestration
- Data analysis and reporting

**Use When**:
- You want to process or transform data
- You want to build data pipelines
- You want to provide data connectors

**Structure**:
- Commands for data processing operations
- Agents for batch processing and pipeline execution
- Skills documenting data formats and processing patterns

See: `templates/plugin-types/data/README.md`

## Component Development

### Creating a Command

Commands are interactive user-facing workflows. Users trigger them with slash notation (e.g., `/command-name`).

#### Step 1: Plan Your Command

Answer these questions:

- What workflow does it guide?
- What inputs does it need?
- What outputs does it produce?
- What are the step-by-step actions?
- Where do users need to make decisions?

#### Step 2: Use the Template

Copy `templates/components/command-template.md` to:
```
plugins/your-plugin/commands/command-name.md
```

#### Step 3: Update Frontmatter

Edit the YAML frontmatter:

```yaml
---
name: command-name
description: Brief description of what the command does
type: interactive
---
```

#### Step 4: Fill in Sections

Complete each section with specific content:

- **Overview**: What does this command do?
- **Required Information**: What inputs does it need?
- **Prerequisites**: What must be true before starting?
- **Process**: Step-by-step workflow
- **Expected Outputs**: What deliverables are produced?
- **Common Issues & Solutions**: Troubleshooting
- **Integration**: Related commands and skills

#### Step 5: Add Examples

Include at least 2 examples:
- Basic usage
- Advanced usage with options

#### Step 6: Update Manifest

Add to `.claude-plugin/plugin.json`:

```json
{
  "commands": [
    {
      "name": "command-name",
      "path": "commands/command-name.md",
      "description": "Brief description"
    }
  ]
}
```

### Creating an Agent

Agents are autonomous workers that execute complex workflows without user intervention.

#### Step 1: Define Autonomy Scope

Determine:

- What decisions does the agent make autonomously?
- When does it escalate to humans?
- What triggers escalation?

#### Step 2: Use the Template

Copy `templates/components/agent-template.md` to:
```
plugins/your-plugin/agents/agent-name.md
```

#### Step 3: Update Frontmatter

```yaml
---
name: agent-name
description: Brief description of the agent's role
type: autonomous
---
```

#### Step 4: Document Workflow

In "Workflow and Logic" section:

1. Define initialization phase
2. Document main execution phases
3. Define error handling and recovery
4. Document completion and reporting

#### Step 5: Define Error Handling

For each error category:

- How is the error detected?
- Can it be recovered from?
- How many retry attempts?
- When to escalate?

#### Step 6: Provide Examples

Include examples of:
- Typical successful execution
- Error handling and escalation

#### Step 7: Update Manifest

Add to `.claude-plugin/plugin.json`:

```json
{
  "agents": [
    {
      "name": "agent-name",
      "path": "agents/agent-name.md",
      "description": "Brief description"
    }
  ]
}
```

### Creating a Skill

Skills are domain expertise repositories. They document workflows, best practices, concepts, and integration patterns.

#### Step 1: Define Skill Scope

Decide:

- What is the skill's domain?
- Who is the audience?
- What problems does it solve?
- How deep should it be?

#### Step 2: Use the Template

Create directory:
```
plugins/your-plugin/skills/skill-name/
```

Copy `templates/components/skill-template.md` to:
```
plugins/your-plugin/skills/skill-name/SKILL.md
```

#### Step 3: Update Frontmatter

```yaml
---
name: skill-name
description: Comprehensive description of the skill's domain
version: 0.1.0
last_updated: YYYY-MM-DD
---
```

#### Step 4: Complete Sections

Write comprehensive content for:

- **Overview**: Detailed domain explanation
- **Core Capabilities**: Main capabilities and use cases
- **Key Concepts**: Fundamental concepts with examples
- **Workflows and Patterns**: Detailed workflow sequences
- **Integration Points**: How it connects to other components
- **Examples and Use Cases**: Real-world practical examples
- **Maintenance Notes**: Update frequency and dependencies

#### Step 5: Create Supporting Documentation

For complex skills, create additional files:

```
skills/skill-name/
├── SKILL.md                 # Main documentation
├── api-reference.md         # API or technical reference
├── patterns.md              # Design patterns and best practices
└── glossary.md              # Domain terminology
```

#### Step 6: Update Manifest

Add to `.claude-plugin/plugin.json`:

```json
{
  "skills": [
    {
      "name": "skill-name",
      "path": "skills/skill-name/SKILL.md",
      "description": "Brief description"
    }
  ]
}
```

## Testing and Validation

### Local Testing

Before submitting, test locally:

1. Verify command/agent/skill is accessible
2. Test all example scenarios
3. Check all links are valid
4. Validate JSON manifest
5. Review documentation for clarity

### Structure Validation

Use the validation guide at `templates/tools/VALIDATION-GUIDE.md`:

```bash
# Validate JSON manifest
jq . .claude-plugin/plugin.json

# Check directory structure
ls -la plugins/your-plugin/

# Verify all referenced files exist
find plugins/your-plugin/ -type f
```

### Content Validation

Check:

- [ ] No placeholder text remains
- [ ] All examples are tested and accurate
- [ ] All links resolve correctly
- [ ] YAML frontmatter is valid
- [ ] No broken references
- [ ] Grammar and spelling are correct
- [ ] Formatting is consistent

### Comprehensive Checklist

Before submitting:

**Plugin Structure**:
- [ ] Plugin directory named correctly (kebab-case)
- [ ] `.claude-plugin/plugin.json` exists and is valid JSON
- [ ] `README.md` exists with proper content
- [ ] All referenced files exist

**Documentation**:
- [ ] README explains purpose and usage
- [ ] All commands are documented
- [ ] All agents are documented
- [ ] All skills are documented
- [ ] Examples are clear and tested
- [ ] No placeholder text remains

**Integration**:
- [ ] Plugin manifest is accurate
- [ ] All component references are correct
- [ ] Related components are documented
- [ ] Cross-plugin references are valid

**Quality**:
- [ ] Documentation is professional and complete
- [ ] Examples demonstrate real-world usage
- [ ] Error handling is documented
- [ ] All validation checks pass

## Best Practices

### Documentation Standards

1. **Be Comprehensive**: Provide enough detail that users understand without external research
2. **Be Clear**: Use simple language, avoid jargon without explanation
3. **Be Accurate**: All examples must be tested and correct
4. **Be Current**: Keep documentation synchronized with implementation
5. **Be Consistent**: Follow established patterns and formatting

### Code Organization

1. **Clear Structure**: Organize files logically in directories
2. **Meaningful Names**: Use descriptive, kebab-case names
3. **Complete Manifests**: Keep JSON manifests accurate and complete
4. **Single Responsibility**: Each command/agent/skill has one clear purpose

### Error Handling

1. **Graceful Degradation**: Handle errors without crashing
2. **Helpful Messages**: Provide clear, actionable error information
3. **Recovery Strategies**: Document how to recover from errors
4. **Logging**: Log sufficient information for debugging

### Integration

1. **Clear Dependencies**: Document required plugins or components
2. **Loose Coupling**: Minimize dependencies between components
3. **Versioning**: Use semantic versioning for releases
4. **Breaking Changes**: Document breaking changes clearly

### Naming Conventions

- **Plugin names**: kebab-case (my-plugin)
- **Command names**: kebab-case (my-command)
- **Agent names**: kebab-case (workflow-executor)
- **Skill names**: kebab-case (skill-name)
- **File names**: kebab-case (my-file.md)

All names should be descriptive and follow the conventions.

## Troubleshooting

### Common Issues

#### Issue: Manifest JSON is Invalid

**Symptom**: `jq .` command fails
**Solution**: Use a JSON linter to find syntax errors (missing commas, quotes, etc.)

#### Issue: Referenced Files Don't Exist

**Symptom**: Plugin loads but commands/agents/skills aren't available
**Solution**: Verify all paths in manifest match actual file locations

#### Issue: Links are Broken

**Symptom**: Documentation references are dead
**Solution**: Verify paths are correct and files exist

#### Issue: Examples Don't Work

**Symptom**: Users report examples produce errors
**Solution**: Test all examples before publishing

#### Issue: Plugin Name Doesn't Match Directory

**Symptom**: Manifest says "my-plugin" but directory is "myplugin"
**Solution**: Ensure directory name exactly matches manifest name

### Getting Help

1. Check existing plugins for similar implementations
2. Review the validation guide for specific issues
3. Ask for feedback in pull requests
4. Consult related documentation and examples

## Integration Patterns

### Using Skills in Commands

Commands should reference and follow patterns documented in skills:

```markdown
## Integration

- **Required Skills**: Uses `skill-name` skill for workflow patterns
```

The command's workflow should follow the patterns defined in the skill.

### Using Skills in Agents

Agents should reference skills for decision-making and error handling:

```markdown
## Integration Points

- **Required Skills**: Uses `skill-name` for orchestration patterns
```

### Cross-Plugin Integration

When components interact across plugins:

1. Document required plugins clearly
2. Reference external components properly
3. Handle missing dependencies gracefully
4. Test integration thoroughly

Example:

```markdown
## Prerequisites

- ✅ github@gtd-cc plugin installed
- ✅ web-research@gtd-cc plugin installed

## Integration Points

- Works with `/gh-issue` command from github plugin
- Leverages skills from documentation plugin
```

### Plugin Type Integration Patterns

**Integration Plugin**:
- Coordinates with external APIs
- Handles authentication
- Documents integration points
- Implements retry and error handling

**Utility Plugin**:
- Designed for composition with other plugins
- Minimal external dependencies
- Clear, reusable interfaces
- Documents batch processing capabilities

**Workflow Plugin**:
- Coordinates multiple steps or commands
- May use other plugins' capabilities
- Implements approval/escalation points
- Documents decision frameworks

**Data Plugin**:
- Transforms data between formats
- Handles bulk operations
- Integrates with other data sources
- Documents data quality assurance

## Plugin Release Process

When releasing a new plugin:

1. **Prepare**: Ensure all validation passes
2. **Create PR**: Submit with clear description
3. **Review**: Address review feedback
4. **Test**: Verify in actual Claude Code
5. **Version**: Use semantic versioning
6. **Merge**: Merge to main branch
7. **Document**: Update marketplace documentation
8. **Announce**: Share with community

## See Also

- Plugin Type Templates: Choose your plugin type
- Component Generator Guide: Detailed component creation guide
- Validation Guide: Ensure quality standards
- Example Plugins: Study existing plugins for reference
