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
| **1** | [Issue Creation](#stage-1-issue-creation) | Transform user request into well-structured issue | → `status-planning-todo` | Minutes |
| **2** | [Planning](#stage-2-planning) | Research codebase, analyze options, create implementation plan | `status-planning-todo` → `status-planning-done` or `status-planning-review` | Hours |
| **3** | [Plan Approval](#stage-3-plan-approval-conditional) | Human reviews and approves (or revises) implementation approach | `status-planning-review` → `status-planning-done` or `status-planning-todo` | Minutes-Hours |
| **4** | [Implementation](#stage-4-implementation) | Write code in isolated worktree, create PR with tests | `status-planning-done` → `status-implementation-todo` | Hours-Days |
| **5** | [Code Review](#stage-5-code-review) | Review code for quality, security, completeness | `status-implementation-todo` → `status-implementation-review` | Minutes-Hours |
| **6** | [Human Approval](#stage-6-human-approval) | Human tests locally, reviews code, approves for merge | `status-implementation-review` → `status-implementation-done` or `status-implementation-todo` | Minutes-Hours |
| **7** | [Merge & Cleanup](#stage-7-merge--cleanup) | Merge PR, close issue, delete branch and worktree | `status-implementation-done` → closed | Minutes |

### Workflow Labels

**Status labels** (track issue progress through planning and implementation):
- `status-planning-todo` - Requires implementation plan
- `status-planning-review` - Plan is under review (conditional stage)
- `status-planning-done` - Planning completed, ready for implementation
- `status-implementation-todo` - Ready for coding
- `status-implementation-review` - Implementation under review
- `status-implementation-done` - Implementation completed, ready to merge
- `blocked` - Work stopped, needs intervention

**Type labels** (categorize issue):
- `type-feature` - New functionality
- `type-bug` - Defect or unexpected behavior
- `type-docs` - Documentation changes
- `type-refactor` - Code improvements without behavior change

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

## Reference Files

All workflow details are contained in individual `.md` files in the `workflows/` directory. Each file follows the standardized template structure described above.
