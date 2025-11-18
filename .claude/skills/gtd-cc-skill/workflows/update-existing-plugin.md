---
description: Add new components or update existing plugin structure
---

# Update Existing Plugin Workflow

## Overview

Update an existing plugin in the gtd-cc marketplace by adding new components (commands, agents, skills), modifying existing ones, or updating plugin configuration.

## Process

### 1. Identify the target plugin

```bash
# List available plugins
ls plugins/

# Select the plugin to update
PLUGIN_NAME="<plugin-name>"
echo "Updating plugin: $PLUGIN_NAME"
```

### 2. Analyze current plugin structure

```bash
# Examine existing plugin structure
echo "=== Current Plugin Structure ==="
find plugins/$PLUGIN_NAME -type f -name "*.md" | sort

# Check current manifest
echo -e "\n=== Current Manifest ==="
cat plugins/$PLUGIN_NAME/.claude-plugin/plugin.json

# Check current README
echo -e "\n=== Current README ==="
head -20 plugins/$PLUGIN_NAME/README.md
```

### 3. Determine what to add/modify

Based on the requirements, identify which components need to be added:

**New Command**: Interactive slash command (`/command-name`)
**New Agent**: Autonomous workflow executor  
**New Skill**: Domain expertise foundation
**Update Manifest**: Add/remove component references
**Update Documentation**: README changes, new examples

### 4. Add new components

#### For New Commands:
```bash
# Create command file
COMMAND_FILE="plugins/$PLUGIN_NAME/commands/<command-name>.md"
touch $COMMAND_FILE

# Add command template
cat > $COMMAND_FILE << 'EOF'
---
name: <command-name>
description: Brief description of what the command does
---

## Context

Explain the context and purpose of this command.

## Process

Step-by-step process for the command workflow.

## Expected Interactions

Describe user interactions and expected inputs.
EOF
```

#### For New Agents:
```bash
# Create agent file
AGENT_FILE="plugins/$PLUGIN_NAME/agents/<agent-name>.md"
touch $AGENT_FILE

# Add agent template
cat > $AGENT_FILE << 'EOF'
---
name: <agent-name>
description: Brief description of what the agent does
---

## Purpose

Explain the autonomous purpose of this agent.

## Process

Step-by-step autonomous workflow process.

## Decision Points

Key decision points and how the agent should handle them.

## Error Handling

How to handle errors and recovery scenarios.

## Success Criteria

What constitutes successful completion.
EOF
```

#### For New Skills:
```bash
# Create skill directory and file
SKILL_DIR="plugins/$PLUGIN_NAME/skills/<skill-name>"
mkdir -p $SKILL_DIR
touch $SKILL_DIR/SKILL.md

# Add skill template
cat > $SKILL_DIR/SKILL.md << 'EOF'
---
description: Domain expertise for <skill-domain>
---

# <skill-name>

Domain expertise and workflows for <skill-domain>.

## When to use this skill

Use this skill when you need to...

## Available workflows

List of workflows this skill provides.

## Integration

How this skill integrates with other components.
EOF
```

### 5. Update plugin manifest

```bash
# Read current manifest
MANIFEST_FILE="plugins/$PLUGIN_NAME/.claude-plugin/plugin.json"
jq . $MANIFEST_FILE

# Add new components to manifest
# Update the appropriate arrays: commands, agents, skills
```

### 6. Update plugin README

```bash
# Update README.md with new components
README_FILE="plugins/$PLUGIN_NAME/README.md"

# Add new components to appropriate sections
# Update component lists and examples
```

### 7. Validate changes

```bash
# Validate JSON syntax
jq . $MANIFEST_FILE

# Check directory structure
echo "=== Updated Plugin Structure ==="
find plugins/$PLUGIN_NAME -type f -name "*.md" | sort

# Verify all referenced files exist
# Check for broken links or missing files
```

### 8. Test integration

```bash
# Test new commands locally if possible
# Verify agents can be invoked
# Check skill accessibility
```

## Guidelines

### Naming Conventions
- **Commands**: kebab-case, prefixed by plugin (e.g., `gh-issue`, `ob-capture`)
- **Agents**: kebab-case with descriptive names (e.g., `plugin-health-agent`)
- **Skills**: kebab-case directories with uppercase `SKILL.md` files

### File Format Standards
- All markdown files use YAML frontmatter
- Include comprehensive documentation
- Provide examples where applicable
- Link to related resources

### Manifest Updates
- Ensure all new components are listed in plugin.json
- Use consistent formatting
- Include version and description updates

## Success Criteria

- [ ] New components are created with proper structure
- [ ] Plugin manifest accurately reflects all components
- [ ] README documentation is updated and accurate
- [ ] JSON syntax is valid
- [ ] All files follow naming conventions
- [ ] No broken links or missing references
- [ ] Components integrate properly with existing plugin structure

## Error Handling

**Invalid JSON**: Fix syntax errors in manifest files
**Missing Files**: Create missing components or update references
**Broken Links**: Update file paths or create missing files
**Naming Conflicts**: Choose unique names following conventions
**Integration Issues**: Verify component dependencies and imports