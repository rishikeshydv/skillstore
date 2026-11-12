# Language features (§2.5–§2.12, §2.14, §2.16, §2.18, §2.19)

Quick verdicts first, details below.

| Feature | Verdict |
| --- | --- |
| Mutable global state | Avoid |
| Module-level constants | Encouraged |
| Nested functions/classes | OK when closing over a local (not `self`/`cls`) |
| Comprehensions | OK — one `for`, at most one filter |
| Default iterators/operators | Use them |
| Generators | Fine; document with `Yields:` |
| Lambdas | One-liners only |
| Conditional expressions | Simple cases, each part on one line |
| Default argument values | OK, never mutable |
| Implicit false | Preferred, with caveats |
| Lexical scoping/closures | OK |
| Threading | Don't rely on built-in atomicity |
| Power features (metaclasses, import hacks, reflection, `__del__`) | Avoid |

## Mutable global state (§2.5)

Avoid module-level or class-level values that change at runtime. They break
encapsulation (e.g. a global DB connection makes talking to two databases
painful) and can change behavior at import time.

If you truly need it: name it `_private`, expose access through functions or
classmethods, and leave a comment (or a linked doc) explaining why.

Constants are good: `_MAX_RETRIES = 3` (internal), `DEFAULT_REGION = 'us-east1'`
(public). ALL_CAPS_WITH_UNDERSCORES.

## Nested / local / inner functions and classes (§2.6)

Fine when the nested function **closes over a local variable** other than
`self` or `cls` (decorators are the classic case). Inner classes are fine.

Don't nest a function just to hide it — nested functions can't be unit-tested.
Make it a module-level `_private_helper` instead.

## Comprehensions and generator expressions (§2.7)

Allowed for simple cases. **No multiple `for` clauses and no multiple filter
expressions.** Optimize for readability over brevity; split across lines when
long.

```python
# Yes
active_ids = [user.id for user in users if user.is_active]

totals_by_region = {
    region: summarize(orders)
    for region, orders in group_orders(raw_orders).items()
    if orders
}

pairs = []
for row in range(rows):
    for col in range(cols):
        if grid[row][col]:
            pairs.append((row, col))

# No — two `for` clauses
pairs = [(r, c) for r in range(rows) for c in range(cols) if grid[r][c]]
```

## Default iterators and operators (§2.8)

Use the built-in iteration and membership protocols.

```python
# Yes
for key in config: ...
if item in allowed: ...
for line in log_file: ...
for name, value in headers.items(): ...

# No
for key in config.keys(): ...
for line in log_file.readlines(): ...
```

Don't mutate a container while iterating over it.

## Generators (§2.9)

Use as needed. Docstrings use **`Yields:`**, not `Returns:`. If the generator
holds an expensive resource (file, connection), make sure cleanup is forced —
wrapping it in a context manager is the clean way.

## Lambdas (§2.10)

OK for one-liners. If it spans lines or runs past ~60–80 characters, make it a
named (possibly nested) function. Prefer generator expressions over
`map()`/`filter()` with a lambda. For arithmetic and attribute/item access, use
`operator` (`operator.mul`, `operator.attrgetter('name')`,
`operator.itemgetter(0)`) instead of a lambda.

## Conditional expressions (§2.11)

OK for simple cases. Each of the three parts — true value, condition, false
value — must fit on one line. If it doesn't, write a full `if` statement.

```python
# Yes
label = 'admin' if user.is_admin else 'member'
label = ('administrator with full access'
         if user.is_admin
         else 'member')

# No — breaks in the middle of a part
label = ('administrator' if
         user.is_admin else 'member')
```

## Default argument values (§2.12)

Fine, but **never use a mutable object or a call evaluated at import time** as
a default. Defaults are evaluated once, when the `def` runs.

```python
# Yes
def add_tags(item, tags: Sequence[str] | None = None):
    if tags is None:
        tags = []

def add_tags(item, tags: Sequence[str] = ()):  # Empty tuple is immutable.
    ...

# No
def add_tags(item, tags=[]): ...                 # Shared across calls.
def add_tags(item, tags: Mapping = {}): ...      # Same bug, typed.
def stamp(event, at=time.time()): ...            # Frozen at import time.
def connect(host=_HOST_FLAG.value): ...          # Flags not parsed yet.
```

## True/False evaluations (§2.14)

Prefer implicit false (`if items:` rather than `if items != []:`). Caveats:

- **`None` checks use `is`**: `if x is None:` / `if x is not None:`. The value
  might be falsy but valid (`0`, `''`).
- **Never compare a bool to `False` with `==`.** Write `if not flag:`. To
  distinguish `False` from `None`: `if not flag and flag is not None:`.
- **Sequences**: `if seq:` / `if not seq:`, not `if len(seq):`.
- **Integers**: implicit false risks treating `None` as `0`. Comparing a value
  known to be an int (and not a `len()` result) against `0` is fine:
  `if count % 10 == 0:`.
- `'0'` (a string) is truthy.
- **NumPy arrays** raise in boolean context — use `.size`: `if not arr.size:`.

```python
# Yes
if not users:
    show_empty_state()
if retries == 0:
    give_up()
def f(x=None):
    if x is None:
        x = []

# No
if len(users) == 0: ...
if not retries: ...      # When retries could be None.
def f(x=None):
    x = x or []          # Replaces a passed-in empty list too.
```

## Lexical scoping (§2.16)

Closures are fine. Watch the classic trap: any assignment to a name anywhere in
a function makes it local for the whole function, so a nested function sees the
*local*, not the global of the same name. Avoid reusing names across those
scopes.

## Threading (§2.18)

Don't rely on built-in types being atomic — dict operations aren't when
`__hash__`/`__eq__` are Python code, and variable assignment goes through
dicts. Communicate between threads with `queue.Queue`; otherwise use
`threading` locks, preferring `threading.Condition` over raw locks.

## Power features (§2.19)

Avoid custom metaclasses, bytecode access, on-the-fly compilation, dynamic
inheritance, object reparenting, import hacks, reflection tricks (some
`getattr()` uses), patching system internals, and `__del__` for cleanup. They
read as clever to the author and opaque to everyone after.

Standard-library tools built on them are fine to *use*: `abc.ABCMeta`,
`dataclasses`, `enum`. Manually writing a property descriptor counts as a power
feature (use `@property`).
