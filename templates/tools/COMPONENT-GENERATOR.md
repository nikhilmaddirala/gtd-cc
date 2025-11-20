# Component Generator Guide

This guide explains how to create and integrate new components (commands, agents, and skills) into existing plugins.

## Overview

The gtd-cc plugin system supports three main component types:

1. **Commands**: Interactive user-facing workflows
2. **Agents**: Autonomous decision-making workflows
3. **Skills**: Domain expertise and reference documentation

This guide provides patterns and best practices for generating each component type.

## Creating a New Command

Commands are interactive workflows triggered by slash notation (e.g., `/command-name`).

### Step-by-Step Process

#### 1. Plan the Command

Before creating, define:

- **Purpose**: What workflow does it guide?
- **Inputs**: What information does it need?
- **Outputs**: What deliverables does it produce?
- **User Flow**: What are the step-by-step actions?
- **Decision Points**: Where does the user need to decide?

#### 2. Use the Command Template

Start with `templates/components/command-template.md`:

- Copy the template to `plugins/your-plugin/commands/command-name.md`
- Update YAML frontmatter with your command details
- Fill in each section with your specific content

#### 3. Complete Required Sections

Each command must include:

- **Overview**: What does this command do?
- **Required Information**: What inputs does it need?
- **Prerequisites**: What must be true before starting?
- **Process**: Step-by-step workflow
- **Expected Outputs**: What does the user get?
- **Common Issues & Solutions**: Troubleshooting
- **Integration**: Related commands and skills

#### 4. Add Examples

Include at least 2 examples:

- Basic usage example
- Advanced usage with additional options

Examples should:

- Show actual command invocation
- Describe expected results
- Be tested and accurate

#### 5. Link to Skills

If your command uses a skill, document:

- Which skill provides knowledge
- Which workflow pattern it follows
- How the skill guides the command logic

#### 6. Update Plugin Manifest

Add your command to `.claude-plugin/plugin.json`:

```json
{
  "commands": [
    {
      "name": "command-name",
      "path": "commands/command-name.md",
      "description": "Brief one-sentence description"
    }
  ]
}
```

### Command Template Customization

The template provides placeholders you should customize:

Replace this:
```markdown
[Brief explanation of command purpose...]
```

With actual description:
```markdown
This command guides you through creating a new GitHub issue with all required details. It ensures issues follow the GTD standard structure with clear requirements, acceptance criteria, and implementation approach options.
```

### Command Naming Conventions

- Use kebab-case: `create-issue`, `validate-plugin`, etc.
- Start with action verb: `create`, `generate`, `validate`, etc.
- Be specific about what the command does
- Keep names concise (1-3 words typically)

### Common Command Patterns

**Setup Command Pattern**:
- Guides user through configuration
- Collects and validates inputs
- Creates initial state or structure
- Example: `/gh-repo`, `/doc-init`

**Workflow Command Pattern**:
- Guides user through multi-step process
- Includes decision points
- Produces deliverable artifacts
- Example: `/gh-issue`, `/gh-plan`

**Utility Command Pattern**:
- Performs focused operation
- Quick to execute
- Minimal configuration
- Example: `/gh-status`, `/plugin-validate`

## Creating a New Agent

Agents are autonomous workers that execute complex workflows without user intervention.

### Step-by-Step Process

#### 1. Plan the Agent

Define:

- **Autonomy Scope**: What decisions does it make?
- **Execution Flow**: What are the phases/stages?
- **Decision Points**: Where does it branch?
- **Error Handling**: What goes wrong? How to recover?
- **Escalation**: When does it need human help?

#### 2. Use the Agent Template

Start with `templates/components/agent-template.md`:

- Copy to `plugins/your-plugin/agents/agent-name.md`
- Update YAML frontmatter
- Fill in workflow and logic sections

#### 3. Define Autonomy Boundaries

Clearly document:

- **Autonomous Decisions**: What the agent decides on its own
- **Human Decision Points**: When it escalates to humans
- **Escalation Triggers**: Error conditions requiring human intervention

Example:

```markdown
### Autonomy Scope

- **Decisions Made Autonomously**:
  - Determines test strategy based on code changes
  - Selects implementation approach based on requirements
  - Handles recoverable errors with retry logic

- **Human Decision Points**:
  - Code architecture changes (blocks and escalates)
  - Breaking API changes (requires human approval)
  - Security implications (escalates for review)
```

#### 4. Document Error Handling

Provide comprehensive error handling:

- Recoverable errors: retry strategies and limits
- Non-recoverable errors: escalation procedures
- Error detection: how agent recognizes failures
- Recovery actions: steps to recover from failures

#### 5. Document State Management

Explain how agent maintains state:

- Initial state setup
- State updates during execution
- Persistence (where state is stored)
- Recovery after failures
- Cleanup after completion

#### 6. Include Concrete Examples

Provide at least 2 examples:

- Typical success case
- Error handling and escalation

Examples should include:

- Initial conditions
- Actions agent takes
- Decisions made
- Final outcome

#### 7. Update Plugin Manifest

Add to `.claude-plugin/plugin.json`:

```json
{
  "agents": [
    {
      "name": "agent-name",
      "path": "agents/agent-name.md",
      "description": "Brief one-sentence description"
    }
  ]
}
```

### Agent Naming Conventions

- Use kebab-case: `workflow-executor`, `error-handler`
- Describe the agent's role or domain
- Consider naming after phase or workflow: `build-agent`, `review-agent`
- Keep names descriptive but concise

### Common Agent Patterns

**Orchestration Agent Pattern**:
- Coordinates multiple steps or components
- Makes routing decisions
- Handles complex workflows
- Example: `gh-build`, `doc-update-agent`

**Processing Agent Pattern**:
- Handles bulk processing of items
- Adapts to different input types
- Validates and transforms data
- Example: `batch-processor`, `data-transformer`

**Integration Agent Pattern**:
- Coordinates with external systems
- Handles authentication and API calls
- Manages retries and error recovery
- Example: `github-sync-agent`, `api-integration`

## Creating a New Skill

Skills are comprehensive knowledge repositories about specific domains.

### Step-by-Step Process

#### 1. Define Skill Scope

Determine:

- **Domain**: What is this skill about?
- **Audience**: Who will use this skill?
- **Purpose**: What problems does it solve?
- **Depth**: How comprehensive should it be?

#### 2. Use the Skill Template

Start with `templates/components/skill-template.md`:

- Create directory: `plugins/your-plugin/skills/skill-name/`
- Copy template to `SKILL.md`
- Update YAML frontmatter

#### 3. Define Core Capabilities

List the main capabilities:

- What can this skill help with?
- What problems does it solve?
- What workflows does it enable?

For each capability, document:

- **Purpose**: Why it matters
- **Scope**: What's included/excluded
- **Use Cases**: When to use it

#### 4. Document Key Concepts

Identify fundamental concepts in your domain:

For each concept:

- **Definition**: Clear one-sentence definition
- **Why It Matters**: Importance and relevance
- **Related Concepts**: How it connects to others
- **Common Misconceptions**: What people get wrong
- **Example Scenario**: Concrete usage example

#### 5. Define Workflows

Document the main workflows:

For each workflow:

- **Purpose**: What it accomplishes
- **Participants**: Who performs actions
- **Prerequisites**: What must be true
- **Steps**: Detailed step sequence
- **Success Criteria**: How to know it worked
- **Common Issues**: Problems and solutions

#### 6. Document Integration

Explain how the skill integrates:

- Which commands use it
- Which agents leverage it
- Related skills
- External dependencies

#### 7. Provide Real-World Examples

Include practical examples:

- Typical use case with walkthrough
- Advanced scenarios
- Edge cases and variations

#### 8. Create Additional Documentation

For complex skills, create supporting files:

- `api-reference.md`: API documentation
- `patterns.md`: Design patterns and examples
- `troubleshooting.md`: Common problems and solutions
- `glossary.md`: Domain terminology

#### 9. Update Plugin Manifest

Add to `.claude-plugin/plugin.json`:

```json
{
  "skills": [
    {
      "name": "skill-name",
      "path": "skills/skill-name/SKILL.md",
      "description": "Brief one-sentence description"
    }
  ]
}
```

### Skill Naming Conventions

- Use kebab-case for skill directory: `github-workflow`, `documentation-patterns`
- Use hyphenated names that describe the domain
- Keep names concise but descriptive
- Match domain of knowledge, not implementation

### Skill Document Structure

A comprehensive skill includes:

```
skills/skill-name/
├── SKILL.md              # Main skill documentation
├── api-reference.md      # API or technical reference
├── patterns.md           # Design patterns and best practices
├── examples/             # Real-world examples
│   ├── example-1.md
│   └── example-2.md
└── glossary.md           # Domain terminology (if complex)
```

## Integration Between Components

### Commands Using Skills

Commands should reference the skill that provides their knowledge:

```markdown
## Integration

- **Required Skills**:
  - Uses `skill-name` skill for decision logic and best practices
```

Commands follow the patterns documented in skills.

### Agents Using Skills

Agents should reference skills for:

- Decision-making frameworks
- Workflow patterns to follow
- Best practices and guidelines
- Error handling patterns

```markdown
## Integration Points

- **Required Skills**: Uses `skill-name` for workflow orchestration
```

### Skills Documenting Components

Skills should document which commands/agents use them:

```markdown
## Integration Points

### Commands That Use This Skill
- **Command Name** (`/command-name`): How it uses this skill

### Agents That Use This Skill
- **Agent Name**: How it uses this skill
```

## Cross-Plugin Integration

When creating components that interact across plugins:

### Document Dependencies

Clearly state which other plugins are required:

```markdown
## Prerequisites

- ✅ github@gtd-cc plugin installed
- ✅ web-research@gtd-cc plugin installed
```

### Reference External Components

Link to components in other plugins:

```markdown
- Related Command: `/gh-issue` from github plugin
- Related Skill: [GitHub Workflow](../github/skills/github-workflow/SKILL.md)
```

### Handle Missing Dependencies

Document graceful degradation if plugins aren't available.

## Testing Your Components

### Command Testing

- [ ] Command executes without errors
- [ ] All inputs are handled correctly
- [ ] Error cases produce helpful messages
- [ ] Examples in documentation work as shown
- [ ] Links to related skills are valid

### Agent Testing

- [ ] Agent completes successful workflows
- [ ] All error conditions are handled
- [ ] Escalation works correctly
- [ ] State is managed properly
- [ ] Integration with other components works

### Skill Testing

- [ ] All concepts are clearly explained
- [ ] Examples are accurate and tested
- [ ] Workflows are complete and actionable
- [ ] Links are valid
- [ ] Content is comprehensive and well-organized

## Component Checklist

Before submitting a new component:

### All Components

- [ ] YAML frontmatter is complete and valid
- [ ] Name follows naming conventions (kebab-case)
- [ ] Description is meaningful and concise
- [ ] No placeholder text remains
- [ ] All required sections are present
- [ ] Examples are tested and accurate

### Commands

- [ ] Overview explains what it does
- [ ] Required information is documented
- [ ] Prerequisites are clear
- [ ] Process steps are detailed
- [ ] Expected outputs are documented
- [ ] Common issues have solutions
- [ ] Integration section identifies related components

### Agents

- [ ] Autonomy scope is clearly defined
- [ ] Workflow phases are detailed
- [ ] Error handling is comprehensive
- [ ] Decision points are documented
- [ ] Examples show success and error cases
- [ ] Escalation procedures are clear

### Skills

- [ ] Overview is comprehensive
- [ ] Core capabilities are documented
- [ ] Key concepts have examples
- [ ] Workflows are detailed and actionable
- [ ] Integration points are listed
- [ ] Examples are real and practical
- [ ] Content is substantial (1000+ words)

## Version Control and Manifest Updates

When adding new components:

1. Create component file in proper directory
2. Update `.claude-plugin/plugin.json` manifest
3. Test all functionality
4. Validate structure and links
5. Create commit with clear message:
   ```
   feat(plugin-name): add new-component command
   ```

## Getting Help

If you're unsure about:

- **Component type to use**: Review the "Common Patterns" section
- **Template structure**: Use the provided templates directly
- **Best practices**: Check related components in existing plugins
- **Integration**: Look at how similar components integrate

## See Also

- Plugin Type Templates: Review your plugin type (integration, utility, workflow, or data)
- Existing Plugins: Study similar plugins for reference
- Validation Guide: Ensure your component passes all validation checks
