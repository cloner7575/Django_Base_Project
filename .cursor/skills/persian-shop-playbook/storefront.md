# Storefront UI (condensed from nightruby-storefront)

**Starter CSS shops:** follow **[design.md](design.md)** first — that is the locked cream system (light-only tokens, jar placeholders, shell, anti-patterns). Use this file for NightRuby home-section order, Alpine APIs, and Tailwind-class names when cloning the full NightRuby front.

Full pixel detail: `~/.cursor/skills/nightruby-storefront/{tokens,visual-rules,components,pages}.md`

Reproduce the look **exactly** when the user wants NightRuby-class UI. No shadcn / indigo / Inter.

## Tokens (verbatim)

```
ruby (charcoal): #14110F  dark #0A0908  light #5A534C  glow #F3EBDF  muted #8A8176
gold: #A67C52  light #D4C2A6
background #F5F0E8  cream #FFFEFB  dusty-rose #EBE3D7  soft/oat #F0E9DF
border #D6CBBC  footer #E9E1D5  linen #FAF6F0
```

Type: **Estedad** display (fallback Vazirmatn), **Vazirmatn** body. Container max 1320px. Radius card 16 / section 24 / btn 10 / pill full.

Section tones: a `#FFFEFB` · b `#F0E9DF` · c `#F5F0E8` · d `#EBE3D7`

Required classes (Tailwind clone): `.btn-ruby-solid` · `.btn-ruby-outline` · `.btn-add-cart` · `.product-card` + `.product-image-wrap` aspect **4/5** · `.mobile-nav-bar` · `.header-search` · `.section-ruby-line`

Starter CSS equivalents: see design.md §8 (`.btn--primary`, `.btn-add-cart`, `.pc-jar`, …).

## Shell order (`base.html`)

```
html lang=fa dir=rtl
meta color-scheme=light
body.has-mobile-nav
  flash · header · main#main · footer
  mobile_nav (lg:hidden) · (optional) search_modal · cart_drawer
  app.js (+ alpine.min.js when using Alpine surfaces)
```

Body pad for bottom nav: `padding-bottom: calc(4.25rem + env(safe-area-inset-bottom))` — none at `lg+`.

**Desktop = `lg` (1024).** Do not treat `md` as desktop.

## Hard visual rules

- Logical CSS (`start`/`end`). Currency always `تومان` + prefer fa digits on storefront.
- Sticky header cream/95; after 40px scroll add shadow.
- Desktop header **two rows**: search | **short brand mark** | actions → centered nav.
- Mobile: hamburger SVG | mark | cart SVG — does **not** replace bottom nav.
- Bottom nav **5**: خانه، فروشگاه، علاقه‌مندی، سبد، حساب.
- Sticky PDP/cart bars: `bottom: calc(4.25rem + safe-area)` — never `bottom-0`.
- No size picker on product **card** — add uses `default_variant_id`.
- No panel cyan on storefront. Ruby is charcoal, not crimson.
- **No empty image cells** — category jar placeholder or real photo (design.md §6).
- **No dark-mode token flip** on cream shops (design.md §10).

## Alpine surface (full NightRuby)

| API | Role |
|-----|------|
| `appStore` | sticky header, search/cart/menu, cart fetch/mutate |
| `Alpine.store('app')` | wishlist localStorage |
| `productDetailPage` | size/color/qty, gallery by color, add |
| `catalogPage` | client filter/sort on products_json |
| `checkoutWizard` | آدرس → ارسال → تأیید |
| `heroSlider` / `testimonialSlider` / … | home/static |

MVP starter may use form POST + `app.js` only; add Alpine when matching NightRuby drawers.

## Home section order (exact full stack)

1 hero · 2 features · 3 categories · 4 new_arrivals · 5 collections · 6 sale · 7 promo banner · 8 brand story · 9 best_sellers · 10 magazine · 11 testimonials · 12 instagram

MVP may ship 1–4 + 9 + 11. Alternate section tones. Do not one flat white page.

## PDP

Grid 1 → `lg:2`. Sticky gallery + sticky info. Color swatches + size chips + qty. Tabs: توضیحات | راهنمای سایز | نظرات. Mobile sticky CTA above bottom nav.

## Checkout steps

آدرس / ارسال / تأیید → Zarinpal. Success: order number + ref.

## Mobile checklist (every page)

Bottom nav + active · content not under nav · sticky CTA clears nav · tap ≥40px · safe-area · no overflow 320px · filters as sheet · footer accordion · flashes under header · icons not raw text for menu/cart.
