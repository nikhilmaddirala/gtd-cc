---
description: Route tasks to different tools and models based on complexity and cost
---

# Cost-optimized routing

## Process

- Assess task complexity (simple lookup, medium analysis, complex refactoring)
- Route to the cheapest tool that can handle it
- Set budget caps on expensive tasks

## Patterns

```bash
# Tier 1: free - use Opencode with free rotating models
opencode run "List all files that import the auth module"

# Tier 2: cheap - use Claude Sonnet for medium tasks
claude -p "Review this function for bugs" --model sonnet --allowedTools "Read"

# Tier 3: expensive - reserve Opus for complex tasks with budget cap
claude -p "Refactor the entire auth system to use JWT" --model opus \
  --allowedTools "Read,Edit,Bash" --max-budget-usd 5.00
```

```bash
# Use fallback model to handle overload gracefully
claude -p "Complex refactoring task" \
  --model opus \
  --fallback-model sonnet \
  --max-budget-usd 10.00
```
