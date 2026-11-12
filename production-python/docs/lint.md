# Lint and formatters (§1, §2.1)

## Tooling the guide assumes

- **pylint** with Google's config: https://google.github.io/styleguide/pylintrc
- **Black** or **Pyink** (Google's Black fork) as the auto-formatter, so nobody
  argues about formatting. If a project has neither, recommend one rather than
  hand-fixing whitespace. Pyink settings that match this guide:

  ```toml
  # pyproject.toml
  [tool.pyink]
  line-length = 80
  pyink-indentation = 4
  pyink-use-majority-quotes = true   # Otherwise it forces double quotes.
  ```
- **isort** with `profile = "google"` for import order (formatters don't sort
  imports).
- A type checker at build time (the guide names **pyrefly**; projects commonly
  use mypy or pyright instead) — see `type-annotations.md`.

## Running pylint

Always run it. Its warnings catch typos, use-before-assignment and similar bugs
a compiler would catch in static languages. A few warnings will be spurious —
suppress those rather than ignoring the whole run, so real problems stay
visible.

## Suppressing a warning

Use a line-level comment with the **symbolic name**, not the numeric code:

```python
def do_GET(self):  # Name required by http.server. pylint: disable=invalid-name
    ...
```

- Prefer `pylint: disable=...`; `disable-msg` is deprecated.
- If the symbolic name doesn't make the reason obvious, add a short explanation
  in the same comment. Line-level suppressions are greppable, which is the point.
- Google-specific checks have names starting with `g-`.
- Discover messages with `pylint --list-msgs`; explain one with
  `pylint --help-msg=<name>`.

## Unused arguments

Preferred: `del` them at the top of the function with a reason.

```python
def handle_event(event: Event, context: Context) -> None:
    del context  # Unused; required by the callback signature.
    process(event)
```

Still allowed but discouraged: naming the parameter `_`, prefixing
`unused_`, or assigning to `_`. These break callers that pass the argument by
keyword and don't actually prove the argument is unused.
