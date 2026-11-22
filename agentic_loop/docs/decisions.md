# Decisions to confirm before M1

The diagram doesn't settle these. Ask about all of them in one message, suggest the default in brackets, and record the answers in `docs/agentic_loop/LOOP_MAP.md`.

1. **The 5 accuracy metrics.** Look for their names and definitions in the repo, PRD or docs first. If you can't find them, **stop and ask**. Don't invent metrics.
2. **Retry budget** for `retries_left?` [default: 2 retries, so 3 attempts in total].
3. **What "Jev" is.** Is it an existing service, module or model? Where does it live, and what does it return?
4. **Fallback response content.** Fixed text, a template, or escalation to a human? [default: fixed safe message plus a logged incident]
5. **Decline response content.** What does the user see? [default: short polite out-of-scope message]
6. **Clarification transport.** How does the pause/resume work in this product (same request, session state, queue)? Where is run state stored while paused?
7. **Tool-loop guard.** The diagram has no limit on call_tool → orchestrator cycles. Should there be a max-iteration guard, and where does it lead? [suggest: max N tool iterations, then treat the run as a failed answer and send it to `retries_left?`]. **This changes the graph, so it needs explicit sign-off.**
8. **final_check in free-form mode.** In free-form mode there is no playbook, so does final_check run only the 5 metrics? [default: yes]
