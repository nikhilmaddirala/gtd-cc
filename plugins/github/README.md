# GitHub Code Workflow Plugin

This plugin provides commands for GitHub workflow management, enabling structured issue-driven development with AI-assisted automation.

**For detailed procedural instructions on executing each workflow stage, see [`SKILL.md`](./skills/github-gtd/SKILL.md)** - the authoritative source for all GitHub workflow operations.

## Overview

### Core principles

- Issues serve as the single source of truth for all development work
- AI agents handle execution between human approval checkpoints
- Git worktrees provide isolated development environments
- Conventional commits ensure clear change history
- Continuous monitoring maintains repository health

### Implementation philosophy

Each workflow stage can be accomplished in three ways, giving you flexibility to choose your level of automation:

**1. Manual** - Do it yourself in GitHub UI
- Full control over every action
- Use GitHub's native interface for issues, PRs, labels
- Example: Create issue manually, write plan in comments, change labels by hand

**2. Interactive with slash commands** - AI assists you interactively
- Run a command, AI helps you complete the task
- You stay in control, AI handles tedious work
- Example: `/gh-plan 123` - AI researches and drafts plan, you review and approve

**3. Non-interactive agents** - Delegate to autonomous AI
- Agent runs independently from start to finish
- Useful for batch operations or when you want full automation
- Example: Agent monitors for `needs planning` label, automatically plans all issues

Most stages offer both commands (interactive) and agents (autonomous). Choose based on your needs.

### Workflow stages

Every issue progresses through these stages:

**0. Repository initialization**
- Trigger: `/gh-repo` command
- Sets up labels, templates, branch protection
- One-time setup per repository

**1. Issue creation**
- Trigger: `/gh-issue "description"` command
- Label: → `status-planning-todo`
- User provides request, AI captures it as lightweight issue with basic categorization

**2. Planning**
- Trigger: `/gh-plan <issue-number>` command
- Label: `status-planning-todo` → `status-planning-review` or `status-planning-done`
- AI researches and creates implementation plan; auto-approves if confident, otherwise requests human review

**3. Plan approval** (conditional)
- Trigger: Human reviews plan in issue comments
- Label: `status-planning-review` → `status-planning-done` or back to `status-planning-todo`
- Only occurs if AI requests human input on approach

**4. Implementation**
- Trigger: `/gh-build <issue-number>` command
- Label: `status-planning-done` → `status-implementation-todo`
- AI creates branch/worktree, writes code, creates draft PR

**5. Code review**
- Trigger: `/gh-review <issue-number>` command
- Label: `status-implementation-todo` → `status-implementation-review`
- AI reviews code for quality, security, completeness

**6. Human approval**
- Trigger: Human approves PR in GitHub UI
- Label: `status-implementation-review` → `status-implementation-done`
- Human tests and approves implementation

**7. Merge and cleanup**
- Trigger: `/gh-merge <issue-number>` command or auto-merge
- Label: `status-implementation-done` → closed
- Squash merge to main, delete branch/worktree

### Label reference

Status labels (track issue progress through planning and implementation):
- `status-planning-todo` - Requires implementation plan
- `status-planning-review` - Plan is under review (conditional stage)
- `status-planning-done` - Planning completed, ready for implementation
- `status-implementation-todo` - Ready for coding
- `status-implementation-review` - Implementation under review
- `status-implementation-done` - Implementation completed, ready to merge
- `blocked` - Work stopped, needs intervention

Type labels (categorize issue):
- `type-feature` - New functionality
- `type-bug` - Defect or unexpected behavior
- `type-docs` - Documentation changes
- `type-refactor` - Code improvements without behavior change



## Workflow Stages (Reference)

This section provides a quick reference for each stage. For detailed procedural instructions on how to execute each workflow stage, see [`SKILL.md`](./skills/github-gtd/SKILL.md).

Issues serve as the single source of truth, with labels tracking workflow state.

| Stage | Label | What Happens | Implementation Status |
|-------|-------|--------------|----------------------|
| 0. Repository initialization | none | AI sets up labels, issue templates, PR templates, branch protection rules | **Manual**: Create repo, configure settings<br>**Command**: `/gh-repo` 📋<br>**Agent**: Repo init agent 📋 |
| 1. Issue creation | → `status-planning-todo` | User provides task description; AI captures lightweight issue with basic categorization | **Manual**: Create issue in GitHub UI<br>**Command**: `/gh-issue "description"` ✅<br>**Agent**: Issue creation agent 📋 |
| 2. Planning | `status-planning-todo` → `status-planning-done` or `status-planning-review` | AI conducts comprehensive analysis: requirement clarification, scoping, repository research, feasibility assessment, and creates detailed implementation plan; self-assesses confidence; if confident auto-approves to `status-planning-done`, otherwise sets `status-planning-review` for human review | **Manual**: Research and write plan in issue comments<br>**Command**: `/gh-plan <issue>` ✅<br>**Agent**: Planning agent 📋 |
| 3. Plan approval (conditional) | `status-planning-review` → `status-planning-done` or `status-planning-todo` | Human reviews AI's plan and reasoning; approves by changing label to `status-planning-done`, or requests revision by changing to `status-planning-todo` with feedback | **Manual**: Review plan, change label in GitHub UI<br>**Command**: `/gh-approve-plan <issue>` 📋<br>**Agent**: N/A (requires human judgment) |
| 4. Implementation | `status-planning-done` → `status-implementation-todo` | AI creates branch `issue-<num>-<slug>`; sets up worktree; implements code with conventional commits; creates draft PR linked to issue; runs tests | **Manual**: Write code, create PR manually<br>**Command**: `/gh-build <issue>` 📋<br>**Agent**: Build agent 📋 |
| 5. Code review | `status-implementation-todo` → `status-implementation-review` | AI reviews code for style, security, completeness, test coverage; adds review comments; marks PR as ready for review | **Manual**: Review code manually in GitHub<br>**Command**: `/gh-review <issue>` 📋<br>**Agent**: Review agent 📋 |
| 6. Human approval | `status-implementation-review` → `status-implementation-done` | Human reviews implementation, tests locally, approves PR in GitHub UI | **Manual**: Review and approve PR in GitHub UI<br>**Command**: `/gh-approve <issue>` 📋<br>**Agent**: N/A (requires human judgment) |
| 7. Merge and cleanup | `status-implementation-done` → closed | AI squash-merges PR to main; closes issue and PR; deletes branch; removes worktree; verifies cleanup | **Manual**: Merge PR, delete branch/worktree<br>**Command**: `/gh-merge <issue>` 📋<br>**Agent**: Merge agent 📋 |

**Implementation Status Legend:**
- ✅ Implemented and functional
- 📋 Planned but not yet developed
- N/A - Not applicable (human judgment required)

**Key Workflow Characteristics:**
- Issues carry workflow state labels (not PRs)
- PRs use GitHub's built-in states (Draft, Ready for review, Approved)
- Stage 3 (Plan approval) is conditional - only occurs when AI requests human input
- All commands operate on issue numbers, not PR numbers
- Worktrees are created in `worktrees/issue-<num>-<slug>` directory
- Branch naming follows `issue-<num>-<slug>` convention
- Three implementation paths per stage: manual (GitHub UI), command (interactive AI), agent (autonomous AI)
- Stages requiring human judgment (3, 6) have manual and command options but no agent option

## Workflow File Standards

All workflow files follow a consistent structure for clarity and maintainability. Use these standards when creating new workflow files.

### Workflow file naming convention

Workflow file names should:
- Be descriptive and match the stage purpose
- Use lowercase with hyphens (kebab-case)
- Remove redundant "-workflow" suffix (files live in `workflows/` directory)
- Examples: `repo-setup.md`, `issue-creation.md`, `implementation.md`, `human-approval.md`

### Workflow file template

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

**Issue/PR to [action]**: [How to identify the target - provided as context]

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

### Template features

- **Overview**: Brief, outcome-focused description
- **Context**: Gathers information needed to execute the workflow
- **Your Task**: Clear goal, target identification, and workflow position
- **Process**: Step-by-step execution with bash code examples
- **Guidelines**: Best practices and principles to follow
- **Success Criteria**: Checklist of completed requirements

## Command naming convention

Commands that invoke workflows should follow this pattern:

**Pattern**: `/gh-<verb>` or `/gh-<verb>-<noun>`

**Naming rules**:
- Command names should be descriptive verbs that clearly indicate the action
- Command names should mirror the corresponding workflow stage when possible
- Use lowercase with hyphens (kebab-case)
- Keep commands concise (1-2 words maximum)

**Workflow to command mapping**:

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

**Naming guidelines**:
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

## Example Workflow Walkthrough

Here's how a typical feature request flows through the complete workflow:

### Scenario: Add dark mode toggle

**0. Repository initialization** (one-time setup)
```bash
/gh-repo
```
AI sets up repository with:
- Workflow labels (status-planning-todo, status-implementation-todo, etc.)
- Issue templates
- PR templates
- Branch protection rules

**1. Issue creation**
```bash
/gh-issue "Add dark mode toggle to user settings"
```
AI creates Issue #123 with:
- Formatted description and acceptance criteria
- Label: `status-planning-todo`

**2. Planning**
```bash
/gh-plan 123
```
AI performs research:
- Analyzes codebase for existing theming patterns
- Researches dark mode implementation approaches (CSS variables, class toggling, theme provider)
- Evaluates trade-offs of each approach
- Creates detailed implementation plan in issue comments

AI self-assesses confidence:
- This is a well-understood pattern with clear implementation path
- **Decision**: Auto-approve
- Updates Issue #123 label: `status-planning-done`

**Alternative scenario**: If the plan involved complex state management or unclear requirements, AI would instead:
- Add comment: "I need human input on this approach because [reason]"
- Update Issue #123 label: `status-planning-review`
- Wait for human to review and change label to `status-planning-done`

**3. Plan approval** (skipped in this example - AI was confident)

**4. Implementation**
```bash
/gh-build 123
```
AI implements the feature:
- Creates branch `issue-123-add-dark-mode-toggle`
- Sets up worktree in `worktrees/issue-123-add-dark-mode-toggle`
- Implements toggle component using CSS custom properties
- Writes tests for theme switching
- Makes conventional commits:
  ```
  feat(ui): add dark mode toggle component
  feat(theming): implement CSS custom properties for theme switching
  test(ui): add dark mode toggle tests
  ```
- Creates draft PR #45 with description, screenshots, linked to Issue #123
- Updates Issue #123 label: `status-implementation-todo`

**5. Code review**
```bash
/gh-review 123
```
AI reviews the implementation:
- Checks code style and patterns
- Verifies security (no XSS vulnerabilities in theme switching)
- Confirms test coverage is adequate
- Adds review comments on PR #45
- Marks PR #45 as "Ready for review"
- Updates Issue #123 label: `status-implementation-review`

**6. Human approval**
Human reviews in GitHub:
- Pulls branch locally: `cd worktrees/issue-123-add-dark-mode-toggle`
- Tests dark mode toggle functionality
- Reviews code changes on PR #45
- Approves PR in GitHub UI
- Issue #123 label automatically updates: `status-implementation-done`

**7. Merge and cleanup**
```bash
/gh-merge 123
```
AI completes the workflow:
- Squash-merges PR #45 to main with clean commit message
- Closes Issue #123
- Closes PR #45
- Deletes branch `issue-123-add-dark-mode-toggle`
- Removes worktree `worktrees/issue-123-add-dark-mode-toggle`
- Verifies no leftover references

**Result**: Dark mode feature is live on main with clean commit history, closed issue, and no leftover branches or worktrees.

## Appendix

### Design Decision: Conditional plan approval

**Decision:** AI self-assesses confidence after creating implementation plan. Request human approval only when needed (see stage 3 above).

**Rationale:**
- Balances speed and oversight - simple changes proceed quickly, complex ones get human review
- AI explains reasoning when requesting approval, making the checkpoint meaningful
- Humans can still provide feedback at PR review stage even for auto-approved plans
- Reduces unnecessary delays while maintaining quality control for complex decisions

**AI requests approval when:**
- Multiple valid approaches exist with significant trade-offs
- Changes affect critical systems (auth, security, data integrity)
- Requirements are ambiguous or conflicting
- Unfamiliar patterns or technologies are involved

**AI auto-approves when:**
- Implementation path is clear and well-established
- Similar patterns exist in the codebase
- Requirements are unambiguous
- Changes are isolated and low-risk

**Alternatives considered:**
- Always require human approval (safer but slower)
- Never require plan approval, only PR review (faster but risks wasted implementation effort)
- Human decides approval requirement at issue creation (adds cognitive load)

### Branch Naming Conventions

**Standard patterns:**
- `issue-<number>-<slug>` - For GitHub issues (primary pattern)
- `hotfix-<slug>` - For urgent fixes outside normal workflow
- `docs-<slug>` - For documentation-only updates

**Examples:**
- `issue-12-workflow-standardization`
- `issue-45-add-user-authentication`
- `hotfix-container-restart-loop`
- `docs-update-installation-guide`

**Slug guidelines:**
- Use lowercase with hyphens
- Keep concise (3-5 words maximum)
- Describe the change, not the problem
- Avoid redundant words like "fix" or "add" if type is clear from context

### Worktree Setup

**Creating worktrees:**
```bash
# Create worktree for issue
git worktree add worktrees/issue-12-workflow-standardization

# Switch to worktree
cd worktrees/issue-12-workflow-standardization

# Start working...
```

**Managing worktrees:**
```bash
# List all worktrees
git worktree list

# Remove worktree (after branch is merged/deleted)
git worktree remove worktrees/issue-12-workflow-standardization

# Prune stale worktree references
git worktree prune
```

**Worktree best practices:**
- One worktree per active issue
- Keep worktrees in dedicated `worktrees/` directory
- Remove worktrees promptly after merging
- Never commit from main repo directory when worktrees are active

### Conventional Commit Format

**Structure:**
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `refactor` - Code refactoring without behavior change
- `test` - Adding or modifying tests
- `chore` - Maintenance tasks, dependency updates
- `ci` - CI/CD configuration changes
- `perf` - Performance improvements
- `style` - Code style/formatting changes

**Scope (optional):**
- Component or area affected (e.g., `auth`, `api`, `ui`)

**Description:**
- Use imperative mood ("add" not "added" or "adds")
- Don't capitalize first letter
- No period at the end
- Keep under 72 characters

**Examples:**
```
feat(auth): add OAuth2 authentication flow
fix(api): resolve race condition in request handler
docs: update installation instructions for macOS
refactor(parser): simplify token processing logic
test(auth): add integration tests for login flow
```
