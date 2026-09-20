# Fonts

Self-hosted so the shell renders identically offline, in CI, and behind a
firewall — no Google Fonts request, no layout shift, no third-party origin.

| File | Family | Licence |
|------|--------|---------|
| `vazirmatn-arabic.woff2` | Vazirmatn (variable, arabic subset) | SIL OFL 1.1 — see `vazirmatn-OFL.txt` |
| `vazirmatn-latin.woff2` | Vazirmatn (variable, latin subset) | SIL OFL 1.1 |
| `jetbrains-mono-latin.woff2` | JetBrains Mono (variable, latin) | SIL OFL 1.1 |

Declared in `static/css/tokens.css` via `--font-sans` / `--font-mono`.
`ibm-plex-sans-latin.woff2` remains in the tree unused by this product.
