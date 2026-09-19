---
name: htmx-patterns
description: HTMX patterns for Django including partial templates, hx-* attributes, and dynamic UI without JavaScript. Use when building interactive UI, handling AJAX requests, or creating dynamic components.
---

# HTMX Patterns for Django

HTMX is not installed yet. Add it when the UI needs partial HTML updates. Server still renders HTML, not JSON.

## Core Rules

- Return `_partial.html` fragments for HTMX, full pages otherwise
- Detect with `request.headers.get("HX-Request")`
- Always include loading indicators (`hx-indicator`)
- Always show errors; never fail silently
- Disable the submit control: `hx-disabled-elt="this"`
- Validate `request.method` and return real HTTP status codes
- Still use `select_related()` / `prefetch_related()` in HTMX views

## View Pattern

```python
def create_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            obj = form.save()
            if request.headers.get("HX-Request"):
                return render(request, "app/_item.html", {"item": obj})
            return redirect("app:list")
        if request.headers.get("HX-Request"):
            return render(request, "app/_form.html", {"form": form}, status=400)
    else:
        form = MyForm()

    return render(request, "app/create.html", {"form": form})
```

## Response Headers

- `HX-Trigger` — fire client events after swap
- `HX-Redirect` — client-side redirect
- `HX-Retarget` / `HX-Reswap` — override target on success vs error
- `HX-Refresh` — full page refresh for major state changes

## CSRF

Include `{% csrf_token %}` in forms. Optionally set `hx-headers='{"X-CSRFToken": "{{ csrf_token }}"}'` on `<body>` so all HTMX requests send the token.

## Pitfalls

- Returning `base.html` to an HTMX request
- Missing `hx-indicator` (double clicks)
- Not returning the form with errors on validation failure
- N+1 queries in partial views

## Integration

- `django-templates`, `django-forms`, `pytest-django-patterns`, `systematic-debugging`
