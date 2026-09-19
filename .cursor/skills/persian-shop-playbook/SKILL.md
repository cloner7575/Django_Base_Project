---
name: persian-shop-playbook
description: >-
  End-to-end playbook to build Iranian Persian RTL shops like NightRuby/falii:
  cream storefront, dark cyan /panel/, size×color variants, session/DB cart,
  Zarinpal, Jalali, تومان. Use when creating فروشگاه آنلاین, online shop,
  NightRuby, falii, storefront, پنل ادمین, catalog, PDP, cart, checkout,
  or when the user wants a reusable shop design system / design.md.
---

# Persian shop playbook (NightRuby-class)

One entry point for shops that should feel like **NightRuby / falii**: cream linen storefront + dark staff `/panel/` + rich catalog (variants, CMS home) + Zarinpal.

Read this skill first. Then open only the section files you need. Do **not** invent a generic SaaS shop UI.

## Read order (starter CSS shop — default)

1. **[design.md](design.md)** — proven UI system (tokens, shell, cards, anti-patterns). **Do this before writing HTML/CSS.**
2. [starter-adapter.md](starter-adapter.md) — map onto `apps/shop` + `apps/panel`
3. [domain.md](domain.md) — models / cart / order snapshots
4. [storefront.md](storefront.md) — NightRuby condensed UX (Alpine/home stack)
5. [panel.md](panel.md) — dark `/panel/`

Deep originals (personal skills — pixel authority for Tailwind clones):

| Skill | Path |
|-------|------|
| `nightruby-store` | `~/.cursor/skills/nightruby-store/` |
| `nightruby-storefront` | `~/.cursor/skills/nightruby-storefront/` |
| `nightruby-panel` | `~/.cursor/skills/nightruby-panel/` |

## Decide the target repo (before coding)

| Situation | Do this |
|-----------|---------|
| NightRuby/falii repo is in the workspace | **Copy** real `store/`, `templates/`, `static/` — do not reconstruct from memory |
| This Django **starter** (`apps/`, `core/settings/`, `AUTH_USER_MODEL=accounts.User`) | Follow [starter-adapter.md](starter-adapter.md) + **[design.md](design.md)**. Keep starter layout. Prefer tokens/`base.css` over Tailwind unless asked |
| Greenfield “exactly like NightRuby” | NightRuby stack (Tailwind ×2, Alpine, single `store` app). See [domain.md](domain.md) |

Always run **`product-intake`** first if `PRODUCT.md` is empty.

After intake on a starter shop: **write/update project-root `design.md`** by copying this skill’s [design.md](design.md) and swapping only the brand mark / category jar map. That file is what the next agent (or you) reuses without rediscovering UI mistakes.

## Non-negotiables (every shop)

1. `html lang="fa" dir="rtl"` · `Asia/Tehran` · user dates **Jalali**
2. Money = integer **تومان**; display with thousand groups + `تومان`; storefront prefers **Persian digits**; gateway = تومان × ۱۰ ریال
3. Sellable unit = **variant** (size × optional color). Colors are **per-product**, not a global Color table
4. `OrderItem` is a **snapshot** (name/size/color/price)
5. Day-to-day ops use custom **`/panel/`** (dark RTL). Django `/admin/` is secondary
6. Storefront and panel are **two design systems** — never mix panel cyan `#00E5FF` into cream storefront
7. Storefront: cream linen + charcoal `#14110F` + gold `#A67C52` · Vazirmatn · jar placeholders when no photo · 5-tab mobile bottom nav · **`color-scheme: light` only**
8. Thin views; business logic in services / adapters (`product_to_dict`)
9. Reproduce known NightRuby gaps only if cloning that product; otherwise ask

## Fast path — “فروشگاه زیبا مثل محفل” on this starter

Do **not** redesign from Pro Max scratch. Reuse the locked system:

```
□ PRODUCT.md confirmed
□ Copy skill design.md → project design.md (brand swap)
□ Paste tokens (light-only) into static/css/tokens.css
□ Scaffold apps/shop (+ panel) per starter-adapter
□ Port: base.html shell, _header, _footer, _mobile_nav, _product_card, home hero
□ product_to_dict + seed with category slugs matching jar tints
□ Browser-check home + /shop/products/ + mobile nav
□ Then panel / Zarinpal / CMS depth
```

Reference templates in a shop that already shipped this look (when present in repo):  
`templates/pages/home.html`, `templates/components/_product_card.html`, `static/css/base.css`.

## Build checklist (copy and tick)

```
Product
- [ ] PRODUCT.md confirmed (brand, fa/RTL, DB, extras)
- [ ] design.md in project root (from playbook design.md + brand swap)
- [ ] Target: NightRuby clone vs starter-adapter

Backend
- [ ] Models: Category, Collection?, Product, ProductImage, ProductColor, ProductVariant
- [ ] Cart (+ guest session), Order + OrderItem snapshots, Payment/Zarinpal
- [ ] Adapter product_to_dict (persian_digits on storefront prices)
- [ ] seed_shop (+ home CMS)

Storefront (read design.md FIRST, then storefront.md)
- [ ] Light-only cream tokens
- [ ] Shell: header (SVG icons + short brand mark), footer, mobile nav
- [ ] Hero + jar visual; category pills; product cards with category jar placeholders
- [ ] Catalog compact intro + grid; PDP; cart; checkout
- [ ] Mobile checklist pass (design.md §4–7)

Panel (panel.md)
- [ ] /panel/ login, KPIs, orders, product basics (tabs if full NightRuby)

Pay
- [ ] Checkout → Zarinpal sandbox → verify callback idempotent
```

## Stack defaults

### NightRuby clone (“دقیقاً مثل قبل”)

Django 6 · Python 3.12 · PostgreSQL · Tailwind 3.4 ×2 · Alpine 3.14 · Chart.js · Zarinpal v4 · WhiteNoise · **no** DRF/Celery/custom user unless asked.

### This starter (default for Base/core)

Keep `apps.*`, `accounts.User`, `TimeStampedModel`, split settings. **CSS tokens + `base.css`** per [design.md](design.md). Optional DRF/Celery/Docker only if intake selected them.

## Quick domain map

```
Category / Collection
Product ── ProductImage
       ── ProductColor (per product)
       ── ProductVariant (size × color?, stock, price override)
Cart ── CartItem(variant)
Order ── OrderItem(snapshot) ── Payment
Home CMS: HeroSlide, SiteFeature, Testimonial, …
```

Templates consume **product dicts** from `product_to_dict`, not raw models on cards.

## Quick UI map

| Surface | Palette | Notes |
|---------|---------|--------|
| Storefront | cream `#F5F0E8`, charcoal `#14110F`, gold `#A67C52` | Light only; see design.md |
| Panel | bg `#0f0f10`, cyan `#00E5FF` | Separate CSS file |

## Do not

- Skip design.md and freestyle a purple SaaS shop
- Dark-mode token remaps on cream storefronts
- Empty product image cells / text-only mobile header
- Mix panel cyan into storefront; crimson “ruby”; Inter/Roboto
- Sticky PDP CTA under the bottom nav
- Change `AUTH_USER_MODEL` away from `accounts.User` on this starter

## Related starter skills

`product-intake` · `persian-locale` · `persian-ecommerce` · `starter-architecture` · `ui-ux`
