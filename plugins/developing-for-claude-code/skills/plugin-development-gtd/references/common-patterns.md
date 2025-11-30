# Common Plugin Development Patterns

This file contains reusable code snippets and patterns that are referenced across multiple workflows.

## Marketplace Registration

### Update Marketplace Manifest

```bash
# Backup existing marketplace manifest
cp .claude-plugin/marketplace.json .claude-plugin/marketplace.json.backup

# Add plugin to marketplace manifest
jq --arg name "$PLUGIN_NAME" \
   --arg path "plugins/$PLUGIN_NAME" \
   --arg desc "$PLUGIN_DESCRIPTION" \
   '.plugins += {name: $name, path: $path, description: $desc}' \
   .claude-plugin/marketplace.json > .claude-plugin/marketplace.json.tmp && \
mv .claude-plugin/marketplace.json.tmp .claude-plugin/marketplace.json

# Validate JSON
jq . .claude-plugin/marketplace.json
```

### Plugin Manifest Template

```json
{
  "name": "$PLUGIN_NAME",
  "version": "$PLUGIN_VERSION",
  "description": "$PLUGIN_DESCRIPTION",
  "components": {
    "commands": [
      {
        "name": "command-name",
        "path": "commands/command-name.md"
      }
    ],
    "agents": [
      {
        "name": "agent-name",
        "path": "agents/agent-name.md"
      }
    ],
    "skills": [
      {
        "name": "skill-name",
        "path": "skills/skill-name/SKILL.md"
      }
    ]
  },
  "dependencies": [],
  "marketplace": "gtd-cc"
}
```

## Component Registration

### Register Component in Plugin Manifest

```bash
# Add command to manifest
jq --arg name "command-name" \
   --arg path "commands/command-name.md" \
   '.components.commands += {name: $name, path: $path}' \
   plugins/$PLUGIN_NAME/.claude-plugin/plugin.json > tmp.json && \
mv tmp.json plugins/$PLUGIN_NAME/.claude-plugin/plugin.json

# Add agent to manifest
jq --arg name "agent-name" \
   --arg path "agents/agent-name.md" \
   '.components.agents += {name: $name, path: $path}' \
   plugins/$PLUGIN_NAME/.claude-plugin/plugin.json > tmp.json && \
mv tmp.json plugins/$PLUGIN_NAME/.claude-plugin/plugin.json

# Add skill to manifest
jq --arg name "skill-name" \
   --arg path "skills/skill-name/SKILL.md" \
   '.components.skills += {name: $name, path: $path}' \
   plugins/$PLUGIN_NAME/.claude-plugin/plugin.json > tmp.json && \
mv tmp.json plugins/$PLUGIN_NAME/.claude-plugin/plugin.json
```

## Directory Structure

### Standard Plugin Directory Structure

```bash
# Create complete plugin structure
mkdir -p plugins/$PLUGIN_NAME/{commands,agents,skills,skills/skill-name/workflows,skills/skill-name/{scripts,references,assets}}

# Create plugin metadata directory
mkdir -p plugins/$PLUGIN_NAME/.claude-plugin

# Create skill subdirectories (when creating skills)
mkdir -p plugins/$PLUGIN_NAME/skills/skill-name/{scripts,references,assets}
mkdir -p plugins/$PLUGIN_NAME/skills/skill-name/workflows
```

## Validation Commands

### Validate Plugin Structure

```bash
# Check all JSON manifests
find . -name "plugin.json" -exec jq . {} \;

# Validate marketplace manifest
jq . .claude-plugin/marketplace.json

# Test plugin discovery
/plugin list

# Test plugin installation
/plugin install $PLUGIN_NAME@gtd-cc
```

## Naming Conventions

### File Naming Patterns

- **Commands**: kebab-case (e.g., `create-plugin.md`)
- **Agents**: kebab-case (e.g., `plugin-builder-agent.md`)
- **Skills**: kebab-case directories with `SKILL.md` (e.g., `plugin-development/`)
- **Workflows**: kebab-case (e.g., `create-new-plugin.md`)

### Manifest Component Registration

All paths in plugin manifests should be relative to the plugin root:
- `commands/command-name.md`
- `agents/agent-name.md`
- `skills/skill-name/SKILL.md`
- `skills/skill-name/workflows/workflow-name.md`