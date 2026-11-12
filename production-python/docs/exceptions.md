# Exceptions and error messages (§2.4, §3.10.2)

Exceptions are fine; use them carefully.

## Raising

- **Prefer built-in exception classes** where they fit. A `ValueError` is the
  normal signal for a programming mistake such as a violated precondition on
  an argument.
- **Custom exceptions** must subclass an existing exception class, end in
  `Error`, and not repeat the module name: `quota.ExceededError`, not
  `quota.QuotaExceededError` (callers already write `quota.` in front).
- A class docstring on an exception says **what it represents**, not when it's
  raised: `"""The account has no remaining quota."""`, not
  `"""Raised when..."""` (see `docstrings-and-comments.md`).

## `assert` is not validation

`assert` may be stripped (`python -O`), so it must never carry application
logic or check preconditions. The test: deleting every `assert` must not change
behavior. Use `if ...: raise ...` for real checks.

```python
# Yes
def reserve_seats(count: int) -> Reservation:
    if count < 1:
        raise ValueError(f'count must be positive, got {count=}')
    reservation = _booking.try_reserve(count)
    if reservation is None:
        raise SoldOutError(f'Could not reserve {count} seats.')
    assert reservation.count == count  # Sanity check only; code doesn't rely on it.
    return reservation

# No — logic depends on asserts
def reserve_seats(count: int) -> Reservation:
    assert count >= 1
    reservation = _booking.try_reserve(count)
    assert reservation is not None
    return reservation
```

Inside **pytest** tests, `assert` is expected and fine.

Don't list `ValueError`-for-API-misuse in the docstring's `Raises:` section —
documenting behavior under contract violation would make it part of the
contract.

## Catching

- **Never** bare `except:`, and don't catch `Exception` (or `BaseException`)
  unless you are:
  - re-raising it, or
  - building an isolation point that records and suppresses errors — e.g. the
    outermost loop of a worker thread that must not die.

  A bare `except:` also swallows `KeyboardInterrupt`, `SystemExit`, test
  failures and `NameError` typos.
- **Keep `try` bodies small** — only the line(s) you expect to raise. A large
  `try` block hides unrelated bugs behind your handler.
- Use **`finally`** for cleanup that must run either way (or better, a `with`
  statement — see `program-structure.md`).

```python
# Yes
try:
    payload = json.loads(raw)
except json.JSONDecodeError as e:
    raise InvalidRequestError(f'Body is not JSON: {raw[:80]!r}') from e
record = build_record(payload)

# No — build_record() bugs get misreported as bad JSON
try:
    payload = json.loads(raw)
    record = build_record(payload)
except Exception:
    raise InvalidRequestError('Body is not JSON')
```

## Error messages (§3.10.2)

Messages on exceptions, and messages shown to users, should:

1. **Match the actual condition precisely.** Don't guess at a cause you didn't
   check.
2. **Make interpolated values obviously interpolated** — `{p=}`, `%r`, or a
   clear `key: value` shape — so a value like `'deleted'` can't be misread as
   part of the sentence.
3. **Be greppable** — a stable literal prefix that's easy to search for.

```python
# Yes
if not 0 <= ratio <= 1:          # Also rejects NaN, unlike `ratio < 0 or ratio > 1`.
    raise ValueError(f'Not a ratio in [0, 1]: {ratio=}')

try:
    os.remove(lock_path)
except OSError as e:
    logging.warning('Could not remove lock file (reason: %r): %r', e, lock_path)

# No — asserts a cause that was never checked
except OSError:
    logging.warning('Lock file was already gone: %s', lock_path)

# No — value blends into prose; hard to grep
    logging.warning('The %s lock could not be removed.', lock_path)
```
