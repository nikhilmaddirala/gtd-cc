---
name: skill-template
description: Template for creating domain expertise and knowledge repositories
version: 0.1.0
last_updated: YYYY-MM-DD
---

# Skill Name

## Overview

[Comprehensive explanation of this skill's domain, scope, and purpose. Include what problems it solves, what workflows it enables, and how it relates to the broader gtd-cc ecosystem. This section should help readers understand whether this skill is relevant to their needs.]

Example: "This skill provides comprehensive knowledge about GitHub workflow automation using an issue-driven development approach. It covers the 7-stage workflow: repository setup, issue creation, planning, approval, implementation, review, and merge. This skill enables developers to automate complex GitHub processes and maintain consistency across projects."

## Core Capabilities

List and describe the main capabilities this skill provides:

- **Capability 1**: One-sentence description of what this capability does
  - **Purpose**: Why this capability exists and when to use it
  - **Scope**: What's included and what's not
  - **Use Cases**: Scenarios where this is valuable

- **Capability 2**: One-sentence description
  - **Purpose**: When and why to use
  - **Scope**: Boundaries and limitations
  - **Use Cases**: Practical applications

- **Capability 3**: One-sentence description
  - **Purpose**: When and why to use
  - **Scope**: Boundaries and limitations
  - **Use Cases**: Practical applications

Example:
- **Repository Setup**: Initializes GitHub repositories with proper labels, issue templates, and worktree structure
  - **Purpose**: Ensures consistent foundation for all projects following GTD workflow
  - **Scope**: Creates repo structure, labels, templates, and initial worktree - does not include permission management
  - **Use Cases**: Starting new projects, standardizing existing repos, onboarding contributors

## Key Concepts

Document fundamental concepts that are essential to understanding this skill:

### Concept 1: Clear Name

**Definition**: Precise one-sentence definition of this concept

**Why It Matters**: Explanation of why this concept is important within the skill's domain

**Related Concepts**: How this concept connects to other concepts in the skill

**Common Misconceptions**: What people often misunderstand about this concept

**Example Scenario**: Concrete example showing this concept in action

Example:
### Issue-Driven Development

**Definition**: A workflow model where all project work is organized around explicitly defined issues with clear requirements, implementation plans, and validation criteria

**Why It Matters**: Creates structure and documentation for complex projects, ensures all work is tracked and reviewable, enables parallel work without conflicts

**Related Concepts**: Connects to "7-Stage Workflow", "Worktree Isolation", and "Conventional Commits"

**Common Misconceptions**: This is not just about GitHub Issues - it's a complete development methodology that coordinates code, planning, and review

**Example Scenario**: Developer starts with issue requesting a new feature. Issue includes requirements, implementation approach options, and acceptance criteria. Implementation happens in isolated worktree. Code review validates against issue requirements. All artifacts are linked back to issue.

### Concept 2: Another Important Concept
[Similar structure]

## Workflows and Patterns

Describe the major workflows this skill enables. These are the "recipes" users follow:

### Workflow 1: Workflow Name

**Purpose**: What does this workflow accomplish and when would you use it?

**Participants**: Who performs actions in this workflow (developer, reviewer, bot, etc.)

**Prerequisites**:
- Precondition 1: What must be true before starting
- Precondition 2: Another required condition
- Precondition 3: Third precondition

**Sequence of Steps**:

1. **Step 1**: Clear action description
   - **Who**: Who performs this action (Developer, AI Agent, etc.)
   - **Input**: What information is needed
   - **Process**: How is this step executed
   - **Output**: What result or artifact is created
   - **Validation**: How do we know this step succeeded?

2. **Step 2**: Next action
   - **Who**: Who performs this action
   - **Input**: What information is needed
   - **Process**: How is this step executed
   - **Output**: What result or artifact is created
   - **Validation**: How do we know this step succeeded?

3. **Step 3**: Final step
   - **Who**: Who performs this action
   - **Input**: What information is needed
   - **Process**: How is this step executed
   - **Output**: What result or artifact is created
   - **Validation**: How do we know this step succeeded?

**Success Criteria**: How do you know the workflow completed successfully?
- Criterion 1: Measurable outcome
- Criterion 2: Verifiable state
- Criterion 3: Deliverable artifact

**Common Issues**: Problems that occur in this workflow and how to solve them
- **Issue**: Clear problem description
  - **Symptom**: How the user recognizes this problem
  - **Root Cause**: Why does this happen
  - **Solution**: Steps to resolve
  - **Prevention**: How to avoid this issue

**Related Workflows**: Other workflows in this skill that connect to or build upon this one
- **After This**: What workflow logically follows
- **Before This**: What workflow typically precedes this
- **Parallel**: What other workflows run simultaneously

Example:
### Workflow 1: Repository Initialization

**Purpose**: Set up a new GitHub repository following GTD standards so that all team members can follow the issue-driven development workflow consistently

**Participants**: Repository Owner (usually with repo admin access), Automated systems for manifest validation

**Prerequisites**:
- Repository exists on GitHub
- User has admin access to the repository
- GTD-GitHub plugin is installed in Claude Code

**Sequence of Steps**:

1. **Initialize Repository Labels**
   - **Who**: Automated process triggered by gh-repo command
   - **Input**: Repository name and URL
   - **Process**: Creates standard label set (in-review, needs-implementation, blocked, etc.)
   - **Output**: GitHub repository with all standard labels applied
   - **Validation**: List all labels and verify count and naming

2. **Create Issue Templates**
   - **Who**: Automated process
   - **Input**: Template specifications from plugin
   - **Process**: Creates GitHub issue templates for feature requests, bugs, documentation
   - **Output**: `.github/ISSUE_TEMPLATE/` directory with template files
   - **Validation**: Test creating an issue using each template

3. **Initialize Worktree**
   - **Who**: Automated process
   - **Input**: Repository path and branch name
   - **Process**: Creates git worktree for isolated development
   - **Output**: Worktree directory structure ready for development
   - **Validation**: Verify worktree can be listed and contains expected structure

**Success Criteria**:
- Repository has all 8 standard labels applied
- Issue templates are accessible and functional
- Worktree is created and ready for issue development
- All developers can see and use the setup

**Common Issues**:
- **Issue**: Labels already exist with conflicting names
  - **Symptom**: Init command reports duplicate label names
  - **Root Cause**: Repository was manually set up before running gh-repo
  - **Solution**: Delete conflicting labels or skip initialization
  - **Prevention**: Run gh-repo on newly created repositories only

## Integration Points

Document how this skill integrates with other parts of the ecosystem:

### Commands That Use This Skill

List the commands that rely on this skill's knowledge:

- **Command Name** (`/command-name`): Brief description of how it uses this skill
  - Uses for: Specific aspect of the skill (e.g., "Understanding workflow sequence")
  - Related pattern: Which workflow pattern does it follow

- **Another Command** (`/another-command`): How it applies this skill's knowledge
  - Uses for: Which part of the skill
  - Related pattern: Which workflow it implements

### Agents That Use This Skill

List autonomous agents that leverage this skill:

- **Agent Name**: Brief description of its role
  - Uses for: Which aspects of the skill
  - Related workflow: Which workflows it executes
  - Autonomy level: What decisions it makes independently

### Related Skills

List skills that complement or extend this one:

- **Skill Name**: How it relates (builds on, complements, depends on)
  - Connection: The relationship between skills
  - Combined Usage: When you'd use both together

### External Dependencies

List external systems this skill depends on:

- **GitHub API**: Which endpoints and operations are used
  - Authentication: How credentials are managed
  - Rate Limits**: Any rate limit considerations

- **External Tools**: CLI tools, services, or platforms
  - Purpose: What each tool is used for
  - Installation**: How to ensure availability
  - Alternatives: What to do if tool is unavailable

## Examples and Use Cases

Provide concrete examples showing how to apply this skill:

### Use Case 1: Scenario Name

**Context**: Situation or problem this addresses
- **User Goal**: What the user wants to accomplish
- **Constraints**: Limitations or requirements
- **Complexity Level**: Beginner, Intermediate, Advanced

**How To Apply This Skill**:
1. Step 1: First action to take
2. Step 2: Second action to take
3. Step 3: Final action to take

**Expected Outcome**: What success looks like
- Measurable result 1
- Deliverable 2
- State change 3

**Variations**: How this might differ in different contexts
- Variation 1: How it changes when X is different
- Variation 2: How it changes when Y is different

### Use Case 2: Another Scenario
[Similar structure]

## Maintenance and Evolution

Document how this skill is maintained and improved:

### Update Frequency
How often does this skill need updates? (e.g., monthly, quarterly, on-demand)

### Known Limitations

What can't this skill currently do or doesn't cover?

- **Limitation 1**: Description of what's not covered and why
- **Limitation 2**: Another constraint
- **Future Work**: How this will be addressed

### Future Enhancements

What improvements are planned?

- **Enhancement 1**: New capability being planned
  - **Timeline**: Expected completion
  - **Motivation**: Why this matters
  - **Impact**: How it improves the skill

- **Enhancement 2**: Another planned improvement
  - **Timeline**: Expected completion
  - **Motivation**: Why this matters
  - **Impact**: How it improves the skill

### Dependencies

What external factors affect this skill?

- **Factor 1**: How it impacts the skill (e.g., GitHub API changes)
- **Factor 2**: Another dependency
- **Tracking**: How to monitor for changes

### Related Issues

Links to GitHub issues tracking enhancements or known problems:

- Issue #X: Brief description of what it addresses
- Issue #Y: Another related issue

## Troubleshooting

Document common problems and solutions:

### Problem Category 1: Type of Problem
- **Symptom**: How the user recognizes this problem
- **Diagnosis**: How to confirm what's wrong
- **Solution**: Steps to fix
- **Prevention**: How to avoid in the future
- **Escalation**: When to seek additional help

### Problem Category 2: Another Type of Problem
[Similar structure]

## FAQ

Answer frequently asked questions:

**Q: Common question?**
A: Clear, concise answer with relevant details and examples if applicable.

**Q: Another common question?**
A: Answer with explanation and context.

## See Also

Related resources and documentation:

- Related Command: `/command-name` - Brief description of what it does
- Related Skill: [Skill Name](../other-skill/SKILL.md) - How it relates
- Developer Guide: [Integration Patterns](../DEVELOPMENT.md#integration)
- External Resource: [Link](https://example.com) - Relevant external documentation
