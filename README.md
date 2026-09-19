# Django starter (core)

Copy this repository for every new Django product. Keep the layout so Cursor skills and rules stay valid.

In Cursor, start with **product intake**: the agent asks brand, language, RTL/LTR, database, and theme, then writes `PRODUCT.md` before planning or coding.

## What you get

- Split settings: `core.settings.development` / `test` / `production`
- Custom user: `apps.accounts.User` (`AUTH_USER_MODEL`)
- Shared `TimeStampedModel` in `apps.common`
- Accessible UI shell: `templates/base.html` + design tokens
- Health endpoint at `/health/`
- pytest, ruff, Cursor skills/rules/hooks

## Layout

```
apps/accounts     Custom user
apps/common       Health, home, TimeStampedModel
core/settings     Environment-specific Django settings
templates/        base, partials, components, pages
static/           css tokens + base styles
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

```bash
.venv/bin/pytest
.venv/bin/ruff check .
```

Production: `DJANGO_SETTINGS_MODULE=core.settings.production` with `DJANGO_SECRET_KEY` and `DJANGO_ALLOWED_HOSTS`.

## New domain app

```bash
.venv/bin/python manage.py startapp billing apps/billing
```

Then set `name = "apps.billing"` and `label = "billing"` on the AppConfig, add it to `INSTALLED_APPS` in `core/settings/base.py`, and include its urls from `core/urls.py`.

Subclass `apps.common.models.TimeStampedModel` for new models.

## Cursor assistant

`AGENTS.md` plus `.cursor/skills` is a senior Django + UI/UX assistant (including UI UX Pro Max design search). It is written to travel with this starter into every derived project.
