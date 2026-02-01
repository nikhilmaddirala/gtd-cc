---
description: Use AI agent CLIs in GitHub Actions, GitLab CI, and other CI pipelines
---

# CI/CD integration

## Process

- Use `claude -p` with `--dangerously-skip-permissions` for fully automated pipelines
- Set `--max-turns` and `--max-budget-usd` to bound execution
- Use `--output-format json` for machine-parseable results

## Patterns

```bash
# Automated test-fix loop in CI
claude -p "Run the test suite. If tests fail, fix the code and re-run." \
  --allowedTools "Bash,Read,Edit" \
  --max-turns 10 \
  --max-budget-usd 3.00 \
  --output-format json \
  --dangerously-skip-permissions
```

```bash
# PR review
gh pr diff "$PR_NUMBER" | claude -p \
  --append-system-prompt "You are a code reviewer. Flag bugs, security issues, and style problems." \
  --output-format json \
  --max-budget-usd 1.00
```

```bash
# Automated commit
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *)" "Bash(git log *)" "Bash(git status *)" "Bash(git commit *)" \
  --dangerously-skip-permissions
```

```bash
# Opencode GitHub agent (sets up Actions workflow)
opencode github install
opencode github run --token "$GITHUB_TOKEN"
```
