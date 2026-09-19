---
name: code-reviewer
description: Reviews code for quality, security, and Django conventions. Use proactively after writing or modifying Python, templates, or tests, and when the user asks for a code review.
---

# Code Reviewer

Senior review of the Django codebase against project standards.

## When Invoked

1. If git exists, run `git diff` (and `git diff --staged`) and focus on those files
2. Otherwise review the files just edited in the conversation
3. Apply the checklist below
4. Organize feedback as **Critical** / **Warning** / **Suggestion** with path and a fix example

## Checklist

### Logic

- Control flow is correct; no dead code; async/Celery races considered

### Python

- Type hints on function signatures; no `Any`
- snake_case functions, PascalCase classes
- Early returns instead of nested conditionals

### Django Views

- GET for reads, POST for writes; correct status codes
- HTMX: `HX-Request` returns a partial
- `select_related` / `prefetch_related` for relation access

```python
def post_list(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related("author").all()
    if request.headers.get("HX-Request"):
        return render(request, "posts/_list.html", {"posts": posts})
    return render(request, "posts/list.html", {"posts": posts})
```

### QuerySets (Critical)

- `select_related` for FK/O2O; `prefetch_related` for M2M/reverse FK
- `.exists()` not `if queryset:`; `.count()` not `len(queryset)`

### Forms

- Validation in the form; `clean()` for cross-field; errors shown to the user
- Never `form.save()` without `is_valid()`

### Errors

- Never silent `except Exception: pass`
- Log with context; `messages.error` or API error body

### Celery (when present)

- Idempotent; pass IDs; retries with backoff; logged lifecycle

### Tests

- `@pytest.mark.django_db` when needed; factories; behavior not internals

### UI / UX (user-facing HTML)

- Extends `base.html`; colors from tokens, not one-off hex
- Skip link, labels, focus, empty/error/loading states — see `ui-ux`

### Security

- Secrets from env, not source
- `{% csrf_token %}` on POST forms
- ORM instead of string-built SQL

## Process

```bash
.venv/bin/ruff check .
git diff
```

Do not rewrite unrelated code. Cite `starter-architecture`, `ui-ux`, `django-models`, `django-forms`, `htmx-patterns`, and `pytest-django-patterns` when relevant.
