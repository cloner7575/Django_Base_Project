---
name: pytest-django-patterns
description: pytest-django testing patterns, Factory Boy, fixtures, and TDD workflow. Use when writing tests, creating test factories, or following TDD red-green-refactor cycle.
---

# pytest-django Testing Patterns

## TDD (RED-GREEN-REFACTOR)

1. **RED**: write a failing test that describes the behavior
2. **GREEN**: write the minimum code to pass
3. **REFACTOR**: clean up while tests stay green

If implementing a feature or fixing a bug, write the test **before** production code.

## Database and Fixtures

- `@pytest.mark.django_db` on tests that touch the DB, or `pytestmark = pytest.mark.django_db` at module level
- Factory Boy for models (`factory.Sequence`, `Faker`, `SubFactory`, `post_generation` for M2M)
- pytest fixtures for clients and auth (`client.force_login(user)`)
- Shared fixtures in `conftest.py`

Keep tests in the starter's `tests/` tree:

```
tests/
├── conftest.py
├── test_starter.py
└── test_<app>_<area>.py
```

## What to Test

**Views**: status codes, authz, context, side effects, HTMX via `HTTP_HX_REQUEST="true"`.

**Forms**: valid/invalid data, `clean_*`, save vs update with `instance=`.

**Models**: methods, custom QuerySets, constraints.

**Tasks**: mock I/O, test logic and idempotency, do not require a live worker.

## Patterns

```python
@pytest.mark.parametrize(("payload", "status"), [({}, 400), ({"title": "x"}, 201)])
def test_create(client, payload, status):
    response = client.post("/api/posts/", payload)
    assert response.status_code == status
```

- `mocker.patch()` for HTTP, email, filesystem
- `refresh_from_db()` after updates
- `CaptureQueriesContext` when asserting query counts
- Do not mock your own domain code; do not re-test Django internals

## Commands

```bash
.venv/bin/pytest
.venv/bin/pytest -x --lf
.venv/bin/pytest -k "test_name"
.venv/bin/pytest tests/apps/posts/
```

Settings: `DJANGO_SETTINGS_MODULE` is `core.settings.test` (see `pytest.ini`).

## Pitfalls

- Forgetting `@pytest.mark.django_db`
- Building models by hand instead of factories once factories exist
- Testing implementation instead of behavior
- Writing tests after the fact and missing edge cases

## Integration

- `systematic-debugging`, `django-models`, `django-forms`, `celery-patterns`, `django-rest-framework`
