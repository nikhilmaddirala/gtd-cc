---
name: github-gtd
description: Comprehensive GitHub workflow automation skill for issue-driven development with planning, implementation, review, and merge stages.
---

# GitHub GTD Workflow Skill

This skill provides complete guidance for executing the 7-stage GitHub workflow used in GTD (Getting Things Done) project management. It serves as the authoritative source for all GitHub workflow operations.

## About This Skill

The GitHub GTD skill is designed to facilitate structured issue-driven development workflows. It encompasses all stages from repository initialization through issue creation, planning, implementation, review, and merge operations. This skill consolidates procedural knowledge, best practices, and detailed workflow instructions used across interactive commands and autonomous agents.

### When to Use This Skill

This skill should be used when:
- Setting up a new repository for issue-driven development (Stage 0)
- Creating well-structured GitHub issues (Stage 1)
- Developing implementation plans with analysis (Stage 2)
- Reviewing and approving implementation approaches (Stage 3)
- Implementing approved plans in isolated development environments (Stage 4)
- Performing code reviews on implementations (Stage 5)
- Reviewing and approving implementations locally (Stage 6)
- Merging approved PRs and cleaning up development artifacts (Stage 7)
- Committing changes with conventional commit messages (General)

## The 7-Stage GitHub Workflow

Every issue progresses through these sequential stages:

| Stage | Workflow | Purpose | Label | Duration |
|-------|----------|---------|-------|----------|
| **0** | [Repository Setup](#stage-0-repository-setup) | Configure labels, templates, and worktree structure | none | One-time |
| **1** | [Issue Creation](#stage-1-issue-creation) | Transform user request into well-structured issue | → `needs planning` | Minutes |
| **2** | [Planning](#stage-2-planning) | Research codebase, analyze options, create implementation plan | `needs planning` → `needs implementation` or `needs plan approval` | Hours |
| **3** | [Plan Approval](#stage-3-plan-approval-conditional) | Human reviews and approves (or revises) implementation approach | `needs plan approval` → `needs implementation` or `needs planning` | Minutes-Hours |
| **4** | [Implementation](#stage-4-implementation) | Write code in isolated worktree, create PR with tests | `needs implementation` → `in review` | Hours-Days |
| **5** | [Code Review](#stage-5-code-review) | Review code for quality, security, completeness | `in review` → `ready for approval` | Minutes-Hours |
| **6** | [Human Approval](#stage-6-human-approval) | Human tests locally, reviews code, approves for merge | `ready for approval` → `approved for merge` or `in review` | Minutes-Hours |
| **7** | [Merge & Cleanup](#stage-7-merge--cleanup) | Merge PR, close issue, delete branch and worktree | `approved for merge` → closed | Minutes |

### Workflow Labels

**Workflow state labels** (track issue progress):
- `needs planning` - Requires implementation plan
- `needs plan approval` - Human must review approach (conditional stage)
- `needs implementation` - Ready for coding
- `in review` - Code under review
- `ready for approval` - Awaiting human approval
- `approved for merge` - Ready to merge
- `blocked` - Work stopped, needs intervention

**Issue type labels** (categorize issue):
- `feature` - New functionality
- `bug` - Defect or unexpected behavior
- `docs` - Documentation changes
- `refactor` - Code improvements without behavior change

## Individual Workflow Guides

Each stage of the workflow has detailed procedural instructions. Select the workflow that matches your current task:

### Stage 0: Repository Setup
**File**: `repo-setup.md`

Sets up essential GitHub workflow infrastructure in the current repository, including workflow labels, issue templates, PR templates, branch protection rules, and worktree directory structure.

**Use this when**: Setting up a new repository for the first time

### Stage 1: Issue Creation
**File**: `issue-creation.md`

Transforms user requirements into well-documented GitHub issues with clear problem statements, acceptance criteria, context, and appropriate labels.

**Use this when**: Creating new issues to track work

### Stage 2: Planning
**File**: `plan.md`

Develops focused implementation plans through codebase research, options analysis, and technical approach definition. Includes self-assessment logic to determine if human approval is needed.

**Use this when**: Planning how to implement an issue

### Stage 3: Plan Approval (Conditional)
**File**: `approve-plan.md`

Guides humans through reviewing AI-generated implementation plans. Provides decision framework for approval, revision requests, or questions.

**Use this when**: Human needs to review an implementation plan (only triggered when AI requests approval)

### Stage 4: Implementation
**File**: `implementation.md`

Autonomously implements approved plans by creating worktrees, writing code, running tests, and creating draft PRs ready for review.

**Use this when**: Building code from an approved implementation plan

### Stage 5: Code Review
**File**: `review.md`

Performs code reviews focusing on compliance with requirements, README guidelines, significant bugs, and architectural alignment. Filters for real issues only.

**Use this when**: Reviewing a pull request for quality and correctness

### Stage 6: Human Approval
**File**: `human-approval.md`

Guides humans through local testing, code review, and approval decision-making for implementations ready for merge.

**Use this when**: Human needs to test and approve an implementation

### Stage 7: Merge & Cleanup
**File**: `merge.md`

Executes final merge operations: squash-merges PR to main, closes issue, deletes branch, and removes worktree.

**Use this when**: Merging an approved implementation to main

### General: Git Commits
**File**: `commit.md`

Creates well-structured git commits with conventional commit format, describing changes with clear intent.

**Use this when**: Committing changes to the repository

## How to Use This Skill

When this skill is referenced by a command or agent:

1. **Select the relevant workflow** based on your current stage or task
2. **Read the workflow file** for that stage (see list above)
3. **Follow the process steps** exactly as written in the workflow
4. **Reference guidelines and success criteria** to ensure quality
5. **Execute the operations** (usually bash/git/gh commands embedded in workflow)

### Workflow Selection Logic

**If you're starting from scratch:**
1. First run `repo-setup.md` (Stage 0) in new repositories
2. Then create issues using `issue-creation.md` (Stage 1)

**If you're advancing an issue:**
1. Start with the workflow corresponding to the issue's current label
2. Follow steps precisely
3. Advance the label when workflow is complete

**If you're addressing feedback:**
1. For planning feedback: Use `plan.md` to revise (Stage 2)
2. For review feedback: Update code and follow `commit.md` (General)
3. For approval feedback: Use `human-approval.md` (Stage 6)

## Key Principles

**Single Source of Truth**: This skill and its workflow files contain all procedural knowledge for GitHub operations. Commands reference this skill rather than containing inline instructions.

**Sequential Progression**: Issues advance through stages in order. Each stage has clear entry conditions (labels/requirements) and exit conditions (what gets updated).

**Conditional Approval**: Stage 3 (Plan Approval) is conditional—it only occurs when AI explicitly requests human input. Simple plans auto-advance to implementation.

**Autonomous Execution**: Implementation details (Step 4, 5, 7) are designed for autonomous agent execution with minimal human interaction, while judgment-based stages (1, 3, 6) require human input.

**Quality Assurance**: Each stage has success criteria and error handling guidelines to maintain workflow integrity.

## Workflow Dependencies

- **Stage 0 must run first**: Repository needs labels and worktree directory before subsequent stages
- **Stage 1 and 2 are sequential**: Issues need clear definition (1) before planning (2)
- **Stages 2-3 are conditional**: Planning (2) may skip to implementation (4) if no approval needed
- **Stages 4-7 are sequential**: Implementation (4) → Review (5) → Approval (6) → Merge (7)

## Error Handling

If workflows encounter blocking issues:
- Document the problem clearly
- Update issue label to `blocked` with explanation in comments
- Suggest alternative approaches or ask for clarification
- Resume when blocker is resolved

## Workflow File Standards

All workflow files follow a consistent structure for clarity and maintainability.

### Workflow File Naming Convention

Workflow file names should:
- Be descriptive and match the stage purpose
- Use lowercase with hyphens (kebab-case)
- Remove redundant "-workflow" suffix (files live in `workflows/` directory)
- Examples: `repo-setup.md`, `issue-creation.md`, `implementation.md`, `human-approval.md`

### Workflow File Template

Each workflow file follows this standardized structure:

```markdown
---
description: [Brief description of what the workflow accomplishes]
allowed_tools: (optional)
  - Bash(command:*)
  - gh(subcommand:*)
---

## Overview

[1-2 sentence overview of the workflow's purpose and outcome]

## Context

[Prerequisites and repository state required to execute this workflow. Include bash code blocks for gathering information.]

## Your Task

**Goal**: [Clear statement of what needs to be accomplished]

**Issue/PR to [action]**: [How to identify the target - from $ARGUMENTS or selection]

**Role**: [Position in the 7-stage workflow, showing current stage with arrow]

### Process

[Step-by-step numbered process, organized by logical phases. Include bash code blocks for operations.]

## Guidelines

- [Principle 1]
- [Principle 2]
- [Principle 3]
- ...

## Success Criteria

- ✅ [Criterion 1]
- ✅ [Criterion 2]
- ✅ [Criterion 3]
- ...
```

### Key Template Features

- **Overview**: Brief, outcome-focused description
- **Context**: Gathers information needed to execute the workflow
- **Your Task**: Clear goal, target identification, and workflow position
- **Process**: Step-by-step execution with bash code examples
- **Guidelines**: Best practices and principles to follow
- **Success Criteria**: Checklist of completed requirements

## Command Naming Convention

Commands that invoke workflows should follow this pattern:

**Pattern**: `/gh-<verb>` or `/gh-<verb>-<noun>`

**Naming rules**:
- Command names should be **descriptive verbs** that clearly indicate the action
- Command names should **mirror the corresponding workflow stage** when possible
- Use lowercase with hyphens (kebab-case)
- Keep commands concise (1-2 words maximum)

**Workflow to Command Mapping**:

| Workflow File | Stage | Command | Purpose |
|---------------|-------|---------|---------|
| `repo-setup.md` | 0 | `/gh-repo` | Set up repository infrastructure |
| `issue-creation.md` | 1 | `/gh-issue` | Create a new issue |
| `plan.md` | 2 | `/gh-plan` | Develop implementation plan |
| `approve-plan.md` | 3 | `/gh-approve-plan` | Review and approve plan |
| `implementation.md` | 4 | `/gh-build` | Build/implement approved plan |
| `review.md` | 5 | `/gh-review` | Perform code review |
| `human-approval.md` | 6 | `/gh-approve` | Approve implementation for merge |
| `merge.md` | 7 | `/gh-merge` | Merge and clean up |
| `commit.md` | General | `/gh-commit` | Create git commit |

**Naming Guidelines**:
- Use action verbs: `build`, `review`, `approve`, `merge`, `plan`, `commit`
- Commands should be self-explanatory without documentation
- The command name should match users' mental model of what they're doing
- If workflow adds complexity, the command can be more specific (e.g., `/gh-approve-plan` vs just `/gh-approve`)

**Examples of good command names**:
- `/gh-issue` - "Create an issue" ✓
- `/gh-plan` - "Create a plan" ✓
- `/gh-build` - "Build/implement code" ✓
- `/gh-review` - "Review code" ✓
- `/gh-approve` - "Approve for merge" ✓
- `/gh-merge` - "Merge changes" ✓

**Examples of poor command names**:
- `/gh-1` - Not descriptive ✗
- `/gh-workflow-stage-4` - Too verbose ✗
- `/gh-implement-approved-plans` - Overly specific ✗

## Reference Files

All workflow details are contained in individual `.md` files in the `workflows/` directory. Each file follows the standardized template structure described above.
