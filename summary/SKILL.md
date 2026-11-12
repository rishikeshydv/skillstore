---
name: summary
description: Summarize everything the agent did in 2-3 plain sentences that still carry the main gist. Use at the end of a multi-step task, or whenever the user asks "what did you do?", "tl;dr", "recap", "summarize your work", or similar.
---

# Work Summary

Condense a session's work into **2–3 sentences** that a busy reader can absorb in five seconds and still know what happened, what changed, and whether anything needs their attention.

## When to use

- The agent has just finished a task with several steps (code changes, research, file edits, tool calls).
- The user asks for a recap, TL;DR, or "what did you do?"
- A handoff is needed (to another agent, a teammate, or a future session).

## How to write it

Before writing, silently answer three questions from the session history:

1. **Outcome** — What is the end result? (Built, fixed, found, decided, or failed.)
2. **Substance** — What were the one or two changes or findings that matter most? Name concrete things: files, functions, numbers, sources, decisions.
3. **Loose ends** — Is anything unfinished, broken, assumed, or waiting on the user?

Then write:

- **Sentence 1 — the outcome.** Lead with the result, not the process.
- **Sentence 2 — the substance.** The key specifics that make the outcome real and checkable.
- **Sentence 3 (only if needed) — loose ends.** Open issues, assumptions made, or the one next step. Skip it if there's genuinely nothing to flag.

## Rules

- **Hard limit: 3 sentences.** No run-on sentences stitched with semicolons to cheat the limit.
- **Outcome over process.** Don't narrate steps ("First I read the file, then I…"). The reader wants the result.
- **Be specific.** "Fixed the null-check in `parse_alert()` that crashed on empty payloads" beats "Fixed a bug."
- **Be honest.** If something failed, was skipped, or is a guess, say so plainly. Never imply success that didn't happen.
- **Plain prose.** No bullets, headers, bold, or emoji. Past tense, active voice.
- **No filler.** Drop openers like "In this session I…" or "Great news!" and closers like "Let me know if you need anything else."
- **Prioritize ruthlessly.** If ten things happened, mention the two that matter; the rest are implied by the outcome.

## Edge cases

- **Nothing changed** (only reading or investigating): state what was learned and what it means. One or two sentences is fine.
- **Task failed**: Sentence 1 says it failed and why; sentence 2 says what was tried or what's still intact; sentence 3 says what would unblock it.
- **Multiple unrelated tasks**: Give each its own clause or sentence, most important first. If they can't fit in 3 sentences, summarize at a higher level ("Completed all four config migrations; only the staging one needed manual fixes").

## Examples

**Good**
> Added retry logic to the webhook sender so failed deliveries are retried up to 3 times with exponential backoff. The change lives in `notifier/send.py`, and all 42 existing tests plus 5 new ones pass. I assumed a 30-second max backoff, so adjust `MAX_DELAY` if your SLA differs.

**Good (research)**
> Compared five vector databases for the RAG pipeline and recommend pgvector, since it covers your scale (~2M embeddings) without a new service to run. Pinecone was the runner-up but costs roughly 4x more at your volume.

**Good (failure)**
> The database migration did not complete because the `users` table has a foreign-key conflict on `org_id`. No data was changed, since the migration rolled back cleanly. Fixing the 12 orphaned rows listed in `orphans.csv` should let it run.

**Bad**
> In this session, I first read through the codebase to understand the structure, then I looked at the webhook module, then I made some changes to improve reliability, and finally I ran the tests which all passed. Let me know if you have questions!

Why it's bad: narrates process, vague ("some changes"), no specifics, filler closer, and buries the outcome.
