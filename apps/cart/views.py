from __future__ import annotations

from django import forms
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET, require_POST

from apps.cart import services as cart_services
from apps.cart.services import CartError
from apps.catalog.adapters import ensure_default_variant
from apps.catalog.forms import AddToCartForm, CartUpdateForm
from apps.catalog.models import Product, ProductVariant


def _wants_json(request: HttpRequest) -> bool:
    accept = request.headers.get("Accept", "")
    return bool(
        request.headers.get("HX-Request")
        or request.headers.get("X-Requested-With")
        or "application/json" in accept
    )


@require_POST
def cart_add(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product.objects.active(), slug=slug)
    ensure_default_variant(product)
    form = AddToCartForm(request.POST)
    if not form.is_valid():
        if _wants_json(request):
            return JsonResponse(
                {"ok": False, "error": "انتخاب نامعتبر است."}, status=400
            )
        messages.error(request, "انتخاب نامعتبر است.")
        return redirect(product.get_absolute_url())
    try:
        variant = form.resolve_variant(product.pk)
    except (ProductVariant.DoesNotExist, forms.ValidationError) as exc:
        err = str(exc) if str(exc) else "بسته نامعتبر است."
        if _wants_json(request):
            return JsonResponse({"ok": False, "error": err}, status=400)
        messages.error(request, err)
        return redirect(product.get_absolute_url())
    try:
        cart_services.add_item(request, variant, form.cleaned_data["quantity"])
    except CartError as exc:
        if _wants_json(request):
            return JsonResponse({"ok": False, "error": str(exc)}, status=400)
        messages.error(request, str(exc))
        return redirect(product.get_absolute_url())
    if _wants_json(request):
        return JsonResponse(cart_services.serialize(request))
    messages.success(request, f"{product.name} به سبد اضافه شد.")
    return redirect("shop:cart_detail")


@require_GET
def cart_detail(request: HttpRequest) -> HttpResponse:
    return render(
        request,
        "shop/cart.html",
        {
            "lines": cart_services.lines(request),
            "total": cart_services.cart_subtotal(request),
            "cart_empty": cart_services.is_empty(request),
            "cart_count": cart_services.cart_count(request),
        },
    )


@require_GET
def cart_api(request: HttpRequest) -> JsonResponse:
    return JsonResponse(cart_services.serialize(request))


@require_POST
def cart_update(request: HttpRequest, variant_id: int) -> HttpResponse:
    variant = get_object_or_404(ProductVariant, pk=variant_id)
    form = CartUpdateForm(request.POST)
    if not form.is_valid():
        if _wants_json(request):
            return JsonResponse(
                {"ok": False, "error": "تعداد نامعتبر است."}, status=400
            )
        messages.error(request, "تعداد نامعتبر است.")
        return redirect("shop:cart_detail")
    try:
        cart_services.set_quantity(request, variant, form.cleaned_data["quantity"])
    except CartError as exc:
        if _wants_json(request):
            return JsonResponse({"ok": False, "error": str(exc)}, status=400)
        messages.error(request, str(exc))
        return redirect("shop:cart_detail")
    if _wants_json(request):
        return JsonResponse(cart_services.serialize(request))
    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request: HttpRequest, variant_id: int) -> HttpResponse:
    cart_services.remove_item(request, variant_id)
    if _wants_json(request):
        return JsonResponse(cart_services.serialize(request))
    messages.success(request, "محصول از سبد حذف شد.")
    return redirect("shop:cart_detail")
