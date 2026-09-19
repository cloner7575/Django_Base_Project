# Product

Fill this during **product-intake**. The agent must not invent these values.

## Identity

- Brand name: محصولات خانگی محفل
- Project slug: mahfel-shop
- Pitch (one sentence): فروش آنلاین ترشی و محصولات خانگی
- Audience: خریداران ترشی و محصولات خانگی
- Industry / product type: E-commerce

## Locale

- UI language code: fa
- Text direction: rtl
- Time zone: Asia/Tehran

## Look

- Color / mood: Pro Max from pitch (appetizing warm red + gold, artisan homemade)
- Pro Max query (if used): homemade pickles food shop warm artisan
- Notes: Vazirmatn for Persian RTL body; map Pro Max primary/accent into tokens.css; Jalali dates; prices in تومان with thousand separators
- Design contract: `design.md` (brand-swapped from `.cursor/skills/persian-shop-playbook/design.md`)

## Platform

- Database: postgres
- REST API: drf
- Background jobs: celery
- Docker: yes
- Auth beyond admin: yes

## MVP

- First screens / features: home, product list/detail, session cart, checkout, Zarinpal sandbox payment, customer login/register, Django admin for catalog/orders, DRF catalog + user orders API, Celery payment notification, Docker Compose (web/db/redis/worker)

## Confirmed

- Date: 2026-09-19
- By: user
