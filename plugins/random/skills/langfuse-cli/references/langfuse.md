# Langfuse reference

Technical reference for the Langfuse API, Claude Code trace schema, and integration patterns.

## API endpoints

Base URL: `$LANGFUSE_HOST/api/public/` (e.g., `https://us.cloud.langfuse.com/api/public/`)

Auth: HTTP Basic with `LANGFUSE_PUBLIC_KEY` as username, `LANGFUSE_SECRET_KEY` as password.

### Core endpoints
- `GET /traces` - list traces (params: `limit`, `user_id`, `tags`, `name`, `cursor`)
- `GET /traces/{id}` - get single trace
- `GET /sessions` - list sessions (params: `limit`, `cursor`)
- `GET /sessions/{id}` - get session with traces
- `GET /observations` - list observations (params: `traceId`, `type`, `limit`, `cursor`)
- `GET /observations/{id}` - get single observation
- `GET /scores` - list scores (params: `trace_id`, `limit`)
- `POST /v2/metrics` - aggregated metrics (Cloud-only, Beta)
- `POST /ingestion` - ingest traces/observations (legacy, prefer OTel)

### OpenAPI spec
- Full spec: `https://cloud.langfuse.com/generated/api/openapi.yml`
- API reference: `https://api.reference.langfuse.com/`
- Postman collection: `https://cloud.langfuse.com/generated/postman/collection.json`

## Claude Code enriched trace schema

The hook at `dragonix/modules/home/ai/claude/hooks/langfuse_hook.py` captures the following from Claude Code transcripts:

### Trace attributes (set via propagate_attributes)
- `sessionId` - conversation UUID (groups multi-turn interactions)
- `userId` - system `$USER` (e.g., `nikhilmaddirala`)
- `tags` - filterable labels:
  - `model:opus`, `model:sonnet`, `model:haiku` — model family
  - `project:<name>` — derived from project directory (e.g., `project:monorepo`)
  - `branch:<name>` — git branch (e.g., `branch:main`)
- `version` - Claude Code version (e.g., `2.1.4`)

### Trace metadata
- `source` - always `"claude-code"`
- `turn_number` - sequential turn index within session
- `claude_code_version` - Claude Code version
- `cwd` - working directory path
- `git_branch` - active git branch
- `anthropic_base_url` - API endpoint (`$ANTHROPIC_BASE_URL` or default)
- `service_tier` - API service tier (e.g., `"standard"`)

### Generation observation
- `model` - full model ID (e.g., `claude-opus-4-5-20251101`)
- `usage.input` - total input tokens (new + cache_read + cache_creation)
- `usage.output` - output tokens
- `usage.total` - sum of input + output
- `metadata.model_family` - simplified: `opus`, `sonnet`, `haiku`
- `metadata.cache_read_tokens` - tokens read from prompt cache (typically the largest component)
- `metadata.cache_creation_tokens` - tokens written to cache this turn
- `metadata.new_input_tokens` - genuinely new (non-cached) input tokens
- `metadata.tool_count` - number of tool calls in this turn
- `metadata.service_tier` - API service tier

### Tool spans
- `name` - prefixed with `"Tool: "` (e.g., `"Tool: Read"`, `"Tool: Bash"`)
- `input` - tool call arguments (file paths, commands, etc.)
- `output` - tool result content
- `metadata.tool_name` - raw tool name
- `metadata.tool_id` - Anthropic `tool_use_id`

## Token cost model

Anthropic pricing tiers (relevant for cost calculations):
- **New input tokens** - full input price
- **Cache read tokens** - ~90% cheaper than new input
- **Cache creation tokens** - ~25% more expensive than new input
- **Output tokens** - most expensive per token

Langfuse calculates cost based on `model` + `usage.input`/`usage.output`. Since we combine all input types into `usage.input`, the calculated cost is an approximation. The metadata breakdown (`cache_read_tokens`, `new_input_tokens`, `cache_creation_tokens`) allows precise cost calculation:

```python
# Anthropic pricing (per million tokens, example for Opus 4.5)
PRICE_INPUT = 15.0       # new input tokens
PRICE_CACHE_READ = 1.5   # cache read (90% discount)
PRICE_CACHE_CREATE = 18.75  # cache creation (25% premium)
PRICE_OUTPUT = 75.0      # output tokens

true_cost = (
    (new_input / 1_000_000) * PRICE_INPUT
    + (cache_read / 1_000_000) * PRICE_CACHE_READ
    + (cache_create / 1_000_000) * PRICE_CACHE_CREATE
    + (output / 1_000_000) * PRICE_OUTPUT
)
```

## Metrics API v2

Endpoint: `POST /api/public/v2/metrics` (Cloud-only, Beta)

### Query structure
```json
{
  "view": "observations",
  "metrics": [{"measure": "totalCost", "aggregation": "sum"}],
  "dimensions": [{"field": "providedModelName"}],
  "filters": [],
  "fromTimestamp": "2026-01-01T00:00:00Z",
  "toTimestamp": "2026-01-24T00:00:00Z",
  "orderBy": [{"field": "totalCost_sum", "direction": "desc"}]
}
```

### Available views
- `observations` - observation-level data with optional trace aggregations
- `scores-numeric` - numeric and boolean scores
- `scores-categorical` - categorical scores

### Measures
`count`, `latency`, `totalCost`, `totalTokens`, `timeToFirstToken`, `countScores`

### Aggregations
`sum`, `avg`, `count`, `max`, `min`, `p50`, `p75`, `p90`, `p95`, `p99`

### Limitations
- High-cardinality fields (id, traceId, userId, sessionId) cannot be used for grouping
- Default row limit: 100

## Python SDK patterns

### Initialization
```python
from langfuse import Langfuse, propagate_attributes

langfuse = Langfuse(
    public_key=os.environ["LANGFUSE_PUBLIC_KEY"],
    secret_key=os.environ["LANGFUSE_SECRET_KEY"],
    host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
)
```

### Query methods
- `langfuse.api.trace.list(limit, user_id, tags, name, cursor)` → traces
- `langfuse.api.trace.get(trace_id)` → single trace
- `langfuse.api.sessions.list(limit, cursor)` → sessions
- `langfuse.api.sessions.get(session_id)` → session with traces
- `langfuse.api.observations_v_2.get_many(trace_id, type, limit, fields)` → observations
- `langfuse.api.observations.get(observation_id)` → single observation
- `langfuse.api.score.list(trace_id)` → scores
- `langfuse.api.score_v_2.get(score_ids)` → single score

### Fields parameter (observations v2)
- `core` - id, traceId, type, name, timestamps
- `basic` - model, level, status, version, metadata
- `usage` - token counts and cost
- `io` - input/output content (can be large)

## Known issues

### session_id not set in official Claude Code guide

The [Claude Code integration guide](https://langfuse.com/integrations/other/claude-code) puts `session_id` in `metadata` which does NOT enable Langfuse session grouping. The fix is to use `propagate_attributes(session_id=...)`:

```python
with langfuse.start_as_current_span(name=trace_name, ...) as span:
    with propagate_attributes(session_id=session_id, user_id=user_id, tags=tags):
        # child observations inherit session_id
        ...
```

Issue filed: [langfuse/langfuse-docs](https://github.com/langfuse/langfuse-docs) (pending)

### Timing data is approximate

The Stop hook processes transcripts after the response completes, so all span timestamps are near-identical. Real latency/TTFT data would require a proxy-level integration.

## External references
- [API Reference](https://api.reference.langfuse.com/)
- [Public API docs](https://langfuse.com/docs/api-and-data-platform/features/public-api)
- [Sessions docs](https://langfuse.com/docs/observability/features/sessions)
- [Observations API v2](https://langfuse.com/docs/api-and-data-platform/features/observations-api)
- [Metrics API](https://langfuse.com/docs/metrics/features/metrics-api)
- [Scores via SDK](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)
- [Data model](https://langfuse.com/docs/observability/data-model)
- [Python SDK v3](https://langfuse.com/changelog/2025-06-05-python-sdk-v3-generally-available)
- [Claude Code Integration Guide](https://langfuse.com/integrations/other/claude-code)
- [Claude Agent SDK Integration](https://langfuse.com/integrations/frameworks/claude-agent-sdk)
