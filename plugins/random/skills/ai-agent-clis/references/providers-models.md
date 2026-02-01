# Providers and models

Last verified: 2026-02-01


## Claude Code

### Authentication

Claude Code uses Anthropic API directly (via subscription or API key).

### Model aliases

Claude Code supports short aliases for `--model`:
- `haiku` → resolves to latest haiku (currently `claude-haiku-4-5-20251001`)
- `sonnet` → resolves to latest sonnet
- `opus` → resolves to latest opus

You can also use full model names (e.g. `claude-sonnet-4-20250514`).

### Cost tiers

- Subscription: ~$20/month (Pro) or ~$100/month (Max) with included usage
- API: pay per token, varies by model


## Opencode

### Authentication

Configured providers are stored in `~/.local/share/opencode/auth.json`. Manage with `opencode auth login/list/logout`.

Currently authenticated:
- OpenAI (oauth)
- Z.AI Coding Plan (api)

### Model format

Opencode uses `provider/model` format. Run `opencode models` to list all available models, or `opencode models <provider>` to filter by provider.

### Available providers and notable models

#### opencode (built-in free tier)

Rotating selection of free models:
- `opencode/gpt-5-nano` - lightweight, good for simple tasks
- `opencode/glm-4.7-free`
- `opencode/kimi-k2.5-free`
- `opencode/minimax-m2.1-free`
- `opencode/trinity-large-preview-free`
- `opencode/big-pickle`

#### openai (authenticated)

- `openai/gpt-5.2` - latest flagship
- `openai/gpt-5.2-codex` - code-optimized
- `openai/gpt-5.1-codex` - previous gen code model
- `openai/gpt-5.1-codex-mini` - smaller/cheaper code model
- `openai/gpt-5.1-codex-max` - max context code model

#### zai-coding-plan (authenticated)

- `zai-coding-plan/glm-4.7` - latest GLM
- `zai-coding-plan/glm-4.7-flash` - fast/cheap GLM
- `zai-coding-plan/glm-4.6` - previous gen
- `zai-coding-plan/glm-4.5` - stable

#### openrouter (requires API key or cookie auth)

Not currently authenticated. Would provide access to:
- `openrouter/anthropic/claude-opus-4.5` - latest Opus
- `openrouter/anthropic/claude-sonnet-4.5` - latest Sonnet
- `openrouter/anthropic/claude-haiku-4.5` - latest Haiku
- `openrouter/google/gemini-2.5-pro` - Google flagship
- `openrouter/google/gemini-2.5-flash` - Google fast model
- `openrouter/deepseek/deepseek-r1:free` - free reasoning model
- `openrouter/qwen/qwen3-coder:free` - free coding model
- Many free models available (suffix `:free`)


## Cost optimization strategy

- Free tasks: use `opencode` built-in free models or OpenRouter `:free` models
- Cheap tasks: use `--model haiku` (Claude Code) or `openai/gpt-5.1-codex-mini` (Opencode)
- Quality tasks: use `--model sonnet` (Claude Code) or `openai/gpt-5.2-codex` (Opencode)
- Max quality: use `--model opus` (Claude Code)
- Always set `--max-budget-usd` on Claude Code to cap spend


## Environment variables

### Claude Code

- `ANTHROPIC_API_KEY` - API key for direct API usage
- `CLAUDE_CODE_USE_BEDROCK=1` - use AWS Bedrock
- `CLAUDE_CODE_USE_VERTEX=1` - use Google Vertex AI

### Opencode

- `OPENCODE_SERVER_PASSWORD` - enable basic auth for serve/web
- `OPENCODE_DISABLE_CLAUDE_CODE=true` - disable reading .claude/ files
- `OPENCODE_DISABLE_CLAUDE_CODE_SKILLS=true` - disable loading .claude/skills only
- Provider API keys can also be set via env vars or `.env` file
