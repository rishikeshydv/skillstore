# Type annotations (§2.21, §3.19)

## Policy (§2.21)

- Strongly encouraged when updating code. **When adding or modifying a public
  API, include annotations** and enable type checking (pyrefly, mypy, pyright)
  in the build.
- Annotations live in the source; use `.pyi` stubs for third-party or
  extension modules.
- If something blocks adoption (bad inference, tooling issue), leave a TODO
  with a bug link explaining it (see `docstrings-and-comments.md` → TODO).

## General rules (§3.19.1)

- Don't annotate `self`/`cls` unless needed; use `typing.Self` when it is
  (`def clone(self) -> Self`, classmethod constructors).
- No need to annotate `__init__`'s return.
- Use `Any` when a type genuinely shouldn't be expressed.
- Not every function needs annotations. Prioritize:
  - public APIs (at minimum)
  - code prone to type bugs or with a history of them
  - hard-to-understand code
  - code whose types have stabilized (mature code can often be fully annotated)

## Line breaking (§3.19.2)

Follow the normal indentation rules. Annotated signatures often become one
parameter per line; add a trailing comma after the last parameter so the
return type gets its own line, with `)` aligned to `def`.

```python
def schedule(
    self,
    job: Job,
    run_at: datetime.datetime | None,
) -> ScheduleResult:
    ...
```

- If everything fits on one line, keep it on one line.
- Break **between** parameters, not between a name and its type.
- Return type on the last parameter's line is acceptable:
  `    run_at: datetime.datetime) -> ScheduleResult:`
- Don't put `)` on its own line aligned with the opening `(` — less readable.
- Avoid breaking inside a type; if unavoidable, keep subtypes intact.
- If one `name: type` is still too long, prefer a type alias; last resort,
  break after the colon and indent 4.

```python
# Yes (last resort)
def load(
    source:
        storage_backends.CompressedRemoteSource,
) -> None: ...

# No
def load(
    source: storage_backends.
        CompressedRemoteSource,
) -> None: ...
```

## Forward declarations (§3.19.3)

To reference a class not yet defined (including itself), use
`from __future__ import annotations`, or quote the name: `'Node'`.

## Defaults (§3.19.4)

Spaces around `=` **only** when the parameter has both an annotation and a
default: `def f(limit: int = 10)`, but `def f(limit=10)`.

## None (§3.19.5)

A parameter that can be `None` must say so. Prefer `X | None` (Python 3.10+);
`Optional[X]` / `Union[...]` are acceptable in older code. **No implicit
Optional.**

```python
# Yes
def find(name: str, default: str | None = None) -> str | int | None: ...

# No
def find(name: str, default: str = None) -> str: ...
def find(name: Union[None, str]) -> str: ...      # Write `str | None`.
```

## Type aliases (§3.19.6)

- CapWords names; `_Private` if module-only.
- Annotate as `TypeAlias` so readers can tell it from a regular global.
- Don't use aliases to dodge the import-modules-not-symbols rule
  (e.g. `Thing = some_module.Thing` just to shorten references in public code).
  A `_Private` alias for an inconveniently long name is OK if it isn't used in
  a public signature.

```python
from typing import TypeAlias

_Embedding: TypeAlias = tuple[float, ...]
SearchIndex: TypeAlias = Mapping[str, _Embedding]
```

## Ignoring types (§3.19.7)

`# type: ignore` disables checking on a line. Prefer the checker's
error-specific form (pyrefly: `# pyrefly: ignore[attribute-error]`; mypy:
`# type: ignore[attr-defined]`).

## Variables (§3.19.8)

Annotate a variable when its type is hard to infer:
`client: BillingClient = make_client()`. This is common for values that come
back as `Any` (`json.load()`, `pickle.load()`, untyped libraries) — annotate
them before returning them from a typed function, or strict checkers report
`no-any-return`:

```python
records: list[Record] = json.load(records_file)['records']
return records
```

**Don't add new `# type:` comments** (pre-3.6 syntax).

## Tuples vs lists (§3.19.9)

`list[T]` holds one type. Tuples are either homogeneous (`tuple[int, ...]`) or
fixed-shape (`tuple[int, str, float]`), the latter common for return values.

## Type variables (§3.19.10)

Use `TypeVar` / `ParamSpec` for generics; constrain where useful
(`TypeVar('Numeric', int, float)`). `AnyStr` covers "all `str` or all
`bytes`".

Naming: a TypeVar must be **descriptive unless it is both private and
unconstrained**.

```python
# Yes
_T = TypeVar('_T')
_P = ParamSpec('_P')
Numeric = TypeVar('Numeric', int, float)
AnyCallable = TypeVar('AnyCallable', bound=Callable)

# No
T = TypeVar('T')                       # Public: needs a descriptive name.
_T = TypeVar('_T', int, float)         # Constrained: needs a descriptive name.
_F = TypeVar('_F', bound=Callable)     # Bounded: same.
```

## String types (§3.19.11)

`str` for text, `bytes` for binary. Don't use `typing.Text` in new code. Use
`AnyStr` when all string-typed params/returns must match.

## Typing imports (§3.19.12)

- From `typing` and `collections.abc`, **import the symbols directly**;
  several per line is allowed:
  `from collections.abc import Mapping, Sequence`,
  `from typing import Any, TYPE_CHECKING, cast`.
- Treat those names like keywords — don't define your own `Any`, `Sequence`,
  etc. On a genuine clash, `from typing import Any as AnyType`.
- In signatures, prefer **abstract** parameter types (`Sequence`, `Mapping`,
  `Iterable`) over concrete ones (`list`, `dict`).
- When concrete types are needed, use built-ins (`list[int]`,
  `tuple[str, int]`, `dict[str, int]`), **not** `typing.List`/`Tuple`/`Dict`.

```python
# Yes
from collections.abc import Sequence

def centroid(points: Sequence[tuple[float, float]]) -> tuple[float, float]: ...

# No
from typing import List, Tuple

def centroid(points: List[Tuple[float, float]]) -> Tuple[float, float]: ...
```

## Conditional imports (§3.19.13)

Discouraged — prefer refactoring so imports can be top-level. When an import is
needed only for type checking and must be avoided at runtime:

- put it in an `if TYPE_CHECKING:` block right after the normal imports
- reference those types as strings
- define anything used only for typing (including aliases) inside the block
- no blank lines within it; sort it like a normal import list

```python
import typing

if typing.TYPE_CHECKING:
    from acme.reports import renderer

def export(doc: 'renderer.Document') -> bytes: ...
```

## Circular dependencies (§3.19.14)

Typing-induced import cycles are a code smell — refactor if you can. Otherwise
replace the offending module with an `Any`-typed alias (one blank line after the
imports) and keep the real type name in a string so it still reads correctly:

```python
from typing import Any

orders = Any  # acme/orders.py imports this module.


def attach(self, order: 'orders.Order') -> None: ...
```

## Generics (§3.19.15)

Always give type parameters to generic types; bare `Sequence` means
`Sequence[Any]`. If the honest answer is "anything", consider a `TypeVar`
before writing `Any`.

```python
# Yes
def index_by_id(records: Sequence[_T]) -> Mapping[int, _T]: ...

# No — silently Sequence[Any] -> Mapping[Any, Any]
def index_by_id(records: Sequence) -> Mapping: ...
```
