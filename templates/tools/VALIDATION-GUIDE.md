# Plugin Validation Guide

This guide defines the validation rules and standards for gtd-cc plugins. Use this to ensure your plugin meets all quality and consistency requirements.

## Validation Checklist

### Structure Validation

Plugin directory structure must follow the standard pattern:

```
plugins/plugin-name/
├── .claude-plugin/
│   └── plugin.json           # REQUIRED
├── README.md                 # REQUIRED
├── commands/                 # Directory (optional if no commands)
│   └── *.md                  # Command files
├── agents/                   # Directory (optional if no agents)
│   └── *.md                  # Agent files
└── skills/                   # Directory (optional if no skills)
    └── skill-name/
        └── SKILL.md          # REQUIRED if skills/ exists
```

Validation checks:

- [ ] `.claude-plugin/plugin.json` exists and is valid JSON
- [ ] `README.md` exists and has proper content
- [ ] At least one of: commands, agents, or skills exists
- [ ] All referenced files exist
- [ ] No unexpected files in root directory
- [ ] Subdirectories have correct naming (kebab-case)

### Manifest Validation

The `.claude-plugin/plugin.json` file must be valid JSON and include:

Required fields:

- [ ] `name`: kebab-case plugin name, matches directory name
- [ ] `version`: semantic versioning format (X.Y.Z)
- [ ] `description`: one-sentence description of plugin
- [ ] `author`: author name
- [ ] `license`: valid license (typically MIT)

Optional but recommended:

- [ ] `homepage`: URL to plugin documentation
- [ ] `keywords`: array of relevant keywords
- [ ] `commands`: array of command definitions
- [ ] `agents`: array of agent definitions
- [ ] `skills`: array of skill definitions

Command/Agent/Skill reference format:

```json
{
  "name": "command-name",
  "path": "commands/command-name.md",
  "description": "Brief description"
}
```

Validation checks:

- [ ] Valid JSON syntax
- [ ] All required fields present
- [ ] Plugin name matches directory name
- [ ] Version follows semantic versioning
- [ ] All referenced paths exist and match file type
- [ ] Names are kebab-case
- [ ] Descriptions are meaningful and concise

### README Validation

The README.md file must include:

- [ ] Plugin name as main heading (H1)
- [ ] Brief description (1-2 sentences)
- [ ] Features/capabilities section
- [ ] Installation instructions
- [ ] Basic usage examples
- [ ] Links to detailed documentation
- [ ] License information
- [ ] Author/maintainer information

Content checks:

- [ ] No broken links to internal documentation
- [ ] Examples are accurate and tested
- [ ] Installation steps are clear and complete
- [ ] README is more than trivial (at least 500 words of useful content)

### Command Validation

Each command file (in `commands/*.md`) must include:

YAML frontmatter:

- [ ] `name`: kebab-case command name
- [ ] `description`: one-sentence description
- [ ] `type`: "interactive" or "automated"

Content sections:

- [ ] Overview: Clear explanation of command purpose
- [ ] Required Information: Input parameters and formats
- [ ] Prerequisites: What must be true before running
- [ ] Process: Step-by-step workflow description
- [ ] Expected Outputs: What the user receives
- [ ] Common Issues & Solutions: Troubleshooting guide
- [ ] Integration: Related commands and skills

Validation checks:

- [ ] YAML frontmatter is valid
- [ ] All required sections present
- [ ] Examples are clear and accurate
- [ ] Links to related skills exist
- [ ] Instructions are clear and actionable

### Agent Validation

Each agent file (in `agents/*.md`) must include:

YAML frontmatter:

- [ ] `name`: kebab-case agent name
- [ ] `description`: one-sentence description
- [ ] `type`: "autonomous"

Content sections:

- [ ] Overview: Clear explanation of agent purpose
- [ ] Autonomy Scope: Defined autonomous decisions and escalation triggers
- [ ] Prerequisites: Required preconditions
- [ ] Workflow and Logic: Detailed execution sequence
- [ ] Error Handling and Recovery: Error scenarios and recovery strategies
- [ ] Decision Points and Logic: Major decisions the agent makes
- [ ] Integration Points: Related components
- [ ] Examples and Use Cases: Concrete examples
- [ ] Testing and Validation: How to test the agent
- [ ] Monitoring and Logging: What gets logged

Validation checks:

- [ ] YAML frontmatter is valid
- [ ] All required sections present
- [ ] Autonomy boundaries are clearly defined
- [ ] Error handling is comprehensive
- [ ] Examples demonstrate realistic scenarios
- [ ] Integration points are documented

### Skill Validation

Each skill file (`skills/skill-name/SKILL.md`) must include:

YAML frontmatter:

- [ ] `name`: kebab-case skill name
- [ ] `description`: one-sentence description
- [ ] `version`: semantic versioning
- [ ] `last_updated`: ISO date format (YYYY-MM-DD)

Content sections:

- [ ] Overview: Comprehensive skill explanation
- [ ] Core Capabilities: List and describe main capabilities
- [ ] Key Concepts: Define fundamental concepts
- [ ] Workflows and Patterns: Detailed workflow descriptions
- [ ] Integration Points: How it connects to other components
- [ ] Examples and Use Cases: Real-world examples
- [ ] Maintenance Notes: Update frequency and dependencies
- [ ] Troubleshooting: Common problems and solutions

Validation checks:

- [ ] YAML frontmatter is valid and complete
- [ ] All required sections present
- [ ] Concepts are clearly explained with examples
- [ ] Workflows are detailed and actionable
- [ ] Integration points are documented
- [ ] Content is substantial (at least 1000 words of useful content)
- [ ] Examples are tested and accurate

## Link Validation

All internal links must be valid:

- [ ] Links to commands: `/command-name`
- [ ] Links to other skills: `../skill-name/SKILL.md`
- [ ] Links to documentation: `../DEVELOPMENT.md#section`
- [ ] No broken links in documentation
- [ ] No references to non-existent files

## Metadata Validation

Check YAML frontmatter in all files:

- [ ] All required fields present
- [ ] No extra/unknown fields
- [ ] Descriptions are meaningful (not placeholder text)
- [ ] Names follow naming conventions (kebab-case)
- [ ] Versions follow semantic versioning

## Content Quality Validation

Check quality of documentation:

- [ ] No placeholder text like "[description]" or "[add description here]"
- [ ] Examples are real and tested
- [ ] Instructions are clear and actionable
- [ ] No TODOs or incomplete sections in published content
- [ ] Grammar and spelling are correct
- [ ] Formatting is consistent
- [ ] Code examples are properly formatted

## Validation Script Usage

To validate a plugin manually:

```bash
# Validate plugin structure
cd plugins/your-plugin
ls -la | grep -E '\.claude-plugin|README|commands|agents|skills'

# Validate JSON manifest
jq . .claude-plugin/plugin.json

# Check for required files
find . -name "*.md" -type f | wc -l
```

## Common Validation Issues and Fixes

### Issue: Manifest JSON is invalid

**Symptom**: `jq` command fails to parse
**Solution**: Use a JSON linter to identify syntax errors (missing commas, quotes, etc.)

### Issue: Referenced files don't exist

**Symptom**: File paths in manifest don't match actual files
**Solution**: Verify all paths use correct case and paths

### Issue: Missing sections in documentation

**Symptom**: Section headers are missing from command/agent/skill files
**Solution**: Add required sections using the templates

### Issue: Broken links

**Symptom**: Links to other files fail
**Solution**: Verify paths are correct and files exist

### Issue: Plugin name doesn't match directory

**Symptom**: Manifest says "my-plugin" but directory is "myplugin"
**Solution**: Ensure directory name exactly matches `name` field in manifest

## Pre-Submission Checklist

Before submitting a plugin for review:

- [ ] All structure validation checks pass
- [ ] All manifest validation checks pass
- [ ] All content validation checks pass
- [ ] All links are valid
- [ ] All examples have been tested
- [ ] No placeholder text remains
- [ ] Plugin has been tested locally
- [ ] README provides clear installation and usage instructions
- [ ] All related plugins and dependencies are documented
- [ ] Version number is set appropriately

## Continuous Validation

Plugins should be validated regularly:

- After any content changes
- Before publishing new versions
- When dependencies change
- When adding new components
- During code review process

This ensures ongoing quality and consistency.
