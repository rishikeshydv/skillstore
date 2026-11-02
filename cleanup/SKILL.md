---
name: cleanup
description: Inspect and safely clean up a code repository, reduce clutter, improve maintainability, and prepare open-source readiness. Invoke with `/cleanup` when asked to clean up, organize, tidy, audit, or prepare a repository for public release. Make focused, reversible improvements and report risks or launch tasks that need owner decisions.
---

# Repository Cleanup

Invoke this skill with `/cleanup`.

Inspect the repository, make focused and reversible improvements that fit its existing conventions, and report remaining cleanup or release-readiness work. Do not assume that preparing for open source means publishing the repository.

## Workflow

1. Read [the cleanup workflow](docs/workflow.md) before inspecting or editing a repository.
2. Read [safety boundaries](docs/safety-boundaries.md) whenever you find secrets, history issues, destructive changes, or external actions.
3. Read [the open-source readiness checklist](docs/open-source-readiness.md) when the user asks to prepare for public release or wants a readiness review.
4. Follow [the reporting guide](docs/reporting.md) when summarizing the result.

Preserve pre-existing user changes. Do not run or add tests unless the user asks for testing or verification. Never claim checks passed unless you ran them and observed the result.
