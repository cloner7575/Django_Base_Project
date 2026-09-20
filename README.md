# Django starter (core)

Copy this repository for every new Django product. Keep the layout so Cursor skills and rules stay valid.

In Cursor, start with **product intake**: the agent asks brand, language, RTL/LTR, database, and theme, then writes `PRODUCT.md` before planning or coding.

## What you get

- Split settings: `core.settings.development` / `test` / `production`, with a
  production module that refuses to boot on a weak secret or empty hosts
- Custom user `apps.accounts.User`, plus login, logout, password change, and
  the full password-reset flow at `/accounts/`
- DRF at `/api/v1/`: namespace versioning, pagination, throttling, session auth,
  and one error envelope (`{detail, code, errors}`)
- HTMX vendored locally, CSRF header wired, error responses swapped
- Accessible template shell: skip link, `dir`-aware, 403/404/500 pages,
  form components that match Django's ARIA output
- A real design system: tokens for type/space/radii/shadow/motion, light and
  dark palettes, self-hosted IBM Plex Sans + JetBrains Mono, and a Lucide icon
  sprite — restyle a product from `static/css/tokens.css` alone
- WhiteNoise static serving with hashed manifest storage in production
- i18n ready: `LocaleMiddleware`, `LOCALE_PATHS`, single-language by default
- Health endpoints at `/health/` (HTML/JSON) and `/api/v1/health/`
- pytest with hermetic test settings, ruff, GitHub Actions CI
- Cursor skills, rules, and hooks that keep the agent honest

## Layout

```
apps/accounts     Custom user, auth screens, me endpoint
apps/common       TimeStampedModel, health, htmx helpers, API plumbing
core/settings     Environment-specific Django settings + env.py
core/api_urls.py  API version namespaces
templates/        base, error pages, registration, partials, components, pages
static/           css tokens, base styles, fonts, icon sprite, app.js, htmx
locale/           Compiled translations
tests/            pytest
.cursor/          skills, rules, hooks
PRODUCT.md        filled after product-intake
```

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements-dev.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver
```

## Checks

```bash
.venv/bin/ruff check .
.venv/bin/pytest
.venv/bin/python manage.py makemigrations --check --dry-run
```

CI runs the same set plus `check --deploy` against production settings.

## Production

```bash
DJANGO_SETTINGS_MODULE=core.settings.production \
DJANGO_SECRET_KEY=<50+ chars> \
DJANGO_ALLOWED_HOSTS=example.com \
.venv/bin/python manage.py collectstatic --noinput
```

Then serve with gunicorn. HSTS, SSL redirect, and secure cookies are on by
default; `DJANGO_SECURE_HSTS_PRELOAD=true` opts into the preload list.

## New domain app

```bash
.venv/bin/python manage.py startapp billing apps/billing
```

Set `name = "apps.billing"` and `label = "billing"` on the AppConfig, add it to `INSTALLED_APPS` in `core/settings/base.py`, and include its urls from `core/urls.py`. Add API routes in `apps/billing/api_urls.py` and include them in `core/api_urls.py`.

Subclass `apps.common.models.TimeStampedModel` for new models, and commit the migration with the model change.

## Cursor assistant

`AGENTS.md` plus `.cursor/` turns this into a senior Django + UI/UX assistant:
skills for each layer, glob-scoped rules, and hooks that format and lint on
edit, flag hardcoded secrets and missing migrations, gate destructive shell
commands, block edits on `main`, and refuse to end a turn on a red suite.
