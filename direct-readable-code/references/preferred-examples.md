# Canonical Preferred Examples

These examples are direct style evidence from the user's ratings. Treat them as authoritative when a general rule is ambiguous. Adapt the syntax to the current language and repository rather than copying Python mechanically.

## 1. Keep an obvious transformation local

```python
active_emails = []

for user in users:
    if user["active"]:
        active_emails.append(user["email"])
```

Prefer this when tiny predicate and accessor helpers would only force the reader to jump around.

## 2. Use a class for meaningful state

```python
class PriceCalculator:
    def __init__(self, tax_rate):
        self.tax_rate = tax_rate

    def calculate(self, items):
        subtotal = sum(item["price"] for item in items)
        return subtotal + subtotal * self.tax_rate


total = PriceCalculator(0.20).calculate(items)
```

Prefer this because the object owns a meaningful pricing input that applies across calculations.

## 3. Name a recognizable operation

```python
def fetch_json(url):
    """Fetch JSON from a URL and fail on an unsuccessful response."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


settings = fetch_json(settings_url)
```

Prefer a focused helper when its name captures a complete operation and hides routine protocol details.

## 4. Make absence and transformation explicit

```python
def get_user_email(repository, user_id):
    """Return the normalized email for a user, or None when absent."""
    user = repository.get(user_id)

    if user is None:
        return None

    clean_email = user.email.strip().lower()
    return clean_email
```

Prefer the visible branch and named intermediate value over a compact conditional expression.

## 5. Use a simple comprehension for pure filtering and mapping

```python
paid_order_ids = [
    order["id"]
    for order in orders
    if order["status"] == "paid"
]
```

Prefer an idiomatic comprehension when the operation is pure and reads linearly.

## 6. Use guard clauses to expose the main path

```python
def send_receipt(order):
    """Send a receipt for a paid order with a destination email."""
    if order is None:
        return

    if not order.paid:
        return

    if not order.email:
        return

    email_receipt(order)
```

Prefer guard clauses over nested conditions when they keep the successful path visible.

## 7. Extract conceptually identical behavior

```python
def normalize_email(value):
    """Normalize an email address for storage and comparison."""
    return value.strip().lower()


primary_email = normalize_email(user["email"])
backup_email = normalize_email(user["backup_email"])
```

Prefer a helper when repeated lines express the same domain policy.

## 8. Make a data shape explicit

```python
from dataclasses import dataclass


@dataclass
class User:
    name: str
    email: str
    active: bool


user = User(
    name="Maya",
    email="maya@example.com",
    active=True,
)
```

Prefer a named data model when fields form a recognizable entity, even in a small script.

## 9. Represent uniform choices as data

```python
DASHBOARD_BY_ROLE = {
    "admin": "/admin/dashboard",
    "editor": "/editor/dashboard",
}


def get_dashboard(role):
    """Return the dashboard path for a role."""
    return DASHBOARD_BY_ROLE.get(role, "/dashboard")
```

Prefer a lookup table when it makes a uniform mapping visible in one place.

## 10. Prefer a domain-specific helper to a generic request layer

```python
def fetch_user_settings(client, user_id):
    """Fetch settings for one user."""
    response = client.get(
        f"/users/{user_id}/settings",
        timeout=10,
    )
    response.raise_for_status()

    return response.json()


settings = fetch_user_settings(client, user_id)
```

Prefer the domain operation because it communicates intent without exposing generic transport parameters at the call site.

## 11. Use a function for a stateless operation

```python
def generate_slug(title):
    """Generate a URL-friendly slug from a title."""
    return title.strip().lower().replace(" ", "-")


slug = generate_slug(article_title)
```

Prefer a function over a class that would exist only as a static namespace.

## 12. Keep one readable workflow together

```python
def register_user(payload, repository, mailer):
    """Register a user and send the welcome email."""
    email = normalize_email(payload["email"])

    if repository.email_exists(email):
        raise ValueError("Email is already registered")

    user = User(
        name=payload["name"].strip(),
        email=email,
    )

    repository.save(user)
    mailer.send_welcome_email(user.email)

    return user
```

Prefer a cohesive top-to-bottom workflow over several single-use helpers that fragment the story.

## 13. Keep a pure multi-stage transformation concise

```python
paid_item_ids = [
    item["id"]
    for order in orders
    if order["status"] == "paid"
    for item in order["items"]
    if not item["refunded"]
]
```

Prefer the multiline comprehension when every clause contributes to one side-effect-free filtering and mapping pipeline.

## 14. Use a dispatch map for uniform behavior selection

```python
NOTIFICATION_SENDERS = {
    "email": send_email,
    "sms": send_sms,
    "push": send_push_notification,
}


def send_notification(channel, message):
    """Send a notification through a supported channel."""
    sender = NOTIFICATION_SENDERS.get(channel)

    if sender is None:
        raise ValueError(f"Unsupported channel: {channel}")

    sender(message)
```

Prefer a dispatch map when all cases have the same calling shape and the supported options should be visible together.

## 15. Define a small contract at a dependency boundary

```python
from typing import Protocol


class UserRepository(Protocol):
    def find(self, user_id: int) -> User | None:
        ...


def get_active_user(
    repository: UserRepository,
    user_id: int,
) -> User | None:
    """Return an active user, or None when missing or inactive."""
    user = repository.find(user_id)

    if user is None or not user.active:
        return None

    return user
```

Prefer a narrow interface when it documents what the consumer needs, even when only one implementation currently exists.

## 16. Use ordinary exceptions for stopping failures

```python
def parse_age(value):
    """Parse a non-negative age."""
    try:
        age = int(value)
    except ValueError as error:
        raise ValueError("Age must be a number") from error

    if age < 0:
        raise ValueError("Age cannot be negative")

    return age
```

Prefer the language's normal exception mechanism when callers should stop or handle failure explicitly.

## 17. Give distinct behaviors distinct tests

```python
def test_admin_uses_admin_dashboard():
    assert get_dashboard("admin") == "/admin/dashboard"


def test_editor_uses_editor_dashboard():
    assert get_dashboard("editor") == "/editor/dashboard"


def test_unknown_role_uses_default_dashboard():
    assert get_dashboard("viewer") == "/dashboard"
```

Prefer separate behavior-named tests when each case communicates a meaningful rule.

## 18. Add a concise purpose docstring

```python
def normalize_email(email):
    """Normalize an email address for storage and comparison."""
    return email.strip().lower()
```

Prefer a brief docstring that makes the helper's purpose immediately visible.
