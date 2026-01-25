# Langfuse upstream contributions

## Pending: GitHub issue for Claude Code integration guide

The official guide has several issues we've fixed locally. Need to file upstream.

**Repository**: [langfuse/langfuse-docs](https://github.com/langfuse/langfuse-docs)

**Page to fix**: `pages/integrations/other/claude-code.mdx` (or similar)

### Issues to report

- [ ] `session_id` in metadata doesn't enable session grouping (must use `propagate_attributes`)
- [ ] "Turn N" trace naming is unhelpful (should use first line of user message)
- [ ] Input tokens undercounted (missing `cache_read_input_tokens` and `cache_creation_input_tokens`)

### Draft issue

Title: **Claude Code integration: session_id not properly set on traces (sessions view empty)**

Body: See `setup-claude-code.md` "Known issues and fixes" section for full details and code examples.

### Potential PR

If filing a PR directly:

1. Fork `langfuse/langfuse-docs`
2. Find the Claude Code integration page (likely `pages/integrations/other/claude-code.mdx`)
3. Update the hook script example to:
   - Import `propagate_attributes` from langfuse
   - Use `propagate_attributes(session_id=...)` inside the span
   - Change trace name from `f"Turn {turn_num}"` to first line of user message
   - Include cache tokens in usage calculation
4. Add a note about the `base64 -w0` requirement for NixOS/Linux
5. Submit PR with reference to the issue

### When to do this

- After verifying the fixes work in production (rebuild home-manager, test new traces)
- Ideally include before/after screenshots from Langfuse dashboard showing:
  - Sessions view populated (after fix)
  - Descriptive trace names (after fix)
  - Accurate token counts (after fix)
