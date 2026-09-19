# Design — محصولات خانگی محفل

Project UI contract for this shop. Agents: treat this as source of truth for storefront look.

Canonical reusable system (copy for the next shop):  
`.cursor/skills/persian-shop-playbook/design.md`

## Brand

| Key | Value |
|-----|--------|
| Mark (header / H1 / jar label) | محفل |
| Full name (`SITE_NAME`) | محصولات خانگی محفل |
| Pitch | ترشی و محصولات خانگی تازه — ارسال با مراقبت |
| Mood | Cream linen · charcoal · gold · homemade / appetizing |

## Locked choices

- **Light-only** cream storefront (`color-scheme: light`) — do not add dark token remaps
- Font: Vazirmatn (display + body)
- Primary CTA: charcoal solid; accent: gold `#A67C52`
- Mobile: 5-tab bottom nav; header uses SVG menu/cart + short mark
- Product cards: category jar placeholders until real photos exist
- Prices: Persian digits + `تومان` via `product_to_dict`

## Category → jar tint

| Slug | Tint |
|------|------|
| `torshiijat` | terracotta |
| `morabba` | rose |
| `labaniat` | oat / dairy |
| `khoshkbar` | gold / spice |

## Implementation map

| Concern | Path |
|---------|------|
| Tokens | `static/css/tokens.css` |
| Components / layout | `static/css/base.css` |
| Panel (separate) | `static/css/panel.css` |
| Shell | `templates/base.html`, `partials/_header.html`, `_footer.html`, `_mobile_nav.html` |
| Card | `templates/components/_product_card.html` |
| Home | `templates/pages/home.html` |
| Adapter | `apps/shop/adapters.py` |

## Next shop

1. Copy `.cursor/skills/persian-shop-playbook/design.md` → new project `design.md`
2. Swap mark, pitch, category slugs/tints
3. Follow playbook **Fast path** in `SKILL.md` — do not freestyle a new palette
