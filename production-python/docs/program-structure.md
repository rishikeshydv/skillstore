# Resources, main, and function length (§3.11, §3.17, §3.18)

## Files, sockets and other stateful resources (§3.11)

**Explicitly close** files, sockets, DB connections, mmaps, h5py files,
matplotlib figures — anything that holds an OS or external resource.

Why not leave it to garbage collection: there's no guarantee when (or whether)
`__del__` runs, stray references (globals, tracebacks) extend lifetimes, open
handles block moves/deletes/unmounts, and a "logically closed" but
still-open handle can be silently used later. Tying resource state to object
lifetime has caused bugs across languages for decades.

**Use `with`:**

```python
with open(report_path) as report:
    for line in report:
        handle(line)
```

For objects without context-manager support, use `contextlib.closing()`:

```python
import contextlib

with contextlib.closing(legacy_client.connect(host)) as conn:
    conn.send(payload)
```

If context management is genuinely infeasible, document clearly how the
resource's lifetime is managed.

## Main (§3.17)

Modules must be importable without side effects (pydoc and tests import them).
For executables, put the main logic in `main()` and guard it:

```python
def main() -> None:
    """Runs the report command-line tool."""
    ...


if __name__ == '__main__':
    main()
```

With absl:

```python
from absl import app


def main(argv: Sequence[str]) -> None:
    """Runs the tool. See the module docstring for usage."""
    del argv  # Unused.
    ...


if __name__ == '__main__':
    app.run(main)
```

pylint's `missing-function-docstring` applies to `main()` too; a one-line
docstring keeps the lint clean.

Everything at module top level runs on import — don't call functions, open
connections, or create heavyweight objects there. (Decorators also run at
import; see `classes-and-decorators.md`.)

## Function length (§3.18)

Prefer small, focused functions. No hard limit, but past roughly **40 lines**,
consider whether it can be split without hurting the structure. Long functions
attract bugs as others extend them later. When working in an existing long,
hard-to-debug function — or wanting to reuse a piece of it — refactor it into
smaller pieces rather than working around it.
