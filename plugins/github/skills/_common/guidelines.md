# Shared Guidelines

- **Worktrees & Branches**: Use `worktrees/issue-<number>-<slug>` and branch `issue-<number>-<slug>` for build/review work; keep main clean.
- **Rebase Hygiene**: Fetch `origin/main` and rebase before PR updates; resolve conflicts immediately and rerun tests.
- **Conventional Commits**: `<type>(<scope>): <description>` in imperative mood.
- **Label Hygiene**: Apply lifecycle labels from `labels.md` to signal stage transitions (planning → build → review → merge).
- **Context Handoff**: When passing between agents, include issue #, PR #, plan link/comment URL, acceptance criteria, CI status, and summary notes.
- **Security & Quality**: Run available tests/lints/builds before handing to review; document any gaps.
