---
name: documentation
description: Implement and maintain GitHub project documentation using a layered system. Use when creating, updating, or auditing documentation.
---

# Documentation Management

## Overview

This skill provides expertise for implementing and maintaining documentation in GitHub projects. Use when you need to create documentation structure, fix/update existing docs, or audit documentation health.


## Context

User wants to work with project documentation. They may:
- Set up documentation for a new project or module
- Fix or update existing documentation after code changes
- Audit and repair documentation across a repository

All sub-skills accept a scope parameter to control how much of the project to work on.


## Sub-skills

CRITICAL: Load the appropriate sub-skill from `sub-skills/` based on user intent.

- **initialize.md**: Create documentation structure where none exists
- **maintain.md**: Fix, update, or audit existing documentation
- **compress.md**: Remediate legacy verbose documentation (should rarely be needed for new docs)

### Scope Parameter

| Scope | Description | Example |
|-------|-------------|---------|
| `repo` | Entire repository | "Fix all docs in this repo" |
| `path=<dir>` | Specific directory | "Fix docs in src/components/" |
| `doc=<file>` | Single document | "Fix this README.md" |
| `depth=N` | Limit recursion | "Repo, 2 levels deep" |


## Process

1. Determine user intent (create, maintain, or compress)
2. Determine scope (repo, path, or doc)
3. Load appropriate sub-skill
4. Follow sub-skill process with scope context
5. Verification: Confirm documentation meets success criteria (no duplication, appropriate length, links work)


## Resources

- **resources/templates/**: Templates for README, CONTRIBUTING, and CHANGELOG files


## Guidelines

- CRITICAL: You MUST use the templates provided by this skill

### Core Principles

**One fact, one place.** Never duplicate information across layers. If something is documented in literate code comments, don't repeat it in the directory README. If it's in a directory README, don't repeat it in the root README. Link instead.

**Conciseness first.** Write tight documentation from the start. If you find yourself needing to compress docs, that's a sign of upstream problems. The compress sub-skill exists for legacy cleanup, not as a normal workflow.

**Document why, not what.** Code shows what happens. Documentation should explain why decisions were made, how pieces connect, and what's not obvious from reading the code.

### Anti-patterns to Avoid

- Same information in root README + directory README + code comments
- README that restates what the code already shows
- Documentation that requires regular "compression" passes
- Directory READMEs that just list files (the filesystem already does that)
- Verbose explanations when a link would suffice

### Literate Code Comments

For small directories (1-2 files), well-written literate code comments may be sufficient. Skip the README if:
- Files have proper literate headers (Title, Context, Decision)
- The directory purpose is obvious from filenames
- No complex interactions between files need explaining

A README adds value when:
- Multiple files interact in non-obvious ways
- External interface needs explanation beyond code
- Directory contains subdirectories needing navigation

### Layer Responsibilities

| Layer | Purpose | Audience |
|-------|---------|----------|
| Root README | Project overview, quick start, entry point | Everyone |
| Directory README | How files in this directory relate, local context | Developers working in this area |
| /docs folder | Cross-cutting topics that span multiple parts of the codebase | Those needing comprehensive understanding |
| Literate comments | Why this code exists, decision rationale | Future maintainers |

Each layer answers different questions. If you're repeating yourself, you're in the wrong layer.

### READMEs vs docs/ folder

READMEs and docs/ serve fundamentally different purposes:

- **READMEs are vertical** - They document a specific location (root project, a module, a directory). Each README belongs to exactly one place in the filesystem.

- **docs/ is horizontal** - It documents topics that span multiple parts of the codebase. Architecture, authentication flows, data pipelines - these have no natural home in any single directory because they cross boundaries.

**When to use each:**

| Content | Location | Why |
|---------|----------|-----|
| "How this module works" | Directory README | Specific to one location |
| "How auth, API, and DB interact" | docs/architecture.md | Spans multiple modules |
| "Quick start for users" | Root README | Entry point for everyone |
| "Complete API reference" | docs/api-reference.md | Reference material, not entry point |
| "Tutorial: building a feature" | docs/tutorials/ | Step-by-step guide touching many areas |

**Cross-references:**

- READMEs link to docs/ for cross-cutting topics: "See [Architecture](docs/architecture.md) for how this module fits into the system"
- docs/ links to READMEs for module-specific details: "For implementation details, see [src/auth/README.md](../src/auth/README.md)"
- docs/index.md serves as navigation hub, linking to both other docs/ files and relevant READMEs


## Appendix

### Documentation Phases

| Phase | Structure | When to Use |
|-------|-----------|-------------|
| 1 | Single README.md | Simple projects, few files |
| 2 | Multiple READMEs | 2+ modules with distinct purposes |
| 3 | READMEs + /docs | Complex architecture, multiple audiences |

### Section-to-file graduation

Some documentation components start as sections within README and graduate to standalone files as the project grows. This avoids over-engineering docs for small projects while providing a clear upgrade path.

| Component | Phase 1 (inline) | Phase 2+ (standalone) |
|-----------|-------------------|----------------------|
| Contributing | Section in README under Developer Guide | CONTRIBUTING.md |
| Changelog | Section in README under Roadmap | CHANGELOG.md |

Graduation triggers:
- The section grows beyond ~30 lines
- Multiple contributors need to reference it independently
- The project is being published or has external users

### Length Guidelines

| Document | Target | Max |
|----------|--------|-----|
| Root README | 200-300 lines | 500 lines |
| Directory README | 200-300 lines | 500 lines |
| /docs files | As needed | Keep focused |

If a document exceeds these limits, it's probably:
- Duplicating information from another layer
- Covering too many topics (split it)
- Too verbose (tighten the prose)

### Success Criteria

- No information duplicated across layers
- Each document serves a clear, distinct purpose
- READMEs are concise entry points, not exhaustive references
- READMEs follow templates provided
- Small directories rely on literate comments when appropriate
- All links work, no orphaned references
