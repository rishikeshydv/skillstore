# Review checklist

Work through this top to bottom when reviewing or self-checking Python. Items
are ordered roughly by impact: correctness and API hazards first, cosmetics
last. Each item points to the doc with the full rule.

When reporting, cite the guide section, show the fix, and label each finding
**must-fix** (bug risk, broken contract, resource leak) or **nit** (style).
Skip anything an auto-formatter already enforces in this repo.

## Correctness and safety

- [ ] No mutable or import-time-evaluated default arguments. → `language-features.md`
- [ ] `None` checked with `is None` / `is not None`; no `x = x or default`
      where a falsy value is valid. → `language-features.md`
- [ ] No bare `except:` / `except Exception:` unless re-raising or at an
      isolation boundary; `try` bodies minimal. → `exceptions.md`
- [ ] No `assert` used for validation or control flow (outside pytest).
      → `exceptions.md`
- [ ] Files, sockets, connections closed via `with` / `contextlib.closing`.
      → `program-structure.md`
- [ ] No mutable global state (or it's `_private`, accessor-wrapped, and
      justified in a comment). → `language-features.md`
- [ ] No reliance on built-in atomicity across threads. → `language-features.md`
- [ ] Executables use `main()` + `if __name__ == '__main__':`; no side effects
      at import. → `program-structure.md`
- [ ] Decorators don't depend on files/network/DB at definition time.
      → `classes-and-decorators.md`
- [ ] Logging uses `%`-pattern literal + args, not f-strings. → `strings-and-logging.md`
- [ ] Error messages state the real condition, mark interpolated values, are
      greppable. → `exceptions.md`

## API design

- [ ] Public functions/methods/classes have type annotations; `X | None`
      explicit; generics parameterized; abstract param types. → `type-annotations.md`
- [ ] Public, non-trivial or non-obvious functions have docstrings with
      `Args:` / `Returns:` or `Yields:` / `Raises:` as needed. → `docstrings-and-comments.md`
- [ ] Properties are cheap and unsurprising; no trivial get/set wrappers.
      → `classes-and-decorators.md`
- [ ] No `@staticmethod` (module function instead); `@classmethod` only for
      named constructors or necessary global state. → `classes-and-decorators.md`
- [ ] Custom exceptions subclass a built-in, end in `Error`, don't stutter.
      → `exceptions.md`
- [ ] No power features (metaclasses, import hacks, `__del__`, reflection
      tricks). → `language-features.md`

## Imports

- [ ] Modules imported, not classes/functions (typing/collections.abc excepted).
      → `imports.md`
- [ ] Full package paths; no relative imports. → `imports.md`
- [ ] One per line; grouped future → stdlib → third-party → local; sorted
      case-insensitively by module path. → `imports.md`
- [ ] `as` aliases only for the allowed reasons / standard abbreviations.
      → `imports.md`

## Readability

- [ ] Names follow the conventions table; descriptive, no type-in-name, no
      vague abbreviations, single letters only where allowed. → `naming.md`
- [ ] Comprehensions have one `for` and at most one filter. → `language-features.md`
- [ ] Ternaries fit one line per part; lambdas are one-liners; `operator`
      used for trivial lambdas. → `language-features.md`
- [ ] Default iteration (`for k in d`, `for line in f`), not `.keys()` /
      `.readlines()`. → `language-features.md`
- [ ] Implicit false for sequences (`if not items:`), not `len(...) == 0`.
      → `language-features.md`
- [ ] Functions much past ~40 lines considered for splitting. → `program-structure.md`
- [ ] Comments explain *why*, not *what*; TODOs use
      `TODO(link): text`. → `docstrings-and-comments.md`
- [ ] String building uses formatting, not `+` chains; no `+=` accumulation in
      loops. → `strings-and-logging.md`

## Formatting (skip if Black/Pyink runs in CI)

- [ ] ≤80 chars (allowed exceptions aside); no backslash continuations.
      → `formatting.md`
- [ ] 4-space indent; aligned or hanging continuation; trailing comma when
      closer is on its own line. → `formatting.md`
- [ ] Blank lines: 2 top-level, 1 between methods, none after `def`.
      → `formatting.md`
- [ ] Whitespace: none inside brackets or before `(`; `=` spacing for kwargs vs
      annotated defaults; no vertical alignment. → `formatting.md`
- [ ] Consistent quote character; `"""` for docstrings. → `strings-and-logging.md`
- [ ] One statement per line; no semicolons. → `formatting.md`

## Finally

- [ ] Does the change match the surrounding file's local conventions? (The
      guide's top rule is consistency.)
