---
description: Merge approved PR, close issue, and clean up branch and worktree
---

## Context

Start by gathering issues and PRs approved for merge:

```bash
# Get issues approved for merge
gh issue list --state open --label "approved for merge" --limit 10 --json number,title,labels,author

# Get corresponding PRs
gh pr list --state open --limit 20 --json number,title,headRefName,mergeable,state,reviews
```

If $ARGUMENTS is empty, show the user recent issues with "approved for merge" label and ask them to select one.

If $ARGUMENTS contains only digits, treat it as an issue number. If $ARGUMENTS contains text, search for matching items from the recent list.

Once you have identified the issue, gather PR and cleanup details:

```bash
# Get issue details
gh issue view ISSUE_NUMBER --json title,body,labels,number,state

# Find linked PR
gh pr list --search "linked:ISSUE_NUMBER" --json number,title,headRefName,url,state,mergeable,reviews

# Get PR details
gh pr view PR_NUMBER --json title,body,state,headRefName,mergeable,mergeStateStatus

# Check if PR is actually mergeable
gh pr checks PR_NUMBER

# Identify worktree and branch to clean up
echo "Worktrees:"
git worktree list | grep "issue-ISSUE_NUMBER" || echo "No worktree found"

echo "Branches:"
git branch -a | grep "issue-ISSUE_NUMBER" || echo "No local branch found"
```

## Your Task

**Goal**: Complete the workflow by merging the approved PR, closing the issue, and cleaning up all artifacts (branch and worktree).

**Issue to merge**: Based on user input ($ARGUMENTS) or selection from recent issues

**Role**: You are Stage 7 (Merge & Cleanup) - the final stage in the workflow:
1. Create Issue → ... → 6. Human approval → **7. Merge & cleanup** ← (You are here - final stage!)

### Process

1. **Verify Merge Readiness**
   - Confirm issue has "approved for merge" label
   - Confirm linked PR exists and is approved
   - Verify PR is mergeable (no conflicts, checks passing)
   - Verify PR has required approvals
   - If not ready, explain what's blocking and ask user how to proceed

2. **Pre-Merge Safety Check**
   Show the user what will happen:
   - Which PR will be merged (number and title)
   - Which issue will be closed (number and title)
   - Which branch will be deleted
   - Which worktree will be removed (if exists)
   - Ask for confirmation before proceeding

3. **Execute Merge**
   Squash-merge the PR to main with clean commit message:

   ```bash
   # Squash merge with custom commit message
   # Format: <type>(<scope>): <description> (#PR_NUMBER)
   # Example: feat(auth): add OAuth2 authentication flow (#45)

   gh pr merge PR_NUMBER --squash --delete-branch --body "Closes #ISSUE_NUMBER"
   ```

   The commit message should:
   - Follow conventional commit format
   - Reference the PR number
   - Be derived from the PR title and issue context

4. **Close Issue**
   The issue should auto-close when PR is merged (if PR body contains "Closes #ISSUE_NUMBER").
   If not, manually close it:

   ```bash
   # Verify issue closed
   gh issue view ISSUE_NUMBER --json state

   # If still open, close it
   gh issue close ISSUE_NUMBER --comment "Merged in #PR_NUMBER"
   ```

5. **Clean Up Worktree**
   Remove the development worktree if it exists:

   ```bash
   # List worktrees to find the path
   WORKTREE_PATH=$(git worktree list | grep "issue-ISSUE_NUMBER" | awk '{print $1}')

   if [ -n "$WORKTREE_PATH" ]; then
     # Remove worktree
     git worktree remove "$WORKTREE_PATH" --force
     echo "Removed worktree: $WORKTREE_PATH"
   else
     echo "No worktree found for issue-ISSUE_NUMBER"
   fi

   # Prune stale worktree references
   git worktree prune
   ```

6. **Clean Up Branch**
   The branch should be auto-deleted if `--delete-branch` was used with merge.
   Verify and clean up any remaining references:

   ```bash
   # Check if remote branch still exists
   git fetch origin --prune

   # Check if local branch still exists
   if git branch | grep "issue-ISSUE_NUMBER"; then
     git branch -D issue-ISSUE_NUMBER-*
     echo "Deleted local branch"
   fi

   # Verify remote branch is gone
   git branch -r | grep "issue-ISSUE_NUMBER" || echo "Remote branch successfully deleted"
   ```

7. **Verify Cleanup**
   Confirm everything is cleaned up:

   ```bash
   # Verify issue is closed
   echo "Issue status:"
   gh issue view ISSUE_NUMBER --json state,closedAt

   # Verify PR is merged
   echo "PR status:"
   gh pr view PR_NUMBER --json state,merged,mergedAt

   # Verify worktree removed
   echo "Remaining worktrees:"
   git worktree list

   # Verify branch deleted
   echo "Branches for this issue:"
   git branch -a | grep "issue-ISSUE_NUMBER" || echo "All branches cleaned up"
   ```

8. **Summary**
   Provide a summary of what was completed:
   - ✅ PR #X merged to main
   - ✅ Issue #Y closed
   - ✅ Branch deleted
   - ✅ Worktree removed
   - Link to merged commit on GitHub

### Guidelines

- **Safety first**: Always confirm before merging and deleting
- **Clean commit history**: Use squash merge to maintain clean main branch
- **Conventional commits**: Ensure merge commit follows repository commit conventions
- **Complete cleanup**: Remove all artifacts (branches, worktrees) to avoid clutter
- **Verify thoroughly**: Check that issue is closed and all references are cleaned
- **Handle errors gracefully**: If merge fails, explain why and suggest remediation
- **Atomic operation**: If any step fails, document what was completed and what needs manual intervention

### Error Handling

If merge fails due to:

**Merge conflicts:**
- Guide user to rebase the branch: `cd worktree && git rebase main`
- Resolve conflicts, push, then retry merge

**Failed checks:**
- Show which checks failed: `gh pr checks PR_NUMBER`
- Wait for checks to pass, then retry

**Missing approvals:**
- Show approval status: `gh pr view PR_NUMBER --json reviews`
- Request necessary approvals, then retry

**Branch deleted but worktree remains:**
- Manually remove worktree: `git worktree remove path --force`

**Issue didn't auto-close:**
- Manually close: `gh issue close ISSUE_NUMBER --comment "Merged in #PR_NUMBER"`

## Success Criteria

Your work is complete when:
- ✅ PR successfully merged to main branch
- ✅ Merge commit follows conventional format
- ✅ Issue is closed
- ✅ Remote branch is deleted
- ✅ Local branch is deleted (if exists)
- ✅ Worktree is removed (if exists)
- ✅ No stale references remain
- ✅ User receives confirmation with link to merged commit
- ✅ Main branch is clean and up to date

## Next Steps

**After successful merge:**
- The workflow for this issue is complete
- User can pull latest main: `git pull origin main`
- Ready to start new work with `/gh-issue "next feature"`

**If cleanup incomplete:**
- Document what remains to be cleaned manually
- Provide specific commands for manual cleanup
- Update issue/PR with cleanup status
