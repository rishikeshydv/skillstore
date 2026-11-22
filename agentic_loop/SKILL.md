---
name: agentic_loop
description: Implement, extend or audit the production agentic loop ("agentic-loop v2") in code so it matches the PRD diagram node-for-node and edge-for-edge. Use when building the loop, wiring classifier/orchestrator/final_check, adding playbooks or tools to it, or verifying an existing implementation against the diagram.
---

# agentic_loop

Build the agentic loop in code **exactly** as drawn on the "agentic-loop v2 (production)" page of the PRD diagram "prd agentic loop". The diagram is the spec: it decides the parts and how they connect. Your job is to turn it into code that anyone can check against the diagram. Ignore the v1 page; it has been replaced.

Diagram: https://lucid.app/lucidchart/ffc2f021-4f7e-4fc8-8d02-d4198023b888/edit

## The loop in one breath

query → **Question Classifier (Jev)** checks for a playbook match and checks scope → if there's a match, the **playbook** goes to the orchestrator in guided mode; if not, an in-scope query goes to the orchestrator in free-form mode and an out-of-scope query gets a **decline** → **orchestrator (Opus)** picks the next action: **call a tool** (the tool can read and write the Database; its result or error goes back to the orchestrator), **ask the user** (pause, then resume with their reply), or **answer** → **final_check (Sonnet)** checks the answer against the playbook and all 5 accuracy metrics → if it passes, send the **final response**; if it fails and retries are left, go back to the orchestrator with the failure reason; if it fails and none are left, send the **fallback response**.

16 nodes, 18 edges, 3 terminal states. Nothing more, nothing less.

## Reference files

Paths below are relative to this skill's folder. Read each file at the step shown.

| File | What's in it | Read it |
|------|--------------|---------|
| `docs/spec.md` | Mermaid diagram, node table (N1–N16), edge table (E1–E18), 7 invariants | First, before touching code. It's the source of truth. |
| `docs/decisions.md` | 8 questions the diagram doesn't answer (the 5 metrics, retry budget, Jev, …) | During M0. Ask the human about all of them in one message. |
| `docs/milestones.md` | M0–M6, each with a **Done when** list | Before starting each milestone. |
| `docs/verification.md` | Graph conformance, 8 end-to-end paths, invariant tests, report format | At M6. Required before calling the loop complete. |

Artifacts you produce go in the **target repo**, not this skill's folder: `docs/agentic_loop/LOOP_MAP.md` (M0) and `docs/agentic_loop/VERIFICATION.md` (M6).

## Workflow

1. Read `docs/spec.md`.
2. **M0:** map the repo to the spec and ask the questions in `docs/decisions.md`. Get the human's approval of `LOOP_MAP.md` before writing loop code.
3. **M1–M5:** build one milestone at a time from `docs/milestones.md`. Don't start the next one until every item in the current one's **Done when** list is true.
4. **M6:** run everything in `docs/verification.md`. Report the loop as complete only when `VERIFICATION.md` is all green.

## Rules

- **No creative changes to the graph.** Don't add, remove, merge or reorder nodes or edges. If the codebase seems to need a change, stop and ask the human first.
- **Keep the diagram's names** in functions, states, enums, log events and trace spans (`question_classifier`, `orchestrator`, `final_check`, …).
- **Write the loop as an explicit state machine or graph** (an enum plus a transition table, or a graph framework). You must be able to list the edges by inspecting the code.
- **Trace from the first commit.** Every node visit emits `{run_id, node, edge_taken, timestamp, attempt}`. Verification depends on these traces.
- **Model routing comes from config:** `ORCHESTRATOR_MODEL` (Opus tier) and `FINAL_CHECK_MODEL` (Sonnet tier). The orchestrator never grades its own answer.
- **Never invent the 5 accuracy metrics.** Find them in the repo or PRD, or stop and ask.
- **Reuse before building.** Connect to the existing Jev classifier, playbooks, tools and DB layer where they exist. Follow the repo's language, lint and test conventions.
- If a verification check fails, fix the code. Never change the spec or the test to make it pass.
