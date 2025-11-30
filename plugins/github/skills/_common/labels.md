# Shared Labels / State Model

- `status-planning-todo`: Needs plan.
- `status-planning-review`: Plan posted, awaiting review/approval.
- `status-planning-done`: Plan approved, ready for build.
- `status-implementation-in-progress`: Build in progress.
- `status-implementation-done`: Build complete, ready for review.
- `status-review-in-progress`: Under code review/human approval.
- `status-review-changes-requested`: Review found issues; send back to build.
- `status-review-approved`: Approved; ready to merge.
- `status-merged`: Work merged/closed.

Agents should update labels as they hand off between stages to keep orchestration accurate.
