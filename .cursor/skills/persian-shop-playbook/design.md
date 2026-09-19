# Persian shop design system (starter CSS)

**Audience:** agents building the next Iranian RTL shop on this Django starter (`tokens.css` + `base.css`, not Tailwind unless asked).

**Goal:** ship a cream NightRuby-class storefront that already looks good on first paint — no rediscovering broken dark mode, empty cards, or text-only chrome.

When `PRODUCT.md` exists for a shop, copy or link this file as project-root `design.md` and only change brand-specific bits (mark, category jar colors, pitch).

---

## 1. One-command mental model

| Layer | File(s) | Rule |
|-------|---------|------|
| Tokens | `static/css/tokens.css` | Cream linen **light only** (`color-scheme: light`). Never flip to dark via `prefers-color-scheme`. |
| Layout + components | `static/css/base.css` | Classes listed below — extend, do not invent parallel systems. |
| Panel | `static/css/panel.css` | Separate dark + cyan. **Never** import panel cyan into storefront. |
| Shell | `templates/base.html` + `partials/_header.html` `_footer.html` `_mobile_nav.html` | Sticky header + 5-tab bottom nav (`lg` = 1024). |
| Cards | `templates/components/_product_card.html` | Always via `product_to_dict` fields. |
| Money / dates | `apps/common/persian.py` + `{% load persian %}` | Integer تومان; storefront prices with `persian_digits=True`. |

Desktop chrome breakpoint: **`1024px` (`lg`)**. Below that: mobile header + bottom nav. Do not treat `768` as desktop.

---

## 2. Tokens (paste into `:root`)

```css
:root {
  color-scheme: light;
  --font-sans: "Vazirmatn", Tahoma, sans-serif;
  --font-display: "Vazirmatn", Tahoma, sans-serif; /* Estedad if licensed/CDN */

  --color-bg: #f5f0e8;
  --color-bg-elevated: #fffefb;
  --color-ink: #14110f;
  --color-muted: #5a534c;
  --color-border: #d6cbbc;
  --color-accent: #a67c52;       /* gold highlights */
  --color-primary: #14110f;      /* charcoal solid CTAs */
  --color-primary-ink: #fffefb;
  --color-oat: #f0e9df;
  --color-dusty: #ebe3d7;
  --color-footer: #e9e1d5;
  --color-ruby-dark: #0a0908;
  --color-gold-light: #d4c2a6;

  --radius: 1rem;
  --radius-btn: 0.625rem;
  --radius-section: 1.5rem;
  --header-h: 4.25rem;
  --mobile-nav-h: 4.25rem;
  --max: 82.5rem;
  --focus: 0 0 0 3px rgb(166 124 82 / 0.35);
  --shadow-sm: 0 4px 16px rgb(20 17 15 / 0.05);
  --shadow: 0 8px 28px rgb(20 17 15 / 0.08);
}
```

`base.html`: `<meta name="color-scheme" content="light">` + Vazirmatn Google Fonts.

**Do not** keep a dark `@media (prefers-color-scheme: dark)` block that remaps cream tokens — that destroyed contrast on Mahfel.

---

## 3. Brand in the UI

| Place | What to show |
|-------|----------------|
| Header logo | Short **mark** (e.g. `محفل`), not the long legal name |
| Home H1 | Same mark, hero-sized (`clamp(3rem, 10vw, 4.5rem)`) |
| `<title>` / footer | Full `SITE_NAME` from settings / PRODUCT.md |
| Eyebrow | Short mood line (`طعم خانه`) in gold `--color-accent` |

Brand test: after removing the nav, the first viewport must still read as this brand (mark + one headline + one CTA + one visual).

---

## 4. Shell checklist

### `base.html`

```
html lang=fa dir=rtl
meta color-scheme=light
csrf-token meta
Vazirmatn + tokens.css + base.css
body.has-mobile-nav
  skip → header → main#main → footer → mobile_nav
  app.js defer
```

Body padding: `padding-bottom: calc(var(--mobile-nav-h) + env(safe-area-inset-bottom))` — **zero** at `min-width: 1024px`.

### Header

- Sticky, cream/92 + blur; `.header-scrolled` shadow after 40px (`app.js`).
- **Desktop (`≥1024`)**: row1 = search | brand mark | wishlist+cart+auth; row2 = centered text nav.
- **Mobile**: hamburger (SVG) | mark | cart (SVG). Expand `#mobile-menu` with `.is-open` + remove `hidden` (see `static/js/app.js`). Bottom nav stays.
- Icons = inline SVG (`stroke`), never emoji. `aria-label` on icon-only buttons.
- Cart badge absolutely positioned on the icon button.

### Mobile bottom nav (5)

خانه · فروشگاه · علاقه · سبد · حساب — SVG 20px + 10–11px label. Active = current route. `lg:hidden`.

### Footer

Muted cream (`--color-footer`), short pitch, storefront links. Keep light.

---

## 5. Home composition

Order (MVP — expand toward full NightRuby stack when CMS is ready):

1. **Hero** (`.mahfel-hero` or rename to `.shop-hero`) — brand mark, accent line, lede, one primary CTA, jar cluster visual  
2. Trust / features (`.trust-bar`)  
3. Categories (`.catalog-cats` pills)  
4. New arrivals (`.product-grid`)  
5. Best sellers (optional section tone `.section-tone-b`)  
6. Testimonials (`.section-tone-d`)

Hero rules:

- One composition, not a dashboard.
- Visual = CSS jar cluster (`.hero-jars` / `.hero-jar`) until real photos exist — never a blank cream slab.
- CTA = `.btn.btn--primary` (charcoal gradient).
- Alternate section backgrounds (`oat` / `dusty`); do not one flat page.

Section headers: title + `.section-ruby-line` + optional «مشاهده همه».

---

## 6. Product cards (critical)

Template: `components/_product_card.html` fed by `product_to_dict`.

### Anatomy

```
article.product-card
  a.product-image-wrap
    img OR .product-card__placeholder--{category_slug}
      .pc-jar > lid + glass + label «محفل»
    .badge--sale | .badge--new
  .product-card__body
    title · category meta · price (old + now + تومان) · .btn-add-cart
```

### Hard rules

| Rule | Detail |
|------|--------|
| No empty cream | Without `image_url`, always show category-tinted jar placeholder |
| Aspect | Mobile `1/1`; desktop `4/5` |
| Prices | `format_toman(..., persian_digits=True)` → `۱۶۵٬۰۰۰` |
| Sale | Show `.price-old` only when `sale_price_num < price_num` |
| Add to cart | POST with `default_variant_id`; **no** size picker on card |
| CTA | Solid charcoal `.btn-add-cart` (not ghost outline) |

### Category jar tints (extend per shop)

| Slug example | Fill mood |
|--------------|-----------|
| `torshiijat` / pickles | terracotta `#c45c3e` → `#6b2a1c` |
| `morabba` / jam | rose `#c45a72` → `#6b2438` |
| `labaniat` / dairy | oat glass `#e8dfd0` + dark label |
| `khoshkbar` / spices | gold `#c4945a` → `#6b4a2e` |

Map `product.category` (slug) onto `product-card__placeholder--{slug}`.

---

## 7. Catalog & PDP

### Catalog

- Compact `.catalog-intro` (h1 + one line) — **not** a tall banner that eats the first viewport.
- Category pills `.catalog-cat` / `.is-active` (ink fill).
- Grid: 2 → 3 (`768`) → 4 (`1100`) columns.

### PDP

- Gallery placeholder uses same jar system + `product-card__placeholder--lg`.
- Size chips / color swatches; sticky mobile CTA clears bottom nav:
  `bottom: calc(var(--mobile-nav-h) + env(safe-area-inset-bottom))`.

---

## 8. Required CSS class map

Copy names; keep semantics stable across shops:

| Class | Role |
|-------|------|
| `.mahfel-hero` / `.shop-hero` | Home hero shell |
| `.hero-jars` `.hero-jar` | Decorative jar cluster |
| `.trust-bar` `.trust-card` | Feature strip |
| `.section-header` `.section-ruby-line` | Section chrome |
| `.section-tone-b` `.section-tone-d` | Alternating bands |
| `.catalog-cats` `.catalog-cat` | Filter pills |
| `.product-grid` `.product-card` | Catalog |
| `.product-image-wrap` `.product-card__placeholder` `.pc-jar` | Media |
| `.product-price` `.price-old` `.price-now` `.toman` | Money |
| `.btn` `.btn--primary` `.btn--ghost` `.btn-add-cart` | Actions |
| `.mobile-nav-bar` `.mobile-nav-item` `.nav-ico` | Bottom nav |
| `.site-header` `.brand__mark` `.header-icon-btn` | Chrome |
| `.nr-pdp-grid` `.nr-size-chip` | PDP |

Logical properties only (`inset-inline-start`, `margin-inline-end`, …).

---

## 9. Money & Persian display

```python
# apps/shop/adapters.py — storefront dicts
format_toman(amount, suffix="", persian_digits=True)  # ۱۶۵٬۰۰۰
```

Templates:

```django
{% load persian %}
<span class="price-now">{{ product.display_price }}</span>
<span class="toman">تومان</span>
```

Gateway: `amount_rial = amount_toman * 10`. Domain stays تومان integers.

Jalali for order dates: `{{ dt|jalali }}` / `format_jalali`.

---

## 10. Anti-patterns (learned the hard way)

1. **Dark-mode token flip** on a cream shop → unreadable / “broken” UI.  
2. **Empty image cells** with only a faint watermark → looks unfinished. Always jars or photos.  
3. **Text «منو» / «سبد»** instead of SVG icons → cheap mobile chrome.  
4. **Long SITE_NAME as H1 and header** → crowds mobile; use short mark.  
5. **Tall catalog banner** above the grid → products pushed below the fold.  
6. **Ghost add-to-cart** on cards → weak primary action; use solid charcoal.  
7. **Panel cyan `#00E5FF` on storefront** → wrong design system.  
8. **Purple/indigo SaaS**, Inter/Roboto, crimson “ruby”.  
9. **Sticky CTA `bottom: 0`** under the mobile nav.  
10. **Latin-only prices** on an otherwise Persian UI (prefer `persian_digits=True` on storefront).

---

## 11. New-shop agent workflow

```
1. product-intake → PRODUCT.md confirmed
2. Read this design.md + persian-shop-playbook/SKILL.md
3. Copy token block → tokens.css (light only)
4. Scaffold apps/shop (+ apps/panel if needed) per starter-adapter.md
5. Port shell partials + _product_card + home sections BEFORE inventing new CSS
6. Wire product_to_dict + seed_shop with categories that match jar tint slugs
7. Browser-check: home hero, /shop/products/ cards, mobile nav, contrast
8. Only then deepen panel / Alpine drawer / CMS sections
```

Reference implementation in this starter (Mahfel):  
`static/css/tokens.css`, `static/css/base.css`, `templates/partials/*`, `templates/components/_product_card.html`, `templates/pages/home.html`.

For pixel-perfect Tailwind+Alpine NightRuby clones, also read `~/.cursor/skills/nightruby-storefront/`. For starter CSS shops, **this file wins**.

---

## 12. Brand swap checklist (next shop)

- [ ] Replace mark string (`محفل`) in header, hero, jar labels  
- [ ] Set `SITE_NAME` / PRODUCT.md full name  
- [ ] Adjust `--color-accent` / jar fills if mood differs (keep charcoal primary)  
- [ ] Map real category slugs → placeholder modifiers  
- [ ] Swap seed copy / hero CMS text  
- [ ] Keep shell structure and class names identical  

Do **not** redesign tokens from scratch unless the user asks for a different visual direction.
