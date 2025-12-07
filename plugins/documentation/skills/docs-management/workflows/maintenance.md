---
description: Implement and maintain documentation health over time
---

## Maintenance Workflow

Keep documentation fresh through PR-based updates and scheduled reviews.
For implementation details, use the update.md workflow with scope=all, type=minor parameters.

## Core Workflows

### 1. PR-Based Maintenance

Add to pull request template:
```markdown
## Documentation
- [ ] Updated README.md if behavior changed
- [ ] Updated CONTRIBUTING.md if contribution processes changed
- [ ] Updated relevant /docs files if structure changed
- [ ] Removed outdated information (don't patch around it)
- [ ] Added cross-references instead of duplicating content
- [ ] Verified all links work
- [ ] Tested Quick Start if commands changed
```

### 2. Scheduled Maintenance

**Release Checklist:**
- [ ] README.md version matches code
- [ ] CONTRIBUTING.md reflects current development processes
- [ ] Getting Started tested end-to-end
- [ ] Configuration documentation current
- [ ] Breaking changes documented
- [ ] Examples work with new code

**Quarterly Review:**
```bash
# Find stale docs (not modified in 3+ months)
find . -name "*.md" -not -path "./node_modules/*" -not -path "./.git/*" -mtime +90 -type f
```

- [ ] Delete stale/obsolete pages
- [ ] Update diagrams to match architecture
- [ ] Trim README to essentials
- [ ] Fix broken cross-references
- [ ] Remove duplicate content
- [ ] Add missing feature documentation

### 3. Common Tasks

**Adding features:** Update appropriate layer (README for quick, /docs for complex), verify no duplication

**Removing features:** Find and delete all references, update README/API docs

**Reorganizing structure:** Update directory READMEs, diagrams, and architecture docs

### 4. Quality Checks

**Verification commands:**
```bash
# Check README size
test $(wc -l < README.md) -gt 500 && echo "README too long"

# Find unresolved items
grep -r "TODO\|FIXME\|XXX" docs/ --include="*.md" && echo "Found unresolved items"

# Check for broken links
grep -r "\[.*\](" . --include="*.md" | grep -oP '\]\(\K[^)]+' | sort | uniq
```

**Documentation Principles:**
- Document as you code
- One fact, one place (link, don't duplicate)
- Remove outdated content (don't comment out)
- Layer by audience (README for quick facts, /docs for details)
- Verify links and examples work

**Audit Checklist:**
- [ ] README <500 lines and clear entry point
- [ ] No broken links or unresolved markers
- [ ] No duplicate content across layers
- [ ] Version numbers match code
- [ ] Code examples work
- [ ] All public APIs documented

## Success Criteria

- ✅ Every behavior-changing PR updates documentation
- ✅ Links verified before merge
- ✅ Outdated information removed
- ✅ Getting Started works end-to-end
- ✅ Quarterly reviews completed
- ✅ No duplicate information across layers