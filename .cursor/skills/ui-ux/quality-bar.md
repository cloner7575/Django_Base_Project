# UI quality bar

Use before calling any user-facing screen “done”.

## Composition

- [ ] Header and footer are product-complete (not starter placeholders)
- [ ] Primary nav matches real IA (no Admin/Health in public nav)
- [ ] One H1; visual hierarchy obvious without reading CSS
- [ ] Sections each have one purpose and enough content to feel real
- [ ] CTA copy matches the business goal

## Visual system

- [ ] All colors/spacing/radii/fonts come from tokens
- [ ] Accent used for actions and focus — not rainbow decoration
- [ ] Imagery or crafted atmosphere present where marketing needs it
- [ ] Missing images have intentional placeholders
- [ ] Dark/light (if supported) both readable

## Interaction

- [ ] Hover/focus/active states on controls
- [ ] Forms validate and explain errors next to fields
- [ ] Empty lists explain what happens next
- [ ] Success feedback is visible after submit

## Responsive

- [ ] 375px: no horizontal scroll, tap targets ok, hero readable
- [ ] 768px: layout adapts (not only stacked clones of desktop)
- [ ] 1024px+: max width respected; hero not sparse-and-broken

## Persian extras (if fa)

- [ ] `persian-ui` definition of done passed
- [ ] No accidental English UI strings
- [ ] Tel/WhatsApp reachable
- [ ] Jalali dates where dates show

## Fail examples (rewrite)

| Symptom | Fix |
|---------|-----|
| English skip/nav | Persian copy; remove starter links |
| Giant Latin deco word | Real photo, pattern, or brand mark |
| Grey empty tiles | Seed media or designed empty state |
| Orbitron / Inter on fa site | Vazirmatn / Estedad in tokens |
| One long homepage dump | Split sections; move secondary content below fold |
