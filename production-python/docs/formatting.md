# Formatting (§3.1–§3.7, §3.14)

Most of this is handled by Black/Pyink. Know the rules for code a formatter
won't touch and for reviewing.

## Semicolons (§3.1)

None — not at line ends, not to join two statements.

## Line length (§3.2)

**80 characters.** Exceptions:

- long import statements
- URLs, paths or long flags in comments
- long module-level string constants with no whitespace (URLs, paths) that
  would be awkward to split
- `# pylint: disable=...` comments

**No backslash line continuation.** Use implicit joining inside `()`, `[]`,
`{}` — add parentheses if needed. (A backslash escaping a newline *inside a
string literal* is fine.)

```python
# Yes
if (response.status == 200 and response.body
        and not response.headers.get('x-cache-miss')):
    ...

with (
    open(src_path) as src,
    open(dst_path, 'w') as dst,
):
    copy(src, dst)

# No
if response.status == 200 and response.body \
        and not response.headers.get('x-cache-miss'):
    ...
```

Long string literal → implicit concatenation in parentheses:

```python
message = ('This report covers every invoice issued during the '
           'billing period, including voided ones.')
```

**Break at the highest syntactic level.** If you break twice, break at the same
level both times.

```python
# Yes
scheduler.enqueue(
    job_id=job.id, payload=serializer.dump(job.payload, compact=True))

if (
    settings is None
    or 'region' not in settings
    or settings['region'].is_deprecated
):
    use_default_region()

# No — break inside a nested call
scheduler.enqueue(job_id=job.id, payload=serializer.dump(
    job.payload, compact=True))
```

Long URL in a comment: put it on its own line, unbroken.

Docstring summary lines must stay within 80. Anything else that still exceeds
80 after the formatter has run is allowed, but break it by hand when sensible.

## Parentheses (§3.3)

Use sparingly. Fine around tuples (and recommended for one-element tuples:
`(item,)`). Not around `return` values or `if`/`while` conditions unless for
line continuation or to mark a tuple.

```python
# Yes
if ready:
    start()
while not done:
    done = step()
return result
return name, value
return (name, value)
single = (name,)       # Parens make a 1-tuple more visible than the comma.
for (key, value) in pairs.items(): ...

# No
if (ready):
    start()
if not(ready):
    wait()
return (result)
```

## Indentation (§3.4)

**4 spaces. Never tabs.** Continuation lines either align with the opening
delimiter or use a **4-space hanging indent with nothing after the opening
bracket on the first line**. A closing bracket on its own line lines up with
the line that opened it.

```python
# Yes — aligned
result = compute_score(user_id, period,
                       weights, normalize=True)

# Yes — hanging indent
result = compute_score(
    user_id, period, weights, normalize=True)

result = compute_score(
    user_id,
    period,
    weights,
    normalize=True,
)

config = {
    'timeout_seconds':
        DEFAULT_TIMEOUT,
}

# No — args on the first line plus hanging indent
result = compute_score(user_id, period,
    weights, normalize=True)

# No — 2-space hanging indent
result = compute_score(
  user_id, period)
```

### Trailing commas (§3.4.1)

Use a trailing comma when the closing `]`/`)`/`}` is on a **different line**
from the last element, and in one-element tuples. Black/Pyink treat a trailing
comma as "explode this to one item per line".

```python
# Yes
sizes = [8, 16, 32]
sizes = [
    8,
    16,
    32,
]

# No
sizes = [
    8,
    16,
    32,]
```

## Blank lines (§3.5)

- 2 between top-level definitions (functions, classes).
- 1 between methods, and between a class docstring and its first method.
- 0 directly after a `def` line.
- Single blank lines inside functions as you see fit.

A comment directly above a definition is fine; consider whether it belongs in
the docstring instead.

## Whitespace (§3.6)

- None just inside brackets: `fn(a[1], {'k': 2}, [])`.
- None before `,` `;` `:`; one after (except at line end).
- None before the `(` or `[` that starts a call, index or slice:
  `fn(1)`, `items[0]`.
- No trailing whitespace.
- One space around assignment, comparisons (`== < > != <= >= in not in is
  is not`) and booleans (`and or not`). Use judgment for arithmetic operators.
- **No spaces around `=` for keyword arguments or unannotated defaults** —
  *but* do use spaces when the parameter has a type annotation:

  ```python
  def resize(image, scale=1.0): ...
  def resize(image, scale: float = 1.0): ...
  resize(img, scale=2.0)
  ```
- **Don't align tokens vertically** across lines (`=`, `:`, `#`) — it's a
  maintenance burden.

## Shebang (§3.7)

Only on files meant to be executed directly. Use `#!/usr/bin/env python3`
(works with virtualenvs) or `#!/usr/bin/python3`. Library modules don't need one.

## Statements (§3.14)

Generally one statement per line. A test and its body may share a line **only**
if the whole statement fits and there's no `else`; never with `try`/`except`.

```python
# Yes
if not items: return

# No
if not items: return
else: process(items)

try: load()
except IOError: recover()
```
