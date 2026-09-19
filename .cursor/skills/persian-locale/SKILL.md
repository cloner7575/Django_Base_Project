---
name: persian-locale
description: >-
  Persian (fa) locale conventions for this Django starter — Jalali calendar
  display, RTL, Vazirmatn, and Persian-friendly numbers/dates. Use when
  LANGUAGE_CODE is fa, PRODUCT.md sets RTL/Persian, building Iranian products,
  or the user mentions تقویم جلالی، شمسی، فارسی، یا تاریخ فارسی.
---

# Persian locale (fa)

Applies when the product UI language is Persian (`fa`) or `PRODUCT.md` has RTL + `fa`.

## Hard rules

1. **Calendars for users are Jalali (شمسی).** Store datetimes in the DB as timezone-aware Gregorian (Django default). Convert only at display / date-input boundaries.
2. Do **not** show Gregorian dates to end users in `fa` UIs (admin list columns that staff see in Persian, order history, “عضویت از”, blog dates, etc.) unless the user explicitly asks for میلادی.
3. Time zone default for Persian products: `Asia/Tehran` (see `product-intake`).
4. Text direction: `rtl` via `DJANGO_TEXT_DIRECTION` / settings — never hardcode `dir` in templates; use `{{ TEXT_DIRECTION }}`.
5. Body font: Vazirmatn (or another Persian-capable face) in `static/css/tokens.css` — see `ui-ux`.

## Package

```bash
.venv/bin/pip install jdatetime
```

Pin in `requirements.txt`. Prefer `jdatetime` for conversion. Add `django-jalali` only when you need Jalali **model fields / admin widgets** for user-entered dates.

## Display helpers (this starter)

Use templatetags in `apps.common.templatetags.persian`:

```django
{% load persian %}
{{ order.created_at|jalali }}          {# 1403/06/28 #}
{{ order.created_at|jalali:"%Y/%m/%d %H:%M" }}
```

In Python:

```python
from apps.common.persian import to_jalali, format_jalali

format_jalali(order.created_at)  # "1403/06/28"
```

## Admin

- For read-only timestamps: format with `format_jalali` in `list_display` callables or a mixin.
- For editable date/datetime fields in Persian staff UIs: `django-jalali` (`jDateField` / `jDateTimeField`) or a Jalali JS widget — do not leave HTML5 Gregorian pickers as the only input when the product is `fa`-first.

## Forms and APIs

- Accept Jalali from Persian forms; parse to Gregorian before `clean()` saves.
- JSON/API payloads: ISO Gregorian is fine for machines; document it. Human-facing API docs/examples for Iranian clients may show Jalali alongside.

## Do not

- Store Jalali strings as the source of truth in the database
- Mix میلادی and شمسی labels on the same user-facing screen without a clear reason
- Forget `USE_TZ = True` when converting with `jdatetime`

## Related

- Money / تومان → `persian-ecommerce`
- Intake locale → `product-intake`
- Templates / RTL chrome / Persian visual quality → **`persian-ui`** + `ui-ux`
