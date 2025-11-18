---
description: Validate all plugins for structure, manifests, and documentation
---

# Validate Existing Plugins Workflow

## Overview

Comprehensive validation of all plugins in the gtd-cc marketplace including structure, manifests, documentation completeness, and marketplace consistency.

## Process

### 1. Scan marketplace for all plugins

```bash
echo "=== Scanning gtd-cc Marketplace ==="
MARKETPLACE_FILE=".claude-plugin/marketplace.json"

# Check if marketplace file exists
if [ ! -f "$MARKETPLACE_FILE" ]; then
  echo "ERROR: Marketplace manifest not found at $MARKETPLACE_FILE"
  exit 1
fi

# List all registered plugins
echo "Registered plugins:"
jq -r '.plugins[].name' $MARKETPLACE_FILE | sort

# Get plugin count
PLUGIN_COUNT=$(jq '.plugins | length' $MARKETPLACE_FILE)
echo "Total plugins registered: $PLUGIN_COUNT"
```

### 2. Validate plugin directory structure

```bash
echo -e "\n=== Validating Plugin Directory Structure ==="

# Check plugins directory exists
if [ ! -d "plugins" ]; then
  echo "ERROR: plugins directory not found"
  exit 1
fi

# Validate each plugin's directory structure
jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  echo -e "\n--- Validating $PLUGIN_NAME ---"
  
  PLUGIN_DIR="plugins/$PLUGIN_NAME"
  
  # Check plugin directory exists
  if [ ! -d "$PLUGIN_DIR" ]; then
    echo "✗ Plugin directory missing: $PLUGIN_DIR"
    continue
  fi
  echo "✓ Plugin directory exists: $PLUGIN_DIR"
  
  # Check required subdirectories
  REQUIRED_DIRS=(
    "$PLUGIN_DIR/.claude-plugin"
    "$PLUGIN_DIR/commands"
    "$PLUGIN_DIR/agents"
    "$PLUGIN_DIR/skills"
  )
  
  for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
      echo "✓ Directory exists: $(basename $dir)"
    else
      echo "✗ Directory missing: $dir"
    fi
  done
done
```

### 3. Validate plugin manifests

```bash
echo -e "\n=== Validating Plugin Manifests ==="

jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  echo -e "\n--- Validating $PLUGIN_NAME manifest ---"
  
  MANIFEST_FILE="plugins/$PLUGIN_NAME/.claude-plugin/plugin.json"
  
  # Check manifest exists
  if [ ! -f "$MANIFEST_FILE" ]; then
    echo "✗ Plugin manifest missing: $MANIFEST_FILE"
    continue
  fi
  
  # Validate JSON syntax
  if jq empty "$MANIFEST_FILE" 2>/dev/null; then
    echo "✓ Valid JSON syntax"
  else
    echo "✗ Invalid JSON syntax in $MANIFEST_FILE"
    continue
  fi
  
  # Check required fields
  REQUIRED_FIELDS=("name" "version" "description" "components")
  for field in "${REQUIRED_FIELDS[@]}"; do
    if jq -e ".$field" "$MANIFEST_FILE" > /dev/null 2>&1; then
      echo "✓ Field exists: $field"
    else
      echo "✗ Required field missing: $field"
    fi
  done
  
  # Validate component arrays
  COMPONENT_TYPES=("commands" "agents" "skills")
  for component in "${COMPONENT_TYPES[@]}"; do
    COMPONENT_COUNT=$(jq ".components.$component | length" "$MANIFEST_FILE" 2>/dev/null || echo "0")
    echo "✓ $component: $COMPONENT_COUNT items"
  done
done
```

### 4. Validate component files exist

```bash
echo -e "\n=== Validating Component Files ==="

jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  echo -e "\n--- Validating $PLUGIN_NAME components ---"
  
  MANIFEST_FILE="plugins/$PLUGIN_NAME/.claude-plugin/plugin.json"
  
  if [ ! -f "$MANIFEST_FILE" ]; then
    echo "Skipping $PLUGIN_NAME - manifest missing"
    continue
  fi
  
  # Check commands
  jq -r '.components.commands[]?' "$MANIFEST_FILE" 2>/dev/null | while read COMMAND; do
    COMMAND_FILE="plugins/$PLUGIN_NAME/commands/$COMMAND.md"
    if [ -f "$COMMAND_FILE" ]; then
      echo "✓ Command file exists: $COMMAND"
    else
      echo "✗ Command file missing: $COMMAND_FILE"
    fi
  done
  
  # Check agents
  jq -r '.components.agents[]?' "$MANIFEST_FILE" 2>/dev/null | while read AGENT; do
    AGENT_FILE="plugins/$PLUGIN_NAME/agents/$AGENT.md"
    if [ -f "$AGENT_FILE" ]; then
      echo "✓ Agent file exists: $AGENT"
    else
      echo "✗ Agent file missing: $AGENT_FILE"
    fi
  done
  
  # Check skills
  jq -r '.components.skills[]?' "$MANIFEST_FILE" 2>/dev/null | while read SKILL; do
    SKILL_FILE="plugins/$PLUGIN_NAME/skills/$SKILL/SKILL.md"
    if [ -f "$SKILL_FILE" ]; then
      echo "✓ Skill file exists: $SKILL"
    else
      echo "✗ Skill file missing: $SKILL_FILE"
    fi
  done
done
```

### 5. Validate documentation

```bash
echo -e "\n=== Validating Documentation ==="

jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  echo -e "\n--- Validating $PLUGIN_NAME documentation ---"
  
  README_FILE="plugins/$PLUGIN_NAME/README.md"
  
  # Check README exists
  if [ -f "$README_FILE" ]; then
    echo "✓ README.md exists"
    
    # Check README content
    if grep -q "## Overview" "$README_FILE"; then
      echo "✓ README has Overview section"
    else
      echo "⚠ README missing Overview section"
    fi
    
    if grep -q "## Components" "$README_FILE"; then
      echo "✓ README has Components section"
    else
      echo "⚠ README missing Components section"
    fi
    
    if grep -q "## Quick Start" "$README_FILE"; then
      echo "✓ README has Quick Start section"
    else
      echo "⚠ README missing Quick Start section"
    fi
  else
    echo "✗ README.md missing"
  fi
done
```

### 6. Validate naming conventions

```bash
echo -e "\n=== Validating Naming Conventions ==="

jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  echo -e "\n--- Validating $PLUGIN_NAME naming ---"
  
  # Check plugin name follows kebab-case
  if [[ "$PLUGIN_NAME" =~ ^[a-z0-9-]+$ ]]; then
    echo "✓ Plugin name follows kebab-case: $PLUGIN_NAME"
  else
    echo "✗ Plugin name violates kebab-case: $PLUGIN_NAME"
  fi
  
  # Check command names
  MANIFEST_FILE="plugins/$PLUGIN_NAME/.claude-plugin/plugin.json"
  if [ -f "$MANIFEST_FILE" ]; then
    jq -r '.components.commands[]?' "$MANIFEST_FILE" 2>/dev/null | while read COMMAND; do
      if [[ "$COMMAND" =~ ^[a-z0-9-]+$ ]]; then
        echo "✓ Command name follows kebab-case: $COMMAND"
      else
        echo "✗ Command name violates kebab-case: $COMMAND"
      fi
    done
  fi
done
```

### 7. Validate marketplace consistency

```bash
echo -e "\n=== Validating Marketplace Consistency ==="

# Check for duplicate plugin names
DUPLICATE_NAMES=$(jq -r '.plugins[].name' $MARKETPLACE_FILE | sort | uniq -d)
if [ -n "$DUPLICATE_NAMES" ]; then
  echo "✗ Duplicate plugin names found:"
  echo "$DUPLICATE_NAMES"
else
  echo "✓ No duplicate plugin names"
fi

# Check all registered plugins have directories
jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  if [ -d "plugins/$PLUGIN_NAME" ]; then
    echo "✓ Plugin $PLUGIN_NAME has directory"
  else
    echo "✗ Plugin $PLUGIN_NAME missing directory"
  fi
done

# Check all plugin directories are registered
for PLUGIN_DIR in plugins/*/; do
  if [ -d "$PLUGIN_DIR" ]; then
    PLUGIN_NAME=$(basename "$PLUGIN_DIR")
    if jq -e ".plugins[] | select(.name == \"$PLUGIN_NAME\")" "$MARKETPLACE_FILE" > /dev/null 2>&1; then
      echo "✓ Plugin $PLUGIN_NAME is registered"
    else
      echo "⚠ Plugin $PLUGIN_NAME exists but not registered in marketplace"
    fi
  fi
done
```

### 8. Generate validation report

```bash
echo -e "\n=== Validation Summary ==="

# Count validation results
TOTAL_PLUGINS=$(jq '.plugins | length' $MARKETPLACE_FILE)
echo "Total plugins in marketplace: $TOTAL_PLUGINS"

# Count plugins with valid manifests
VALID_MANIFESTS=0
jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  if [ -f "plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" ] && jq empty "plugins/$PLUGIN_NAME/.claude-plugin/plugin.json" 2>/dev/null; then
    ((VALID_MANIFESTS++))
  fi
done

echo "Plugins with valid manifests: $VALID_MANIFESTS/$TOTAL_PLUGINS"

# Count plugins with README
README_COUNT=0
jq -r '.plugins[].name' $MARKETPLACE_FILE | while read PLUGIN_NAME; do
  if [ -f "plugins/$PLUGIN_NAME/README.md" ]; then
    ((README_COUNT++))
  fi
done

echo "Plugins with README: $README_COUNT/$TOTAL_PLUGINS"

echo -e "\nValidation complete. Review the output above for any issues that need to be addressed."
```

## Guidelines

### Validation Criteria

**Critical Issues** (must fix):
- Missing plugin directories or manifests
- Invalid JSON syntax
- Missing required manifest fields
- Unregistered plugin directories

**Important Issues** (should fix):
- Missing component files referenced in manifests
- Missing README.md files
- Naming convention violations

**Minor Issues** (nice to fix):
- Incomplete README sections
- Missing optional documentation

### Fix Priority

1. **Critical**: Fix JSON syntax, missing files, registration issues
2. **Important**: Add missing documentation, fix naming
3. **Minor**: Enhance documentation, add examples

## Success Criteria

- [ ] All registered plugins have valid directory structures
- [ ] All plugin manifests have valid JSON syntax
- [ ] All required manifest fields are present
- [ ] All referenced component files exist
- [ ] All plugins have README.md documentation
- [ ] Naming conventions are followed
- [ ] Marketplace registration is consistent
- [ ] No duplicate plugin names exist

## Error Handling

**JSON parsing errors**: Fix syntax issues in manifest files
**Missing directories**: Create required directory structure
**File not found errors**: Create missing files or update references
**Naming convention violations**: Rename components following conventions
**Marketplace inconsistencies**: Update registration or remove orphaned directories

## Automation

This validation workflow can be automated to run:
- Before releases to ensure marketplace health
- In CI/CD pipelines to catch issues early
- On demand to check plugin status
- Periodically to maintain marketplace quality