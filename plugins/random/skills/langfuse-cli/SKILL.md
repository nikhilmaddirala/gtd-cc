---
name: langfuse-cli
description: Query and analyze Langfuse traces, sessions, observations, scores, and metrics via CLI using the Python SDK and REST API
version: 1.0.0
author: gtd-cc

# Skill metadata
domain: observability
category: llm-tracing
tags: [langfuse, observability, tracing, evaluation, llm, agents, cost-tracking]

# Skill classification
type: domain-expertise
complexity: intermediate
scope: comprehensive

# Usage information
prerequisites:
  - "Langfuse account (cloud or self-hosted)"
  - "LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY environment variables"
  - "LANGFUSE_HOST environment variable (defaults to https://cloud.langfuse.com)"
  - "Python 3.11+ with uv available"

provides:
  - "Trace querying and inspection"
  - "Session listing and drill-down"
  - "Observation analysis (generations, spans, events)"
  - "Score retrieval and evaluation workflows"
  - "Cost and token usage analytics via Metrics API"
  - "Direct REST API access via curl"

# Integration notes
compatible_tools:
  - langfuse (Python SDK)
  - curl
  - jq
  - uv
---

# Langfuse CLI interaction skill

Query, inspect, and analyze LLM traces, sessions, and evaluations from Langfuse using the Python SDK or direct REST API calls.

## Data model overview

Langfuse organizes data in a hierarchy:

- **Sessions** - group of related traces (e.g., a multi-turn conversation)
  - **Traces** - a single request/operation (e.g., one user message)
    - **Observations** - individual steps within a trace (nested)
      - **Generations** - LLM calls with input/output/tokens/cost
      - **Spans** - timed operations (tool calls, retrieval, etc.)
      - **Events** - point-in-time occurrences
- **Scores** - evaluation metrics attached to traces or observations

## Claude Code trace schema

Our hook captures enriched data from Claude Code transcripts. Each trace contains:

### Trace-level fields
- `name` - first line of user message (up to 80 chars)
- `sessionId` - groups all turns from one conversation
- `userId` - system username (`$USER`)
- `tags` - filterable labels: `model:opus`, `project:monorepo`, `branch:main`
- `version` - Claude Code version (e.g., `2.1.4`)
- `metadata.source` - always `"claude-code"`
- `metadata.turn_number` - turn index within session
- `metadata.claude_code_version` - Claude Code version
- `metadata.cwd` - working directory
- `metadata.git_branch` - active git branch
- `metadata.anthropic_base_url` - API endpoint
- `metadata.service_tier` - `"standard"` or other tier

### Generation observation fields
- `model` - full model ID (e.g., `claude-opus-4-5-20251101`)
- `usage.input` - total input tokens (new + cache_read + cache_creation)
- `usage.output` - output tokens
- `metadata.model_family` - simplified: `opus`, `sonnet`, or `haiku`
- `metadata.cache_read_tokens` - tokens read from prompt cache (bulk of context)
- `metadata.cache_creation_tokens` - tokens written to cache
- `metadata.new_input_tokens` - genuinely new input tokens
- `metadata.service_tier` - API service tier

### Tool span fields
- `name` - `"Tool: Read"`, `"Tool: Edit"`, `"Tool: Bash"`, etc.
- `input` - tool call arguments
- `output` - tool result
- `metadata.tool_name` - tool name
- `metadata.tool_id` - Anthropic tool_use ID

## Authentication

All methods require these environment variables:

```bash
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://us.cloud.langfuse.com"  # or your self-hosted URL
```

For REST API calls, use HTTP Basic Auth with public key as username and secret key as password.

## Quick start: Python SDK (recommended)

Use uv inline script metadata for zero-install execution:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "langfuse>=2.0.0",
# ]
# ///
import os
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

# List recent traces
traces = langfuse.api.trace.list(limit=10)
for t in traces.data:
    print(f"{t.id[:8]}  {t.name or 'unnamed'}  {t.timestamp}")
```

## Querying traces

### List traces with filters

```python
# Recent traces
traces = langfuse.api.trace.list(limit=20)

# Filter by user
traces = langfuse.api.trace.list(user_id="nikhilmaddirala", limit=50)

# Filter by tags (model family, project, branch)
traces = langfuse.api.trace.list(tags=["model:opus"], limit=50)
traces = langfuse.api.trace.list(tags=["project:monorepo"], limit=50)
traces = langfuse.api.trace.list(tags=["branch:main", "model:sonnet"], limit=50)

# Filter by name
traces = langfuse.api.trace.list(name="chat-completion", limit=20)
```

### Get a specific trace

```python
trace = langfuse.api.trace.get("trace-id-here")
print(f"Name: {trace.name}")
print(f"Input: {trace.input}")
print(f"Output: {trace.output}")
print(f"Session: {trace.session_id}")
print(f"Tags: {trace.tags}")
print(f"Metadata: {trace.metadata}")
```

### REST API equivalent (curl)

```bash
# List traces
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces?limit=10" | jq '.data[] | {id, name, timestamp}'

# Get specific trace
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/traces/TRACE_ID" | jq '.'
```

## Querying sessions

### List sessions

```python
sessions = langfuse.api.sessions.list(limit=20)
for s in sessions.data:
    print(f"{s.id}  traces={len(s.traces) if s.traces else '?'}  created={s.created_at}")
```

### Get session details

```python
session = langfuse.api.sessions.get("session-id-here")
print(f"Session: {session.id}")
print(f"Traces: {len(session.traces)}")
for trace in session.traces:
    print(f"  - {trace.id[:8]} {trace.name} ({trace.timestamp})")
```

### REST API equivalent

```bash
# List sessions
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/sessions?limit=10" | jq '.data[] | {id, createdAt}'

# Get session with traces
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/sessions/SESSION_ID" | jq '.'
```

## Querying observations

Observations are the individual steps (generations, spans, events) within traces.

### List observations (v2 API recommended)

```python
# All observations for a trace
obs = langfuse.api.observations_v_2.get_many(
    trace_id="trace-id-here",
    limit=100,
    fields="core,basic,usage"  # selective fields for performance
)
for o in obs.data:
    print(f"  {o.type}: {o.name} cost={o.calculated_total_cost} tokens={o.usage}")

# Filter by type
generations = langfuse.api.observations_v_2.get_many(
    type="GENERATION",
    limit=50,
    fields="core,basic,usage,io"
)

# Get a specific observation
obs = langfuse.api.observations.get("observation-id")
print(f"Model: {obs.model}")
print(f"Input: {obs.input}")
print(f"Output: {obs.output}")
print(f"Tokens: {obs.usage}")
```

### Field selection options

The v2 observations API supports selective field retrieval for performance:

- `core` - id, traceId, type, name, timestamps
- `basic` - model, level, status, version, metadata
- `usage` - token counts and cost
- `io` - input/output content (can be large)

### REST API equivalent

```bash
# List observations for a trace
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations?traceId=TRACE_ID&limit=50" | \
  jq '.data[] | {id, type, name, model, calculatedTotalCost}'

# Get specific observation with full I/O
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/observations/OBS_ID" | jq '.'
```

## Querying scores

Scores are evaluation metrics attached to traces or observations.

### List and filter scores

```python
# Get scores for a specific trace
scores = langfuse.api.score.list(trace_id="trace-id-here")
for s in scores.data:
    print(f"  {s.name}: {s.value} (source={s.source})")

# Get a specific score
score = langfuse.api.score_v_2.get(score_ids="score-id-here")
```

### REST API equivalent

```bash
# List scores
curl -s -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/scores?limit=20" | \
  jq '.data[] | {name, value, traceId, source}'
```

## Metrics API (analytics and aggregation)

The Metrics API provides aggregated analytics across traces and observations.

### Available measures and aggregations

Measures: `count`, `latency`, `totalCost`, `totalTokens`, `timeToFirstToken`, `countScores`

Aggregations: `sum`, `avg`, `count`, `max`, `min`, `p50`, `p75`, `p90`, `p95`, `p99`

### Cost by model

```bash
curl -s -X POST -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/v2/metrics" \
  -H "Content-Type: application/json" \
  -d '{
    "view": "observations",
    "metrics": [{"measure": "totalCost", "aggregation": "sum"}],
    "dimensions": [{"field": "providedModelName"}],
    "filters": [],
    "fromTimestamp": "2026-01-01T00:00:00Z",
    "toTimestamp": "2026-01-24T00:00:00Z",
    "orderBy": [{"field": "totalCost_sum", "direction": "desc"}]
  }' | jq '.'
```

### Token usage over time

```bash
curl -s -X POST -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/v2/metrics" \
  -H "Content-Type: application/json" \
  -d '{
    "view": "observations",
    "metrics": [
      {"measure": "totalTokens", "aggregation": "sum"},
      {"measure": "totalCost", "aggregation": "sum"}
    ],
    "dimensions": [{"field": "startTime", "granularity": "day"}],
    "filters": [],
    "fromTimestamp": "2026-01-01T00:00:00Z",
    "toTimestamp": "2026-01-24T00:00:00Z",
    "orderBy": [{"field": "startTime", "direction": "asc"}]
  }' | jq '.'
```

### Latency percentiles

```bash
curl -s -X POST -u "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" \
  "$LANGFUSE_HOST/api/public/v2/metrics" \
  -H "Content-Type: application/json" \
  -d '{
    "view": "observations",
    "metrics": [
      {"measure": "latency", "aggregation": "p50"},
      {"measure": "latency", "aggregation": "p95"},
      {"measure": "latency", "aggregation": "p99"}
    ],
    "dimensions": [{"field": "providedModelName"}],
    "filters": [{"field": "type", "operator": "=", "value": "GENERATION"}],
    "fromTimestamp": "2026-01-01T00:00:00Z",
    "toTimestamp": "2026-01-24T00:00:00Z"
  }' | jq '.'
```

## Common workflows

### Debugging a failed agent run

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["langfuse>=2.0.0"]
# ///
import os, sys
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

trace_id = sys.argv[1] if len(sys.argv) > 1 else None
if not trace_id:
    print("Usage: ./debug_trace.py <trace-id>")
    sys.exit(1)

trace = langfuse.api.trace.get(trace_id)
print(f"Trace: {trace.name} ({trace.id})")
print(f"Session: {trace.session_id}")
print(f"Input: {str(trace.input)[:200]}")
print(f"Output: {str(trace.output)[:200]}")
print()

# Get all observations
obs = langfuse.api.observations_v_2.get_many(
    trace_id=trace_id, limit=100, fields="core,basic,usage,io"
)
print(f"Observations ({len(obs.data)}):")
for o in obs.data:
    status = "ERROR" if o.level == "ERROR" else "ok"
    cost = f"${o.calculated_total_cost:.4f}" if o.calculated_total_cost else "n/a"
    print(f"  [{status}] {o.type}: {o.name} | model={o.model} cost={cost}")
    if o.level == "ERROR":
        print(f"       Output: {str(o.output)[:300]}")
```

### Daily cost summary

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["langfuse>=2.0.0", "rich>=13.0.0"]
# ///
import os
from datetime import datetime, timedelta
from langfuse import Langfuse
from rich.table import Table
from rich.console import Console

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

console = Console()

# Get recent traces with cost info
traces = langfuse.api.trace.list(limit=100)

table = Table(title="Recent Traces - Cost Summary")
table.add_column("Trace ID", style="dim")
table.add_column("Name")
table.add_column("Timestamp")
table.add_column("Tags")

for t in traces.data:
    table.add_row(
        t.id[:12],
        t.name or "unnamed",
        str(t.timestamp)[:19],
        ", ".join(t.tags) if t.tags else "-",
    )

console.print(table)
```

### List recent sessions with trace counts

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["langfuse>=2.0.0", "rich>=13.0.0"]
# ///
import os
from langfuse import Langfuse
from rich.table import Table
from rich.console import Console

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

console = Console()
sessions = langfuse.api.sessions.list(limit=20)

table = Table(title="Recent Sessions")
table.add_column("Session ID", style="dim")
table.add_column("Created")
table.add_column("Traces")

for s in sessions.data:
    table.add_row(
        s.id[:20] if s.id else "?",
        str(s.created_at)[:19] if s.created_at else "?",
        str(len(s.traces)) if s.traces else "?",
    )

console.print(table)
```

### Evaluate agent quality (attach scores)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["langfuse>=2.0.0"]
# ///
import os, sys
from langfuse import Langfuse

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

trace_id = sys.argv[1]
score_name = sys.argv[2] if len(sys.argv) > 2 else "quality"
score_value = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
comment = sys.argv[4] if len(sys.argv) > 4 else None

langfuse.score(
    trace_id=trace_id,
    name=score_name,
    value=score_value,
    comment=comment,
)
langfuse.flush()
print(f"Score '{score_name}={score_value}' attached to trace {trace_id}")
```

Usage: `./score_trace.py <trace-id> quality 0.8 "Good but missed edge case"`

### Cache token analysis and true cost breakdown

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["langfuse>=2.0.0", "rich>=13.0.0"]
# ///
import os
from langfuse import Langfuse
from rich.table import Table
from rich.console import Console

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

console = Console()

# Get recent generations with cache data
obs = langfuse.api.observations_v_2.get_many(
    type="GENERATION", limit=20, fields="core,basic,usage"
)

table = Table(title="Cache Token Analysis")
table.add_column("Model", style="dim")
table.add_column("New Input")
table.add_column("Cache Read")
table.add_column("Cache Create")
table.add_column("Output")
table.add_column("Cache Hit %", style="green")
table.add_column("Cost")

for o in obs.data:
    meta = o.metadata or {}
    cache_read = meta.get("cache_read_tokens", 0)
    cache_create = meta.get("cache_creation_tokens", 0)
    new_input = meta.get("new_input_tokens", 0)
    total_input = cache_read + cache_create + new_input
    cache_pct = f"{(cache_read / total_input * 100):.0f}%" if total_input > 0 else "n/a"
    cost = f"${o.calculated_total_cost:.4f}" if o.calculated_total_cost else "n/a"

    table.add_row(
        meta.get("model_family", o.model or "?"),
        str(new_input),
        str(cache_read),
        str(cache_create),
        str(o.usage.output if o.usage else 0),
        cache_pct,
        cost,
    )

console.print(table)
```

### Filter traces by model and project

```bash
# Get only Opus traces from the monorepo project
AUTH=$(echo -n "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" | base64 -w0)
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=20&tags=model:opus&tags=project:monorepo" | \
  jq '.data[] | {name, timestamp: .timestamp[0:19], cost: .totalCost}'
```

### Session overview (grouped conversations)

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["langfuse>=2.0.0", "rich>=13.0.0"]
# ///
import os
from langfuse import Langfuse
from rich.table import Table
from rich.console import Console

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)

console = Console()
sessions = langfuse.api.sessions.list(limit=10)

table = Table(title="Recent Sessions (Conversations)")
table.add_column("Session ID", style="dim")
table.add_column("Created")
table.add_column("Turns")
table.add_column("First Message")

for s in sessions.data:
    # Get traces for this session to find the first message
    first_msg = "?"
    if s.traces and len(s.traces) > 0:
        first_trace = s.traces[-1]  # oldest trace
        if hasattr(first_trace, "name"):
            first_msg = first_trace.name[:50]

    table.add_row(
        s.id[:16] if s.id else "?",
        str(s.created_at)[:19] if s.created_at else "?",
        str(len(s.traces)) if s.traces else "?",
        first_msg,
    )

console.print(table)
```

## Useful one-liners

Note: On NixOS/systems where `base64` adds line breaks, use `base64 -w0` to suppress them:

```bash
# Set up auth (use in all curl commands below)
AUTH=$(echo -n "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" | base64 -w0)
```

### Get the latest trace ID

```bash
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=1" | jq -r '.data[0].id'
```

### Count traces today

```bash
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=1" | jq '.meta.totalItems'
```

### Get all generation models used

```bash
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/observations?type=GENERATION&limit=100" | \
  jq -r '[.data[].model] | unique | .[]'
```

### Filter by model family tag

```bash
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=20&tags=model:opus" | \
  jq '.data[] | {name, cost: .totalCost, tags}'
```

### Get Claude Code version distribution

```bash
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=100" | \
  jq -r '[.data[].metadata.claude_code_version] | group_by(.) | map({version: .[0], count: length}) | .[]'
```

### Export trace inputs/outputs as JSONL

```bash
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=100" | \
  jq -c '.data[] | {id, name, input, output, tags, userId, sessionId}' > traces_export.jsonl
```

## Pagination

All list endpoints support cursor-based pagination:

```python
# Paginate through all traces
all_traces = []
cursor = None
while True:
    result = langfuse.api.trace.list(limit=100, cursor=cursor)
    all_traces.extend(result.data)
    if not result.meta.next_cursor:
        break
    cursor = result.meta.next_cursor

print(f"Total traces: {len(all_traces)}")
```

## References

- [Langfuse API reference](https://api.reference.langfuse.com/)
- [Public API documentation](https://langfuse.com/docs/api-and-data-platform/features/public-api)
- [Query via SDK](https://langfuse.com/docs/api-and-data-platform/features/query-via-sdk)
- [Metrics API](https://langfuse.com/docs/metrics/features/metrics-api)
- [Observations API v2](https://langfuse.com/docs/api-and-data-platform/features/observations-api)
- [Scores via API/SDK](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)
- [Tracing data model](https://langfuse.com/docs/observability/data-model)
- [OpenAPI spec](https://cloud.langfuse.com/generated/api/openapi.yml)
