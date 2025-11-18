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
- Label: → `needs planning`
- User brain dumps task, AI creates formatted issue

**2. Planning**
- Trigger: `/gh-plan <issue-number>` command
- Label: `needs planning` → `needs implementation` or `needs plan approval`
- AI researches and creates implementation plan; auto-approves if confident, otherwise requests human review

**3. Plan approval** (conditional)
- Trigger: Human reviews plan in issue comments
- Label: `needs plan approval` → `needs implementation` or back to `needs planning`
- Only occurs if AI requests human input on approach

**4. Implementation**
- Trigger: `/gh-build <issue-number>` command
- Label: `needs implementation` → `in review`
- AI creates branch/worktree, writes code, creates draft PR

**5. Code review**
- Trigger: `/gh-review <issue-number>` command
- Label: `in review` → `ready for approval`
- AI reviews code for quality, security, completeness

**6. Human approval**
- Trigger: Human approves PR in GitHub UI
- Label: `ready for approval` → `approved for merge`
- Human tests and approves implementation

**7. Merge and cleanup**
- Trigger: `/gh-merge <issue-number>` command or auto-merge
- Label: `approved for merge` → closed
- Squash merge to main, delete branch/worktree

### Label reference

Workflow states (applied to issues):
- `needs planning` - Requires implementation plan
- `needs plan approval` - Human must review approach
- `needs implementation` - Ready for coding
- `in review` - Code under review
- `ready for approval` - Awaiting human approval
- `approved for merge` - Ready to merge
- `blocked` - Work stopped, needs intervention

Issue types (categorization):
- `feature` - New functionality
- `bug` - Defect or unexpected behavior
- `docs` - Documentation changes
- `refactor` - Code improvements without behavior change



## Workflow Stages (Reference)

This section provides a quick reference for each stage. For detailed procedural instructions on how to execute each workflow stage, see [`SKILL.md`](./skills/github-gtd/SKILL.md).

Issues serve as the single source of truth, with labels tracking workflow state.

| Stage | Label | What Happens | Implementation Status |
|-------|-------|--------------|----------------------|
| 0. Repository initialization | none | AI sets up labels, issue templates, PR templates, branch protection rules | **Manual**: Create repo, configure settings<br>**Command**: `/gh-repo` 📋<br>**Agent**: Repo init agent 📋 |
| 1. Issue creation | → `needs planning` | User provides task description; AI creates formatted issue with details | **Manual**: Create issue in GitHub UI<br>**Command**: `/gh-issue "description"` ✅<br>**Agent**: Issue creation agent 📋 |
| 2. Planning | `needs planning` → `needs implementation` or `needs plan approval` | AI researches codebase and approaches; creates implementation plan with options; self-assesses confidence; if confident auto-approves to `needs implementation`, otherwise sets `needs plan approval` for human review | **Manual**: Research and write plan in issue comments<br>**Command**: `/gh-plan <issue>` ✅<br>**Agent**: Planning agent 📋 |
| 3. Plan approval (conditional) | `needs plan approval` → `needs implementation` or `needs planning` | Human reviews AI's plan and reasoning; approves by changing label to `needs implementation`, or requests revision by changing to `needs planning` with feedback | **Manual**: Review plan, change label in GitHub UI<br>**Command**: `/gh-approve-plan <issue>` 📋<br>**Agent**: N/A (requires human judgment) |
| 4. Implementation | `needs implementation` → `in review` | AI creates branch `issue-<num>-<slug>`; sets up worktree; implements code with conventional commits; creates draft PR linked to issue; runs tests | **Manual**: Write code, create PR manually<br>**Command**: `/gh-build <issue>` 📋<br>**Agent**: Build agent 📋 |
| 5. Code review | `in review` → `ready for approval` | AI reviews code for style, security, completeness, test coverage; adds review comments; marks PR as ready for review | **Manual**: Review code manually in GitHub<br>**Command**: `/gh-review <issue>` 📋<br>**Agent**: Review agent 📋 |
| 6. Human approval | `ready for approval` → `approved for merge` | Human reviews implementation, tests locally, approves PR in GitHub UI | **Manual**: Review and approve PR in GitHub UI<br>**Command**: `/gh-approve <issue>` 📋<br>**Agent**: N/A (requires human judgment) |
| 7. Merge and cleanup | `approved for merge` → closed | AI squash-merges PR to main; closes issue and PR; deletes branch; removes worktree; verifies cleanup | **Manual**: Merge PR, delete branch/worktree<br>**Command**: `/gh-merge <issue>` 📋<br>**Agent**: Merge agent 📋 |

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

## Example Workflow Walkthrough

Here's how a typical feature request flows through the complete workflow:

### Scenario: Add dark mode toggle

**0. Repository initialization** (one-time setup)
```bash
/gh-repo
```
AI sets up repository with:
- Workflow labels (needs planning, needs implementation, etc.)
- Issue templates
- PR templates
- Branch protection rules

**1. Issue creation**
```bash
/gh-issue "Add dark mode toggle to user settings"
```
AI creates Issue #123 with:
- Formatted description and acceptance criteria
- Label: `needs planning`

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
- Updates Issue #123 label: `needs implementation`

**Alternative scenario**: If the plan involved complex state management or unclear requirements, AI would instead:
- Add comment: "I need human input on this approach because [reason]"
- Update Issue #123 label: `needs plan approval`
- Wait for human to review and change label to `needs implementation`

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
- Updates Issue #123 label: `in review`

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
- Updates Issue #123 label: `ready for approval`

**6. Human approval**
Human reviews in GitHub:
- Pulls branch locally: `cd worktrees/issue-123-add-dark-mode-toggle`
- Tests dark mode toggle functionality
- Reviews code changes on PR #45
- Approves PR in GitHub UI
- Issue #123 label automatically updates: `approved for merge`

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
