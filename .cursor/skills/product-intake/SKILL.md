---
name: product-intake
description: Interview the user before building or planning a new product from this starter. Ask brand, language, RTL/LTR, database, color theme, and other product-design choices. Use when starting a new project, cloning the base, first plan, or PRODUCT.md is missing. Triggers on "new project", "start this product", "bootstrap", "از این بیس پروژه بساز".
---

# Product intake

**Do not write a plan or code until this interview is done** and the user has confirmed the summary.

Skip only when `PRODUCT.md` already exists, is filled in (not the example), and the user is continuing that product.

## How to ask

1. Prefer the **AskQuestion** tool for multiple-choice items. Put related questions in **one** form.
2. Ask free-text items (names, pitch) in the same turn, in the user's language.
3. Do not dump a 20-item questionnaire. Two rounds max, then a written summary to confirm.
4. Offer sensible defaults; never invent a brand or locale.

Persian users: ask in Persian. Keep `PRODUCT.md` keys in English so settings stay stable.

## Round 1 — identity (chat)

Ask:

- **Brand name** (shown in the header)
- **Project / repo name** (slug, e.g. `shop`)
- **One sentence**: what does this product do and for whom?
- **Industry** if not obvious (SaaS, shop, clinic, education, internal tool, …)

## Round 2 — AskQuestion (one form)

Include at least:

**Product type** (single)

- Public marketing site + app
- Logged-in web app / dashboard
- E-commerce
- Content / blog
- Internal admin-heavy tool
- API-first (DRF) with a thin UI

**Database** (single)

- SQLite (local / starter default)
- PostgreSQL
- MySQL

**UI language** (single)

- Persian (`fa`)
- English (`en-us`)
- Both (Persian default)
- Other (user will type the code)

**Text direction** (single)

- RTL (right-to-left) — default if language is `fa` / `ar` / `he` / `ur`
- LTR (left-to-right) — default for `en`
- Follow language automatically

**Color / mood** (single)

- Generate with UI UX Pro Max from the pitch
- Calm / warm (current starter tokens)
- Trust blue / SaaS
- Dark-first
- I will give exact hex colors

**Need now** (multiple)

- Public pages only (home is enough)
- Django admin customization
- REST API (DRF)
- Background jobs (Celery)
- Docker Compose
- Auth pages (login/register) beyond admin

## After answers

1. Write `PRODUCT.md` from the template `PRODUCT.md.example`. Fill every field; use `n/a` only when refused.
2. Show a short summary and wait for confirmation.
3. If they asked for a **plan**, write the plan from `PRODUCT.md`.
4. If they asked to **build**, apply in this order:

   - `.env` / `.env.example`: `DJANGO_SITE_NAME`, `DJANGO_LANGUAGE_CODE`, `DJANGO_TIME_ZONE`, `DJANGO_TEXT_DIRECTION`, `DATABASE_URL`
   - `html` `lang` / `dir` come from settings — do not hardcode
   - For Persian + RTL, prefer a Persian-capable font in tokens (e.g. Vazirmatn) via `ui-ux`
   - If they chose Pro Max colors: run `search.py --design-system -p "<brand>"` and map into `static/css/tokens.css`
   - Add optional packages **only** if they selected them (DRF, Celery, Docker)
   - First domain app under `apps/` per `starter-architecture`

## Defaults when they say "you decide"

| Topic | Default |
|-------|---------|
| Database | SQLite until production |
| Language | User's chat language (`fa` → `fa`, else `en-us`) |
| Direction | RTL for `fa`/`ar`/`he`/`ur`, else LTR |
| Theme | Pro Max from pitch |
| Extras | None |
| Time zone | `Asia/Tehran` if Persian, else `UTC` |

## Do not

- Start implementing mid-interview
- Switch `AUTH_USER_MODEL`
- Add Tailwind because Pro Max mentioned it
- Skip confirmation
