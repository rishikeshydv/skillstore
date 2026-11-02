# Cleanup Workflow

## 1. Establish repository context

- Locate the repository root and read applicable `AGENTS.md` files and contribution instructions.
- Inspect the current branch and working tree before editing. Preserve all pre-existing user changes; do not overwrite or reformat unrelated work.
- Identify the language, build system, package manifests, test and CI setup, documentation, and ignore rules from repository files.
- If no repository is available or the target is ambiguous, ask the user to open or identify it.

## 2. Review concrete cleanup opportunities

Inspect the repository for:

- Stale generated output, temporary files, accidental duplication, obsolete comments, and clearly unused code. Preserve TODOs and partial work whose purpose is unclear.
- Likely credentials or sensitive files. Do not print secret values; report findings with values redacted.
- Large or generated files that may not belong in version control. Confirm intent before deleting assets or changing tracking behavior.
- Dependency, security, or CI issues only when there is evidence in the repository or from an explicitly requested check. Do not imply a live audit if none was performed.
- Gaps in README, licensing, contribution guidance, code of conduct, docs, issue templates, or vulnerability reporting when reviewing open-source readiness.

Prioritize a short list of useful improvements. Avoid speculative refactors and avoid deleting code unless its lack of use is clear from references and configuration.

## 3. Make safe, focused edits

- Limit changes to the requested scope and follow local conventions.
- Add or update ignore rules only for clearly generated or local-only files; make sure useful project files will not be hidden.
- Remove code only when it is demonstrably unused and no configuration, generated entry point, or dynamic lookup depends on it.
- Update documentation only with verified project details. Do not invent commands, supported platforms, maintainers, security contacts, release status, or badges.
- Never choose a software license for the owner. If it is missing, report that the owner needs to choose one.
- Do not run tests, add tests, or claim tests passed unless the user asks for testing or verification. If asked, use the documented project commands and report observed results.

## 4. Review the result

Inspect the final diff for scope, unintended deletions, formatting, and preservation of existing changes. Report exactly what changed, what remains unresolved, and what verification was actually performed.
