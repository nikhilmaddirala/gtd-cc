---
description: Update documentation based on scope and type parameters
---

# Update Documentation Workflow

Keep documentation synchronized with code changes using structured parameters.

## Parameters

- **scope**: Determines documentation reach
  - single: Update individual documents
  - multiple: Update across documentation layers
  - all: Systematic maintenance across all documentation

- **type**: Determines update nature
  - minor: Update references, key information, version numbers
  - refactor: Restructure content, reorganize sections
  - release: Prepare documentation for release

## Context

Before starting:
- Code changes have been made that affect documentation
- Or you're preparing for a release
- Or doing scheduled maintenance (scope=all, type=minor)
- Documentation follows three-layer model

## Process

### Step 1: Analyze Update Requirements

Use the shared folder-exploration component to understand what needs updating:
> "Use the shared folder-exploration component to analyze project structure and identify documentation requirements"

### Step 2: Execute Based on Parameters

#### scope=single, type=minor (Individual Document Updates)

1. **Identify target document**
   ```bash
   # Find document related to code changes
   grep -r "function/class/module_name" docs/ *.md
   ```

2. **Update specific sections**
   - Version numbers
   - API references
   - Configuration examples
   - Cross-references

3. **Reference templates as needed**
   - Use `../templates/template-readme.md` for structure reference
   - Ensure consistent formatting across updates

#### scope=multiple, type=minor (Cross-Layer Updates)

1. **Update root README.md** using `../templates/template-readme.md`
   - Quick start instructions
   - Version compatibility
   - Key feature changes

2. **Update directory READMEs**
   - Module interfaces
   - Inter-module dependencies
   - Local examples

3. **Update /docs files**
   - API reference changes
   - Configuration updates
   - Tutorial adjustments

#### scope=single, type=refactor (Document Restructure)

1. **Analyze current structure**
   ```bash
   # Document current organization
   grep -n "^#" target-document.md
   ```

2. **Plan restructure**
   - Identify sections to move/merge/delete
   - Plan new organization
   - Maintain cross-reference integrity

3. **Execute restructure**
   - Reference `../templates/template-readme.md` for consistency
   - Preserve critical information
   - Update all internal links

#### scope=multiple, type=refactor (Architecture Updates)

1. **Assess documentation architecture**
   - Phase appropriateness (1→2→3 transitions)
   - Content distribution across layers
   - Redundancy identification

2. **Restructure across layers**
   - Move content to appropriate layers
   - Eliminate duplication
   - Update cross-references

3. **Consider phase transitions**
   - Phase 1→2: Add module READMEs
   - Phase 2→3: Create /docs folder
   - Move detailed content from READMEs to /docs

#### scope=all, type=minor (Maintenance)

1. **Quarterly maintenance checklist**
   ```bash
   # Check for outdated content or unresolved items
   find . -name "*.md" -exec grep -l "TODO|FIXME|v[0-9]\." {} \;

   # Check broken links
   find . -name "*.md" -exec markdown-link-check {} \;
   ```

2. **Update all references**
   - Version numbers across all documents
   - Outdated feature descriptions
   - Deprecated configuration options
   - External links

3. **Remove outdated information**
   - Don't patch around it - delete and replace
   - Add cross-references instead of duplicating

### Step 2: Locate Documentation to Update

Find all places that mention the changed feature:

```bash
# Find all mentions of the changed feature
grep -r "old-feature-name" . --include="*.md" | grep -v node_modules

# Check README
grep -i "feature" README.md

# Check /docs
find docs -name "*.md" -type f | xargs grep -l "feature" 2>/dev/null
```

### Step 3: Update in Right Layer

Apply the structure rules from SKILL.md:

**For quick facts:** Update README.md

**For installation/setup:** Update /docs/tutorials/getting-started.md, reference from README

**For detailed API:** Update /docs/api-reference.md, link from README

**For architecture/design:** Update /docs/architecture.md

**For configuration:** Update /docs/configuration.md

**For module context:** Update relevant directory README.md

### Step 4: Remove Duplication

If the change is mentioned in multiple places:

```bash
# Check for duplicates
grep -r "feature-name" . --include="*.md" | wc -l
```

Keep only in ONE authoritative place, link from others:

```markdown
For complete configuration options, see [Configuration Guide](../../docs/configuration.md).
```

### Step 5: Update Examples

Test that all code examples still work:

```bash
# For quick start examples
# Copy commands from README and run them manually
# Verify output matches what's documented

# For API examples
# Run code examples as shown in /docs/api-reference.md
# Verify they compile/run correctly
```

Update broken examples:

- Fix deprecated API calls
- Update version numbers
- Fix import paths
- Ensure examples match current behavior

### Step 6: Structure Changes

If directory structure changed:

```bash
# Find all directory READMEs
find . -path "./docs" -prune -o -path "./node_modules" -prune -o -name "README.md" -type f -print

# Update each one to reflect new structure
```

Update affected directory READMEs:

- Rename or remove sections
- Update structure explanation
- Update "How to Extend" instructions
- Fix cross-references

### Step 7: Link Verification

Verify all links work:

```bash
# Find all links in documentation
grep -r "\[.*\](" . --include="*.md" | grep -oP '\]\(\K[^)]+' | sort | uniq

# Manually check key links:
test -f docs/api-reference.md && echo "✓ api-reference exists"
test -f docs/architecture.md && echo "✓ architecture exists"
test -f CONTRIBUTING.md && echo "✓ CONTRIBUTING exists"
test -f README.md && echo "✓ README exists"
```

Fix broken links:

- Update relative paths if structure changed
- Remove links to deleted files
- Add missing links between layers

### Step 8: For Release

Before releasing, run release checklist:

```bash
# Version match
grep -i "version" README.md

# Quick start verification
# Follow every step in README Getting Started
# Verify it works with new code

# Check documentation completeness
# Scan /docs for incomplete items or placeholders
grep -r "TODO\|FIXME" docs/ --include="*.md"

# Configuration reference current?
ls docs/configuration.md && wc -l docs/configuration.md

# API reference complete?
ls docs/api-reference.md && grep "##" docs/api-reference.md | wc -l
```

### Step 9: Organize Your Changes

If you reorganized content:

- Ensure content moved to right layer (README → /docs, etc.)
- Remove duplication
- Create cross-references
- Verify navigation still works

Example reorganization:

```bash
# Before: Installation in README (100 lines)
# Action: Move to docs/tutorials/getting-started.md
# Then: Update README with link to tutorial
# Result: README stays short, detailed guide in /docs
```

### Step 10: Verify No Duplication

For each important piece of information:

```bash
# Check it appears in ONE authoritative place
# Other places should link to it, not repeat it

# Example: installation instructions
grep -r "npm install" . --include="*.md" | wc -l
# Should be 1-2 (once in /docs, link in README)
```

### Step 11: Commit Documentation Changes

When documentation is updated:

```bash
# Stage documentation changes
git add README.md docs/ [directory READMEs]

# Commit with clear message
git commit -m "docs: update [what changed]

- Updated API reference for new function
- Removed deprecated configuration options
- Fixed examples to match v2.0
- Moved installation to tutorials/"
```

## Examples

### Example 1: Added a Feature

```bash
# Feature: new widget API added

# 1. Find mentions
grep -r "api" . --include="*.md"

# 2. Update
# - Add to /docs/api-reference.md (authoritative)
# - Update README with link to new feature
# - Add example to /docs/tutorials/basic-usage.md

# 3. Check duplication
grep -r "widget" . --include="*.md"
# Should appear in: api-reference, tutorials, README link

# 4. Test examples
# Run code examples from docs/tutorials/
```

### Example 2: Changed Installation

```bash
# Change: Node.js version requirement increased

# 1. Identify all mentions
grep -r "node" . --include="*.md" -i

# 2. Update
# - Update /docs/tutorials/getting-started.md
# - Update README (if mentions version)
# - Update any CI/deployment docs

# 3. Test
# Follow exact steps in getting-started.md
# Verify they work with new version requirement
```

### Example 3: Restructured Code

```bash
# Change: Moved utils from src/lib to src/utils

# 1. Find affected docs
grep -r "src/lib" . --include="*.md"

# 2. Update
# - Update src/lib/README.md if exists
# - Update src/utils/README.md
# - Update architecture if structure shown there

# 3. Verify navigation
# Check all cross-references still work
```

## Guidelines

- Update documentation on same PR that changes behavior
- Document changes before submitting PR
- Use appropriate layer - don't put everything in README
- Remove duplication - link instead
- Test that examples still work
- Verify all links work
- For releases: verify quick start works end-to-end
- Make documentation updates part of definition of done

## Success Criteria

- ✅ Code changes documented in appropriate layer
- ✅ No information duplicated across layers
- ✅ All links verified and working
- ✅ Code examples tested and working
- ✅ Quick start still works end-to-end (for releases)
- ✅ Version numbers match release (for releases)
- ✅ TODOs and placeholders resolved
