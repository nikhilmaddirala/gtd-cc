---
description: Compress documentation to reduce verbosity while preserving critical information
---

# Compress Documentation

Compress verbose documentation in-place to improve clarity while preserving critical information.

## Additional Parameters

- **level**: Compression intensity
  - `light` (2-3x) - Remove examples and verbose explanations, keep structure
  - `medium` (5-8x) - Remove verbose explanations, keep decisions and critical details
  - `heavy` (10x+) - Keep only essential details, API contracts, thresholds

## Process

### Step 1: Measure Baseline

```bash
wc -l <file>
wc -w <file>
```

### Step 2: Identify Critical Information

```bash
# Find key sections
grep -E "^##? " <file>

# Find decisions and recommendations
grep -E "should|must|always|never" <file>

# Find numbers and constraints
grep -E "[0-9]+" <file>
```

**Always preserve:**
- Definitions of concepts
- Key decisions and rationale
- Numbers, thresholds, constraints
- Caveats, gotchas, limitations
- API contracts and function signatures

**Safe to remove:**
- Verbose explanations
- Repeated information
- Examples (unless essential)
- Marketing language
- Detailed walkthroughs

### Step 3: Choose Format

- Dense bullet points
- Quick reference tables
- API contracts only
- Checklist format

### Step 4: Compress In-Place

Rewrite preserving:
- All terminology exactly (no simplification)
- All numbers and thresholds
- All critical decisions
- Scannable structure

### Step 5: Verify

```bash
wc -l <file>
grep -E "should|must|never" <file>  # Decisions preserved
grep -E "[0-9]+" <file>              # Numbers preserved
```

## Compression Guidelines by Document Type

| Document Type | Level | Target |
|---------------|-------|--------|
| API Reference | medium-heavy | Signatures + critical details |
| Architecture | light-medium | Components + data flow + decisions |
| Configuration | heavy | Table of options, defaults, constraints |
| README | medium | Under 300-500 lines |

## Success Criteria

- Target compression level achieved
- All critical information preserved
- All numbers and decisions included exactly
- Terminology preserved (no substitution)
- Document is scannable
- All cross-references work
