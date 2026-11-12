# Imports (§2.2, §2.3, §2.20, §3.13)

## What to import (§2.2)

Import **packages and modules**, not individual classes, functions or
constants. At the call site `x.Thing` then tells the reader exactly where
`Thing` lives.

| Form | When |
| --- | --- |
| `import x` | importing a package or module |
| `from x import y` | `x` is the package prefix, `y` is a module |
| `from x import y as z` | two modules named `y`; `y` clashes with a top-level name in this module; `y` clashes with a common public parameter name (e.g. `features`); `y` is very long; `y` is too generic here (`from storage.file_system import options as fs_options`) |
| `import y as z` | only for standard abbreviations: `import numpy as np`, `import pandas as pd`, `import tensorflow as tf` |

```python
# Yes
from billing.payments import ledger
ledger.post_entry(entry)

# No — imports a class, hides its origin at the call site
from billing.payments.ledger import post_entry
```

**Exemption**: symbols from `typing`, `collections.abc` and
`typing_extensions` are imported directly (`from typing import Any`), and
several may share a line. See `type-annotations.md` → Typing imports.

## Full package paths, no relative imports (§2.2, §2.3)

Always import by the module's full package path, even from the same package.
Relative imports (`from . import x`, `from .x import y`) and bare
same-directory imports (`import sibling`) are not allowed: they depend on
`sys.path` and can import the same module twice under two names.

Don't assume the main script's directory is on `sys.path`. Treat `import foo`
as meaning a top-level or third-party `foo`, never a local `foo.py`.

## `from __future__` imports (§2.20)

Encouraged. They let a file opt into newer semantics per-file and make runtime
upgrades smoother. Keep them until you're sure the code only ever runs on a
version where the behavior is the default — even if the file doesn't currently
need the feature, the import stops later edits from relying on the old
behavior. `from __future__ import annotations` is the common one (see
`type-annotations.md` → Forward declarations).

## Formatting and ordering (§3.13)

- **One import per line**: `import os` and `import sys` on separate lines,
  never `import os, sys`. (Again, `typing` / `collections.abc` may combine:
  `from collections.abc import Mapping, Sequence`.)
- **Placement**: top of the file, after the module docstring/comments, before
  globals and constants.
- **Groups**, most generic first:
  1. `from __future__ import ...`
  2. standard library
  3. third-party packages
  4. your repository's own packages
- Within a group, sort lexicographically **ignoring case** by the full module
  path (the `path` in `from path import name`). A blank line between groups is
  optional but common.
- The old fifth group ("same top-level package as this file") is deprecated —
  just sort those with group 4.

```python
from __future__ import annotations

import collections
import json
import sys

from absl import flags
import numpy as np
import requests

from acme.billing import invoices
from acme.common import retry
```

Note `from absl import flags` sorts before `import numpy` because ordering is
by module path (`absl` < `numpy`), not by statement form.

Tool: `isort --profile google` reproduces this order. (Black and Pyink format
code but do not sort imports.)
