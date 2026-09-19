from __future__ import annotations

from django.core.paginator import Page, Paginator
from django.db.models import QuerySet

from apps.catalog.adapters import ensure_default_variant, product_to_dict
from apps.catalog.models import Category, Collection, Product

PAGE_SIZE = 12


def active_products() -> QuerySet[Product]:
    return Product.objects.active().with_relations()


def paginate_products(
    qs: QuerySet[Product],
    *,
    page: int = 1,
    page_size: int = PAGE_SIZE,
) -> tuple[Page, list[dict[str, object]]]:
    paginator = Paginator(qs, page_size)
    page_obj = paginator.get_page(page)
    products = list(page_obj.object_list)
    for product in products:
        ensure_default_variant(product)
    return page_obj, [product_to_dict(p) for p in products]


def home_product_dicts(limit: int = 10) -> list[dict[str, object]]:
    products = list(active_products().order_by("-best_seller", "name")[:limit])
    for product in products:
        ensure_default_variant(product)
    return [product_to_dict(p) for p in products]


def active_categories(*, limit: int | None = None) -> QuerySet[Category]:
    qs = Category.objects.filter(is_active=True).order_by("sort_order", "name")
    if limit is not None:
        return qs[:limit]
    return qs


def active_collections(*, limit: int | None = None) -> QuerySet[Collection]:
    qs = Collection.objects.filter(is_active=True).order_by("title")
    if limit is not None:
        return qs[:limit]
    return qs


def sale_product_dicts(limit: int = 8) -> list[dict[str, object]]:
    products = list(
        active_products().filter(is_sale=True).order_by("-updated_at")[:limit]
    )
    for product in products:
        ensure_default_variant(product)
    dicts = [product_to_dict(p) for p in products]
    return dicts or home_product_dicts(limit)
