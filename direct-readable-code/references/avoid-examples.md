# Canonical Avoid Examples

These examples are rejected style choices for the stated context. Do not interpret them as universal language bans. Use the reason under each example to identify the underlying problem.

## 1. Do not fragment an obvious transformation into trivial callbacks

```python
def is_active(user):
    return user["active"]


def get_email(user):
    return user["email"]


active_emails = list(map(get_email, filter(is_active, users)))
```

Avoid because the helper names add navigation without adding domain meaning, and `map` plus `filter` hides a simple operation.

## 2. Do not flatten meaningful reusable state into repeated parameters

```python
def calculate_total(items, tax_rate):
    subtotal = sum(item["price"] for item in items)
    return subtotal + subtotal * tax_rate


total = calculate_total(items, 0.20)
```

Avoid in this context when the tax rate represents calculator state or policy that naturally belongs with repeated pricing behavior.

## 3. Do not leave a recognizable protocol operation scattered at the call site

```python
response = requests.get(settings_url, timeout=10)
response.raise_for_status()

settings = response.json()
```

Avoid when fetching validated JSON is a meaningful operation that benefits from one focused name and one error-handling location.

## 4. Do not compress an important branch into a conditional expression

```python
def get_user_email(repository, user_id):
    user = repository.get(user_id)

    return None if user is None else user.email.strip().lower()
```

Avoid because the missing-user path and normalization step are easier to see as separate statements.

## 5. Do not expand a simple pure transformation without a reason

```python
paid_order_ids = []

for order in orders:
    if order["status"] == "paid":
        paid_order_ids.append(order["id"])
```

Avoid in this context because a standard comprehension expresses the pure filter-and-map operation more directly.

## 6. Do not hide the successful path inside deep nesting

```python
def send_receipt(order):
    if order is not None:
        if order.paid:
            if order.email:
                email_receipt(order)
```

Avoid because each condition adds indentation and makes the main action harder to find.

## 7. Do not duplicate one domain policy at multiple call sites

```python
primary_email = user["email"].strip().lower()
backup_email = user["backup_email"].strip().lower()
```

Avoid because both lines express the same normalization rule and should share one named implementation.

## 8. Do not use an unstructured dictionary for a stable entity shape

```python
user = {
    "name": "Maya",
    "email": "maya@example.com",
    "active": True,
}
```

Avoid in this context because a named data model makes the entity and its fields explicit and supports type checking.

## 9. Do not repeat uniform value selection as control flow

```python
def get_dashboard(role):
    if role == "admin":
        return "/admin/dashboard"

    if role == "editor":
        return "/editor/dashboard"

    return "/dashboard"
```

Avoid because the role-to-path relationship is data and is easier to scan as one lookup table.

## 10. Do not invent a generic transport abstraction for one domain operation

```python
def request_json(client, method, path, *, timeout=10):
    response = client.request(
        method,
        path,
        timeout=timeout,
    )
    response.raise_for_status()

    return response.json()


settings = request_json(
    client,
    "GET",
    f"/users/{user_id}/settings",
)
```

Avoid because the generic helper exposes transport details and creates flexibility that the current domain operation does not need.

## 11. Do not create a stateless class as a namespace

```python
class SlugGenerator:
    @staticmethod
    def generate(title):
        return title.strip().lower().replace(" ", "-")


slug = SlugGenerator.generate(article_title)
```

Avoid because the class has no state, lifecycle, identity, or polymorphic behavior; a function communicates the operation more directly.

## 12. Do not split one short workflow into single-use micro-functions

```python
def build_user(payload):
    return User(
        name=payload["name"].strip(),
        email=normalize_email(payload["email"]),
    )


def ensure_email_is_available(user, repository):
    if repository.email_exists(user.email):
        raise ValueError("Email is already registered")


def save_and_notify(user, repository, mailer):
    repository.save(user)
    mailer.send_welcome_email(user.email)


def register_user(payload, repository, mailer):
    user = build_user(payload)
    ensure_email_is_available(user, repository)
    save_and_notify(user, repository, mailer)

    return user
```

Avoid because understanding one registration story now requires jumping among several helpers that are neither reused nor independently complex.

## 13. Do not replace a readable pure pipeline with boilerplate accumulation

```python
paid_item_ids = []

for order in orders:
    if order["status"] != "paid":
        continue

    for item in order["items"]:
        if item["refunded"]:
            continue

        paid_item_ids.append(item["id"])
```

Avoid in this context because every clause belongs to one side-effect-free collection transformation that remains readable as a multiline comprehension.

## 14. Do not repeat uniform dispatch as an if-elif chain

```python
def send_notification(channel, message):
    if channel == "email":
        send_email(message)
    elif channel == "sms":
        send_sms(message)
    elif channel == "push":
        send_push_notification(message)
    else:
        raise ValueError(f"Unsupported channel: {channel}")
```

Avoid because all branches share the same call shape and are easier to extend and inspect in one dispatch map.

## 15. Do not leave an important dependency contract implicit

```python
def get_active_user(repository, user_id):
    user = repository.find(user_id)

    if user is None or not user.active:
        return None

    return user
```

Avoid in this context because the function depends on a meaningful repository boundary whose required operation should be stated explicitly.

## 16. Do not add a generic result type when ordinary exceptions fit

```python
from dataclasses import dataclass
from typing import Generic, TypeVar


T = TypeVar("T")


@dataclass
class Result(Generic[T]):
    value: T | None = None
    error: str | None = None

    @property
    def succeeded(self):
        return self.error is None


def parse_age(value):
    try:
        age = int(value)
    except ValueError:
        return Result(error="Age must be a number")

    if age < 0:
        return Result(error="Age cannot be negative")

    return Result(value=age)
```

Avoid because the wrapper adds a type, state combinations, and caller ceremony without improving a stopping failure path.

## 17. Do not hide distinct behavior stories inside a parameter table

```python
import pytest


@pytest.mark.parametrize(
    ("role", "expected_dashboard"),
    [
        ("admin", "/admin/dashboard"),
        ("editor", "/editor/dashboard"),
        ("viewer", "/dashboard"),
    ],
)
def test_dashboard_for_role(role, expected_dashboard):
    assert get_dashboard(role) == expected_dashboard
```

Avoid in this context because the admin, editor, and fallback rules deserve separate descriptive test names.

## 18. Do not omit a useful purpose statement from a reusable helper

```python
def normalize_email(email):
    return email.strip().lower()
```

Avoid in this context because a one-sentence docstring clarifies why the normalization exists and how the value is intended to be used.
