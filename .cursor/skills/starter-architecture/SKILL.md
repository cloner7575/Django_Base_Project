---
name: starter-architecture
description: Architecture of this Django starter and how to extend it for any new product. Use when adding apps, changing settings, cloning the base, or deciding where a file belongs.
---

# Starter architecture

This repo is a **cookie-cutter Django base**. Derived projects keep the same tree so Cursor skills keep working.

## Boundaries

| Path | Owns |
|------|------|
| `core/` | Project wiring only: settings, root urls, WSGI/ASGI |
| `apps/accounts` | `User` and auth-admin. Do not put product features here |
| `apps/common` | Abstract models, health, shell pages, context processors |
| `apps/<name>` | One bounded context (billing, catalog, …) |
| `templates/` | Cross-app HTML. App-specific templates: `templates/<app>/` or `<app>/templates/<app>/` |
| `static/` | Design tokens and global CSS/JS |
| `tests/` | pytest. Mirror app names: `tests/test_<app>_*.py` |

Never add a second settings module outside `core/settings/`. Never introduce a top-level Django app beside `apps/`.

## Settings

- Shared: `core/settings/base.py`
- Local: `core/settings/development.py` (`DEBUG=True`, default for `manage.py`)
- Tests: `core/settings.test`
- Prod: `core/settings.production` — fails without `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`

Secrets live in `.env` (see `.env.example`). Product identity (brand, locale, DB, theme) lives in `PRODUCT.md` after `product-intake`. `AUTH_USER_MODEL` is already `accounts.User` — do not switch it.

## New domain app

```bash
.venv/bin/python manage.py startapp catalog apps/catalog
```

1. `AppConfig.name = "apps.catalog"` and `label = "catalog"`
2. Append `"apps.catalog.apps.CatalogConfig"` to `INSTALLED_APPS`
3. `path("catalog/", include("apps.catalog.urls"))` in `core/urls.py`
4. Models subclass `TimeStampedModel`
5. Tests under `tests/`

## What not to do

- Do not create `config/` as a second project package
- Do not use `django.contrib.auth.models.User`
- Do not put business views in `core/`
- Do not copy-paste a new CSS framework that ignores `tokens.css`

## Integration

- Cloning/renaming a product → `bootstrap-project`
- UI → `ui-ux`
- Models → `django-models`
