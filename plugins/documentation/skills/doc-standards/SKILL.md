---
name: doc-standards
description: GitHub project documentation implementation and maintenance based on three-layer model with Best README Template patterns
---

# Documentation Standards Skill

Comprehensive documentation guidance for GitHub projects using a scalable three-layer model that grows naturally with project complexity.

## About This Skill

This skill implements a unified, lightweight, and scalable documentation system based on the Best README Template approach. It provides guidance for structuring, evolving, and maintaining repository documentation across projects of all sizes while keeping maintenance overhead minimal.

The skill covers:

- The purpose of each documentation layer
- How documentation evolves as projects grow
- Folder and file structure conventions
- Maintenance rules for long-term health
- Templates and checklists for consistency

## Core Documentation Philosophy

Documentation should scale naturally with project complexity using three layers:

```
README.md          → Entry point (primary door)
CONTRIBUTING.md    → Contributor guidance (evolves with project)
Directory READMEs  → Local context (module explanations)
/docs/             → Deep dives (multi-page content)
```

This three-layer model prevents:

- README bloat from too much detail
- Scattered context across files
- Confusion about where documentation lives
- Unnecessary duplication

**Core Documentation Files:** README.md and CONTRIBUTING.md are the foundational documentation files that define project understanding and contribution pathways for all users and collaborators.

## Key Principles

1. The README is the front door - keep it simple and user-focused
2. CONTRIBUTING.md guides contributor onboarding and evolves with project complexity
3. Directory docs localize complexity to relevant modules
4. Deep docs in /docs handle multi-page explanations
5. Each fact lives in only one place - no duplication
6. Documentation grows downward as needed - start minimal
7. Maintenance is continuous, not occasional - tie doc updates to PRs
8. Version documentation as the project evolves
9. Documentation rot is prevented through quarterly reviews

## Documentation Lifecycle: Three Phases

Choose your documentation approach based on project stage (this should be explicitly called out in the root README):

Single README
- Single README.md
- Solo developer or simple scripts
- Early MVP stage

Multiple READMEs
- README.md + directory READMEs
- 2+ modules with separate concerns
- Contributors need local context

READMEs + docs (rarely use)
- README.md + directory READMEs + /docs
- Complex architecture or multiple tutorials
- Internal and external documentation needs

## Documentation Components

### Root README.md

The primary entry point for all users and contributors.

Must include:
- Project title and short description
- Badges (optional)
- Table of contents (if long)
- About / Motivation section
- Built with / Tech stack
- Getting started (install, usage)
- Roadmap (optional)
- Contributing, License, Contact sections

Guidelines:
- Keep it clear, short, and actionable
- User-focused, not internal-focused
- Link to deeper docs in /docs rather than including them
- Update on every PR that changes behavior

### CONTRIBUTING.md

Core contributor guidance document that evolves with project complexity.

Purpose:
- Defines contribution pathways and expectations
- Scales from simple section to comprehensive guide
- Prevents contributor confusion and fragmentation

Evolution:
- **Phase 1**: Section within README.md for simple projects
- **Phase 2**: Maintained in main README with module-specific guidance in directory READMEs
- **Phase 3**: Dedicated file or /docs/guides/contributing.md with comprehensive processes

Guidelines:
- Keep instructions actionable and clear
- Include development setup, testing, and PR processes
- Reference current project standards and tools
- Update when workflows or requirements change

### Directory READMEs

Add a README inside any directory where context is needed.

Each directory README should answer:
- What lives in this folder?
- How is it organized?
- How to extend or modify this component?
- Any conventions, constraints, or common pitfalls?
- Cross-references to related documentation

Guidelines:
- Keep them short and focused
- Avoid duplication with root README or /docs
- Update when structure or purpose changes

### /docs Folder

Holds documentation that is too large or detailed for the main README.

Use /docs for:
- Architecture diagrams and design decisions
- Configuration reference
- API reference
- Tutorials and walkthroughs
- Contribution guidelines
- Design notes and rationale
- Versioning information (optional)
- Troubleshooting guides

Typical /docs structure:
```
/docs
  index.md
  architecture.md
  configuration.md
  api_reference.md
  tutorials/
    getting-started.md
    advanced-usage.md
  diagrams/
    architecture.excalidraw
  guides/
    contributing.md
    troubleshooting.md
```

### CONTRIBUTING.md Evolution

Contribution guidelines evolve with your project documentation:

#### Phase 1: Single README
- Include "Contributing" section in main README.md
- Cover basic guidelines: issue reporting, PR process, code style
- Keep it concise and focused on immediate contributor needs

#### Phase 2: Multiple READMEs
- Maintain Contributing section in main README.md
- Add module-specific contribution guidance in directory READMEs
- Reference main contributing guidelines from directory docs

#### Phase 3: READMEs + docs
- Move detailed contributing guidelines to `/docs/guides/contributing.md`
- Keep brief "Contributing" section in main README with link to detailed guide
- Include comprehensive development setup, testing, and review processes
- Add contribution templates and examples in `/docs/guides/`

This evolutionary approach prevents contribution guideline fragmentation while scaling guidance appropriately with project complexity.

## Maintenance Framework

Documentation stays healthy when maintained systematically:

### On Every PR

- [ ] Update relevant docs (README, folder docs, or /docs)
- [ ] Remove outdated content instead of patching around it
- [ ] Link instead of duplicating information
- [ ] Ensure examples still work with the changes

### Release Checklist

- [ ] README matches current behavior
- [ ] Configuration table or reference up to date
- [ ] Important changes reflected in architecture or API docs
- [ ] New features documented in appropriate layer
- [ ] Breaking changes clearly noted

### Quarterly Sweep

- [ ] Delete stale or obsolete pages
- [ ] Update diagrams to match current architecture
- [ ] Trim README back to essentials
- [ ] Ensure directory READMEs reflect real structure
- [ ] Fix broken cross-references
- [ ] Update version numbers and dates

## Documentation Length Guidelines

Target lengths for different document types to guide compression and identify bloat:

### README.md

- **Target:** 200-500 lines
- **Purpose:** Entry point, quick start, links to deeper docs
- **Triggers Phase 2→3 transition:** If >500 lines, content belongs in /docs
- **Compress if:** >400 lines by moving sections to /docs

### Directory READMEs

- **Target:** 100 - 300 lines
- **Purpose:** Local context, structure explanation, how to extend
- **Too long if:** >100 lines (over-documenting local context)
- **Compress if:** Explanations can be shortened or moved to parent /docs

These targets are guidelines, not hard limits. Compress when:
- Document exceeds its type's upper limit
- Team needs quick-reference version
- Original will remain as detailed version

## Structuring Your Documentation

Follow these principles when organizing documentation across layers:

### Basic Structure Rules

- **One fact, one place** - Never duplicate information. Link to the authoritative source instead.
- **Layer by audience** - README for everyone, directory READMEs for module maintainers, /docs for deep dives
- **README should be short** - If README exceeds 500 lines, move content to /docs
- **Directory READMEs explain local context** - Don't repeat what's in README, add module-specific information
- **Link between layers** - Create clear navigation from README to /docs and between layers

### When to Move Content Between Layers

| Situation | Action |
|-----------|--------|
| Installation in README + /docs | Keep in /docs/tutorials/getting-started.md, link from README |
| Configuration listed in README + /docs | Keep in /docs/configuration.md, link from README |
| Architecture explained in README | Move to /docs/architecture.md, reference from README |
| Large README (>400 lines) | Move sections to /docs, keep summary in README |
| Directory structure explained in README | Move to relevant directory README.md |

### Adding Directory READMEs

Create a README.md in any directory where context is needed:

- Explain what the directory contains
- Show the structure/organization
- Describe how to extend it
- Link to related documentation

Standard directory README structure:

```markdown
# [Folder Name]

Brief description of what this folder contains.

## Structure

- Item A — description
- Item B — description

## How to Extend

[Instructions for adding new content]

## Related Documentation

- [Architecture](../../docs/architecture.md)
- [API Reference](../../docs/api-reference.md)
```

## Workflows in This Skill

This skill includes detailed workflows for:

- **initialization.md** - Initialize documentation structure and choose your phase
- **update-docs.md** - Update documentation when code changes or before releases
- **maintenance.md** - Implement systematic maintenance and audit documentation health
- **compress.md** - Create information-dense condensed versions of documentation for quick reference

## Success Criteria

A well-maintained documentation system:

- README is the clear entry point, not overwhelming
- CONTRIBUTING.md provides clear contributor guidance appropriate to project complexity
- Directory READMEs make local context obvious
- /docs is organized and cross-referenced
- No information duplicated across layers
- Updates are tied to code changes
- Quarterly reviews keep docs fresh
- New contributors can navigate easily
- Links work correctly (no dead references)

## Integration Points

This skill works with:

- GitHub workflow plugin - Documentation updates on PRs
- Knowledge management systems - Obsidian integration possible
- Project planning - Documentation as part of definition of done

## Quick Reference

### When to Create Each Layer

| Situation | Action |
|-----------|--------|
| Solo developer, simple project | README.md only |
| 2+ modules, multiple contributors | Add directory READMEs |
| Architecture needs explanation | Add /docs folder |
| Tutorial content needed | Create /docs/tutorials |
| Configuration reference needed | Add /docs/configuration.md |
| Architecture diagram needed | Add /docs/diagrams |

### Naming Conventions

- README.md - Standard name for visibility
- Docs filenames reflect goals - configuration.md, api_reference.md, getting-started.md
- Directory names are descriptive and consistent
- Use kebab-case for multi-word filenames
- Organize by user goals, not internal structure

### Common Anti-Patterns to Avoid

- README bloat (everything in one file)
- Duplication across README, folder docs, and /docs
- Outdated information left in place
- Links to non-existent files
- No table of contents when README is long
- Directory docs that don't explain purpose
- Inconsistent formatting or structure
- "Will document later" (document as you code)

Detailed procedures for each are available in the workflow files within this skill.

## Resources

This skill includes reference materials and examples to help with documentation implementation:

### [Best-README-Template](./resources/best-readme-template.md)

An exact copy of the popular Best-README-Template from https://github.com/othneildrew/Best-README-Template. This is the complete, unmodified template that you can use as a starting point for your own README files.

**This template includes:**
- Professional badges and shields
- Table of contents with collapsible sections
- About the project section with built-with technologies
- Getting started with prerequisites and installation
- Usage examples section
- Roadmap with checklist format
- Contributing guidelines with workflow
- License information
- Contact details
- Acknowledgments section
- Reference-style links for clean markdown

**How to use:**
1. Copy the template content to your project's README.md
2. Replace placeholder content with your project information
3. Update badges, links, and references to point to your repository
4. Remove sections you don't need (keep it minimal!)
5. Follow the three-layer model principles when adapting

This template demonstrates excellent documentation practices and serves as a concrete example of the documentation principles taught in this skill.
