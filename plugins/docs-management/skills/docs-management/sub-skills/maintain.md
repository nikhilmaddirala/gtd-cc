---
description: Fix, update, or audit existing documentation at any scope
---

# Maintain Documentation

Fix, update, or audit existing documentation. Works at any scope.

## Additional Parameters

- **trigger** (optional context):
  - Code change: User specifies what changed
  - Audit: No specific change, scan for all problems
  - Release: Pre-release verification

## Process

### Step 1: Analyze Scope

**scope=doc**
```bash
wc -l <file>
```

**scope=path**
```bash
find <path> -name "*.md" -type f
```

**scope=repo**
```bash
find . -name "*.md" -type f -maxdepth ${depth:-999}
```

### Step 2: Identify Problems

```bash
# Find outdated markers
grep -r "TODO\|FIXME\|XXX" --include="*.md" <scope>

# Find potential broken links
grep -r "\[.*\](" --include="*.md" <scope> | grep -oP '\]\(\K[^)]+'

# Check README lengths (should be <500 lines)
find <scope> -name "README.md" -exec wc -l {} \;

# Find version references that may be outdated
grep -rE "v[0-9]+\.[0-9]+" --include="*.md" <scope>
```

If trigger is a code change:
- Find docs that reference changed files/functions
- Identify examples that may be affected

### Step 3: Categorize Fixes

**Content:** Outdated info, incorrect examples, missing docs for new features

**Structure:** README too long, duplicate info, missing cross-references

**Links:** Broken internal links, outdated external links

**Hygiene:** Unresolved TODOs, inconsistent formatting

### Step 4: Execute Fixes

- Update in authoritative location only (don't duplicate)
- Keep READMEs concise, move details to /docs
- Update cross-references after moving content

**Verify links:**
```bash
for link in $(grep -oP '\]\(\K[^)]+' file.md); do
  test -e "$link" || echo "Broken: $link"
done
```

### Step 5: Verify Fixes

```bash
# Re-run problem detection
grep -r "TODO\|FIXME" --include="*.md" <scope>

# Check lengths
find <scope> -name "README.md" -exec wc -l {} \;
```

## Scope-Specific Guidelines

**scope=doc:** Focus on internal consistency, verify examples are current

**scope=path:** Check consistency across docs, verify cross-references, consolidate duplicates

**scope=repo:** Check documentation coverage, verify three-layer structure is appropriate, identify orphaned docs

## Examples

### Targeted Update After Code Change

```
Trigger: Renamed function getUserData to fetchUserProfile

1. grep -r "getUserData" --include="*.md" .
2. Update each occurrence
3. Verify no orphaned references remain
```

### Full Repository Audit

```
Trigger: Quarterly maintenance
Scope: repo

1. Find all .md files
2. Scan for problems (links, TODOs, lengths)
3. Prioritize: broken links > outdated content > hygiene
4. Fix systematically
5. Verify fixes
```

## Success Criteria

- All identified problems fixed
- No broken links remain
- README lengths within guidelines
- Examples tested and working
- Cross-references verified
