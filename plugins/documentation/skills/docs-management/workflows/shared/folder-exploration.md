---
description: Shared component for exploring folder structure and understanding code-documentation relationships using structured subagent delegation
---

# Folder Exploration Component

Shared component used by documentation workflows to analyze project structure and return data for updating documentation. This component gathers data through subagent delegation and returns structured findings for making targeted documentation updates.

## Purpose

This component provides a systematic approach to:
- Gather project structure data through parallel subagent analysis
- Identify existing documentation patterns and locations
- Analyze code-documentation relationships
- Return structured context for documentation updates
- Enable targeted updates to existing README files

## When to Use

This component is referenced by other workflows when they need to:
- Assess the current state of documentation for updates
- Identify which specific documents need updating
- Understand project complexity for phase determination
- Map code changes to documentation requirements
- Gather data before making documentation updates

## Process

### Phase 1: Primary Parallel Analysis

Launch three subagents in parallel to gather comprehensive project data:

#### Subagent 1: Root Structure Analyzer
```markdown
Task: Analyze the top-level directory structure and return data
- List all files and directories in the project root
- Identify configuration files, build files, and special directories
- Count immediate subdirectories
- Note any unusual patterns or naming conventions
- Return: Structured data with file paths and descriptions
```

#### Subagent 2: Documentation Locator
```markdown
Task: Find all documentation files and return locations
- Search for all README files (case insensitive)
- Find all markdown files (*.md, *.MD)
- Locate docs directories and their contents
- Identify other documentation formats (rst, txt, etc.)
- Return: Complete inventory data with file paths and locations
```

#### Subagent 3: Module Mapper
```markdown
Task: Map code modules to their documentation status
- Examine each top-level directory
- Check for README files in each module
- Identify main code files and their purposes
- Note any module-specific documentation
- Return: Matrix data of modules vs documentation coverage
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
- Check for outdated references or unresolved items
- Identify complex code lacking explanation
- Note configuration files without documentation
- Output: Prioritized list of documentation needs
```

### Phase 4: Return Structured Context

Compile all subagent results into structured data for documentation updates:

1. **Phase Determination Data**:
   - **Phase 1**: Single README.md, simple structure (<5 modules)
   - **Phase 2**: Multiple READMEs, 2+ modules, moderate complexity
   - **Phase 3**: READMEs + docs folder, complex architecture

2. **Documentation Coverage Data**:
   - Percentage of modules with documentation
   - List of missing documentation files
   - Locations of outdated or incomplete sections

3. **Update Targets Data**:
   - Specific files that need updating
   - Types of updates required (version, links, content)
   - Priority levels for each update

## Return Format

The component returns structured data for making documentation updates:

```
Project Structure Data:
- Phase: 1|2|3
- Total directories: N
- Total files: N
- Documentation coverage: N%

Documentation Files Data:
- Root README: path/to/README.md (exists/missing)
- Module READMEs: [list of paths and status]
- Docs folder: path/to/docs/ (exists/missing)
- Other docs: [list of paths]

Update Targets Data:
- Files needing updates: [file paths]
- Update types: [version|links|content|structure]
- Priority order: [high|medium|low]

Gap Analysis Data:
- Missing documentation: [locations]
- Outdated information: [file paths and sections]
- Coverage gaps: [specific areas needing attention]
```

## Subagent Task Templates

When implementing this component, use these task templates:

```markdown
# Root Structure Analyzer Task
Analyze the project root directory structure and return data. Use Glob and Read tools to:
1. List all files in root with full paths
2. Identify file types and purposes
3. Determine project type and technology stack
4. Note special patterns (monorepo, multi-module, etc.)
5. Return structured data with file paths and descriptions

# Documentation Locator Task
Find all documentation files and return location data. Use Glob and Grep tools to:
1. Find all README files with full paths
2. Locate all markdown files with paths
3. Find docs directories and list contents
4. Identify other documentation formats
5. Return complete inventory data with file paths

# Module Mapper Task
Map module documentation status and return coverage data. Use Read and Glob tools to:
1. Examine each top-level directory
2. Check for module READMEs and note their paths
3. Identify main code files and their purposes
4. Create matrix data of modules vs documentation coverage
5. Return structured mapping data

# Deep Directory Analyzer Task (conditional)
Perform recursive analysis and return structure data. Use Task tool to:
1. For each large directory, analyze subdirectory structure
2. Map subdirectory relationships and dependencies
3. Identify nested documentation patterns
4. Return hierarchical structure data with documentation gaps

# Gap Analyzer Task (conditional)
Identify documentation gaps and return needs data. Use Grep and Read tools to:
1. Search for incomplete documentation or unresolved items
2. Find complex code without explanations
3. Identify configuration files lacking documentation
4. Cross-reference with code changes for outdated docs
5. Return prioritized data of documentation needs
```

## Performance Considerations

- **Small Projects** (<10 directories): Use primary subagents only
- **Medium Projects** (10-50 directories): Add selective secondary analysis
- **Large Projects** (>50 directories): Full two-level recursion with all subagents
- **Timeout Handling**: Each subagent has independent timeout to prevent blocking

## Integration

Workflows reference this component using:
> "Use the shared folder-exploration component to analyze project structure and identify documentation requirements"

The component returns structured data for making targeted documentation updates without creating separate report files.