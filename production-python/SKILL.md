---
name: production-python
description: Write, refactor and review Python to the Google Python Style Guide (pyguide) — imports, naming, docstrings (Args/Returns/Raises), type annotations, exceptions, formatting, strings and logging. Use whenever the user writes or edits Python, asks for a code review or lint cleanup, mentions "Google style", "pyguide", pylint, Black/Pyink, or Google-style docstrings, or wants a Python codebase made consistent — even if they don't name the guide.
---

# Google Python Style

This skill encodes the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
as a set of focused reference files. SKILL.md is the router: it holds the
workflow, the rules that apply to almost every file, and a map of which
`docs/` file to open for everything else. Open only the docs the task needs.

## The overriding rule: be consistent

The guide closes with one principle that outranks the rest: **match the code
around you**. Style rules exist so readers can focus on *what* the code says,
not *how* it's written. So:

- **Editing existing code** → read the surrounding file first and follow its
  local conventions (quote style, docstring indent, naming suffixes), even where
  they differ from the defaults below.
- **New files or new projects** → apply the guide as written.
- Consistency doesn't justify spreading a clearly outdated pattern (e.g.
  `typing.List`, `# type:` comments, relative imports) into new code. When a
  local convention conflicts with a correctness or clarity rule, follow the rule
  and mention the difference to the user.

## Workflow

**When writing or modifying Python:**
1. Skim the target file (if one exists) for local conventions.
2. Apply the *Always-on rules* below while writing.
3. Open the relevant `docs/` file when you touch its topic — e.g. writing a
   public function → `docs/docstrings-and-comments.md` and
   `docs/type-annotations.md`; adding imports → `docs/imports.md`.
4. Before finishing, run through `docs/review-checklist.md` on the code you
   produced.

**When reviewing code:**
1. Read `docs/review-checklist.md` and work through it top to bottom.
2. For each finding, cite the guide section (e.g. "§3.16 Naming") so the author
   can look it up, show the fix, and separate *must-fix* (bugs, correctness,
   API hazards) from *style nits*.
3. Don't flag things an auto-formatter (Black/Pyink) would fix unless the
   project has no formatter — suggest adding one instead.

## Always-on rules (the 80/20)

These come up in nearly every file. Details and edge cases live in the docs.

- **Imports**: `import x` / `from pkg import module` — import modules, not
  classes or functions (exception: `typing`, `collections.abc`,
  `typing_extensions`). Full package paths, never relative. One per line,
  grouped stdlib → third-party → local, sorted. → `docs/imports.md`
- **Naming**: `module_name`, `ClassName`, `function_name`, `CONSTANT_NAME`,
  `_internal`. Descriptive, no ambiguous abbreviations, no type in the name.
  → `docs/naming.md`
- **Layout**: 4-space indent, no tabs, 80-char lines, no backslash
  continuations (use parentheses), two blank lines between top-level defs.
  → `docs/formatting.md`
- **Docstrings**: `"""` always; one-line summary ≤80 chars ending in
  punctuation; `Args:` / `Returns:` (or `Yields:`) / `Raises:` sections for
  public, non-trivial or non-obvious functions. → `docs/docstrings-and-comments.md`
- **Types**: annotate public APIs; `X | None` explicitly, never `x: str = None`;
  built-in generics (`list[int]`) and abstract params (`Sequence`).
  → `docs/type-annotations.md`
- **Exceptions**: no bare `except:` or `except Exception` unless re-raising or
  at an isolation boundary; never `assert` for validation; small `try` bodies.
  → `docs/exceptions.md`
- **Defaults & truthiness**: no mutable default args; `if x is None:` for
  None checks; `if not seq:` for emptiness. → `docs/language-features.md`
- **Strings & logging**: format with f-strings / `%` / `.format`, not `+`
  chains; logging calls take a `%`-pattern literal plus args, never an
  f-string. → `docs/strings-and-logging.md`
- **Executables**: logic in `main()`, guarded by `if __name__ == '__main__':`.
  → `docs/program-structure.md`

## Docs map

| Topic | File | Guide sections |
| --- | --- | --- |
| pylint usage, suppressions, formatters | `docs/lint.md` | §1, §2.1 |
| import style, packages, ordering, `__future__` | `docs/imports.md` | §2.2, §2.3, §2.20, §3.13 |
| raising/catching, custom exceptions, error messages | `docs/exceptions.md` | §2.4, §3.10.2 |
| globals, nesting, comprehensions, iterators, generators, lambdas, ternaries, defaults, truthiness, scoping, threading, power features | `docs/language-features.md` | §2.5–§2.12, §2.14, §2.16, §2.18, §2.19 |
| properties, decorators, `staticmethod`/`classmethod`, getters/setters | `docs/classes-and-decorators.md` | §2.13, §2.17, §3.15 |
| semicolons, line length, parens, indentation, trailing commas, blank lines, whitespace, shebang, one statement per line | `docs/formatting.md` | §3.1–§3.7, §3.14 |
| module/function/class docstrings, comments, TODOs | `docs/docstrings-and-comments.md` | §3.8, §3.12 |
| string formatting, quotes, multi-line strings, logging | `docs/strings-and-logging.md` | §3.10, §3.10.1 |
| naming conventions table, names to avoid, file names, math notation | `docs/naming.md` | §3.16 |
| files/sockets/resources, `main()`, function length | `docs/program-structure.md` | §3.11, §3.17, §3.18 |
| type hints: rules, line breaks, `None`, aliases, TypeVars, typing imports, cycles, generics | `docs/type-annotations.md` | §2.21, §3.19 |
| condensed review checklist | `docs/review-checklist.md` | all |

## Attribution

Rules are paraphrased and condensed from the Google Python Style Guide
(https://google.github.io/styleguide/pyguide.html), © Google, licensed under
CC BY 3.0. Examples are rewritten for this skill. When in doubt about a
detail, the upstream guide is authoritative.
