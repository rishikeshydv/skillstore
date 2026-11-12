# Docstrings and comments (§3.8, §3.12)

## General docstring shape (§3.8.1)

- Always triple **double** quotes: `"""`.
- First line: a summary that fits on one physical line (≤80 chars), ending in
  `.`, `?` or `!`.
- If there's more (encouraged): a blank line, then the body, aligned with the
  opening quotes.

## Modules (§3.8.2)

- Every file carries the project's license boilerplate (Apache 2.0, MIT, BSD,
  etc.) if the project uses one.
- Then a module docstring describing contents and usage.

```python
"""Retry helpers for flaky network calls.

Provides decorators and context managers that retry an operation with
exponential backoff and jitter.

Typical usage example:

  @retry_on(ConnectionError, attempts=5)
  def fetch_profile(user_id):
      ...
"""
```

### Test modules (§3.8.2.1)

- Test modules don't need a module docstring.
- `unittest.TestCase` subclasses and their `test_*` methods don't need
  docstrings.
- Add one only when it carries information — how to run the test, golden-file
  update commands, unusual setup or external dependencies.
- Don't write docstrings that restate the name (`"""Tests for foo."""`,
  `"""Tests that bar works."""`).

## Functions and methods (§3.8.3)

"Function" here includes methods, generators and properties.

**A docstring is required** if the function is any of:
- part of the public API
- non-trivial in size
- non-obvious in logic

The docstring should let someone **call the function without reading its
body**: calling syntax and semantics, not implementation — unless an
implementation detail affects callers (e.g. it mutates an argument). Notes for
maintainers go in comments in the code.

**Mood**: descriptive (`"""Fetches rows..."""`) or imperative
(`"""Fetch rows..."""`) — pick one per file. **Properties** read like
attributes: `"""The cache directory."""`, not `"""Returns the cache
directory."""`.

### Sections

Each starts with a heading ending in `:`; contents use a hanging indent of 2 or
4 spaces (consistent within a file). Omit sections when the name and signature
make a one-line docstring sufficient.

**`Args:`**
- Each parameter by name, then `:` and a space or newline, then a description.
- Wrapped descriptions get a hanging indent (2 or 4 more than the name).
- Include types only if the code has no annotation.
- List varargs as `*args` / `**kwargs` (with their real names).

**`Returns:`** (or **`Yields:`** for generators)
- Semantics of the value, plus any type info the annotation doesn't convey.
- Omit if it only returns `None`.
- May be omitted when the docstring *starts* with "Returns"/"Yields" and that
  sentence fully describes the value: `"""Returns the user's display name."""`.
- Tuples: describe as one tuple — "A tuple (rows, cursor), where rows is …".
  Don't use NumPy-style named multiple returns.
- Generators: document what `next()` returns, not the generator object.

**`Raises:`**
- Exceptions that are part of the interface, same `Name: description` format.
- Don't document exceptions raised for violating the documented API (e.g.
  `ValueError` on bad arguments).

```python
def fetch_invoices(
    client: billing.Client,
    customer_ids: Sequence[str],
    include_void: bool = False,
) -> Mapping[str, list[Invoice]]:
    """Fetches invoices for the given customers.

    Results are read from the billing replica, so invoices issued in the last
    few seconds may be missing.

    Args:
        client: An authenticated billing client.
        customer_ids: IDs of customers whose invoices to fetch. Duplicates are
          ignored.
        include_void: If True, voided invoices are included.

    Returns:
        A dict mapping each customer ID to that customer's invoices, newest
        first. Customers with no invoices map to an empty list.

    Raises:
        billing.UnavailableError: The billing replica could not be reached.
    """
```

Equally valid: each arg's description on the line after its name, indented.

**Decorated functions**: describe behavior *after* decoration (e.g. a
`@contextlib.contextmanager` function's docstring describes the context
manager it returns).

### Overridden methods (§3.8.3.1)

With `@override` (from `typing`), an overriding method needs no docstring —
unless it materially changes the base contract or adds side effects, in which
case document at least the differences. **Without** `@override`, a docstring
is required. `"""See base class."""` adds nothing when `@override` is present.

## Classes (§3.8.4)

- A docstring under the `class` line describing what an **instance
  represents**.
- Public attributes (not properties) go in an `Attributes:` section, formatted
  like `Args:`.
- Don't say "Class that…" — it's obviously a class.
- Exceptions describe the condition they represent, not when they're raised.
- Decorated classes: describe post-decoration behavior.

```python
# Yes
class RateLimit:
    """A per-key request budget that refills over time.

    Attributes:
        capacity: Maximum number of requests stored in the bucket.
        refill_per_second: Requests added back each second.
    """

class QuotaExceededError(Exception):
    """The caller has used its full request budget."""

# No
class RateLimit:
    """Class that represents a rate limit."""

class QuotaExceededError(Exception):
    """Raised when the quota is exceeded."""
```

An `__init__` that takes arguments documents them in its own docstring's
`Args:` section, as in the guide's class example.

## Block and inline comments (§3.8.5)

- Comment the tricky parts. If you'd have to explain it in code review, write
  the comment now.
- Complicated logic: a few lines of comment **before** it. Non-obvious single
  lines: an end-of-line comment.
- End-of-line comments: at least **2 spaces** before `#`, then `# ` and text.
- **Never describe the code** — assume the reader knows Python better than you
  but doesn't know your intent. Explain *why*.

```python
if n & (n - 1) == 0:  # True when n is 0 or a power of two.
    use_fast_path()

# BAD: Loop over the list and add one to each element.
for i, value in enumerate(values):
    values[i] = value + 1
```

## Punctuation, spelling, grammar (§3.8.6)

Comments should read like prose: capitalized, punctuated, usually full
sentences. Short end-of-line comments can be less formal, consistently.

## TODO comments (§3.12)

For temporary code, short-term fixes, or "good enough for now".

Format: `TODO` in caps, a **parenthesized link to context (ideally a bug)**,
a colon, then the explanation.

```python
# TODO(github.com/acme/billing/issues/412): Batch these writes.
```

- The older `# TODO: link - text` style is discouraged in new code.
- Don't use a person or team as the context: avoid `# TODO(alice): ...`.
- "Do X later" TODOs need a concrete date or a concrete triggering event.
