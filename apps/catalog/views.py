from __future__ import annotations

import json

from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.http import require_GET

from apps.catalog.adapters import ensure_default_variant, product_to_dict
from apps.catalog.forms import AddToCartForm
from apps.catalog.models import Category, HeroSlide, Product, SiteFeature, Testimonial
from apps.catalog.selectors import (
    active_categories,
    active_collections,
    active_products,
    home_product_dicts,
    paginate_products,
    sale_product_dicts,
)


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    product_dicts = home_product_dicts(12)
    categories = []
    for cat in active_categories(limit=8):
        image_url = ""
        if cat.image:
            try:
                image_url = cat.image.url
            except ValueError:
                image_url = ""
        if not image_url:
            sample = (
                Product.objects.active().filter(category=cat).exclude(image="").first()
            )
            if sample and sample.image:
                image_url = sample.image.url
        categories.append(
            {
                "title": cat.name,
                "subtitle": cat.subtitle,
                "slug": cat.slug,
                "image_url": image_url,
                "url": f"{reverse('shop:product_list')}?category={cat.slug}",
            }
        )
    collections = []
    for col in active_collections(limit=4):
        image_url = ""
        if col.image:
            try:
                image_url = col.image.url
            except ValueError:
                image_url = ""
        if not image_url:
            sample = (
                Product.objects.active()
                .filter(collections=col)
                .exclude(image="")
                .first()
            )
            if sample and sample.image:
                image_url = sample.image.url
        collections.append(
            {
                "title": col.title,
                "subtitle": col.subtitle,
                "slug": col.slug,
                "image_url": image_url,
                "url": f"{reverse('shop:product_list')}?collection={col.slug}",
            }
        )
    return render(
        request,
        "pages/home.html",
        {
            "hero_slides": list(HeroSlide.objects.filter(is_active=True)),
            "features": SiteFeature.objects.filter(is_active=True),
            "testimonials": Testimonial.objects.filter(is_active=True),
            "new_products": [d for d in product_dicts if d["is_new"]][:5]
            or product_dicts[:5],
            "best_sellers": [d for d in product_dicts if d["best_seller"]][:5]
            or product_dicts[:5],
            "sale_products": sale_product_dicts(5),
            "categories": categories,
            "collections": collections,
        },
    )


@require_GET
def product_list(request: HttpRequest) -> HttpResponse:
    products_qs = active_products()
    category_slug = request.GET.get("category", "").strip()
    collection_slug = request.GET.get("collection", "").strip()
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "name").strip()
    categories = active_categories()
    active_category = None
    if category_slug:
        active_category = get_object_or_404(
            Category, slug=category_slug, is_active=True
        )
        products_qs = products_qs.filter(category=active_category)
    if collection_slug:
        products_qs = products_qs.filter(collections__slug=collection_slug)
    if query:
        products_qs = products_qs.filter(name__icontains=query)
    if sort == "price_asc":
        products_qs = products_qs.order_by("price")
    elif sort == "price_desc":
        products_qs = products_qs.order_by("-price")
    elif sort == "new":
        products_qs = products_qs.order_by("-is_new", "name")
    else:
        products_qs = products_qs.order_by("name")

    try:
        page = int(request.GET.get("page", "1"))
    except ValueError:
        page = 1
    try:
        page_obj, product_dicts = paginate_products(products_qs, page=page)
    except (EmptyPage, PageNotAnInteger):
        page_obj, product_dicts = paginate_products(products_qs, page=1)

    return render(
        request,
        "shop/product_list.html",
        {
            "products": product_dicts,
            "products_json": json.dumps(product_dicts, ensure_ascii=False),
            "page_obj": page_obj,
            "categories": categories,
            "active_category": active_category,
            "q": query,
            "sort": sort,
        },
    )


@require_GET
def product_detail(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product.objects.active().with_relations(), slug=slug)
    ensure_default_variant(product)
    product_dict = product_to_dict(product)
    form = AddToCartForm(
        initial={"variant_id": product_dict["default_variant_id"], "quantity": 1}
    )
    return render(
        request,
        "shop/product_detail.html",
        {
            "product": product,
            "product_dict": product_dict,
            "product_json": json.dumps(product_dict, ensure_ascii=False),
            "form": form,
        },
    )


@require_GET
def wishlist(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/wishlist.html")
