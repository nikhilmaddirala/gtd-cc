# GitHub Code Workflow Plugin

This plugin provides commands for GitHub workflow management. The plugin structure is set up for future expansion with agents and skills.

## TODOs
- Write workflow table with better structure
- Write lifecycle of issues and PRs (decide if plan goes in issue or PR)

## Architecture Overview

**Core Principles:**
- Issues serve as the single source of truth for all development work
- AI agents handle execution between human approval checkpoints
- Git worktrees provide isolated development environments
- Conventional commits ensure clear change history
- Continuous monitoring maintains repository health

**Workflow Stages:**
0. Repo initialization → 1. Issue creation → 2. Planning → 3. Plan approval → 4. Implementation → 5. AI review → 6. Human review → 7. Merge & cleanup

**Human Approval Gates:**
- After planning (strategic oversight of implementation approach)
- After AI review (final approval before merging changes)

## Workflow Stages

Issues and pull requests serve as the central coordination points, with labels tracking workflow stage and driving multiple components (commands, agents, skills).

| Stage | Issue/PR Label | Entity | Implementation | Inputs | Outputs | Next Steps |
|-------|--------------|--------|----------------|---------|----------|------------|
| 0. Initialize Repo | **repo: needs initialization** | Repository | ✅ `commands/gh-repo`<br>📋 Repo initialization agent | New repository | Repository with labels, templates, issue templates, branch protection | Create Issue → **issue: needs planning** |
| 1. Create Issue | **issue: needs planning** | Issue | ✅ `commands/gh-issue`<br>📋 Issue creation agent | User has a task in mind / in task list | Issue following template with "needs planning" label | Creates implementation plan → **issue: needs plan approval** |
| 3. Plan Implementation | **issue: needs planning** | Issue | ✅ `commands/gh-plan`<br>📋 AI agent (non-interactive) | Issue with "needs planning" label | Implementation plan with options analysis; label "issue: needs plan approval" | Do internal/external research to develop detailed plan; add options and tradeoffs analysis |
| | **issue: needs plan approval** | Issue | 🔄 Human only | Issue with plan + "issue: needs plan approval" label | Label → "issue: needs implementation" or back to "issue: needs planning" with feedback | Approve → **issue: needs implementation**<br>Request changes → **issue: needs planning** |
| 4. Build Code | **issue: needs implementation** | Issue | ✅ `commands/gh-build`<br>📋 AI agent (non-interactive) | Approved plan + "issue: needs implementation" label | Branch + worktree with commits; draft PR with "pr: needs review" label; passing tests | Creates branch/PR → **pr: in progress** |
| | **pr: in progress** | PR | 🔄 ✅ `commands/gh-build`<br>📋 Build agent | Branch + worktree with commits; draft PR | Implementation active, PR in draft | Completes work → **pr: needs review** |
| 5. Review Changes | **pr: needs review** | PR | 📋 `commands/gh-review`<br>📋 AI agent (non-interactive) | PR ready with "pr: needs review" label; CI checks complete | Label → "pr: ready for approval" or "issue: needs implementation"; detailed review comment | Passes review → **pr: ready for approval**<br>Needs changes → **issue: needs implementation** |
| | **pr: ready for approval** | PR | 📋 `commands/gh-approve`<br>🔄 Human + AI (interactive) | PR with "pr: ready for approval" label; AI review complete | Label → "pr: approved for merge" or "issue: needs implementation" or "issue: needs planning"; detailed feedback | Approve → **pr: approved for merge**<br>Request changes → **issue: needs implementation**<br>Major revisions → **issue: needs planning** |
| 6. Merge & Cleanup | **pr: approved for merge** | PR | 📋 `commands/gh-merge`<br>📋 AI agent | PR labeled "pr: approved for merge"; approved by human; CI passing; no conflicts | Changes merged to main; issue closed; clean repository state | Auto-merge & cleanup → **Closed** |
| 7. Maintenance | **issue/pr: blocked** | Issue/PR | 📋 `commands/gh-maintenance`<br>🔄 Human intervention<br>📋 maintenance agent | Work stopped due to blocker | Resolve blocker → appropriate state | Monitor health continuously: verify issue status, branches/worktrees, identify stale work (>7 days), flag waiting PRs; sync labels with actual state; generate reports |
| | **needs cleanup** | Issue/PR | 📋 `commands/gh-cleanup`<br>📋 Cleanup agent, maintenance skills | Issue/PR closed but branches remain | Clean up branches/worktrees | Updated labels; project board sync; daily reports; automated cleanup |

**Implementation Status:**
- ✅ Completed: Implementation exists and is functional
- 🔄 In Progress: Stage represents ongoing work or waiting states
- 📋 Planned: Implementation planned but not yet developed

**Issue States:**
- **Open**: Issue is active and being worked on
- **Closed**: Issue is complete and merged, or abandoned

**Type Labels:**
- `feature` - New functionality
- `bug` - Defect or unexpected behavior
- `docs` - Documentation changes
- `refactor` - Code improvements without behavior change

**Workflow State Labels:**
- `repo: needs initialization` - Repository requires setup (labels, templates, branch protection)
- `issue: needs planning` - Issue requires implementation planning
- `issue: needs plan approval` - Implementation plan ready for human review
- `issue: needs implementation` - Plan approved, ready for code implementation
- `pr: in progress` - Pull request actively being developed
- `pr: needs review` - Pull request ready for AI code review
- `pr: ready for approval` - AI review complete, ready for human approval
- `pr: approved for merge` - Human approved, ready for automated merge
- `issue/pr: blocked` - Work stopped due to blocker (applies to issues or PRs)

**Workflow Integration:**
- Labels drive automation: agents query for issues with specific labels
- Maintenance agent ensures labels stay synchronized with actual state
- Project board columns mirror label states for visualization

## Example Workflow Walkthrough

Here's how a typical feature request flows through the complete workflow:

### Scenario: Add Dark Mode Toggle

**1. Repo Initialization**
```
/gh-repo
```
*AI sets up repository with labels, templates, and branch protection*

**2. Issue Creation**
```
/gh-issue "Add dark mode toggle to user settings"
```
*AI creates Issue #123 with "issue: needs planning" label*

**3. Planning Phase**
- AI agent analyzes codebase for theming patterns
- Researches dark mode implementation approaches
- Creates detailed plan with options and trade-offs
- Updates label to "issue: needs plan approval"

**4. Plan Review**
*Human reviews plan, adds feedback: "Use CSS custom properties for theming"*
- Updates label to "issue: needs implementation"

**5. Implementation**
- AI creates branch `issue-123-add-dark-mode-toggle`
- Sets up worktree in `worktrees/issue-123-add-dark-mode-toggle`
- Implements toggle component with CSS variables
- Adds conventional commits:
  ```
  feat(ui): add dark mode toggle component
  feat(theming): implement CSS custom properties for theme switching
  test(ui): add dark mode toggle tests
  ```
- Creates draft PR with description and screenshots

**6. AI Review**
- AI reviews code for style, security, and completeness
- Updates label to "pr: ready for approval"

**7. Human Review**
```
/gh-review #123
```
*Human tests locally, approves implementation*
- Updates label to "pr: approved for merge"

**8. Merge & Cleanup**
- AI squash-merges PR to main
- Closes Issue #123
- Deletes branch and worktree
- Maintenance agent verifies cleanup

**Result**: Feature is live with clean commit history and no leftover branches.

## Troubleshooting

### Common Issues

**Issue stuck in wrong state:**
- Check issue labels match the current workflow stage
- Use `/gh-plan` to manually trigger planning if needed
- Contact repository maintainers if labels are incorrect

**Worktree conflicts:**
```bash
# List all worktrees
git worktree list

# Remove conflicting worktree
git worktree remove worktrees/issue-<number>-<slug>

# Prune stale references
git worktree prune
```

**Failed CI checks:**
- Review CI logs for specific errors
- Address linting, test, or build failures
- Re-run CI after fixes are committed

**Branch naming conflicts:**
- Ensure branch follows `issue-<number>-<slug>` format
- Check for existing branches with similar names
- Use descriptive slugs that avoid conflicts

**Stale work detection:**
- Issues inactive >7 days get flagged for review
- Check maintenance agent reports for stale work
- Re-engage or close abandoned issues

### Getting Help

- Check issue comments for specific error messages
- Review the project board for workflow status
- Contact team members with workflow expertise
- Check repository documentation for project-specific guidelines

## Glossary

**Worktree**: Isolated git working directory that shares history with the main repository, allowing parallel development without branch conflicts.

**Conventional Commits**: Standardized commit message format (`type(scope): description`) that enables automated changelog generation and semantic versioning.

**Slash Commands**: Special commands prefixed with `/` (like `/gh-issue`) that trigger workflow actions and AI agent behaviors.

**Draft PR**: GitHub pull request in draft state, indicating work in progress that is not yet ready for formal review.

**Squash Merge**: Git merge strategy that combines multiple commits into a single commit when merging a feature branch.

**CI/CD**: Continuous Integration/Continuous Deployment - automated testing and deployment pipelines that run on code changes.

**Label**: GitHub issue/PR tags that track workflow state and drive automation (e.g., "issue: needs planning", "pr: ready for approval").

**Maintenance Agent**: Background AI process that continuously monitors repository health, syncs labels, and performs cleanup tasks.

## Appendix

### Design Decision: Plan Approval Gate

**Decision:** Always wait for explicit human approval before implementation (see "needs plan approval" stage above).

**Rationale:**
- Ensures human oversight before significant work begins
- Prevents wasted effort from misaligned approaches
- Allows humans to provide strategic input on trade-offs
- Slight delays are acceptable given the benefits of alignment

**Alternatives considered:**
- Auto-proceed and get feedback on PR (faster but risks wasted effort)
- Hybrid approach based on complexity (adds decision complexity)

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

### Common Commands Quick Reference

> These commands support the workflow stages described above.

```bash
# Create worktree
git worktree add worktrees/issue-<num>-<slug>

# Fetch and rebase
git fetch origin && git rebase origin/main

# Remove worktree when done
git worktree remove worktrees/issue-<num>-<slug>

# View issue details
gh issue view <number>

# Create draft PR
gh pr create --draft --title "Title" --body "Description"

# View PR details
gh pr view <number>

# Quickfix workflow
git checkout main && git pull origin main
# make changes, test, then:
git add . && git commit -m "quickfix: description"
git push origin main
```

### Key Resources

- Issue templates: Create new issue and select appropriate template
- Project board: Track issue status and workflow stages
- CI status: Monitor automated checks and test results
- Repository settings: Branch protection, required reviews, auto-merge settings
