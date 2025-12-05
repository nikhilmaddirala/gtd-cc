---
name: docs-management
description: GitHub project documentation implementation and maintenance skill using three-layer scalable documentation system
---

# Documentation Standards Skill

## Overview

This skill provides expertise for implementing and maintaining documentation in GitHub projects using a three-layer model that scales with project complexity. This skill should be used when users need to create, edit, or refactor any documentation, or establish documentation practices for their projects.

## Workflows

Use the appropriate workflow from the `workflows/` directory:

### Main Workflows
- **initialize.md** (phase: 1|2|3): For setting up documentation structure based on project complexity
  - Phase 1: Single README.md for solo developers
  - Phase 2: Multiple READMEs for projects with 2+ modules
  - Phase 3: READMEs + /docs folder for complex projects

- **update.md** (scope: single|multiple, type: minor|refactor): For updating documentation
  - scope=single: Update individual documents
  - scope=multiple: Update across documentation layers
  - type=minor: Update references and key information
  - type=refactor: Restructure and reorganize content
  - Note: Maintenance tasks use scope=all, type=minor

- **compress.md**: Standalone workflow for reducing document bloat while preserving critical information

### Shared Components
- **shared/folder-exploration.md**: Component used by workflows to analyze folder structure and understand code-documentation relationships

## Resources

- **resources/**: Contains templates and reference materials
- **workflows/**: Contains detailed procedures for documentation tasks

## Guidelines

Follow these general guidelines when executing any workflow in this skill:

- Use templates where available
- **Low documentation overhead**: Don't document the obvious - focus on what's not clear from code itself
- **One fact, one place**: Link to information rather than duplicating it across documentation layers
- **Layer by audience**: Structure documentation with README for everyone, directory READMEs for maintainers, and /docs for deep dives
- **Maintain length guidelines**: Keep READMEs concise (200-500 lines) to maintain readability

## Additional Information

This section contains domain-specific information for the documentation standards skill:

### Three-Layer Philosophy

Documentation scales using three phases based on project complexity:
- **Phase 1**: Single README.md for solo developers and simple projects
- **Phase 2**: Multiple READMEs when projects have 2+ modules and multiple contributors
- **Phase 3**: READMEs + /docs folder for complex architecture requiring tutorials and detailed guides

### Key Architecture Patterns

**Documentation Structure:**
```
./README.md - Project entry point (200-500 lines)
./some-dir/README.md - Component entry points (100-300 lines)
./docs/some-doc.md - Deep dive content for complex projects
```


### Success Criteria

- README serves as clear entry point without being overwhelming
- Directory READMEs explain local context and organization
- No information is duplicated across documentation layers
- Documentation updates are tied to code changes
- Quarterly reviews keep documentation fresh and accurate
- All links work correctly with no dead references
- Avoid README bloat (everything in one file)
- Avoid outdated information left in place
- Avoid links to non-existent files
- Avoid directory documentation that doesn't explain purpose
- Avoid "will document later" mentality (document as you code)
