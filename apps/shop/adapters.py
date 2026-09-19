from __future__ import annotations

from typing import Any

from apps.common.persian import format_toman
from apps.shop.models import Product, ProductVariant


def _image_url(product: Product) -> str:
    primary = next((img for img in product.images.all() if img.is_primary), None)
    if primary is not None:
        return primary.file.url
    first = product.images.first()
    if first is not None:
        return first.file.url
    if product.image:
        return product.image.url
    return ""


def product_to_dict(product: Product) -> dict[str, Any]:
    variants = list(product.variants.all())
    colors = [
        {"id": c.pk, "name": c.name, "hex": c.hex_code} for c in product.colors.all()
    ]
    gallery = []
    for img in product.images.all():
        gallery.append({"id": img.pk, "url": img.file.url, "alt": img.alt_text})
    if not gallery and product.image:
        gallery.append({"id": 0, "url": product.image.url, "alt": product.name})

    matrix: dict[str, Any] = {}
    sizes: list[str] = []
    for variant in variants:
        key = f"{variant.size}|{variant.color_name}"
        matrix[key] = {
            "id": variant.pk,
            "stock": variant.stock,
            "price": variant.get_base_price(),
            "sale_price": variant.get_sale_price(),
            "effective_price": variant.effective_price,
            "display_price": format_toman(
                variant.effective_price, suffix="", persian_digits=True
            ),
            "size": variant.size,
            "color": variant.color_name,
        }
        if variant.size not in sizes:
            sizes.append(variant.size)

    default = product.default_variant()
    catalog_price = product.catalog_price()
    base_for_display = default.get_base_price() if default else product.price

    return {
        "id": product.pk,
        "slug": product.slug,
        "name": product.name,
        "description": product.description,
        "url": product.get_absolute_url(),
        "price": format_toman(base_for_display, suffix="", persian_digits=True),
        "price_num": base_for_display,
        "sale_price": (
            format_toman(default.get_sale_price() or 0, suffix="", persian_digits=True)
            if default and default.is_on_sale
            else (
                format_toman(product.sale_price, suffix="", persian_digits=True)
                if product.is_on_sale
                else ""
            )
        ),
        "sale_price_num": (
            default.get_sale_price()
            if default and default.is_on_sale
            else (product.sale_price if product.is_on_sale else None)
        ),
        "effective_price_num": catalog_price,
        "display_price": format_toman(catalog_price, suffix="", persian_digits=True),
        "image_url": _image_url(product),
        "gallery": gallery,
        "category": product.category.slug,
        "category_title": product.category.name,
        "is_new": product.is_new,
        "is_sale": product.is_on_sale or product.is_sale,
        "best_seller": product.best_seller,
        "sizes": sizes,
        "colors": colors,
        "variants": list(matrix.values()),
        "variant_matrix": matrix,
        "default_variant_id": default.pk if default else None,
        "in_stock": product.is_in_stock,
    }


def ensure_default_variant(product: Product) -> ProductVariant:
    """Create a single default variant from product stock/price if none exist."""
    existing = product.variants.first()
    if existing is not None:
        return existing
    return ProductVariant.objects.create(
        product=product,
        size="استاندارد",
        stock=product.stock or 10,
        price=None,
        sale_price=None,
    )
