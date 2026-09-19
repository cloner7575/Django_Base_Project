---
name: django-templates
description: Django template patterns including inheritance, partials, tags, and filters. Use when working with templates, creating reusable components, or organizing template structure.
---

# Django Template Patterns

## Template Organization

This starter already has:

```
templates/
├── base.html
├── partials/_header.html
├── partials/_footer.html
├── partials/_messages.html
├── components/_button.html
├── components/_field.html
├── pages/home.html
└── <app>/
    ├── list.html
    ├── detail.html
    ├── _list.html
    └── _form.html
```

- Full pages extend `base.html`
- HTMX partials: `_list.html` (underscore prefix)
- Shared chrome: `partials/`; reusable UI: `components/`
- Follow the `ui-ux` skill for a11y and tokens

## Inheritance

1. `base.html` — HTML skeleton, navbar, footer
2. Optional section templates
3. Page templates that extend base or a section

Standard blocks: `title`, `content`, `extra_css`, `extra_js`. Use `{{ block.super }}` when appending.

## Partials and Components

```django
{% include "components/_button.html" with text="Submit" variant="primary" %}
{% include "_card.html" with title=post.title only %}
```

## Custom Tags and Filters

- `simple_tag` — return a string
- `inclusion_tag` — render a fragment
- Filters — transform a single value

Put them in `<app>/templatetags/<app>_tags.py` (include `__init__.py`).

## Anti-Patterns

- Complex conditionals in templates — move to views or model methods (`user.can_moderate`)
- Hardcoded paths — use `{% url 'posts:detail' pk=post.pk %}`
- Inline styles — use CSS classes
- Loops without `{% empty %}`

## Integration

- `htmx-patterns` for dynamic partials
- `django-forms` for form rendering
- `pytest-django-patterns` for template tests
