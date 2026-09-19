# Persian corporate / marketing sites

Use with `persian-ui` when building سایت شرکتی، لندینگ خدمات، گالری نمونه کار، بلاگ آموزشی، فرم مشاوره.

## Information architecture (default)

| Route | Purpose | Must include |
|-------|---------|--------------|
| `/` | Trust + convert | Brand hero, short proof, services or featured work, CTA to contact |
| Services or portfolio | Evidence | Filterable list, detail with story, CTA |
| Blog / آموزش | SEO + trust | List + Jalali dates, readable prose width |
| Contact | Lead capture | Form + phone + WhatsApp + address |

Keep nav to 4–6 items. One primary conversion path.

## Home composition (first viewport)

Allowed in the first viewport:

- Brand (hero-level)
- One headline or supporting line
- One short sentence
- One CTA group (primary + optional secondary)
- One dominant visual plane (photo, workshop atmosphere, or crafted brand graphic — **not** a Latin word as decoration)

Not in the first viewport: KPI strips, blog teasers, long service grids, address blocks, multi-card dashboards.

Below the fold: services → proof/gallery → education teaser → final CTA.

## Visual recipes by industry (pick one, commit)

| Industry | Atmosphere | Accent direction |
|----------|------------|------------------|
| تابلو / نئون / چاپ | Dark workshop, controlled glow | Cyan / magenta neon — sparingly |
| کلینیک / سلامت | Calm light surfaces | Trust blue/teal, soft borders |
| حقوقی / B2B | Restrained light or charcoal | Single strong accent, generous whitespace |
| آموزش | Clear hierarchy, readable cards | Warm accent, strong type scale |

Do not blend neon cyberpunk with cream linen unless the brand asks.

## Gallery / portfolio

- Consistent aspect ratio (e.g. 4:5 or 3:2)
- Title + category under image; whole tile clickable
- Missing image: designed placeholder (gradient/pattern + icon), never a collapsed empty `<img>`
- Detail: cover, short story, gallery, CTA «مشاوره برای پروژه مشابه»

## Blog / آموزش

- Excerpt on list; Jalali `time datetime`
- Article: breadcrumb, title, lede, prose `max-width: ~40rem`
- End with soft CTA to contact when relevant

## Contact page

Two-column on desktop (intro + form), single column on mobile.

Always show:

- Phone click-to-call
- WhatsApp deep link (`https://wa.me/98…`)
- City / address from product facts

Validate phone in the form; show field errors in Persian.

## Trust without fake stats

Prefer real facts: city, years if known, service list, sample projects.  
Avoid invented «۵۰۰+ پروژه» / «۹۸٪ رضایت» unless the user provided numbers.

## Copy tone

- Clear, professional Persian; short sentences
- Buttons as verbs: «درخواست مشاوره»، «مشاهده نمونه کار»، «تماس تلفنی»
- Empty: «هنوز نمونه‌ای ثبت نشده» + what to do next

## Self-review questions

1. Would this look at home next to a real Iranian business site in the same niche?
2. Can a user call or WhatsApp within one tap from any page?
3. Is anything still English because it was copied from the starter?
4. Does the hero work if images fail to load?
