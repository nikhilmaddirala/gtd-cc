---
description: Run multiple agent CLI instances concurrently for independent tasks
---

# Parallel tasks

## Process

- Launch multiple `claude -p` or `opencode run` instances with `&`
- Write each result to a temp file
- `wait` for all to complete
- Optionally combine results with another agent call

## Patterns

```bash
# Run multiple reviews in parallel
claude -p "Review auth/ for security issues" --output-format json > /tmp/auth-review.json &
claude -p "Review api/ for performance issues" --output-format json > /tmp/api-review.json &
wait

# Combine results
cat /tmp/auth-review.json /tmp/api-review.json | \
  claude -p "Summarize these two code reviews into a single report" --output-format json
```

```bash
# Parallel analysis of multiple files
for file in src/services/*.py; do
  claude -p "Review $file for error handling issues" \
    --output-format json \
    --allowedTools "Read" \
    --max-turns 3 \
    > "/tmp/review-$(basename $file).json" &
done
wait

# Aggregate
cat /tmp/review-*.json | claude -p "Combine these reviews into a prioritized list"
```
