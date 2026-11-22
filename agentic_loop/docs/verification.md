# Final verification (required, last step)

Don't report the loop as complete until all of these pass. If any check fails, fix the code. Never change the spec or the test to make a check pass.

## 1 Graph conformance
Read the node and transition set from the implementation itself (the state machine definition or the graph object), not from the docs, and compare it with `docs/spec.md` §1.2 and §1.3.
- Expected: **16 nodes, 18 edges, 0 missing, 0 extra.** Any guard approved in `docs/decisions.md` item 7 is listed as an approved deviation.

## 2 Path coverage (end-to-end, mocked models and tools)
Each scenario must produce **exactly** this node sequence in its trace:

| # | Scenario | Expected trace |
|---|----------|----------------|
| P1 | Out of scope | query → question_classifier → playbook_match?(no) → in_agent_scope?(no) → decline |
| P2 | Playbook-guided happy path | … playbook_match?(yes) → playbook → orchestrator[guided] → next_action?(answer) → final_check → pass?(yes) → final_response |
| P3 | Free-form happy path | … playbook_match?(no) → in_agent_scope?(yes) → orchestrator[free_form] → next_action?(answer) → final_check → pass?(yes) → final_response |
| P4 | Tool success then answer | … orchestrator → next_action?(call_tool) → tool_calling ↔ database → orchestrator → next_action?(answer) → final_check → pass?(yes) → final_response |
| P5 | Tool error recovery | as P4, but the tool raises; orchestrator gets an `error` result and still ends in a terminal state |
| P6 | Clarification round trip | … next_action?(ask_user) → ask_user_for_clarification → [paused] → reply → orchestrator → … → final_response |
| P7 | Fail then pass on retry | … final_check → pass?(no) → retries_left?(yes) → orchestrator (feedback has the failure reason) → … → pass?(yes) → final_response |
| P8 | Retries exhausted | final_check fails on every attempt → retries_left?(no) → fallback_response after exactly `1 + retry_budget` final_check calls |

## 3 Invariant checks
Write a test for each of the 7 invariants in `docs/spec.md` §1.4. At minimum, check these:
- No trace has `final_response` without a `pass?(yes)` immediately before it.
- P1 makes zero orchestrator, tool and final_check calls.
- The orchestrator calls use `ORCHESTRATOR_MODEL` and final_check calls use `FINAL_CHECK_MODEL`; the two are never the same call.
- In P7, the orchestrator input on attempt 2 contains attempt 1's `failure_reason`.

## 4 Live smoke test (behind a flag, real models)
Run P1, P2 and P3 against real models with one real query each, if the environment allows it. Record the traces. Skip this test, and say so in the report, if credentials aren't available.

## 5 Report
Write `docs/agentic_loop/VERIFICATION.md` with:
- The conformance result from the graph conformance check (node and edge counts, diff).
- A table: each edge E1–E18 → the test(s) covering it → pass/fail. **Every edge must be covered by at least one test.**
- A table: each path P1–P8 → test name → pass/fail → trace excerpt.
- Invariant results.
- Deviations from the diagram: either **none**, or each one listed with who approved it.
- Open items (for example, a live smoke test that was skipped).

Only after this report is all green: tell the human the loop is complete and link the report.
