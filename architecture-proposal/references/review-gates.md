# Review gates by artifact

Use as an internal critique after drafting. Address the issues in the document rather than asserting it was "approved" or "review passed".

## Shared integrity
- Claims distinguish supplied facts, assumptions, estimates, recommendations, and unknowns.
- No invented owners, dates, measured baselines, architecture facts, approval, or cost.
- Acronyms explained once; terms and component names consistent across selected artifacts.
- Focus on audience questions and actual architectural implications; omit irrelevant boilerplate.

## One-Pager quality gate
- Exactly 6 headings and the sixth is **Maintenance & Ownership**.
- One rendered Letter page, without a cover page; legible text and clean diagram if used.
- Problem, solution, benefits, technical direction, risks, and maintenance are each concrete.
- No implicit promise of resources/approval or a recommendation/next steps replacement header.

## HLD quality gate
- Brief executive summary and correct 8-section structure (section 5 may be omitted only when absolutely duplicative).
- Section 4 tells a **single coherent architecture story**: context, major components, runtime flow, integration/data movement.
- Architectural decision rationale engages the strongest credible alternative fairly.
- Quality requirements name exact measurable outcomes/mechanisms where known; no generic "high scale" fillers.
- Security and operations treated inside actual relevant sections, not forced as stand-alone chapter.
- Section 7 covers **Rollout / Phases of Execution**, not generic migration/adoption ceremony.
- Last section **Risks & Open Questions**; no Approval heading.

## LLD quality gate
- Eight core sections, not fifteen mandatory chapters. Each contains useful content, no fake N/A walls.
- Major modules have boundaries, contracts, and ownership clear enough for independent implementation.
- Nontrivial algorithms include examples/pseudocode; interfaces include precise data types and errors where relevant.
- If stateful or concurrent, sources of truth, write ownership, consistency, retry/idempotency/partial failure semantics explicit.
- If a reusable framework, supported extension API, lifecycle, compatibility and developer usage are concrete.
- Test cases map to requirements and relevant failure modes; deployments/upgrades/diagnostics are realistic.
- Specialized security, scale, infrastructure, and storage details only when needed. No unverified guarantees.

## Final presentation
- Verify logo correct and undistorted, heading colors, table styles, readable font and diagrams.
- No clipped tables, duplicate cover pages, orphaned section headings, mysterious placeholders or text overflows.
- For any missing diagrams, never silently replace one with a fabricated diagram; clearly surface omission.
