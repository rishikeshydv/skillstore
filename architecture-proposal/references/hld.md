# High-Level Design: eight-section outline

**Purpose:** WHAT architecture is proposed, WHY does it make sense, and how do its important boundaries and guarantees hold together? **No page limit.** Include diagrams when they clarify decisions. Never force an HLD into a one-page shape.

## 1. Executive Summary
- **Brief** summary, ideally 3-5 sentences: technical problem, proposed architecture, expected outcome.
- Avoid retelling the full One-Pager. No long executive essay.

## 2. Problem & Current State
- 2.1 Existing architecture: relevant current systems and data/control flow.
- 2.2 Current limitations: measurable bottlenecks, coupling, failures, missing capabilities.
- 2.3 Reason for change: why the current design is insufficient.
- Include an as-is diagram only when useful.

## 3. Goals, Non-Goals & Requirements
- 3.1 Functional goals and observable behavior.
- 3.2 Non-goals / explicit exclusions.
- 3.3 Functional requirements with identifiers when available.
- 3.4 **Specific** relevant quality requirements (e.g., p99 latency, recovery behavior, data consistency), not generic qualities.
- 3.5 Technical constraints, assumptions, and relevant dependencies.

## 4. Proposed Architecture
**Keep this as a single, connected narrative**, merging formerly separate component, runtime flow, and integration/data sections.
- 4.1 Solution overview: what will be introduced and the architectural approach.
- 4.2 Proposed architecture diagram: major services/components, boundaries, storage, producers/consumers.
- 4.3 Component responsibilities: each component's role, interface, source of truth, ownership; avoid lists without a purpose.
- 4.4 End-to-end execution flow: concrete use case from entry point through components to result; sequence diagram where useful.
- 4.5 Integration & data flow: upstream/downstream dependencies, contracts/protocols, high-level persistence and data lifecycle, compatibility.
- 4.6 Key architectural characteristics: only mechanisms material to the design (for example, async processing, isolation, extension strategy or consistency model), with reasons.

## 5. Quality Requirements & Design Guarantees
**Do not use vague "Scalability, Performance & Reliability" filler.** Select ONLY relevant concrete guarantees and pair each with architecture implications/verification:
- Workload/throughput assumptions and mechanism to handle them; numerical target when available.
- Latency budget and expected bottleneck if response times matter.
- Availability and failure/recovery behavior for production-critical services.
- Consistency, ordering, durability where stateful or distributed.
- Extensibility, supported compatibility guarantees for SDK/framework use cases.
- Security controls/operability guarantees only if they impose architectural constraints.
If this section would only repeat requirements from section 3 with no architecture implications, integrate the useful content into section 3 and omit section 5 **in that specific document**.

## 6. Architectural Decisions & Trade-offs
- Credible alternatives, including extending existing architecture where appropriate.
- Evaluation criteria linked to goals and constraints.
- Why the selected design wins; what trade-offs and limits it accepts.
- Link ADR-style records for consequential choices. No strawman alternatives.

## 7. Rollout / Phases of Execution
- Describe actual, project-specific stages (foundational capability, integration, production enablement are examples only).
- Key dependencies and completion/validation criteria for each phase.
- Include migration, adoption, rollback details only when important to the proposal; avoid forcing extraneous headings.
- Do not turn this into sprint planning.

## 8. Risks & Open Questions
- Architecture risks, impact, mitigations, major dependencies, unresolved decisions.
- Mark owner/date TBD if unknown; do not invent them.
- **Do not include an Approval heading or decision-approval section.**

## Security and operations placement
Do **not** require a stand-alone "Security & Operations" header. Put requirements in section 3, concrete trust/isolation/security/operability mechanisms in section 4, relevant guarantees in section 5, and unresolved issues in section 8. A high-security feature may warrant a clearly labeled subsection inside these sections.

## Diagrams
Use system/context and container views for architecture; use critical runtime sequence where helpful. Avoid code/class diagrams and full wire contracts here unless essential for a major architecture decision; those normally belong in the LLD.
