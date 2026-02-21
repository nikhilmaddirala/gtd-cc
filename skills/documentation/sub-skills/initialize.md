---
description: Create documentation structure where none exists
---

# Initialize Documentation

Set up documentation structure for a project or directory that lacks documentation.

## Additional Parameters

- **phase** (for scope=repo):
  - `1` - Single README.md (solo developer, simple projects)
  - `2` - Multiple READMEs (2+ modules, multiple contributors)
  - `3` - READMEs + /docs folder (complex architecture, tutorials needed)
  - `auto` - Determine phase based on project analysis (default)

## Process

### Step 1: Analyze Project Structure

**scope=repo**
```bash
find . -type f -name "*.md" | head -20
find . -type d -maxdepth ${depth:-2} | head -30
ls -la
```

**scope=path**
```bash
ls -la <path>
find <path> -type f | head -20
```

**scope=doc**
```bash
ls -la $(dirname <file>)
```

### Step 2: Determine Phase (scope=repo only)

If phase=auto, determine based on analysis:

| Indicator | Phase |
|-----------|-------|
| < 5 files, single module | 1 |
| 2+ modules, moderate complexity | 2 |
| Complex architecture, tutorials needed | 3 |

### Step 3: Create Documentation Structure

#### phase=1: Single README

Create root README.md using `resources/templates/README.md`:
- Project title and description
- Quick start instructions
- Basic prerequisites
- Simple usage examples
- Contributing as inline section (under Developer Guide)
- Changelog as inline section (under Roadmap)
- Target: Under 500 lines

#### phase=2: Multiple READMEs

1. Create root README.md (overview, links to modules, under 400 lines)
2. Graduate contributing and changelog to standalone files:
   - CONTRIBUTING.md using `resources/templates/CONTRIBUTING.md`
   - CHANGELOG.md using `resources/templates/CHANGELOG.md`
   - Remove inline sections from README, replace with links

3. Create directory README for each module:
```markdown
# [Module Name]

Brief description of this module's purpose.

## Structure

- [Key file] - [Purpose]

## Usage

[How to use this module]

## Related

- [Parent Documentation](../README.md)
```

#### phase=3: READMEs + /docs

1. Create root README.md (high-level only, under 300 lines)
2. Create module READMEs (as in phase 2)
3. Standalone CONTRIBUTING.md and CHANGELOG.md (as in phase 2)
4. Create docs/ for cross-cutting topics:
   - `docs/getting-started.md` - Tutorials touching multiple modules
   - `docs/api-reference.md` - API documentation (reference material)
   - `docs/architecture.md` - How modules interact (cross-cutting)

#### scope=path: Module README

Create README.md for the specific directory with Structure, Usage, and Related sections.

#### scope=doc: Specific Document

Create the specified document using appropriate template.

### Step 4: Validate Structure

```bash
find . -name "README*" -type f
wc -l README.md
```

## Success Criteria

- Documentation structure matches project complexity
- Root README.md exists and is appropriate length
- Directory READMEs created for Phase 2+
- /docs folder created for Phase 3
- Phase 1: Contributing and changelog are inline README sections
- Phase 2+: CONTRIBUTING.md and CHANGELOG.md exist as standalone files
- All templates customized (no placeholder text)
- Cross-references are correct
