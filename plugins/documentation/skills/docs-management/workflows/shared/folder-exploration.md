---
description: Shared component for exploring folder structure and understanding code-documentation relationships using structured subagent delegation
---

# Folder Exploration Component

Shared component used by documentation workflows to analyze project structure, identify documentation locations, and understand the relationship between code and documentation through structured subagent delegation.

## Purpose

This component provides a systematic approach to:
- Understanding current folder structure through parallel analysis
- Identifying existing documentation patterns efficiently
- Analyzing code-documentation relationships with scalable recursion
- Determining appropriate documentation updates based on comprehensive findings

## When to Use

This component is referenced by other workflows when they need to:
- Assess the current state of documentation
- Identify which documents need updating
- Understand project complexity for phase determination
- Map code changes to documentation requirements
- Handle large projects with scalable analysis

## Process

### Phase 1: Primary Parallel Analysis

Launch three subagents in parallel to gather comprehensive project data:

#### Subagent 1: Root Structure Analyzer
```markdown
Task: Analyze the top-level directory structure
- List all files and directories in the project root
- Identify configuration files, build files, and special directories
- Count immediate subdirectories
- Note any unusual patterns or naming conventions
- Output: Structured list of root contents with descriptions
```

#### Subagent 2: Documentation Locator
```markdown
Task: Find all documentation files and patterns
- Search for all README files (case insensitive)
- Find all markdown files (*.md, *.MD)
- Locate docs directories and their contents
- Identify other documentation formats (rst, txt, etc.)
- Output: Complete inventory of documentation with locations
```

#### Subagent 3: Module Mapper
```markdown
Task: Map code modules to their documentation status
- Examine each top-level directory
- Check for README files in each module
- Identify main code files and their purposes
- Note any module-specific documentation
- Output: Matrix of modules vs documentation coverage
```

### Phase 2: Checkpoint Analysis

Aggregate results from primary subagents and evaluate:

1. **Project Size Assessment**:
   - Total directories: <10 (small), 10-50 (medium), >50 (large)
   - Total files: <100 (small), 100-1000 (medium), >1000 (large)
   - Documentation files: ratio to code files

2. **Complexity Indicators**:
   - Multiple programming languages
   - Complex directory nesting
   - Mixed project types (frontend, backend, tools)
   - Large subdirectories requiring deeper analysis

3. **Recursion Decision**:
   - Launch secondary subagents if:
     - Any directory has >10 immediate subdirectories
     - Any directory has >50 files total
     - Mixed code patterns require separate analysis

### Phase 3: Secondary Deep Analysis (Conditional)

If checkpoint indicates need for deeper analysis:

#### Subagent 4: Deep Directory Analyzer
```markdown
Task: Perform two-level recursive analysis
- For each large directory identified:
  - Analyze immediate subdirectories
  - Identify code organization patterns
  - Look for nested documentation
  - Map dependencies between subdirectories
- Output: Hierarchical structure with documentation gaps
```

#### Subagent 5: Gap Analyzer
```markdown
Task: Identify specific documentation gaps and needs
- Cross-reference code with missing documentation
- Check for outdated references or TODOs
- Identify complex code lacking explanation
- Note configuration files without documentation
- Output: Prioritized list of documentation needs
```

### Phase 4: Synthesize Findings

Compile all subagent results into a structured report:

1. **Phase Determination**:
   - **Phase 1**: Single README.md, simple structure (<5 modules)
   - **Phase 2**: Multiple READMEs, 2+ modules, moderate complexity
   - **Phase 3**: READMEs + docs folder, complex architecture

2. **Documentation Coverage Score**:
   - Calculate percentage of modules with documentation
   - Identify critical missing documentation
   - Note outdated or incomplete sections

3. **Recommendations**:
   - Immediate documentation needs
   - Structural improvements
   - Maintenance requirements

## Output Format

The component provides structured output that other workflows can use:

```markdown
## Project Structure Analysis

### Overview
- **Phase**: 1|2|3
- **Total Directories**: N
- **Total Files**: N
- **Documentation Coverage**: N%

### Documentation Inventory
- **Root README**: ✓/✗
- **Module READMEs**: N found, N missing
- **Docs Folder**: ✓/✗ (if present)
- **Other Documentation**: List

### Module Analysis
| Module | README | Docs | Status |
|--------|--------|-------|--------|
| module1 | ✓ | ✗ | Basic coverage |
| module2 | ✗ | ✓ | Needs module README |
| ... | ... | ... | ... |

### Critical Gaps
1. Missing documentation for [module/function]
2. Outdated information in [file]
3. Complex code in [location] needs explanation

### Recommendations
- [Priority 1] Create README for [module]
- [Priority 2] Update [section] in existing docs
- [Priority 3] Add API documentation for [component]
```

## Subagent Task Templates

When implementing this component, use these task templates:

```markdown
# Root Structure Analyzer Task
Analyze the project root directory structure. Use Glob and Read tools to:
1. List all files in root (ls -la equivalent)
2. Describe each file/directory's purpose
3. Identify project type and technology stack
4. Note any special patterns (monorepo, multi-module, etc.)

# Documentation Locator Task
Comprehensive documentation search. Use Glob and Grep tools to:
1. Find all README files (including case variations)
2. Locate all markdown files
3. Find docs directories and their contents
4. Identify API docs, guides, or other documentation formats

# Module Mapper Task
Map each module's documentation status. Use Read and Glob tools to:
1. Examine each top-level directory
2. Check for module READMEs
3. Identify main code files and their purposes
4. Create a matrix of modules vs documentation coverage

# Deep Directory Analyzer Task (conditional)
Two-level recursive analysis for large directories. Use Task tool to:
1. For each large directory, spawn a subagent to analyze its structure
2. Map subdirectory relationships
3. Identify nested documentation patterns
4. Report on organizational complexity

# Gap Analyzer Task (conditional)
Identify specific documentation needs. Use Grep and Read tools to:
1. Search for TODO, FIXME, or documentation markers
2. Find complex functions without comments
3. Identify configuration files without explanation
4. Cross-reference with code changes to find outdated docs
```

## Performance Considerations

- **Small Projects** (<10 directories): Use primary subagents only
- **Medium Projects** (10-50 directories): Add selective secondary analysis
- **Large Projects** (>50 directories): Full two-level recursion with all subagents
- **Timeout Handling**: Each subagent has independent timeout to prevent blocking

## Integration

Workflows reference this component using:
> "Use the shared folder-exploration component to analyze project structure and identify documentation requirements"

The component maintains backward compatibility while providing enhanced analysis through subagent delegation.