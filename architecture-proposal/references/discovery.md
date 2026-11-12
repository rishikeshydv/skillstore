# Adaptive discovery and source policy

## Inputs
Accept rough prose, PRDs, architecture notes, pasted API definitions, diagrams, source files, or existing proposals. Ask questions only for missing facts needed to make a **useful first draft**. Do not require full answers before starting: uncertain items belong in Assumptions/Open Questions.

## After document selection: minimal interview

Ask up to 3-5 grouped high-value questions, omitting known answers:
1. What feature/framework is proposed, and who uses it? What pain point exists now?
2. What system/services exist today and what must change? Any architecture diagrams or code?
3. What requirements, constraints, relevant scale/security/compatibility expectations, and important ownership facts are known?
4. Which credible architectural alternatives have been considered?
5. For LLD: what interfaces, runtime environment, state, persistence, concurrency and key error semantics are expected?

For **One-Pager**, focus on problem, proposed direction, value, risks, ownership, maintenance. Keep the interview brief. For **HLD**, ask mainly about current state, component boundaries, data flow, alternatives, relevant quality attributes. For **LLD**, ask about exact contracts, lifecycles, implementation constraints, failure behavior and testing. For **All Three**, collect a shared fact base once, then layer detail separately.

## Inputs not answered
- Never invent owner, dates, metrics, budget, compatibility, compliance, architecture facts, expected results, approvals, or claim verification.
- Mark unknown facts `TBD`; for risk-sensitive blockers, create a clear Open Question.
- Distinguish measured / supplied fact / estimate / assumption / recommendation.
- Compute estimates only with visible user-supplied inputs and arithmetic.
- Explain consequential technologies in everyday words before implementation detail.

## Review and feedback
Accept feedback in text or as per-section decisions: Keep, Modify, Merge, Remove. Preserve everything untouched; change the selected sections and any necessary cross-links only. Never treat reviewer comments as explicit approval unless user states so.

## Example invocation and handling
- "Propose a stream ingestion framework" -> **first ask:** One-Pager, HLD, LLD, or All Three?
- "Write a one pager for an internal SDK" -> generate only a one-page One-Pager.
- "Create an HLD for service migration" -> generate only HLD, no page cap.
- "Use these code snippets to make an LLD" -> generate only LLD; don't invent missing contracts.
- "Give me all three documents" -> share three separate files.
- "Remove HLD security section; merge component + data flow" -> preserve unrelated headings; integrate security into actual requirements/architecture sections.
