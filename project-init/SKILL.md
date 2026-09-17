---
name: project-init
description: Sets up and maintains a project's "init" — CLAUDE.md, docs/Architecture.md, docs/Prod-Spec.md, and docs/Milestones.md — so coding sessions stay grounded in a real spec instead of drifting from prompt to prompt. Use this whenever the user starts a new coding project or feature, says something like "let's build X," "set up project docs," "vibe code this," or asks to scaffold/standardize a project. Also use it mid-project whenever an implementation decision, scope change, or completed task needs to be written back into the docs — even if the user doesn't explicitly ask, since letting the docs go stale defeats the point. If these files already exist in the project, this skill's job shifts from creating them to reading and keeping them current.
---

# Project Init

A small set of living documents that give Claude (and the user) persistent
memory across coding sessions, instead of re-deriving context from scratch
every time. Modeled on the idea that the spec, not the code, is the primary
artifact — the code is just what the spec compiles down to.

This skill has two modes. Always check which one applies before doing
anything else.

## Step 0: Detect the mode

Look in the project root (and `docs/`) for:

- `CLAUDE.md`
- `docs/Architecture.md`
- `docs/Prod-Spec.md`
- `docs/Milestones.md`

**None of these exist → SCAFFOLD MODE.** Go to "Scaffolding a new project."

**Some or all exist → MAINTAIN MODE.** Go to "Maintaining an existing
project." Never regenerate files that already exist without being asked —
read them first, always.

---

## Scaffolding a new project

Don't generate these files from a one-line prompt. A thin spec produces a
confidently wrong implementation just as easily as no spec does. Ask first,
generate second.

### Ask the user (keep it to one pass, not a long interview)

1. **What are you building?** One or two sentences — the outcome, not the
   feature list.
2. **What's explicitly out of scope?** What might Claude be tempted to add
   that shouldn't happen (auth, payments, extra pages, etc.)?
3. **Any hard constraints?** Tech stack, libraries to avoid, performance or
   security requirements, things that are already decided and non-negotiable.
4. **Any hard "never" rules?** Things Claude should never do without asking
   first (schema changes, new dependencies, touching auth, deleting data).

If the user says "just use sensible defaults," proceed with reasonable
defaults and state them plainly in the generated files rather than leaving
blanks — a spec with a stated assumption is far better than a spec with a
silent one.

### Generate the four files

Create them in this order, since each one leans on the last:

**1. `docs/Prod-Spec.md`** — what the system should do

```markdown
# Product Spec

Last updated: [DATE]
Status: Draft

## Outcome
[One or two sentences: the user-facing behavior this delivers, not a
feature list.]

## In Scope
- [...]

## Out of Scope
- [Explicit exclusions — this list matters as much as the in-scope list]

## Constraints & Assumptions
- Tech stack: [...]
- Prohibited: [...]
- Performance / security requirements: [...]

## Acceptance Criteria
- [ ] [Concrete, checkable conditions — not "works well"]

## Decisions Log
[Empty at scaffold time. Every time an implementation choice gets made
that isn't already written above, it gets appended here with a date.]
```

**2. `docs/Architecture.md`** — why it's built this way

```markdown
# Architecture

Last updated: [DATE]

## Stack
[Languages, frameworks, storage, key libraries — and why, briefly]

## Key Decisions
[One entry per decision: what was decided, and the one-line reason.
This is the file that stops a future session from "helpfully" undoing
something you chose on purpose.]

## Structure
[Directory / module map — what lives where and why]
```

**3. `CLAUDE.md`** — the operational manual, read at the start of every
session

```markdown
# CLAUDE.md — Project Init

Last updated: [DATE]

## Read First
Before doing anything, read docs/Prod-Spec.md, docs/Architecture.md, and
docs/Milestones.md. Don't assume — check.

## Build & Test
build: [command]
test: [command]
lint: [command]

## Severity Hierarchy
✅ ALWAYS: [e.g. run lint + affected tests before considering a task done]
⚠️ ASK FIRST: [e.g. new dependencies, schema changes, touching auth]
🚫 NEVER: [e.g. commit secrets, skip type checks, delete data without confirmation]

## When Reality Diverges From the Docs
If an implementation decision isn't already written in Prod-Spec.md or
Architecture.md, write it there immediately — same session, not later.
An undocumented decision is a decision nobody else can see.
```

**4. `docs/Milestones.md`** — the task list and progress record

```markdown
# Milestones

Last updated: [DATE]

## Now
- [ ] [Small, independently checkable task]

## Next
- [ ]

## Done
[Move items here as they're verified against Prod-Spec.md's acceptance
criteria — not just "written," but checked.]
```

After generating, show the user all four files and ask them to skim
Prod-Spec.md and Architecture.md in particular — those two are where a
wrong assumption does the most damage if it slips through.

---

## Maintaining an existing project

This is the mode that matters more, and the one people skip.

### At the start of a session

Read all four files before writing any code. Don't rely on memory from
earlier in the conversation — re-read them, since they may have changed.

### While working

- **Follow the Severity Hierarchy in CLAUDE.md.** If something is marked
  "ask first," ask — don't proceed and mention it afterward.
- **If you make a decision that isn't already in the docs** — chose a
  library, handled an edge case a specific way, deviated from the plan for
  a good reason — write it into the right file *in the same turn*, not as
  a follow-up:
  - Scope or behavior change → `docs/Prod-Spec.md` (Decisions Log)
  - Technical/architectural choice → `docs/Architecture.md` (Key Decisions)
  - Task state change → `docs/Milestones.md`
- **If a task is completed,** check it against Prod-Spec.md's acceptance
  criteria before marking it done in Milestones.md — not just "code
  written," but "behavior verified."
- **If the user asks for something that contradicts Prod-Spec.md,** flag
  the contradiction before implementing it. Update the spec first, then
  build — don't let code and spec quietly disagree.

### Red flags to watch for and say out loud

- A task in Milestones.md has been "in progress" across several sessions
  with no corresponding update to Prod-Spec.md or Architecture.md — likely
  sign of undocumented decisions piling up.
- The user describes current behavior that doesn't match what
  Prod-Spec.md says — that's drift; surface it rather than silently coding
  around it.

---

## Notes

- Keep entries in the Decisions Log and Key Decisions short — one line of
  what, one line of why. These files are meant to be read at the start of
  every session, so bloat defeats the purpose.
- This is intentionally lighter than a full enterprise SDD process (no
  separate Coordinator/Implementor/Verifier agents, no multi-phase human
  sign-off). It's sized for a single person or small team doing iterative,
  AI-assisted coding — the goal is catching drift early, not adding
  ceremony.
