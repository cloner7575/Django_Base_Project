---
name: persian-ui
description: >-
  Complete, production-grade Persian (fa) RTL UI/UX for Iranian websites on this
  Django starter — typography, chrome, forms, marketing pages, trust patterns,
  and a hard quality bar against skeleton designs. Use when LANGUAGE_CODE is fa,
  PRODUCT.md is Persian/RTL, building سایت شرکتی، لندینگ، فرم تماس، گالری، بلاگ،
  or when the user says طراحی فارسی، UI فارسی، RTL، یا طراحی سایت ایرانی.
---

# Persian UI (fa / RTL)

Ship **finished Iranian web UI**, not a translated English skeleton. Pair with `ui-ux` (Django tokens/templates) and `persian-locale` (Jalali). Cream shops still follow `persian-shop-playbook/design.md`.

## Mandatory workflow (every fa screen)

1. Read `PRODUCT.md` (brand, audience, mood).
2. Run Pro Max for palette/mood, then **override Latin-only fonts**:
   ```bash
   python3 .cursor/skills/ui-ux-pro-max/scripts/search.py "<industry> <mood> persian rtl" --design-system -p "$SITE_NAME"
   ```
3. Map colors into `static/css/tokens.css`. Set `--font-sans` / `--font-display` to **Vazirmatn, Estedad, or another Persian-capable face** — never Orbitron / Inter / Roboto as primary UI fonts.
4. Build **full page compositions** (header → hero → sections → footer). Do not stop at a headline + two buttons.
5. Pass the [Definition of done](#definition-of-done) before claiming finished.
6. For corporate/marketing detail patterns, read [corporate-sites.md](corporate-sites.md).

## Hard rules — Persian / RTL

| Topic | Rule |
|-------|------|
| Direction | `dir="{{ TEXT_DIRECTION }}"` from settings. Logical CSS: `margin-inline`, `padding-inline`, `inset-inline`, `text-align: start` |
| Copy | All user-facing strings in Persian (nav, skip link, buttons, empty states, errors, `aria-label`) |
| Phone / numbers | `dir="ltr"` on tel links and numeric inputs; display can use Persian digits |
| Dates | Jalali via `persian-locale` — no میلادی for end users |
| WhatsApp / call | Sticky or always-visible contact path on marketing sites (tel + wa.me) |
| Forms | Visible Persian labels; errors next to fields; success message in Persian |
| Admin | Persian `verbose_name`s when product is fa-first |

## Visual quality bar (reject if any fail)

**Fail / rewrite immediately when you see:**

- Starter leftovers: “A reusable Django base”, English “Home/Admin/Health” nav, Latin decorative words as the hero (“NEON”, “OPEN”, “LUXURY”)
- Hero that is only gradient + text with no craft (no real photo treatment, no patterned atmosphere, no brand mark system)
- Empty grey boxes as “gallery” without intentional empty-state design
- Thin footer: one sentence, no address/phone/links
- Pro Max Latin display fonts left as primary type
- Pages that look done on desktop but collapse into an unreadable stack on 375px
- Purple-on-white / cream-serif-terracotta AI clichés unless the product asked for them (see user frontend rules)

**Pass when:**

- Brand name is the hero-level signal on marketing first viewport
- One clear primary CTA in Persian matching the business goal (سفارش، مشاوره، تماس، …)
- Sections each have one job, real Persian copy, and spacing from tokens
- Header + footer feel like a real Iranian business site (phone, WhatsApp, city)
- Motion is intentional (2–3 cues) and respects `prefers-reduced-motion`
- Empty/loading/error/success states are designed, not blank

## Typography

- Body: Vazirmatn (or Estedad) — self-host under `static/fonts/` when possible; CDN ok for MVP
- Headings: same family at heavier weights, or Estedad for display
- Line-height ~1.7 for Persian body; avoid cramped Latin metrics
- Do not mix 3+ Persian fonts

## Chrome patterns (marketing / corporate)

**Header:** brand · primary nav (خانه، خدمات/نمونه کار، …) · phone (`dir="ltr"`) · optional CTA button  
**Footer:** brand blurb · tel · WhatsApp · address/city · same nav links  
**Mobile:** readable tap targets; consider bottom-safe padding if sticky call bar exists

## Forms (Iranian users)

- Labels above fields (not placeholder-only)
- Phone field: `inputmode="tel"`, `autocomplete="tel"`, `dir="ltr"`
- Submit button states the outcome: «ارسال درخواست مشاوره» not «Submit»
- After success: clear Persian confirmation + how you will follow up

## Definition of done

Before marking a fa UI task complete:

- [ ] No English UI strings on public pages (except intentional brand Latin if the brand uses it)
- [ ] Tokens updated; pages use token colors/spacing only
- [ ] Header + footer complete for the product type
- [ ] First viewport passes brand test (remove nav → still recognizable)
- [ ] Empty states written in Persian
- [ ] 375 / 768 / 1024 checked mentally or in browser
- [ ] `ui-ux` a11y rules still hold (skip link, focus, labels)

## Do not

- Ship the Django starter home template adapted with one Persian headline
- Use emoji as icons
- Treat Pro Max Immersive/3D recommendations as a license for unfinished “glow boxes”
- Hardcode `dir="rtl"` in HTML when settings provide `TEXT_DIRECTION`

## Related

- Visual system + Django adapter → `ui-ux` + `ui-ux-pro-max`
- Jalali / numbers helpers → `persian-locale`
- تومان / shop → `persian-ecommerce` / `persian-shop-playbook`
- Corporate page recipes → [corporate-sites.md](corporate-sites.md)
