# Strings and logging (§3.10, §3.10.1)

## Formatting (§3.10)

Format with an **f-string**, the **`%` operator**, or **`.format()`** — even
when every piece is already a string. A single `a + b` join is fine; building
a formatted string out of `+` pieces is not.

```python
# Yes
line = f'{user.name}: {score} points'
line = '%s: %d points' % (user.name, score)
line = '{}: {} points'.format(user.name, score)
full_path = base_dir + filename          # One plain join is OK.

# No
line = user.name + ': ' + str(score) + ' points'
```

## Don't accumulate with `+=` in loops

String `+=` in a loop can be quadratic; CPython's optimization of it is an
implementation detail you can't rely on. Collect pieces in a list and
`''.join()` them, or write to an `io.StringIO`.

```python
# Yes
rows = ['<ul>']
for item in items:
    rows.append(f'<li>{html.escape(item.title)}</li>')
rows.append('</ul>')
markup = ''.join(rows)

# No
markup = '<ul>'
for item in items:
    markup += f'<li>{html.escape(item.title)}</li>'
markup += '</ul>'
```

## Quotes

- Pick `'` or `"` per file and stick with it.
- Switching to the other quote to avoid backslash-escaping is fine:
  `"It's ready"` in a single-quote file.
- Multi-line strings: prefer `"""`. A project may use `'''` for non-docstring
  multi-line strings only if it also uses `'` for regular strings.
  **Docstrings are always `"""`.**

## Multi-line strings and indentation

Triple-quoted strings don't follow code indentation. To avoid stray leading
spaces, use implicit concatenation or `textwrap.dedent()`:

```python
# Yes — leading spaces acceptable
help_text = """Usage: tool [options]
    -v  verbose"""

# Yes — implicit concatenation
help_text = ('Usage: tool [options]\n'
             '  -v  verbose\n')

# Yes — dedent
help_text = textwrap.dedent("""\
    Usage: tool [options]
      -v  verbose
    """)

# No — flush-left text breaks the visual indentation
    help_text = """Usage: tool [options]
-v  verbose
"""
```

(The `\` right after `"""` escapes a newline inside the literal; it isn't a
forbidden line continuation.)

## Logging (§3.10.1)

For logging APIs that take a `%`-style pattern as the first argument
(`logging`, `absl.logging`, most loggers): pass a **string literal pattern**
and the values as **separate arguments**. **Never an f-string or pre-formatted
string.**

Why: some backends index the unexpanded pattern as a queryable field, and the
message isn't rendered at all if nothing will output it.

```python
# Yes
logging.info('Loaded %d records from %s', len(records), path)
logging.error('Cannot write to cache dir, path=%r', cache_dir)

# No
logging.info(f'Loaded {len(records)} records from {path}')
logging.info('Loaded records from:')
logging.info(path)                 # Split messages lose context.
```

Error-message wording rules (precise, clearly interpolated, greppable) are in
`exceptions.md` → Error messages.
