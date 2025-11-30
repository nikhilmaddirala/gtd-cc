---
name: doc-standards
description: GitHub project documentation implementation and maintenance skill. You MUST use this skill whenever you need to create, edit, or refactor any documentation.
---

# Documentation Standards Skill

Three-layer documentation system for GitHub projects that scales with complexity.

## Philosophy

Documentation scales using three layers:

- Phase 1: Single README.md
    - Solo developer, simple scripts, MVP

**Phase 2: Multiple READMEs**
- 2+ modules, separate concerns
- Contributors need local context

**Phase 3: READMEs + docs**
- Complex architecture, multiple tutorials
- Internal/external documentation needs

- ./README.md: Entry point for the project
- ./some-dir/README.md: Entry point for individual components 
- ./docs/some-doc.md: Deep dive documentation, user guides, etc. (only for complex projects)

**Key Principles:**
- Low documentation overhead. Don't write things that are obvious from code. E.g. listing plugins in documents is a bad practice because it creates too much doc overhead.
- Each doc should be concise: 200 - 500 lines max
- One fact, one place (no duplication)
- README is front door (keep simple)
- Documentation grows downward as needed
- Maintenance tied to PRs
- Quarterly reviews prevent rot

## Documentation Lifecycle

Choose based on project stage:


## Documentation Components

### Root README.md
**Target:** 200-500 lines

**Must include:**
- Project title, description, badges (optional)
- Table of contents (if long)
- About/Motivation, Built with/Tech stack
- Getting started (install, usage)
- Roadmap (optional)
- Contributing, License, Contact sections

**Guidelines:**
- User-focused, not internal-focused
- Link to /docs instead of including details
- Update on every PR that changes behavior

### CONTRIBUTING.md
Evolves with project complexity:

**Phase 1:** Section in README.md (basic guidelines)
**Phase 2:** Main README + module-specific guidance in directory READMEs
**Phase 3:** Dedicated file or `/docs/guides/contributing.md` (comprehensive)

### Directory READMEs
**Target:** 100-300 lines

Create where context needed. Answer:
- What lives in this folder?
- How is it organized?
- How to extend/modify?
- Conventions, constraints, pitfalls?
- Cross-references to related docs

### /docs Folder
For content too large/detailed for README:

**Use for:**
- Architecture diagrams, design decisions
- Configuration reference, API reference
- Tutorials, contribution guidelines
- Design notes, versioning, troubleshooting

**Typical structure:**
```
/docs
  index.md
  architecture.md
  configuration.md
  api_reference.md
  tutorials/ (getting-started.md, advanced-usage.md)
  diagrams/ (architecture.excalidraw)
  guides/ (contributing.md, troubleshooting.md)
```

## Maintenance Framework

### On Every PR
- [ ] Update relevant docs
- [ ] Remove outdated content (don't patch around)
- [ ] Link instead of duplicating
- [ ] Ensure examples still work

### Release Checklist
- [ ] README matches current behavior
- [ ] Configuration reference up to date
- [ ] Changes reflected in architecture/API docs
- [ ] New features documented
- [ ] Breaking changes clearly noted

### Quarterly Sweep
- [ ] Delete stale/obsolete pages
- [ ] Update diagrams to match architecture
- [ ] Trim README to essentials
- [ ] Fix broken cross-references
- [ ] Update version numbers

## Length Guidelines

**README.md:** 200-500 lines (compress if >400)
**Directory READMEs:** 100-300 lines (compress if >100)
**/docs files:** Varies by type

Compress when document exceeds target or team needs quick-reference version.

## Structure Rules

**Basic Principles:**
- One fact, one place (link, don't duplicate)
- Layer by audience (README → everyone, directory READMEs → maintainers, /docs → deep dives)
- Keep README short (<500 lines)
- Directory READMEs explain local context only
- Link between layers clearly

**Content Movement:**
| Situation | Action |
|-----------|--------|
| Installation in README + /docs | Keep in /docs/tutorials/getting-started.md |
| Configuration in both | Keep in /docs/configuration.md |
| Architecture in README | Move to /docs/architecture.md |
| Large README (>400 lines) | Move sections to /docs |
| Directory structure in README | Move to directory README.md |

**Directory README Structure:**
```markdown
# [Folder Name]
Brief description

## Structure
- Item A — description
- Item B — description

## How to Extend
[Instructions]

## Related Documentation
- [Architecture](../../docs/architecture.md)
```

## Workflows

- **initialization.md** - Initialize structure and choose phase
- **update-docs.md** - Update docs when code changes
- **maintenance.md** - Systematic maintenance and health audits
- **compress.md** - Create condensed versions for quick reference

## Success Criteria

- README is clear entry point (not overwhelming)
- CONTRIBUTING.md provides appropriate guidance
- Directory READMEs explain local context
- /docs is organized and cross-referenced
- No information duplicated across layers
- Updates tied to code changes
- Quarterly reviews keep docs fresh
- Links work correctly (no dead references)

## Integration Points

- GitHub workflow plugin - Documentation updates on PRs
- Knowledge management systems - Obsidian integration
- Project planning - Documentation as definition of done

## Quick Reference

**When to Create Each Layer:**
| Situation | Action |
|-----------|--------|
| Solo developer, simple project | README.md only |
| 2+ modules, multiple contributors | Add directory READMEs |
| Architecture needs explanation | Add /docs folder |
| Tutorial content needed | Create /docs/tutorials |
| Configuration reference needed | Add /docs/configuration.md |
| Architecture diagram needed | Add /docs/diagrams |

**Naming Conventions:**
- README.md - Standard name for visibility
- Docs filenames reflect goals (configuration.md, api_reference.md)
- Use kebab-case for multi-word filenames
- Organize by user goals, not internal structure

**Anti-Patterns to Avoid:**
- README bloat (everything in one file)
- Duplication across layers
- Outdated information left in place
- Links to non-existent files
- Directory docs that don't explain purpose
- "Will document later" (document as you code)

## Resources

**[Best-README-Template](./resources/best-readme-template.md)**
Complete template from https://github.com/othneildrew/Best-README-Template with professional badges, structured sections, and reference-style links. Use as starting point, then follow three-layer model principles.
