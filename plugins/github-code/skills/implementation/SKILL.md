# Implementation Skill

## Overview

This skill provides foundation knowledge and patterns for implementing approved plans, managing code changes, and ensuring quality standards during the implementation phase of the GitHub workflow.

## Core Capabilities

### Plan Parsing and Execution
- Extracting implementation plans from issue comments
- Breaking down complex plans into actionable steps
- Tracking progress against plan acceptance criteria
- Adapting plans when blockers are encountered

### Development Workflow
- Setting up isolated development environments (worktrees)
- Managing feature branches
- Following conventional commit standards
- Creating atomic, focused commits

### Code Quality Assurance
- Running tests and verifying coverage
- Executing linting and formatting
- Performing security scans
- Validating build success

### Documentation
- Writing comprehensive commit messages
- Creating clear PR descriptions
- Updating README and CONTRIBUTING docs
- Documenting architecture decisions

## Key Practices

### Conventional Commits
Following the conventional commit format:
```
type(scope): subject

body

footer
```

Types: feat, fix, docs, style, refactor, test, chore

### Acceptance Criteria
- All items from the implementation plan are completed
- Code builds without errors
- All tests pass (unit, integration, regression)
- Code quality checks pass (lint, format, security)
- Documentation is updated
- Changes are committed and tested

### Error Handling
- Graceful degradation when blockers are encountered
- Clear documentation of workarounds
- Creation of follow-up issues for blocked tasks
- Transparent communication through PR comments

## Integration Points

This skill integrates with:
- **gh-build agent**: Executes implementation plans
- **GitHub workflow skill**: Manages code changes and PRs
- **Tools**: Testing frameworks, linters, build systems
- **Repository standards**: Follows project conventions

## Quality Standards

Implementation changes must meet:
- All acceptance criteria from approved plan
- Existing tests continue to pass
- New code is tested
- Code follows project style guide
- Changes are documented
- Commits follow conventional format
- PR description explains changes clearly
