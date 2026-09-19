---
name: ui-ux
description: UI/UX for this Django starter. Combines local templates/tokens with UI UX Pro Max search (styles, palettes, UX rules). Use when editing templates, CSS, JS, HTMX, landing pages, dashboards, or reviewing accessibility.
---

# UI/UX for Django screens

You are responsible for how the product **looks and feels**, not only whether the view returns 200.

For a **new product**, finish `product-intake` first (`PRODUCT.md`). Then for visual direction apply `ui-ux-pro-max` and run its local search (Python stdlib only, no network).

Set `<html lang>` and `dir` from settings (`LANGUAGE_CODE`, `TEXT_DIRECTION`). Persian + RTL: use a Persian-capable font (e.g. Vazirmatn) in tokens.

## Django adapter (this starter)

Pro Max defaults to HTML + Tailwind and 22 other stacks. **This repo is Django templates + `static/css`.** Do not add Tailwind, shadcn, or a React SPA unless the user asked.

| Pro Max output | Apply here |
|----------------|------------|
| Color roles (`--color-primary`, …) | Map onto `static/css/tokens.css` (`--color-accent`, `--color-bg`, …). Keep light **and** dark pairs. |
| Font pairing | Set `--font-sans` / heading font in tokens; load Google Fonts in `templates/base.html` if needed |
| Landing pattern / sections | New templates under `templates/pages/` extending `base.html` |
| UX guidelines / a11y | Templates + CSS. Keep skip link, landmarks, focus |
| `--stack html-tailwind` | Translate utilities into classes in `base.css` or existing components |
| Icons | SVG (Heroicons/Lucide/Phosphor), never emoji-as-icon |

```bash
python3 .cursor/skills/ui-ux-pro-max/scripts/search.py "<product industry keywords>" --design-system -p "$SITE_NAME"
python3 .cursor/skills/ui-ux-pro-max/scripts/search.py "error summary validation" --domain ux
```

Persist only with `--persist --output-dir .` when the user wants a lasting design system. Then read `design-system/<slug>/MASTER.md` before restyling. Never `--force` without asking.

Do not let a Glassmorphism/SaaS recommendation blow away an existing product look unless the user asked for a restyle.

## Source of truth

- Tokens: `static/css/tokens.css`
- Chrome: `templates/base.html` + `partials/_header.html` / `_footer.html` / `_messages.html`
- Primitives: `components/_button.html`, `components/_field.html`
- Intelligence: `.cursor/skills/ui-ux-pro-max/` (search + CSV databases)

## Hierarchy and layout

- One `<h1>` per page. One primary action.
- Use `.stack`, `.card`, `.card-grid`, `.hero` from `base.css` before inventing new layout classes
- Spacing from `--space-*`. Do not sprinkle magic pixels
- Line length for reading text stays around 40rem (see `.lede`)

## Accessibility (must pass)

- Skip link to `#main` (already in `base.html`)
- Landmarks: header / `nav` with label / `main` / footer
- Visible `:focus-visible` (token `--focus`). Never `outline: none` without a replacement
- Every input has a `<label for>`
- Errors: `role="alert"` for failures; `role="status"` / `aria-live="polite"` for confirmations
- Buttons say the action (“Save book”), not “Submit”
- Images: meaningful `alt`, or `alt=""` if decorative
- Contrast: ink on bg from tokens, 4.5:1 for body text
- Honor `prefers-reduced-motion`
- No emoji as icons; `cursor: pointer` on clickable non-links

## Forms

- Include `components/_field.html` per field
- Show `form.non_field_errors` above fields
- Keep labels visible (placeholders are not labels)
- `autocomplete` on email/password/name
- Minimum touch target ~2.75rem (already on `.btn` and inputs)
- HTMX: `hx-indicator`, `hx-disabled-elt="this"`, return `_partial.html` on `HX-Request`

## States

Every list/detail/form needs empty, loading, error, and success — never a blank page.

## Responsive and color

- Layouts use `auto-fit` / `clamp`
- `color-scheme: light dark`; tokens already flip in `prefers-color-scheme`
- Check 375 / 768 / 1024 / 1440 before calling a page done

## Anti-patterns

- Inline `style=` except a one-off that cannot be a class
- Icon-only controls without an accessible name
- Opening a modal/toast/sidebar without keyboard trap/escape
- Copying Bootstrap/Tailwind CDN that fights `tokens.css`
- Mixing a new Pro Max style with the current tokens without updating tokens first

## Integration

- `ui-ux-pro-max`, `django-templates`, `htmx-patterns`, `django-forms`, `code-reviewer`
