---
name: artifact
description: Publish a Claude Code Artifact in the user's established house style (warm neutral palette, IBM Plex Sans/Mono, status-pill cards, an optional stats strip, evidence-driven prose with an explicit "still open" section, a governance-aware footer). Use whenever the user asks to turn findings, a report, a status update, or a project summary into a shareable page, or invokes /artifact directly.
argument-hint: <topic or content to turn into an artifact>
user-invocable: true
---

# House-style artifact

Publish an Artifact using a fixed visual and structural system, instead of
deriving a fresh design from scratch. This skill is a thin layer on top of the
`artifact-design` skill, not a replacement for it.

## Before anything else

1. Load the `artifact-design` skill. It remains authoritative for the page
   *contract*: the CDN allowlist, `<title>` rules, the three-tier theme-token
   structure, responsive rules, size limits, and favicon requirement. Everything
   below fixes the *choices* that contract leaves open — it does not override any
   rule stated there.
2. Read `template.html` in this skill's directory. It is the starting point for
   the `<style>` block and page skeleton — copy it into the new artifact file,
   then adapt it per the rules below. Do not publish `template.html` itself, and
   do not treat it as a fill-in-the-blanks form to leave unedited.
3. Understand what `$ARGUMENTS` actually is before writing anything: a topic name,
   a pile of findings, a file path, or a request to summarize the current
   conversation. Ground the whole page in real content from it — never lorem,
   never a placeholder structure the content doesn't support.

## Palette

- Warm paper background, never pure white. A considered off-black ink, a muted
  warm grey for secondary text, a hairline warm-toned border.
- **Pick one deliberate accent hue for this subject** — do not default to the
  same color as the last artifact. Stay in a warm-neutral-compatible family:
  teal, copper/amber, muted indigo, sage, and rust all work; choose based on what
  actually fits the subject (an audit or investigation can read differently from
  a dashboard or a proposal).
- A semantic good/warn/bad triad with soft background tints, used only for real
  status, never decoration.
- Full light/dark support via `template.html`'s three-tier pattern. When picking
  a new accent, recompute its dark-mode twin too (usually lighter and more
  saturated so it still reads on a dark ground) — don't just reuse the light
  value under `prefers-color-scheme: dark`.

## Type

- IBM Plex Sans for body/UI text and IBM Plex Mono for data, code, and any
  aligned numbers (`font-variant-numeric: tabular-nums`) are the fixed base for
  every artifact this skill produces.
- A serif display face for headings (Fraunces, or one with similar warmth and
  character) is an **optional per-subject flourish**, not a rule. Add it when the
  page reads as a report or investigation; skip it when the page should feel more
  like a live dashboard or tool. Decide once per artifact and apply it
  consistently to `h1`/`h2`/any numbered node — never mix serif and sans headings
  on the same page.

## Anatomy

In order, top to bottom:

1. **Eyebrow** — uppercase, mono, colored with the accent. Names the project or
   area, not the page's own title.
2. **H1** — short and specific, 2-4 words, naming this exact subject (never a
   generic label like "Report" or "Update").
3. **Thesis** — one paragraph, muted color, capped near 62 characters wide. What
   this page documents, why it exists now, what the reader should walk away
   knowing.
4. **Meta row** — date, and a privacy/status note if relevant (e.g. "Private ·
   not for redistribution").
5. **Stats strip** — 3-4 big mono-number tiles with a short caption each. Include
   this only when there are that many real headline numbers worth leading with;
   don't manufacture one to fill the slot.
6. **Content**, sectioned. See "Structure" below for the two shapes to choose
   between.
7. **Footer** — a governance/exclusion note whenever real or sensitive data
   underlies the content (what's deliberately left out, e.g. "contains no
   customer question or answer text"), plus the date and a sourcing pointer if
   there's a fuller record elsewhere (a doc, a plan file, a repo).

## Structure: pick one, don't default to the numbered trail

- **Plain sectioned cards** (the default): a `<section>` per topic, each with a
  `.card` containing an `h2`, optionally a status `.pill`, and real content. Use
  this whenever the topics are independent or only loosely ordered.
- **Numbered trail** (`.trail`/`.finding`/`.node`): a connected, numbered spine of
  cards. Use this *only* when the content is genuinely sequential — a real
  investigation where each finding led to the next, a timeline, a build order.
  Numbering must encode real information (what happened 1st, 2nd, 3rd), never be
  decoration on an unordered list. This is `artifact-design`'s own "structure is
  information" rule, applied to this specific component.

Within either shape, use only the smaller components the content actually calls
for:

- **Status pills** — one closed vocabulary of real states for *this* subject
  (e.g. done/blocked/open, or shipped/paused/investigating — name them for what
  they mean here, never a generic "status: active").
- **`.ev`/`.ev-row`** — key/value evidence blocks for citing something concrete
  inline: a count, a commit hash, a cost, a file path.
- **`.callout`** — reserve for exactly one key insight per section. If a section
  has no single standout insight, skip the callout rather than forcing one.
- **Tables** — for real tabular comparisons, with numeric columns in mono.

## Content and tone

- Every claim is backed by something concrete: a real number, a commit hash, a
  file:line reference, a measured cost — never a vague summary standing in for
  evidence.
- When something genuinely isn't decided, say so plainly in its own section
  ("still open," "your call") rather than implying false certainty or silently
  picking an answer.
- Report negative or inconclusive results as directly as positive ones — an
  artifact in this style is a record of what's actually true, not a highlight
  reel.

## After publishing

Report the link back in the same plain, direct terms as the rest of this style —
what the page covers, and, if relevant, what's still open that the page itself
flags.
