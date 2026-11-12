# Naming (§3.16)

## Conventions table (§3.16.4)

| Kind | Public | Internal |
| --- | --- | --- |
| Packages | `lower_with_under` | |
| Modules | `lower_with_under` | `_lower_with_under` |
| Classes | `CapWords` | `_CapWords` |
| Exceptions | `CapWords` (ending in `Error`) | |
| Functions | `lower_with_under()` | `_lower_with_under()` |
| Global / class constants | `CAPS_WITH_UNDER` | `_CAPS_WITH_UNDER` |
| Global / class variables | `lower_with_under` | `_lower_with_under` |
| Instance variables | `lower_with_under` | `_lower_with_under` (protected) |
| Methods | `lower_with_under()` | `_lower_with_under()` (protected) |
| Function / method parameters | `lower_with_under` | |
| Local variables | `lower_with_under` | |

"Internal" = internal to a module, or protected/private within a class.

Acronyms in CapWords are all caps: `HTTPServerError`, not `HttpServerError`.
In snake_case they're lowercase: `send_via_https`.

## General principles

- **Descriptive** names for everything — functions, classes, variables, files.
- **Avoid abbreviations**, especially ones unfamiliar outside the project, and
  never abbreviate by deleting letters inside a word (`cnt`, `msg_q`).
- How descriptive a name must be scales with **how far it's visible**: `i` is
  fine in a 5-line loop, not across nested scopes.
- Follow PEP 8 where this guide is silent.

## Names to avoid (§3.16.1)

- Single characters, **except**:
  - counters/iterators: `i`, `j`, `k`, `v`
  - `e` for an exception in `except ... as e`
  - `f` for a file handle in `with open(...) as f`
  - private unconstrained type variables: `_T = TypeVar('_T')`,
    `_P = ParamSpec('_P')`
  - names that match established notation in a cited paper/algorithm (below)
- Dashes in any package or module name.
- `__dunder__` names (reserved by Python).
- Offensive terms.
- Names that restate the type: `user_list`, `id_to_name_dict` → `users`,
  `names_by_id`.

## Underscores (§3.16.2)

- Single leading `_` marks module-internal or protected. Linters flag
  outside access; **tests may access** protected names of the module under test.
- Double leading `__` (name mangling) is **discouraged** — hurts readability and
  testability and isn't truly private. Use a single `_`.

## Modules and classes

- Put related classes and top-level functions together in one module; one class
  per file is not required.
- Module files are `lower_with_under.py`, not `CapWords.py` (avoids
  `import Foo` vs `from Foo import Foo` confusion).

## Test method names

New unit tests use PEP 8 snake_case, e.g. `test_<method_under_test>_<state>`:
`test_parse_header_rejects_empty_input`. Legacy CapWords suites may use
`testParseHeader_emptyInput`; follow the file's existing pattern.

## Exemption (§3.16.2.1)

Code tightly coupled to an external or non-Python codebase (e.g. an FFI over
C++) may follow that codebase's conventions for consistency.

## File names (§3.16.3)

Must end in `.py` and contain no dashes, so they're importable and testable.
For an extension-less executable, use a symlink or a tiny wrapper script
(`exec "$0.py" "$@"`).

## Mathematical notation (§3.16.5)

In math-heavy code, short names matching a reference's notation (`x`, `W`,
`mu`, `sigma_sq`) are preferred. When you do this:

1. Cite the source of the notation (link to the paper/algorithm) in a comment
   or docstring, or document the convention if the source isn't accessible.
2. Keep **public APIs** on descriptive PEP 8 names — they're seen out of
   context.
3. Silence lint with a narrowly scoped `# pylint: disable=invalid-name` — per
   line for a few names, at block start for many.
