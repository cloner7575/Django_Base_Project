# Design — فیتیله شاپ

Project copy of `.cursor/skills/persian-shop-playbook/design.md`, brand-swapped for **فیتیله شاپ**.

**Authority:** falii/NightRuby **structure and quality** + Fitile identity (candle/stone decor mood).  
Not a gold→pink pixel clone of NightRuby.

## Brand

| Place | Value |
|-------|--------|
| Mark / logo text | فیتیله |
| Full name (`SITE_NAME`) | فیتیله شاپ |
| Slogan | نور و بافت خانه |
| Pitch | شمع و سنگ مصنوعی برای دکور و هدیه |
| Header logo | **`static/img/logo-header.svg`** (or PNG); Estedad wordmark fallback — **never Georgia** |

## Palette delta (vs NightRuby gold)

Keep cream linen + charcoal ruby. Swap gold accent → pink:

| Token | NightRuby | فیتیله |
|-------|-----------|--------|
| Accent | `#A67C52` | `#C45A7A` |
| Accent light | `#D4C2A6` | `#E8B4C4` |
| New badge | gold | pink |
| Section ruby-line mid stop | gold | pink |
| Primary CTA | charcoal gradient | unchanged |
| Card add-to-cart | cream outline | unchanged |

## Catalog mood (placeholders only if no photo)

| Slug | Soft stage |
|------|------------|
| `shama` | warm wax amber |
| `sang` | rose-stone |
| `set` | oat + pink label |

**Default product visual = photograph 4:5**, not jars.

## Must match falii structure

- Two-row desktop header · 5-tab mobile nav · cart drawer · search modal  
- Hero `.hero-shell` **slider** (photo preferred, DB slides)  
- Home section order from playbook storefront.md (MVP may omit magazine/IG)  
- `.btn-ruby-solid` for primary · `.btn-add-cart` cream for cards  
- PDP: gallery, color/size, sticky CTA above bottom nav  
- Cart/checkout pages use the same NR shell — not starter `.stack` alone  

## Architecture note

Bounded apps: `catalog` / `cart` / `orders` / `payments` / `panel`. See playbook `domain.md`.

## Implementation note

Storefront: `nr-main.css` + `fitile-theme.css` (pink overrides, Estedad mark, logo). Alpine cart/search/PDP.
