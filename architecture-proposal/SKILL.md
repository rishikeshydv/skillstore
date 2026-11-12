---
name: architecture-proposal
description: Create or revise LG Ad Solutions-branded architecture proposal documents for a new technical feature, software framework, platform, service, or system redesign. First ask which deliverable the user wants (One-Pager, High-Level Design/HLD, Low-Level Design/LLD, or All Three), unless explicitly selected. Adaptively interview for missing technical context, critique architectural trade-offs, and deliver only the selected polished DOCX document(s). Use also for iterative reviewer comments, proposal restructuring, or design review of these artifacts.
---

# Architecture Proposal

Build one or more **separate** branded deliverables from the user's architecture idea. Do not automatically generate all three.

## Mandatory document selection

1. Read the existing user conversation, notes, and files. Never re-ask something already answered.
2. If the user has not selected a deliverable, **stop and ask exactly one selection question**: "Which would you like me to create: (1) One-Pager, (2) HLD, (3) LLD, or (4) All Three?" Wait for the selection. Do not assume the HLD is one page.
3. If the user explicitly requests one deliverable, proceed directly, without the selection question. If they explicitly request multiple, create only those requested.
4. If **All Three** is selected, generate three **independent, cross-referenced files**: One-Pager, HLD, and LLD, with progressively deeper detail. Avoid copying the same prose into all three.
5. Preserve the user's later selection and edits within the conversation. On revision, update **only** the named documents and sections unless asked to rebuild the others.

## Purpose of the three documents

| Deliverable | Length | Main question | Required references |
|---|---|---|---|
| One-Pager | **Exactly one physical page** | Why propose it, and who will own it? | `references/one-pager.md` |
| HLD | As long as needed | What architecture should we adopt, and why? | `references/hld.md` |
| LLD | In depth where warranted | How exactly should we build, verify, and maintain it? | `references/lld.md` |

The One-Pager is **not** a shortened HLD. An HLD is **not** constrained to one page. An LLD is **not** a fixed checklist of specialist concerns.

## Workflow

1. **Select** document(s) per the mandatory rule above.
2. **Discover**: read `references/discovery.md`; ask only the smallest useful set of missing questions. Inputs may be unstructured notes, architecture diagrams, code snippets, requirements, existing files, or conversation details. For the LLD, ask for key interface and lifecycle constraints if missing, but do not demand all technical minutiae up front.
3. **Structure**: read only the reference(s) for selected document(s). Preserve the exact core headings from those references. Include conditional subtopics only when relevant; avoid filler headings.
4. **Draft**: write problem/customer behavior before infrastructure. Label evidence, measured facts, assumptions, estimates, and open questions separately. Never invent numbers, costs, deadlines, approvers, architecture facts, or final decisions. Mark unknowns `TBD` or Open Question.
5. **Critique**: use `references/review-gates.md` to challenge major decisions, boundaries, alternatives, correctness, rollout, failure behavior, security, and operational implications in proportion to the selected deliverable.
6. **Generate**: read `references/output-and-brand.md` for the JSON contract, LG Ad Solutions design, rendering commands, page limits, and verification. Use bundled `scripts/render_proposal.py`. Default to a branded editable DOCX; also provide other requested output formats if feasible.
7. **Verify**: render all pages to images, inspect, and repair layout issues. **For a One-Pager, verify actual page count is one**; if longer, summarize/eliminate low-value detail rather than shrinking text into unreadability.
8. **Deliver**: share only selected document links and a concise summary of key open issues. For All Three, provide three independently labeled download links.

## Reviewer comments and iteration

- Accept comments on headings or sections such as "keep", "modify", "merge", "remove", and free-text notes.
- Preserve untouched sections and content; apply edits only to selected areas and update impacted cross-references.
- If the user requests an in-chat review instead of immediate files, present the section outline with editable/commentable notes before document generation.
- Do not add an HLD "Approval" section: its closing section is **Risks & Open Questions**.
- Do not add an One-Pager "Recommendation & Next Steps" section: its closing section is **Maintenance & Ownership**.
- For LLD, keep **eight core sections**; nest specialized detail inside them or optional deep dives instead of mandating large standalone sections.

## Data boundaries and reference priorities

- Use user-provided conversation/files as the source of truth. Do not call private organizational connectors unless the user **explicitly requests** them and use is authorized.
- Public web research is optional if explicitly requested or materially needed to verify unfamiliar/current facts. Never infer internal system facts from public sources.
- Reuse validated LG Ad Solutions brand files in `assets/`. Do not recolor, distort, shadow, or redistribute typeface files. The bundle includes logo images and brand specifications, **no proprietary fonts**.
- Stop at architecture/implementation readiness unless downstream delivery plans are explicitly requested.
