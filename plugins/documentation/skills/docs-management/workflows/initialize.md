---
description: Initialize documentation structure based on project phase
---

# Initialize Documentation Workflow

Set up proper documentation structure for a project based on its complexity phase.

## Overview

This workflow guides you through choosing and implementing the appropriate documentation layer for your project. It helps prevent documentation that's either too minimal or unnecessarily complex.

## Parameters

- **phase**: Determines documentation complexity
  - 1: Solo developer, simple projects - Single README.md
  - 2: Small teams, multiple modules - Multiple READMEs
  - 3: Complex architecture, tutorials - READMEs + /docs folder

## Context

Before starting:
- Understand your project size and team structure
- Know what documentation currently exists
- Identify primary users (developers, end users, both)
- Consider maintenance capacity

## Process

### Step 1: Analyze Current Project Structure

Use the shared folder-exploration component to understand your project:
> "Use the shared folder-exploration component to analyze project structure and identify documentation requirements"

Based on the analysis, confirm the appropriate phase:
- **Phase 1**: < 5 files, single module, solo developer
- **Phase 2**: 2+ modules, small team, moderate complexity
- **Phase 3**: Complex architecture, tutorials needed, multiple audiences

### Step 2: Initialize Based on Phase

#### Phase 1: Single README.md

1. Create or update root README.md using templates:
   - Reference: `../templates/template-readme.md`
   - Customize for your project
   - Keep under 500 lines

2. Include essential sections:
   - Project title and description
   - Quick start instructions
   - Basic prerequisites
   - Simple usage examples

#### Phase 2: Multiple READMEs

1. Update root README.md using `../templates/template-readme.md`
   - Focus on project overview
   - Link to module documentation
   - Keep under 400 lines

2. Create directory READMEs for each module:
   ```bash
   # For each module directory
   touch module-name/README.md
   ```

3. Directory README structure:
   ```markdown
   # [Module Name]
   Brief description of this module's purpose

   ## Structure
   - [Key file] - [Purpose]
   - [Key file] - [Purpose]

   ## Usage
   [How to use this module]

   ## Related Documentation
   - [Parent Documentation](../README.md)
   ```

#### Phase 3: READMEs + /docs Folder

1. Update root README.md using `../templates/template-readme.md`
   - High-level overview only
   - Link to detailed documentation
   - Keep under 300 lines

2. Create docs directory structure:
   ```bash
   mkdir -p docs/{tutorials,guides,api}
   ```

3. Create documentation files as needed:
   - `docs/getting-started.md` - User tutorials
   - `docs/api-reference.md` - API documentation
   - `docs/architecture.md` - Technical deep dives
   - `docs/contributing.md` - Developer guide

### Step 3: Validate Initialization

```bash
# Check file structure
find . -name "README*" -type f
tree docs/ 2>/dev/null || echo "No docs directory"

# Check line counts
wc -l README.md
find . -name "README.md" -exec wc -l {} + | tail -1
```

### Step 4: Update Project Files

Add documentation references where needed:
- Package.json: "docs" field pointing to documentation
- CI/CD: Add documentation checks if desired
- Git: Ensure .gitignore doesn't exclude documentation

## Success Criteria

- [ ] Documentation structure matches project phase
- [ ] Root README.md exists and is appropriate length
- [ ] Directory READMEs created for Phase 2+
- [ ] /docs folder created for Phase 3
- [ ] All templates customized appropriately
- [ ] Cross-references are correct
- [ ] Documentation is discoverable and navigable

## Next Steps

- Use `update.md` workflow to keep documentation current
- Schedule regular reviews (quarterly recommended)
- Consider adding documentation checks to CI/CD
- Train team on documentation standards