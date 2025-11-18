---
description: Perform code review on pull requests for quality and compliance
allowed_tools:
  - Bash(gh issue view:*)
  - Bash(gh search:*)
  - Bash(gh issue list:*)
  - Bash(gh pr comment:*)
  - Bash(gh pr diff:*)
  - Bash(gh pr view:*)
  - Bash(gh pr review:*)
  - Bash(gh pr list:*)
---

## Overview

Provide comprehensive code reviews for pull requests, checking for implementation correctness, readme compliance, and significant bugs.

## Context

Repository and PR information gathered via:
- PR details, changes summary, and state
- Original issue and any approved implementation plan
- Git history and context of modified code
- Existing README.md files in modified directories

## Your Task

**Goal**: Review PR changes for correctness and compliance, identifying only real and significant issues.

**Process**:
1. Check if the PR is closed, a draft, automated, or already reviewed by you. If so, do not proceed.
2. Fetch the PR details and summarize the changes.
3. Review the PR changes for:
   - Addresses the original issue and aligns with any approved implementation plan
   - Compliance with relevant README.md files in modified directories
   - Obvious bugs and issues in the code changes themselves (focus on significant issues, not nitpicks)
   - Any issues based on git history and context of the modified code
4. Filter issues to only those that are real and significant (not false positives, nitpicks, or pre-existing issues).
5. Comment on the PR with any issues found, or indicate no issues if clean.

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
- When linking to code, follow this format precisely: `https://github.com/owner/repo/blob/[sha]/path/file#L[start]-L[end]`
  - Requires full git sha
  - Repo name must match the repo you're code reviewing
  - # sign after the file name
  - Line range format is L[start]-L[end]
  - Provide at least 1 line of context before and after the issue
- For your comment, follow the following format precisely (assuming for this example that you found 3 issues):

---

## Code review

Found 3 issues:

1. <brief description of bug> (README.md says "<...>")

<link to file and line with full sha1 + line range for context, eg. https://github.com/anthropics/claude-code/blob/1d54823877c4de72b2316a64032a54afc404e619/README.md#L13-L17>

2. <brief description of bug> (some/other/README.md says "<...>")

<link to file and line with full sha1 + line range for context>

3. <brief description of bug> (bug due to <file and code snippet>)

<link to file and line with full sha1 + line range for context>

---

- Or, if you found no issues:

---

## Auto code review

No issues found. Checked for bugs and README.md compliance.

---

## Success Criteria

- ✅ PR has been reviewed for implementation correctness
- ✅ Compliance with README.md requirements checked
- ✅ Only real and significant issues identified (false positives filtered out)
- ✅ Comment posted on PR with findings or confirmation of no issues
- ✅ All issues cited with proper links and context
