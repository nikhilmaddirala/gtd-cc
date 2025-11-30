---
name: gh-plan
description: GitHub workflow automation skill for implementation planning and research.
---

# GitHub Plan Skill

## Overview

This skill provides comprehensive guidance for GitHub planning workflows including implementation planning and codebase research. It serves as the authoritative source for all GitHub planning operations. Use this skill when researching codebase to understand existing patterns and architecture, developing implementation plans through analysis and options evaluation, creating technical approaches and development strategies, or documenting acceptance criteria and implementation requirements.

## Workflows

Use the appropriate workflow from the `workflows/` directory:

- **plan.md** - Develops focused implementation plans through codebase research, options analysis, and technical approach definition. Includes self-assessment logic to determine if human approval is needed.

## Resources

- **resources/plan-template.md** - Template structure for posting implementation plans as issue comments. Use this when creating plan comments to ensure consistent formatting and completeness.

## Guidelines

Follow these general guidelines when executing any workflow in this skill:

- **Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub planning operations.
- **Research-First Approach**: Planning workflows emphasize thorough codebase research and analysis before implementation decisions.
- **Requirements Clarity**: Focus on creating clear problem statements, acceptance criteria, and technical specifications.
- **Comprehensive Analysis**: Since issue creation is lightweight, conduct thorough requirement gathering, scoping, and analysis.
- **Detail for Execution**: Create plans detailed enough for autonomous execution by gh-build agent. Specify enough context to avoid ambiguity.
- **Options Analysis**: If multiple significant approaches exist, compare alternatives with key tradeoffs and considerations.
- **Repository Context**: Research recent issues, pull requests, and documentation to understand project standards and processes.
- **When this skill is referenced by a command or agent**: Read the workflow file, follow the process steps exactly as written, reference guidelines and success criteria to ensure quality.

## Additional Information

### Error Handling

If workflows encounter blocking issues:
- Document the problem clearly in issue comments or planning documentation
- Suggest alternative approaches or ask for clarification
- Identify missing information or requirements
- Resume when blocker is resolved

### Dependencies

- **Repository Setup**: Repository must have proper labels and issue templates configured
- **Team Coordination**: Planning often requires stakeholder input and approval
- **Technical Analysis**: Planning depends on access to codebase and architecture understanding
