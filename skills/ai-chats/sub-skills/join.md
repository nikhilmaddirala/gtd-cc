# join

## Overview

Join an existing inter-agent chat session using a slug. Read the chat file, mark the session as active, write a greeting, then enter the poll-and-reply loop.

## Process

### Step 1: validate and open the session

The user provides a slug (e.g., `calm-frost-hawk`). Read the file at:

```
tmp/ai-chats/<slug>.md
```

If the file doesn't exist, tell the user the slug is invalid and ask them to check it.

### Step 2: join the session

Update the `Status:` line from `waiting-for-partner` to `active` by editing the file.

Then append your first message:

```markdown
## [agent-b] <HH:MM:SS>

<your greeting/opening message>

---

```

Use `agent-b` as your speaker label (the joining agent is always `agent-b`).

### Step 3: enter the conversation loop

1. After writing your message, poll the file for a new `## [agent-a]` section
2. When you see a new message from agent-a, read it
3. Write your reply by appending to the file (same format as step 2)
4. Repeat

### Step 4: ending the chat

If the conversation reaches a natural conclusion, or the user asks to stop, or you see `## END` in the file, append:

```markdown
## END

Session closed by agent-b at <HH:MM:SS>.
```

Report the outcome to the user.

## Polling mechanics

- Use the Read tool to read the chat file
- Compare the content length or last heading to detect new messages
- Poll interval: ~5 seconds (use `sleep 5` in Bash between reads)
- Timeout: 2 minutes of no new message triggers a "still waiting" notice to the user

## Message guidelines

- Be conversational but concise
- Stay on-topic — the user will have told you what to discuss
- If the user gave you a specific role or topic, follow it
- If no topic was specified, greet agent-a and ask what they'd like to discuss
