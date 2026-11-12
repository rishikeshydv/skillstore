# Properties, decorators, getters and setters (§2.13, §2.17, §3.15)

## Properties (§2.13)

Use a property only for access that is **cheap, straightforward and
unsurprising** — the reader assumes `obj.attr` is free. Good uses: controlling
access (read-only), or a *trivially* derived value.

- A property that only gets/sets a private attribute with no logic is not
  allowed — make the attribute public instead.
- Create with `@property`; hand-written descriptors are a power feature.
- Don't use properties for computations a subclass might want to override or
  extend — inheritance with properties is non-obvious.
- If it's expensive, does I/O, or has side effects, it's a method, not a
  property.

```python
class Order:
    def __init__(self, items: Sequence[LineItem]):
        self.items = list(items)           # Plain public attribute; no property needed.

    @property
    def item_count(self) -> int:
        """The number of line items."""   # Trivially derived: OK.
        return len(self.items)

    def fetch_shipping_quote(self) -> Quote:   # Network call: a method.
        ...
```

## Getters and setters (§3.15)

Use explicit `get_foo()` / `set_foo()` only when access is meaningfully
complex or costly (now or plausibly later) — e.g. setting invalidates or
rebuilds state. The call syntax signals "non-trivial operation here".

- Trivial getter/setter pairs → public attribute.
- Simple logic → a property may fit.
- Name them per the naming rules: `get_timeout()`, `set_timeout()`.
- If something used to be a property and becomes expensive, don't bind the new
  getter/setter back onto the property — let old callers break visibly so they
  notice the cost change.

## Decorators (§2.17)

Use them when there's a clear advantage.

- Same import and naming rules as functions.
- The docstring must say it's a decorator, and the decorated function's
  docstring describes behavior **after** decoration.
- Write unit tests for decorators.
- Decorators run at definition time — for module-level code, at import. So:
  no external dependencies in the decorator itself (files, sockets, DB
  connections), and a decorator called with valid arguments should essentially
  never fail. Failures at import are near-impossible to recover from.

### `staticmethod` and `classmethod`

- **Never `@staticmethod`** unless an existing library's API forces it. Write a
  module-level function.
- **`@classmethod` only** for named constructors (`Config.from_file(path)`) or
  class-specific routines that must touch necessary global state such as a
  process-wide cache.

```python
# Yes
def parse_header(raw: bytes) -> Header:     # Module-level, not @staticmethod.
    ...

class Config:
    @classmethod
    def from_file(cls, path: str) -> Self:  # Named constructor.
        ...
```
