# Setting up Langfuse with Claude Agent SDK

Complete guide to enabling LLM observability for custom agents built with Claude Agent SDK (Python).

## Overview

The Claude Agent SDK can be instrumented with Langfuse via OpenTelemetry. This provides automatic tracing of all tool calls and model completions, plus manual enrichment with user/session metadata.

## Architecture

```
Your Agent Application
    ↓ (uses Claude Agent SDK)
OpenTelemetry Instrumentation (via LangSmith)
    ↓ (exports spans)
Langfuse OTel Endpoint
    ↓
Langfuse Cloud/Self-hosted
```

## Installation

```bash
pip install langfuse anthropic-agent-sdk
# For OTel instrumentation via LangSmith bridge
pip install "langsmith[claude-agent-sdk]" "langsmith[otel]"
```

Or with uv inline metadata:

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "langfuse>=3.0.0",
#   "anthropic-agent-sdk>=0.1.0",
#   "langsmith[claude-agent-sdk]",
#   "langsmith[otel]",
# ]
# ///
```

## Environment variables

```bash
# Langfuse credentials
export LANGFUSE_PUBLIC_KEY="pk-lf-..."
export LANGFUSE_SECRET_KEY="sk-lf-..."
export LANGFUSE_HOST="https://us.cloud.langfuse.com"  # or EU: https://cloud.langfuse.com

# Anthropic API
export ANTHROPIC_API_KEY="sk-ant-..."

# Enable OTel tracing via LangSmith bridge
export LANGSMITH_OTEL_ENABLED="true"
export LANGSMITH_OTEL_ONLY="true"
export LANGSMITH_TRACING="true"
```

## Basic setup

### 1. Initialize Langfuse client

```python
import os
from langfuse import get_client

langfuse = get_client()

# Verify authentication
if langfuse.auth_check():
    print("Langfuse authenticated!")
else:
    print("Authentication failed - check credentials")
```

### 2. Enable OpenTelemetry instrumentation

```python
from langsmith.integrations.claude_agent_sdk import configure_claude_agent_sdk

# This patches the Agent SDK to emit OTel spans
configure_claude_agent_sdk()
```

### 3. Run your agent

```python
from anthropic_agent_sdk import Agent, Tool

# Define tools
@Tool
def get_weather(city: str) -> str:
    return f"Weather in {city}: 72°F, sunny"

# Create agent
agent = Agent(
    model="claude-sonnet-4-20250514",
    tools=[get_weather],
    system="You are a helpful assistant.",
)

# Run - traces are automatically captured
response = agent.run("What's the weather in San Francisco?")
print(response)

# Ensure traces are flushed
langfuse.flush()
```

## Enriching traces with metadata

Use `propagate_attributes` to add user tracking, session grouping, and custom metadata:

### Decorator pattern

```python
from langfuse import observe, propagate_attributes

@observe()
def process_user_request(user_id: str, session_id: str, query: str):
    with propagate_attributes(
        user_id=user_id,
        session_id=session_id,
        tags=["agent", "production"],
        metadata={"source": "api", "client_version": "1.0"},
        version="1.0.0",
    ):
        result = agent.run(query)

        # Optionally update the trace with final I/O
        langfuse.update_current_trace(
            input={"query": query},
            output={"response": result},
        )

        return result
```

### Context manager pattern

```python
from langfuse import get_client, propagate_attributes

langfuse = get_client()

with langfuse.start_as_current_observation(as_type="span", name="agent-request"):
    with propagate_attributes(
        user_id="user_123",
        session_id="session_abc",
        tags=["agent"],
    ):
        result = agent.run("Hello, agent!")

langfuse.flush()
```

## Session grouping for multi-turn conversations

To group multiple agent interactions into a single session (e.g., a chat thread):

```python
import uuid

class ChatSession:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.session_id = str(uuid.uuid4())
        self.turn_count = 0

    def send_message(self, message: str) -> str:
        self.turn_count += 1

        with langfuse.start_as_current_observation(
            as_type="span",
            name=f"Turn {self.turn_count}: {message[:50]}",
        ):
            with propagate_attributes(
                user_id=self.user_id,
                session_id=self.session_id,
                tags=["chat", f"turn:{self.turn_count}"],
            ):
                return agent.run(message)

# Usage
session = ChatSession(user_id="alice")
session.send_message("Hi!")
session.send_message("What can you help me with?")
session.send_message("Tell me a joke")

langfuse.flush()
```

All three turns will appear grouped under a single session in Langfuse.

## Adding evaluation scores

Attach scores to traces for quality evaluation:

```python
# After getting a response, score it
langfuse.score(
    trace_id=current_trace_id,  # or use langfuse.get_current_trace_id()
    name="quality",
    value=0.9,
    comment="Good response, answered the question",
)

# Categorical scores
langfuse.score(
    trace_id=current_trace_id,
    name="sentiment",
    value="positive",
)
```

## Cost tracking

The OTel instrumentation automatically captures token usage. To access cost data:

```python
# Via API after traces are ingested
traces = langfuse.api.trace.list(limit=10)
for t in traces.data:
    print(f"{t.name}: ${t.total_cost:.4f}")

# For precise cost with cache breakdown, check generation metadata
obs = langfuse.api.observations_v_2.get_many(
    trace_id=trace_id,
    type="GENERATION",
    fields="core,usage",
)
for o in obs.data:
    print(f"Input: {o.usage.input}, Output: {o.usage.output}, Cost: ${o.calculated_total_cost}")
```

## Chainlit integration

If using Chainlit for the UI, wrap your agent handlers:

```python
import chainlit as cl
from langfuse import observe, propagate_attributes

@cl.on_message
@observe()
async def handle_message(message: cl.Message):
    user_id = cl.user_session.get("user_id", "anonymous")
    session_id = cl.user_session.get("session_id", str(uuid.uuid4()))

    with propagate_attributes(
        user_id=user_id,
        session_id=session_id,
        tags=["chainlit", "chat"],
    ):
        response = agent.run(message.content)
        await cl.Message(content=response).send()

    langfuse.flush()
```

## Debugging

### Verify traces are being sent

```python
import logging
logging.getLogger("langfuse").setLevel(logging.DEBUG)
```

### Check OTel instrumentation is active

```python
from opentelemetry import trace
tracer = trace.get_tracer(__name__)
print(f"Tracer provider: {trace.get_tracer_provider()}")
```

### Query recent traces

```bash
AUTH=$(echo -n "$LANGFUSE_PUBLIC_KEY:$LANGFUSE_SECRET_KEY" | base64 -w0)
curl -s -H "Authorization: Basic ${AUTH}" \
  "$LANGFUSE_HOST/api/public/traces?limit=5" | \
  jq '.data[] | {name, sessionId, userId, totalCost}'
```

## Best practices

- **Always call `langfuse.flush()`** at the end of requests to ensure traces are sent
- **Use `propagate_attributes` early** in your request handler to ensure all nested spans inherit the attributes
- **Set meaningful trace names** using the user's query or request type
- **Tag by environment** (`tags=["production"]` vs `["staging"]`) for filtering
- **Include version** to track changes across deployments

## References

- [Claude Agent SDK Integration](https://langfuse.com/integrations/frameworks/claude-agent-sdk)
- [Python SDK v3 Documentation](https://langfuse.com/docs/sdk/python/decorators)
- [Sessions Documentation](https://langfuse.com/docs/observability/features/sessions)
- [Scores and Evaluation](https://langfuse.com/docs/evaluation/evaluation-methods/scores-via-sdk)
- [OpenTelemetry Integration](https://langfuse.com/guides/cookbook/otel_integration_python_sdk)
