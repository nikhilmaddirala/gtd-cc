---
name: gh-plan
description: GitHub workflow automation skill for implementation planning and research.
---

# GitHub Plan Skill

This skill provides comprehensive guidance for GitHub planning workflows including implementation planning and codebase research. It serves as the authoritative source for all GitHub planning operations.

## About This Skill

The GitHub Plan skill is designed to facilitate structured planning workflows. It encompasses codebase research, developing implementation plans through analysis and options evaluation, creating technical approaches and development strategies, and documenting acceptance criteria and implementation requirements. This skill consolidates procedural knowledge, best practices, and detailed workflow instructions used across interactive commands and autonomous agents.

### When to Use This Skill

This skill should be used when:
- Researching codebase to understand existing patterns and architecture
- Developing implementation plans through analysis and options evaluation
- Creating technical approaches and development strategies
- Documenting acceptance criteria and implementation requirements

## Available Workflows

This skill provides detailed guidance for the following workflows:

- **Plan** - Develop focused implementation plans through codebase research, options analysis, and technical approach definition

## Individual Workflow Guides

Each workflow provides detailed procedural instructions in its respective markdown file:

### Plan
**File**: `workflows/plan.md`

Develops focused implementation plans through codebase research, options analysis, and technical approach definition. Includes self-assessment logic to determine if human approval is needed.

**Use this when**: Planning how to implement an issue

## How to Use This Skill

When this skill is referenced by a command or agent:

1. **Read the workflow file** for the appropriate workflow (see list above)
2. **Follow the process steps** as written in the workflow
3. **Reference guidelines and success criteria** to ensure quality
4. **Execute the operations** (usually bash/git/gh commands embedded in workflow)

## Key Principles

**Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub planning operations. Commands reference this skill rather than containing inline instructions.

**Research-First Approach**: Planning workflows emphasize thorough codebase research and analysis before implementation decisions.

**Requirements Clarity**: Focus on creating clear problem statements, acceptance criteria, and technical specifications.

**Quality Assurance**: Each workflow has success criteria and error handling guidelines to maintain planning integrity.

## Error Handling

If workflows encounter blocking issues:
- Document the problem clearly in issue comments or planning documentation
- Suggest alternative approaches or ask for clarification
- Identify missing information or requirements
- Resume when blocker is resolved

## Dependencies

- **Repository Setup**: Repository must have proper labels and issue templates configured
- **Team Coordination**: Planning often requires stakeholder input and approval
- **Technical Analysis**: Planning depends on access to codebase and architecture understanding

## Reference Files

All workflow details are contained in individual `.md` files in the `workflows/` directory. Each file provides complete procedural guidance for its specific workflow.
