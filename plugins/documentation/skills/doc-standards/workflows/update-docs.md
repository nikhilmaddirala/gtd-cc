---
description: Update documentation based on code changes, structure changes, or before releases
---

## Update Documentation Workflow

Keep documentation synchronized with code changes and prepare documentation for releases.

## Overview

This workflow guides you through updating documentation when code changes or before releases. It ensures changes are documented in the right layer without duplication.

## Context

Before starting:

- You've made code changes that affect user-facing behavior
- Or you're preparing for a release
- Or you want to restructure existing documentation
- Documentation exists and follows three-layer model

## Your Task

- Goal: Update documentation to reflect code/structure changes
- Target: Documentation is current and in the right layers
- Role: Maintain documentation accuracy across layers

### Step 1: Identify What Changed

```bash
# Review recent code changes
git log --oneline HEAD~5..HEAD

# Check what files were modified
git diff --name-only HEAD~1

# See what behavior changed
git diff HEAD~1 | head -50
```

Categorize the change:

- **Installation/setup changed** → Update README or /docs/tutorials/getting-started.md
- **Feature added** → Add to README or /docs/api-reference.md
- **Configuration changed** → Update /docs/configuration.md if exists
- **Architecture changed** → Update /docs/architecture.md and directory READMEs
- **API changed** → Update /docs/api-reference.md
- **Directory structure changed** → Update directory READMEs
- **Contribution processes changed** → Update CONTRIBUTING.md
- **Bug fixed** → Document in /docs/troubleshooting.md or release notes

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
# Scan /docs for TODOs or placeholders
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
