---
description: Implement the ralph wiggum loop pattern (iterative agent retry with completion promise) using Claude Agent SDK and Opencode SDK, with full orchestrator visibility and mid-loop interaction
---

# Iterative agent loop with completion promise

## Concept

Run the same goal prompt against an agent repeatedly. Each iteration, the agent sees its previous work via both conversation memory and file state. The loop exits when the agent outputs a completion promise token. The orchestrator has full streaming visibility and can inject commands or redirect the agent at any point between iterations.

Inspired by [open-ralph-wiggum](https://github.com/Th0rgal/open-ralph-wiggum) but implemented as an SDK pattern rather than a standalone CLI.

## Key differences from ralph

- Ralph spawns a fresh process each iteration (no conversation memory). `ClaudeSDKClient` maintains a persistent session — the agent remembers what it tried before, what failed, and what worked.
- Ralph offers limited mid-loop interaction (`--add-context` from another terminal). `ClaudeSDKClient` gives the orchestrator direct session control — you can redirect, interrupt, or re-prompt the agent between iterations.
- Ralph parses stdout for tool usage. SDK gives structured message objects (`AssistantMessage` with `TextBlock`, `ToolUseBlock` in `.content`).

## With Claude Agent SDK (Python)

### Basic loop with streaming visibility

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["claude-agent-sdk"]
# ///

import asyncio
import subprocess
from claude_agent_sdk import (
    ClaudeSDKClient, ClaudeAgentOptions,
    AssistantMessage, TextBlock, ToolUseBlock, ResultMessage,
)

COMPLETION_PROMISE = "COMPLETE"
MAX_ITERATIONS = 20
TASK_FILE = ".loop/tasks.md"


async def run_loop(goal: str, model: str = "sonnet", plugin_path: str | None = None):
    """
    Run an iterative agent loop until the agent signals completion.

    Uses ClaudeSDKClient to maintain a persistent session across iterations.
    The agent remembers everything from previous iterations — no need to
    re-explain context or re-read files each time.
    """
    iteration = 0
    context_injection: str | None = None

    options = ClaudeAgentOptions(
        model=model,
        max_turns=30,
        allowed_tools=["Bash", "Write", "Edit", "Read", "Glob", "Grep"],
        **({"plugins": [{"type": "local", "path": plugin_path}]} if plugin_path else {}),
    )

    async with ClaudeSDKClient(options=options) as client:
        while iteration < MAX_ITERATIONS:
            iteration += 1
            print(f"\n{'='*60}")
            print(f"  Iteration {iteration}/{MAX_ITERATIONS}")
            print(f"{'='*60}\n")

            # Build the iteration prompt
            prompt = build_prompt(goal, iteration, context_injection)
            context_injection = None  # consumed

            result_text = ""
            tools_used: dict[str, int] = {}

            # Send prompt to the persistent session.
            # The agent sees its full conversation history from
            # all previous iterations — no session ID juggling needed.
            await client.query(prompt)

            # Stream every message for full visibility.
            # The orchestrator (you) sees tool calls, text, and results
            # as they happen — not just a final summary.
            async for message in client.receive_response():
                # Tool call and text visibility
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock):
                            print(block.text, end="", flush=True)
                            result_text += block.text
                        elif isinstance(block, ToolUseBlock):
                            tool_name = block.name
                            tools_used[tool_name] = tools_used.get(tool_name, 0) + 1
                            print(f"  [tool] {tool_name}")

                # Final result
                if isinstance(message, ResultMessage):
                    if message.result:
                        result_text = message.result

            # --- Iteration complete. Orchestrator regains control. ---

            print(f"\n\n--- Iteration {iteration} summary ---")
            print(f"Tools: {tools_used}")

            # Check for completion promise
            if f"<promise>{COMPLETION_PROMISE}</promise>" in result_text:
                if iteration < 2:
                    print("Completion detected but < 2 iterations. Continuing.")
                    context_injection = (
                        "You claimed completion too early. Verify your work "
                        "thoroughly — run tests, check edge cases, then re-signal."
                    )
                    continue
                print(f"\nDone in {iteration} iterations.")
                auto_commit(f"Loop complete after {iteration} iterations")
                return True

            # Auto-commit iteration progress
            auto_commit(f"Loop iteration {iteration}: work in progress")

            # --- THIS IS WHERE THE ORCHESTRATOR CAN INTERACT ---
            #
            # Between iterations, the orchestrator has full control.
            # When the user says "tell the agent to focus on X" or
            # "skip to the next task", the orchestrator sets
            # context_injection which gets prepended to the next prompt.
            #
            # Examples of orchestrator interventions:
            #   context_injection = "Focus on the auth module first."
            #   context_injection = "The test failures are due to a missing env var. Add TEST_DB_URL to .env."
            #   context_injection = "Skip the current task and move to the next one."
            #
            # The orchestrator can also modify options mid-loop:
            #   await client.disconnect()
            #   options = ClaudeAgentOptions(..., model="opus")  # upgrade model
            #   client = ClaudeSDKClient(options=options)
            #   await client.connect()

        print(f"\nMax iterations ({MAX_ITERATIONS}) reached.")
        return False


def build_prompt(goal: str, iteration: int, context: str | None) -> str:
    """
    Build the prompt for a single iteration.

    The prompt structure:
    1. Loop metadata (iteration number, completion rules)
    2. User-injected context (if any, from orchestrator intervention)
    3. The actual goal
    4. Completion instructions
    """
    context_section = ""
    if context:
        context_section = f"""
## Orchestrator directive (priority)

{context}

---
"""

    return f"""# Iterative loop - iteration {iteration}

You are in an iterative development loop. Your work from previous
iterations is visible in the files on disk and in our conversation history.
{context_section}
## Goal

{goal}

## Rules

- Read the current state of files to understand what was done before
- Make incremental progress each iteration
- Run tests or verification when applicable
- When the goal is GENUINELY complete, output: <promise>{COMPLETION_PROMISE}</promise>
- Do NOT output the promise until the work is verified
- If stuck, try a different approach

Iteration {iteration}/{MAX_ITERATIONS}. Work on the goal now.
"""


def auto_commit(message: str):
    """Commit any changes made during the iteration."""
    try:
        status = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True
        ).stdout.strip()
        if status:
            subprocess.run(["git", "add", "-A"], check=True)
            subprocess.run(
                ["git", "commit", "-m", message],
                capture_output=True, check=True
            )
            print(f"  [commit] {message}")
    except Exception:
        pass


if __name__ == "__main__":
    import sys
    goal = sys.argv[1] if len(sys.argv) > 1 else "Build a REST API for todos with tests"
    asyncio.run(run_loop(goal))
```

### Interactive mid-loop control

The orchestrator (Claude Code running this skill) controls the loop. When the user asks to intervene, the orchestrator modifies the loop state between iterations.

The key mechanism is `context_injection` — a string that gets prepended to the next iteration's prompt with high priority. The orchestrator sets this based on user instructions:

```python
# User says: "tell the agent to focus on error handling"
context_injection = "Focus on error handling. The happy path works, prioritize edge cases and error responses."

# User says: "the agent is stuck, give it a hint"
context_injection = "The test is failing because the database schema changed. Run 'python manage.py migrate' first."

# User says: "skip this task, move to the next one"
context_injection = "Mark the current task as complete and move to the next task in the task list."

# User says: "stop after this iteration"
MAX_ITERATIONS = iteration  # will exit after current iteration completes

# User says: "interrupt the agent right now"
await client.interrupt()  # ClaudeSDKClient supports mid-execution interrupts
```

The orchestrator never needs to kill the agent or lose state — it just waits for the current iteration to finish, then redirects. Or uses `interrupt()` for immediate control. This is the main advantage over ralph's `--add-context` which writes to a file and hopes the agent reads it.

### With task decomposition

For larger goals, break the work into tasks. The agent works on one task per iteration cycle, signaling with a task-level promise before moving on.

```python
TASK_PROMISE = "READY_FOR_NEXT_TASK"

# The prompt includes the task list from a markdown file:
task_section = f"""
## Tasks

Read the task list from {TASK_FILE}. Work on the first incomplete task.
When the current task is done, mark it [x] and output:
<promise>{TASK_PROMISE}</promise>

When ALL tasks are done, output:
<promise>{COMPLETION_PROMISE}</promise>
"""

# In the main loop, check for both promises:
if f"<promise>{TASK_PROMISE}</promise>" in result_text:
    print(f"Task completed. Moving to next task.")
    context_injection = "Good. Pick up the next incomplete task."
    continue
```

### Struggle detection

Monitor iteration patterns to detect when the agent is stuck:

```python
no_change_count = 0
short_iteration_count = 0

# After each iteration:
files_changed = subprocess.run(
    ["git", "diff", "--name-only"],
    capture_output=True, text=True
).stdout.strip()

if not files_changed:
    no_change_count += 1
else:
    no_change_count = 0

if iteration_duration_seconds < 30:
    short_iteration_count += 1
else:
    short_iteration_count = 0

if no_change_count >= 3:
    # Agent is spinning without progress — intervene
    context_injection = (
        "You have made no file changes in 3 iterations. "
        "You appear to be stuck. Try a completely different approach."
    )

if short_iteration_count >= 3:
    # Agent is bailing out quickly — likely hitting an error
    context_injection = (
        "Your last 3 iterations were very short. Read the error "
        "carefully and address the root cause, not the symptom."
    )
```

The orchestrator can also surface these to the user: "The agent hasn't made progress in 3 iterations. Want me to give it a hint, change the model, or stop?"


## With Opencode SDK (TypeScript)

Same pattern, different SDK. Opencode uses a persistent server with session management.

### Basic loop

```typescript
import { createOpencode } from "@opencode-ai/sdk"

const COMPLETION_PROMISE = "COMPLETE"
const MAX_ITERATIONS = 20

async function runLoop(goal: string, model = "opencode/gpt-5-nano") {
  // Start or connect to persistent server.
  // The server keeps MCP connections warm across iterations,
  // avoiding cold-boot overhead that adds up over 10+ iterations.
  const { client } = await createOpencode({ port: 4096 })

  const session = await client.session.create({
    body: { title: `Loop: ${goal.slice(0, 50)}` }
  })

  let contextInjection: string | null = null

  for (let iteration = 1; iteration <= MAX_ITERATIONS; iteration++) {
    console.log(`\n${"=".repeat(60)}`)
    console.log(`  Iteration ${iteration}/${MAX_ITERATIONS}`)
    console.log(`${"=".repeat(60)}\n`)

    const prompt = buildPrompt(goal, iteration, contextInjection)
    contextInjection = null

    // Send prompt to existing session.
    // Unlike Claude SDK's ClaudeSDKClient, Opencode sessions are
    // inherently persistent — the agent keeps its full history
    // within the session without needing explicit session management.
    const result = await client.session.prompt({
      path: { id: session.id },
      body: {
        model: { providerID: model.split("/")[0], modelID: model.split("/")[1] },
        parts: [{ type: "text", text: prompt }]
      }
    })

    console.log(result)

    // Check completion
    const resultText = typeof result === "string" ? result : JSON.stringify(result)
    if (resultText.includes(`<promise>${COMPLETION_PROMISE}</promise>`)) {
      console.log(`\nDone in ${iteration} iterations.`)
      return true
    }

    // --- ORCHESTRATOR CONTROL POINT ---
    // Set contextInjection here based on user instructions.
    // Same pattern as the Claude SDK version.
  }

  console.log(`\nMax iterations reached.`)
  return false
}

function buildPrompt(goal: string, iteration: number, context: string | null): string {
  const contextSection = context
    ? `\n## Orchestrator directive (priority)\n\n${context}\n\n---\n`
    : ""

  return `# Iterative loop - iteration ${iteration}

You are in an iterative development loop.
${contextSection}
## Goal

${goal}

## Rules

- Read files to understand previous iteration work
- Make incremental progress
- When GENUINELY complete, output: <promise>${COMPLETION_PROMISE}</promise>
- Do NOT output the promise until verified

Iteration ${iteration}/${MAX_ITERATIONS}.`
}
```

### Opencode visibility notes

Opencode SDK visibility is currently less granular than Claude Agent SDK:
- Claude SDK streams individual messages (`AssistantMessage` with `TextBlock`/`ToolUseBlock` in `.content`) as they happen
- Opencode SDK returns the final result of a prompt — intermediate tool calls are not exposed via the SDK (they are visible in the Opencode web UI if running `opencode serve`)
- For full tool-level visibility with Opencode, use the CLI shorthand with `--format json` and parse the output stream

This is a temporary limitation. As the Opencode SDK matures, expect streaming message support similar to Claude Agent SDK.


## Orchestrator interaction pattern

When the user asks to interact with the agent during a loop, the orchestrator follows this pattern:

```
User: "the agent keeps failing on the database migration"

Orchestrator (you):
1. Current iteration is running — wait for it to complete
   (or use client.interrupt() if the agent is wasting turns)
2. Set context_injection for the next iteration:
   "The migration is failing because the postgres container
   isn't running. Run 'docker compose up -d db' first,
   then retry the migration."
3. Tell the user: "I've queued a directive for the next
   iteration. The agent will see it when iteration N+1 starts."
```

```
User: "stop the loop and let me review"

Orchestrator:
1. Set MAX_ITERATIONS = current iteration (loop exits naturally)
2. Show the user a summary of what was accomplished
3. The ClaudeSDKClient can be kept alive — the loop can be resumed later
```

```
User: "the agent is too slow, use a better model"

Orchestrator:
1. This requires creating a new ClaudeSDKClient with different options
   (model is set at connection time)
2. The new client starts a fresh session — file state is preserved,
   conversation history is not
3. Tell the user: "Upgraded to opus. Starting fresh session but files are intact."
```

The orchestrator is the user's proxy into the agent loop. Every interaction goes through the orchestrator — the user never needs to touch files or run commands in a separate terminal.
