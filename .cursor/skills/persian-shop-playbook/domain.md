# Domain & commerce (condensed from nightruby-store)

Full detail: `~/.cursor/skills/nightruby-store/{architecture,commerce}.md`

## Models (single shop app)

### Catalog
- **Category** — title, slug, subtitle, description, dual image (file + legacy path), optional size_guide, sort_order, is_active
- **Collection** — same dual image + banner; M2M via Product.collections
- **Product** — name, slug, description, price, sale_price (nullable toman), category, collections M2M, size_guide?, flags is_new/is_sale/best_seller/is_active, rating, review_count; `effective_price`, `is_on_sale`
- **ProductImage** — file or static_path, alt, sort_order, is_primary
- **ProductColor** — FK product, unique (product, name), hex_code, optional color image, sort_order
- **ProductVariant** — size, optional color FK, stock (default 10), sku, optional price/sale_price (null = inherit); unique (product, size, color); list price = cheapest variant effective when matrix exists

### Size guide
- **SizeGuide** — columns JSON `[{key,label}]`, is_default (clear others on save), rows via **SizeGuideRow** values JSON
- Resolve: product → category → is_default → first active
- Default columns: سایز، دور سینه، دور کمر، دور باسن

### Users / addresses
- Profile phone required; Address (title, full_name, phone, address, postal_code, is_default)
- Starter: keep `accounts.User`; add profile OneToOne if needed — do not switch AUTH_USER_MODEL

### Cart / orders
- **Cart** — user XOR session_key
- **CartItem** — variant FK, color_name denormalized, qty; unique (cart, variant); line_total from variant.effective_price
- **Order** — status pipeline pending→confirmed→processing→shipped→delivered|cancelled; payment_status pending|paid|failed; shipping standard|express; snapshot address fields; subtotal/shipping/total; zarinpal_authority/ref_id; order_number e.g. `{BRAND}-{jalali_year}-{nnn}`
- **OrderItem** — snapshot only (product_name, size, color_name, color_hex, unit_price, qty, line_total)

### Home CMS (DB-first, mock fallback)
HeroSlide · SiteFeature · Testimonial · InstagramPost · BrandStory (pk=1 + stats) · PromoBanner (pk=1, countdown)

Magazine may stay mock unless asked.

## Services

| Module | Role |
|--------|------|
| catalog | Active queries, search, related, home slices |
| product_adapter | `product_to_dict`, `variant_matrix["{size}|{color}"]` |
| cart | get/create, add/update/remove, stock checks, merge guest on login |
| zarinpal | request/verify v4; amount rial = toman×10 |
| home_content | CMS + mock fallback |
| size_guide | Resolve + dict for templates |

Thin views + context mixins for nav, cart count, catalog JSON.

## Commerce rules

1. Guest cart by session; merge on login/register
2. Checkout form: full_name, phone, address, postal_code, shipping_method → Order + snapshots → session pending_order_id → Zarinpal redirect
3. Shipping: express = fixed cost (e.g. 45_000); standard often free in NightRuby — ask before charging
4. Callback: Status OK + verify 100/101 → paid + confirmed, clear cart; idempotent
5. Wishlist: Alpine + localStorage key `{brand_slug}_wishlist` — not a Django model
6. Stock checked on cart mutate; NightRuby does **not** decrement on payment unless user asks to fix

## Product dict keys (cards / PDP)

```
id, slug, name, price, sale_price, display_price, effective_price_num,
rating, review_count, image_url, gallery_urls, category_title,
is_new, is_sale, best_seller, sizes, colors, variants, variant_matrix,
default_variant_id, description, tagline, highlights, specs, care_tips,
discount_percent, size_guide
```

## Storefront URL map (app_name store/shop)

`/` home · `/products/` · `/products/new|sale/` · `/products/<slug>/` · `/categories|collections/<slug>/` · `/search/` · `/wishlist/` · `/cart/` + add|update|remove|api · `/checkout/` · `/payment/callback|success/` · `/login|logout|account/` · static pages · `/magazine/`

## Seed

`seed_store` · `seed_home_content` · `seed_size_guides` (adapt names on starter: `seed_shop`, etc.)
