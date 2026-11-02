# Reporting Cleanup Work

At the end of a cleanup task, summarize:

- What changed and why.
- What was inspected but left unchanged, especially risky or uncertain items.
- Suspected secrets with values redacted, and whether credential rotation is advised.
- Open-source readiness gaps that need owner decisions, external access, or a separate task.
- Verification performed only if requested; distinguish inspected facts from unverified assumptions.

Be clear about limitations. Do not say a test, security scan, dependency audit, or release check passed unless it was actually run and its result was observed.
