---
description: Create new plugin with proper structure and marketplace registration
---

# Create New Plugin Workflow

## Overview

Create a brand new plugin in the gtd-cc marketplace with complete directory structure, manifests, initial components, and marketplace registration.

## Process

### 1. Define plugin specifications

```bash
# Gather plugin information
PLUGIN_NAME="<plugin-name>"
PLUGIN_DESCRIPTION="<Brief description of plugin purpose>"
PLUGIN_VERSION="0.1.0"

echo "Creating plugin: $PLUGIN_NAME"
echo "Description: $PLUGIN_DESCRIPTION"
echo "Version: $PLUGIN_VERSION"
```

### 2. Create plugin directory structure

```bash
# Create main plugin directory
mkdir -p plugins/$PLUGIN_NAME

# Create subdirectories
mkdir -p plugins/$PLUGIN_NAME/.claude-plugin
mkdir -p plugins/$PLUGIN_NAME/commands
mkdir -p plugins/$PLUGIN_NAME/agents
mkdir -p plugins/$PLUGIN_NAME/skills

echo "Created directory structure for $PLUGIN_NAME"
```

### 3. Create plugin manifest

```bash
# Create plugin.json manifest
cat > plugins/$PLUGIN_NAME/.claude-plugin/plugin.json << EOF
{
  "name": "$PLUGIN_NAME",
  "version": "$PLUGIN_VERSION",
  "description": "$PLUGIN_DESCRIPTION",
  "components": {
    "commands": [],
    "agents": [],
    "skills": []
  },
  "dependencies": [],
  "marketplace": "gtd-cc"
}
EOF

echo "Created plugin manifest"
```

### 4. Create plugin README

```bash
# Create README.md
cat > plugins/$PLUGIN_NAME/README.md << EOF
# $PLUGIN_NAME Plugin

## Overview

$PLUGIN_DESCRIPTION

## Components

### Commands

Interactive slash commands for $PLUGIN_NAME workflows.

### Agents

Autonomous agents for $PLUGIN_NAME operations.

### Skills

Domain expertise and workflows for $PLUGIN_NAME.

## Quick Start

### Installation

Add this plugin to Claude Code:

\`\`\`bash
/plugin install $PLUGIN_NAME@gtd-cc
\`\`\`

### Available Commands

List available commands here once implemented.

### Available Agents

List available agents here once implemented.

## Development

This plugin follows the gtd-cc marketplace conventions. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## Structure

\`\`\`
$PLUGIN_NAME/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── commands/                # Interactive commands
├── agents/                  # Autonomous agents
├── skills/                  # Domain expertise
└── README.md               # This file
\`\`\`

## Support

- **Issues**: Report bugs via GitHub Issues
- **Documentation**: See plugin-specific documentation
EOF

echo "Created plugin README"
```

### 5. Create initial components (optional)

#### Create initial skill (recommended):
```bash
# Create domain-specific skill
SKILL_DIR="plugins/$PLUGIN_NAME/skills/$PLUGIN_NAME-skill"
mkdir -p $SKILL_DIR

cat > $SKILL_DIR/SKILL.md << EOF
---
description: Domain expertise for $PLUGIN_NAME operations
---

# $PLUGIN_NAME-skill

Domain expertise and workflows for $PLUGIN_NAME operations.

## When to use this skill

Use this skill when you need to:
- Perform $PLUGIN_NAME-specific operations
- Work with $PLUGIN_NAME data and workflows
- Integrate $PLUGIN_NAME with other systems

## Available workflows

### basic-workflow
Fundamental $PLUGIN_NAME operations and procedures.

**Use when**: You need to perform basic $PLUGIN_NAME tasks.

## Integration

This skill integrates with:
- github-gtd workflows for project management
- Other gtd-cc marketplace plugins as needed

## Success criteria

- $PLUGIN_NAME operations complete successfully
- Data integrity is maintained
- Integration points work correctly
EOF

echo "Created initial skill: $PLUGIN_NAME-skill"
```

#### Create initial command (optional):
```bash
# Create basic command
cat > plugins/$PLUGIN_NAME/commands/$PLUGIN_NAME-help.md << EOF
---
name: $PLUGIN_NAME-help
description: Get help and information about $PLUGIN_NAME plugin
---

## Overview

Provides help and usage information for the $PLUGIN_NAME plugin.

## Process

1. Display plugin overview and capabilities
2. List available commands and agents
3. Provide usage examples
4. Show integration points with other plugins

## Available Components

### Commands
- \`/$PLUGIN_NAME-help\` - This help command

### Agents
- (List agents here when created)

### Skills
- \`$PLUGIN_NAME-skill\` - Core domain expertise

## Examples

Basic usage examples will be added as the plugin develops.

## Integration

This plugin works with:
- github-gtd for project management workflows
- Other gtd-cc marketplace plugins
EOF

echo "Created initial command: $PLUGIN_NAME-help"
```

### 6. Update marketplace manifest

```bash
# Read current marketplace manifest
MARKETPLACE_FILE=".claude-plugin/marketplace.json"
echo "Current marketplace plugins:"
jq '.plugins' $MARKETPLACE_FILE

# Add new plugin to marketplace
jq --arg name "$PLUGIN_NAME" --arg desc "$PLUGIN_DESCRIPTION" '.plugins += [{name: $name, description: $desc, version: "0.1.0"}]' $MARKETPLACE_FILE > $MARKETPLACE_FILE.tmp && mv $MARKETPLACE_FILE.tmp $MARKETPLACE_FILE

echo "Added $PLUGIN_NAME to marketplace manifest"
```

### 7. Update plugin manifest with initial components

```bash
# Update plugin.json to include initial components
if [ -d "plugins/$PLUGIN_NAME/skills/$PLUGIN_NAME-skill" ]; then
  jq --arg skill "$PLUGIN_NAME-skill" '.components.skills += [$skill]' plugins/$PLUGIN_NAME/.claude-plugin/plugin.json > plugins/$PLUGIN_NAME/.claude-plugin/plugin.json.tmp && mv plugins/$PLUGIN_NAME/.claude-plugin/plugin.json.tmp plugins/$PLUGIN_NAME/.claude-plugin/plugin.json
fi

if [ -f "plugins/$PLUGIN_NAME/commands/$PLUGIN_NAME-help.md" ]; then
  jq --arg cmd "$PLUGIN_NAME-help" '.components.commands += [$cmd]' plugins/$PLUGIN_NAME/.claude-plugin/plugin.json > plugins/$PLUGIN_NAME/.claude-plugin/plugin.json.tmp && mv plugins/$PLUGIN_NAME/.claude-plugin/plugin.json.tmp plugins/$PLUGIN_NAME/.claude-plugin/plugin.json
fi

echo "Updated plugin manifest with initial components"
```

### 8. Validate plugin structure

```bash
# Validate JSON syntax
echo "=== Validating JSON files ==="
jq . plugins/$PLUGIN_NAME/.claude-plugin/plugin.json
jq . .claude-plugin/marketplace.json

# Check directory structure
echo -e "\n=== Plugin Structure ==="
find plugins/$PLUGIN_NAME -type f -name "*.md" | sort
find plugins/$PLUGIN_NAME -name "*.json"

# Verify required files exist
echo -e "\n=== Required Files Check ==="
REQUIRED_FILES=(
  "plugins/$PLUGIN_NAME/.claude-plugin/plugin.json"
  "plugins/$PLUGIN_NAME/README.md"
)

for file in "${REQUIRED_FILES[@]}"; do
  if [ -f "$file" ]; then
    echo "✓ $file exists"
  else
    echo "✗ $file missing"
  fi
done
```

### 9. Test plugin installation

```bash
# Test plugin can be found in marketplace
echo "=== Testing Marketplace Registration ==="
jq --arg name "$PLUGIN_NAME" '.plugins[] | select(.name == $name)' .claude-plugin/marketplace.json

# Verify plugin structure matches marketplace conventions
echo -e "\n=== Plugin Structure Validation ==="
echo "Plugin directory: plugins/$PLUGIN_NAME"
echo "Manifest exists: $([ -f "plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" ] && echo 'Yes' || echo 'No')"
echo "README exists: $([ -f "plugins/$PLUGIN_NAME/README.md" ] && echo 'Yes' || echo 'No')"
```

## Guidelines

### Naming Conventions
- **Plugin names**: kebab-case, descriptive (e.g., `web-research`, `obsidian`)
- **Commands**: kebab-case, prefixed by plugin (e.g., `web-crawl`, `ob-capture`)
- **Agents**: kebab-case with descriptive names
- **Skills**: kebab-case with `-skill` suffix

### Required Components
Every plugin must have:
- `.claude-plugin/plugin.json` manifest
- `README.md` documentation
- At least one skill or command to be useful

### Marketplace Integration
- All plugins must be registered in `.claude-plugin/marketplace.json`
- Plugin names must be unique within the marketplace
- Version numbers should follow semantic versioning

## Success Criteria

- [ ] Plugin directory structure created correctly
- [ ] Plugin manifest is valid JSON with required fields
- [ ] Plugin README is comprehensive and accurate
- [ ] Plugin is registered in marketplace manifest
- [ ] Initial components (skill/command) are created
- [ ] All naming conventions are followed
- [ ] Plugin can be discovered via marketplace commands

## Error Handling

**Plugin name exists**: Choose a different name or update existing plugin
**JSON validation errors**: Fix syntax in manifest files
**Missing directories**: Create required directory structure
**Marketplace conflicts**: Ensure unique plugin names
**Component registration errors**: Verify component names and paths

## Next Steps

After creating the basic plugin:
1. Implement domain-specific workflows in the skill
2. Add useful commands for common operations
3. Create agents for autonomous workflows
4. Write comprehensive documentation
5. Test integration with other gtd-cc plugins
6. Create examples and tutorials