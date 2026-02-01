---
description: Use Opencode serve/attach pattern to avoid MCP cold boot on repeated runs
---

# Batch with server

## Process

- Start `opencode serve` once as a background process
- Run batch tasks with `opencode run --attach` against the server
- This avoids MCP server cold boot on every invocation

## Patterns

```bash
# Start server once
opencode serve --port 4096 &
sleep 3  # wait for server startup

# Run batch of tasks against it
for file in src/*.py; do
  opencode run --attach http://localhost:4096 "Review $file for type safety" &
done
wait

kill %1  # stop server
```

```bash
# With authentication
OPENCODE_SERVER_PASSWORD=secret opencode serve --port 4096 &
sleep 3

opencode run --attach http://opencode:secret@localhost:4096 "Task here"
```

```bash
# Web interface for monitoring batch progress
opencode web --port 4096 &
# Open http://localhost:4096 in browser to watch

opencode run --attach http://localhost:4096 "First task" &
opencode run --attach http://localhost:4096 "Second task" &
wait
```
