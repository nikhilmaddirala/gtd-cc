---
description: Perform code review on pull requests for quality and compliance
allowed_tools:
  - Bash(gh issue:*)
  - Bash(gh pr:*)
  - Bash(gh search:*)
---

## Overview

Provide comprehensive code reviews for pull requests, checking for implementation correctness, readme compliance, and significant bugs.

## Context

Repository and PR information gathered via:
- PR details, changes summary, and state
- Original issue and any approved implementation plan
- Git history and context of modified code
- Existing README.md files in modified directories
- CI checks and status signals

Review structure follows the [PR review template](../../_common/templates/pr-review-checklist.md) format with merge blockers and nice-to-haves.

## Your Task

**Goal**: Review PR changes for correctness and compliance, identifying only real and significant issues.

**Process**:
1. Check if the PR is closed, a draft, automated, or already reviewed by you. If so, do not proceed.
2. Fetch the PR details and summarize the changes.
3. Inspect CI signals and status checks:
   - Review any failing or pending checks
   - Determine if CI failures are blocking or expected
   - Assess impact on merge readiness
4. Review the PR changes for:
   - Addresses the original issue and aligns with any approved implementation plan
   - Compliance with relevant README.md files in modified directories
   - Obvious bugs and issues in the code changes themselves (focus on significant issues, not nitpicks)
   - Any issues based on git history and context of the modified code
5. Filter issues to only those that are real and significant (not false positives, nitpicks, or pre-existing issues).
6. Comment on the PR with findings using the review template format (merge blockers vs nice-to-haves).

## Guidelines

- Use `gh` to interact with Github (e.g., to fetch a pull request, or to create inline comments), rather than web fetch
- Make a todo list first
- You must cite and link each bug (e.g., if referring to a README.md, you must link it)
- Avoid false positives:
  - Pre-existing issues
  - False positives that don't hold up to scrutiny
  - Nitpicks a senior engineer wouldn't mention
  - Issues that linters/type checkers/tests will catch (assume CI handles these)
  - General code quality issues, unless explicitly required in README.md
  - Issues called out in README.md but explicitly silenced in code (e.g., lint ignore comments)
- When citing issues in your comment, use this link format precisely:
  - `https://github.com/owner/repo/blob/[full-sha]/path/file#L[start]-L[end]`
  - Requires full git SHA (not abbreviated)
  - Hash (#) sign after file name
  - Line range format is L[start]-L[end]
  - Include at least 1 line of context before and after the issue
- Comment on the PR following the [PR review template](./references/pr-review-template.md) format

## Success Criteria

- ✅ PR has been reviewed for implementation correctness
- ✅ Compliance with README.md requirements checked
- ✅ CI signals and status checks evaluated for merge readiness
- ✅ Only real and significant issues identified (false positives filtered out)
- ✅ Comment posted on PR following the review template with merge blockers and nice-to-haves
- ✅ All issues cited with proper links, full SHAs, and line ranges
