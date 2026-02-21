# start

## Overview

Create a new inter-agent chat session. Generates a slug, creates the chat file, writes an opening message, then enters a poll-and-reply loop waiting for the other agent.

## Process

### Step 1: create the session

```bash
mkdir -p tmp/ai-chats
```

Generate a slug by picking 3 random words in `adjective-noun-noun` format, joined by hyphens:

```bash
a=$(shuf -n1 -e bold calm cool dark deep fast fond free glad keen mild open pure rare slim soft tall warm wise)
b=$(shuf -n1 -e amber cedar coral drift ember flame frost glass maple night ocean pearl river scout shade spark steel storm trail)
c=$(shuf -n1 -e bear crow deer dove fawn frog hawk hare ibis lark lynx moth newt orca pike puma rook vole wren)
slug="${a}-${b}-${c}"
```

This produces slugs like `calm-frost-hawk`, `soft-ember-moth`, `wise-maple-wren`.

Create the chat file at `tmp/ai-chats/<slug>.md` with this initial structure:

```markdown
# ai-chat: <slug>

Started: <ISO 8601 timestamp>
Status: waiting-for-partner

---

```

### Step 2: report the slug

Tell the user:

> Chat session started. Give this slug to the other agent:
> **`<slug>`**
>
> I'll wait here until they join. The other session should run: `/ai-chat join <slug>`

### Step 3: wait for the partner to join

Poll the file every 5 seconds using Read tool. Look for `Status: active` which indicates the other agent has joined and written a message.

While waiting, briefly tell the user you're polling (don't spam — mention it once, then poll silently).

### Step 4: enter the conversation loop

Once the partner has joined and written a message:

1. Update `Status: active` if not already set
2. Read the file to see the latest message
3. Write your reply by appending to the file:

```markdown
## [agent-a] <HH:MM:SS>

<your message here>

---

```

Use `agent-a` as your speaker label (the starting agent is always `agent-a`).

4. After appending your message, poll the file for a new `## [agent-b]` section
5. When you see a new message from agent-b, read it and repeat from step 3

### Step 5: ending the chat

If the conversation reaches a natural conclusion, or the user asks to stop, or you see `## END` in the file, append:

```markdown
## END

Session closed by agent-a at <HH:MM:SS>.
```

Report the outcome to the user.

## Polling mechanics

- Use the Read tool to read the chat file
- Compare the content length or last heading to detect new messages
- Poll interval: ~5 seconds (use `sleep 5` in Bash between reads)
- Timeout: after 5 minutes of no partner joining, ask the user if they want to keep waiting
- After partner joins, timeout resets: 2 minutes of no new message triggers a "still waiting" notice to the user

## Message guidelines

- Be conversational but concise
- Stay on-topic — the user will have told you what to discuss
- If the user gave you a specific role or topic, follow it
- If no topic was specified, introduce yourself and ask the other agent what they'd like to discuss
