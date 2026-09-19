# Adapter: NightRuby patterns → this Django starter

Use when the workspace is the **Base/core starter** (or a clone): `apps/`, `core/settings/`, `AUTH_USER_MODEL = accounts.User`.

**UI source of truth for starter CSS shops:** [design.md](design.md). Read it before editing templates or `tokens.css`.

## Keep starter architecture

| NightRuby | This starter |
|-----------|----------------|
| `core/` + single `store/` app | `core/` + `apps/shop` (+ optional `apps/panel`) |
| Built-in User + UserProfile | `apps.accounts.User` — extend with profile OneToOne if phone needed; **never** change AUTH_USER_MODEL |
| `store/utils/jalali.py` (no dep) | Prefer `jdatetime` + `apps.common.persian` (`jalali`, `toman` filters) already in starter |
| `store/templatetags/money.py` | `{% load persian %}{{ n|toman }}` — storefront dicts use `persian_digits=True` |
| Tailwind storefront + panel | Default: [design.md](design.md) → `tokens.css` + `base.css`. **Only add Tailwind** if user wants the exact NightRuby Tailwind/Alpine build |
| Alpine cart/PDP | Alpine OK when matching NightRuby UX; form POST + `app.js` OK for MVP |
| `/panel/` under `store/panel/` | `apps/panel/` with `app_name='panel'` |
| Seeds `seed_store` | `manage.py seed_shop` |

## App split (recommended on starter)

```
apps/shop/          # models, storefront views/urls, services, adapters
apps/panel/         # staff panel only
apps/accounts/      # User + login/register
apps/common/        # TimeStampedModel, persian helpers
templates/shop/
templates/panel/
templates/components/_product_card.html
templates/partials/_header.html _footer.html _mobile_nav.html
static/css/tokens.css   # cream light-only — see design.md §2
static/css/base.css     # shell + cards + hero
static/css/panel.css    # dark cyan — never merge into storefront tokens
design.md               # project copy of playbook design.md (brand-swapped)
```

Models subclass `TimeStampedModel`.

## Token mapping (no Tailwind)

Paste the block from [design.md](design.md) §2. Critical:

- `color-scheme: light` on `:root` and `<meta name="color-scheme" content="light">`
- **No** `prefers-color-scheme: dark` remapping of cream tokens
- Charcoal primary buttons; gold accent only for highlights/eyebrows

Panel: separate `panel.css` with cyan — do not overload storefront tokens.

## UI port order (avoid ugly first paint)

1. `tokens.css` (light cream)  
2. Shell: `base.html`, header (SVG + short **brand mark**), footer, mobile nav  
3. `_product_card.html` with **category jar placeholders** (never empty cream cells)  
4. Home hero (mark + jar cluster + one CTA)  
5. Catalog compact intro + grid  
6. PDP / cart / checkout  

Then deepen Alpine drawer, CMS sections, panel tabs.

## Intake defaults for fa shops

When user says «مثل NightRuby / فروشگاه کامل / مثل محفل»:

- Language fa · RTL · Asia/Tehran · Jalali · تومان
- Write project `design.md` from this playbook’s design.md (swap mark + jar categories)
- Custom `/panel/` yes · Zarinpal sandbox yes · variants + home CMS yes
- DRF/Celery/Docker: only if they ask

## MVP slices (starter-friendly)

1. Cream tokens + shell + catalog cards (jar placeholders) + session cart + Zarinpal + Django admin  
2. Variants + PDP size/color + stronger cart API  
3. Custom `/panel/` dashboard + orders + product list  
4. Home CMS + Alpine polish  

Do not claim “NightRuby-complete” until the playbook SKILL checklist is mostly green.

## Related project skills

`persian-locale`, `persian-ecommerce`, `product-intake`, `starter-architecture`, `ui-ux`.
