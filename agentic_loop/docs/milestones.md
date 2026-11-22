# Milestones

Do them in order. A milestone is done only when every item in its **Done when** list is true. Don't start the next one before that.

### M0 — Recon and loop map
Read the repo and the PRD. Produce `docs/agentic_loop/LOOP_MAP.md` with:
- Every node N1–N16 mapped to `file:function` (existing) or `NEW`.
- Every edge E1–E18 mapped to where it will be implemented.
- Answers to all of `docs/decisions.md`.

**Done when:** all 16 nodes and 18 edges are mapped, the 5 metrics are named and defined, the retry budget is set, and the human has approved the map.

### M1 — State machine skeleton and tracing
- Define all 16 nodes as states, all 18 edges as transitions, and the 3 terminal states plus the paused state.
- Stub every process node with the real input/output types in `docs/spec.md` §1.2.
- Add trace events on every transition.
- Add a **graph conformance test** that reads the transitions from the code and checks them against the table in `docs/spec.md` §1.3.

**Done when:** the conformance test passes (exactly 16 nodes and 18 edges, nothing missing or extra), and a run with stubs ends in a terminal state with a full trace.

### M2 — Intake: classifier, routing, decline, playbook
Implement N1–N6 and E1–E7. The classifier returns the playbook match and the scope decision in one call.

**Done when:** tests prove that a matched query → `playbook` → orchestrator in `guided` mode, an unmatched in-scope query → orchestrator in `free_form` mode, and an unmatched out-of-scope query → `decline` with **zero** orchestrator or tool calls.

### M3 — Orchestrator, next action, tools, database
Implement N7–N10 and E8–E11. The orchestrator runs on `ORCHESTRATOR_MODEL` and returns a structured decision: `call_tool` / `ask_user` / `answer`. Tool results **and errors** go back into the orchestrator's context.

**Done when:** tests prove each `next_action` value routes correctly, a tool reads and writes the DB, and a tool that throws produces an error result the orchestrator receives and can recover from. The run doesn't crash.

### M4 — Ask user for clarification
Implement N11 and E12: save the run state, send the clarification question, resume on the user's reply with the reply in the orchestrator's context, and keep the run_id and attempt count.

**Done when:** a test runs a full ask → pause → reply → resume → answer cycle and the trace shows it as one continuous run.

### M5 — final_check, retries, terminals
Implement N12–N16 and E13–E18. `final_check` runs on `FINAL_CHECK_MODEL`, checks against the playbook (when there is one) and all 5 metrics, and returns `pass` plus a `failure_reason` that names the metric(s) that failed.

**Done when:** tests prove that pass → `final_response`; fail with retries left → orchestrator gets the failure reason in context on the next attempt; fail with no retries left → `fallback_response`; and the attempt counter is correct.

### M6 — Final verification
Run `docs/verification.md` in full and produce the report.

**Done when:** every check in `docs/verification.md` is green and `docs/agentic_loop/VERIFICATION.md` is committed.
