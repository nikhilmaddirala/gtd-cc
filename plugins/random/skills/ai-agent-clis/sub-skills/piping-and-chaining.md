---
description: Pipe output between agent CLI instances for multi-step workflows
---

# Piping and chaining

## Process

- Use `--output-format json` on the source step and `jq` to extract the result
- Pipe into the next `claude -p` instance via stdin or variable
- For structured extraction, use `--json-schema` and parse `structured_output`

## Patterns

```bash
# Get structured analysis, then use it
result=$(claude -p "Analyze the test failures in test_auth.py" \
  --output-format json \
  --allowedTools "Read,Bash" \
  | jq -r '.result')

# Feed result into another task
echo "$result" | claude -p "Based on this analysis, fix the root cause" \
  --allowedTools "Read,Edit,Bash"
```

```bash
# Pipe a PR diff into a security review
gh pr diff 123 | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

```bash
# Chain with jq for structured extraction
claude -p "Extract all API endpoints from the codebase" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"endpoints":{"type":"array","items":{"type":"object","properties":{"method":{"type":"string"},"path":{"type":"string"}}}}}}' \
  | jq '.structured_output.endpoints[] | "\(.method) \(.path)"'
```
