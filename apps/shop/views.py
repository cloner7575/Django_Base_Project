from __future__ import annotations

import json
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods, require_POST

from apps.common.persian import toman_to_rial
from apps.shop.adapters import ensure_default_variant, product_to_dict
from apps.shop.cart import Cart, CartError
from apps.shop.forms import AddToCartForm, CartUpdateForm, CheckoutForm
from apps.shop.models import (
    Category,
    HeroSlide,
    Order,
    Payment,
    Product,
    ProductVariant,
    SiteFeature,
    Testimonial,
)
from apps.shop.payments.zarinpal import ZarinpalError, request_payment, verify_payment
from apps.shop.services import CheckoutError, create_order_from_cart

logger = logging.getLogger(__name__)


def home(request: HttpRequest) -> HttpResponse:
    products = list(
        Product.objects.active().with_relations().order_by("-best_seller", "name")[:8]
    )
    for product in products:
        ensure_default_variant(product)
    product_dicts = [product_to_dict(p) for p in products]
    return render(
        request,
        "pages/home.html",
        {
            "hero_slides": HeroSlide.objects.filter(is_active=True),
            "features": SiteFeature.objects.filter(is_active=True),
            "testimonials": Testimonial.objects.filter(is_active=True),
            "new_products": [d for d in product_dicts if d["is_new"]][:4]
            or product_dicts[:4],
            "best_sellers": [d for d in product_dicts if d["best_seller"]][:4]
            or product_dicts[:4],
            "categories": Category.objects.filter(is_active=True)[:8],
        },
    )


@require_GET
def product_list(request: HttpRequest) -> HttpResponse:
    products_qs = Product.objects.active().with_relations()
    category_slug = request.GET.get("category", "").strip()
    categories = Category.objects.filter(is_active=True)
    active_category = None
    if category_slug:
        active_category = get_object_or_404(
            Category, slug=category_slug, is_active=True
        )
        products_qs = products_qs.filter(category=active_category)
    products = list(products_qs)
    for product in products:
        ensure_default_variant(product)
    product_dicts = [product_to_dict(p) for p in products]
    return render(
        request,
        "shop/product_list.html",
        {
            "products": product_dicts,
            "products_json": json.dumps(product_dicts, ensure_ascii=False),
            "categories": categories,
            "active_category": active_category,
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


@require_POST
def cart_add(request: HttpRequest, slug: str) -> HttpResponse:
    product = get_object_or_404(Product.objects.active(), slug=slug)
    ensure_default_variant(product)
    form = AddToCartForm(request.POST)
    if not form.is_valid():
        messages.error(request, "انتخاب نامعتبر است.")
        return redirect(product.get_absolute_url())
    try:
        variant = form.resolve_variant(product.pk)
    except (ProductVariant.DoesNotExist, forms.ValidationError) as exc:  # type: ignore[name-defined]
        messages.error(request, str(exc) if str(exc) else "بسته نامعتبر است.")
        return redirect(product.get_absolute_url())
    cart = Cart(request)
    try:
        cart.add(variant, form.cleaned_data["quantity"])
    except CartError as exc:
        messages.error(request, str(exc))
        return redirect(product.get_absolute_url())
    messages.success(request, f"{product.name} به سبد اضافه شد.")
    if request.headers.get("HX-Request") or request.headers.get("X-Requested-With"):
        return JsonResponse(cart.serialize())
    return redirect("shop:cart_detail")


# Fix ValidationError import
from django import forms  # noqa: E402


@require_GET
def cart_detail(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    return render(
        request,
        "shop/cart.html",
        {
            "lines": cart.lines(),
            "total": cart.total(),
            "cart_empty": cart.is_empty,
            "cart_count": len(cart),
        },
    )


@require_GET
def cart_api(request: HttpRequest) -> JsonResponse:
    return JsonResponse(Cart(request).serialize())


@require_POST
def cart_update(request: HttpRequest, variant_id: int) -> HttpResponse:
    variant = get_object_or_404(ProductVariant, pk=variant_id)
    form = CartUpdateForm(request.POST)
    if not form.is_valid():
        messages.error(request, "تعداد نامعتبر است.")
        return redirect("shop:cart_detail")
    cart = Cart(request)
    try:
        cart.set_quantity(variant, form.cleaned_data["quantity"])
    except CartError as exc:
        messages.error(request, str(exc))
    return redirect("shop:cart_detail")


@require_POST
def cart_remove(request: HttpRequest, variant_id: int) -> HttpResponse:
    Cart(request).remove(variant_id)
    messages.success(request, "محصول از سبد حذف شد.")
    return redirect("shop:cart_detail")


@login_required
@require_http_methods(["GET", "POST"])
def checkout(request: HttpRequest) -> HttpResponse:
    cart = Cart(request)
    if cart.is_empty:
        messages.warning(request, "سبد خرید خالی است.")
        return redirect("shop:product_list")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                order = create_order_from_cart(
                    request=request,
                    user=request.user,
                    full_name=form.cleaned_data["full_name"],
                    phone=form.cleaned_data["phone"],
                    address=form.cleaned_data["address"],
                )
            except CheckoutError as exc:
                messages.error(request, str(exc))
                return redirect("shop:cart_detail")
            return _start_payment(request, order)
    else:
        initial = {
            "full_name": request.user.get_full_name() or request.user.get_username(),
        }
        form = CheckoutForm(initial=initial)

    return render(
        request,
        "shop/checkout.html",
        {
            "form": form,
            "lines": cart.lines(),
            "total": cart.total(),
        },
    )


def _start_payment(request: HttpRequest, order: Order) -> HttpResponse:
    callback_url = getattr(
        settings, "ZARINPAL_CALLBACK_URL", ""
    ) or request.build_absolute_uri(reverse("shop:payment_callback"))
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        status=Payment.Status.INITIATED,
    )
    try:
        result = request_payment(
            amount=toman_to_rial(order.total_amount),
            description=f"سفارش #{order.pk} — محصولات خانگی محفل",
            callback_url=callback_url,
        )
    except ZarinpalError as exc:
        payment.status = Payment.Status.FAILED
        payment.raw_response = {"error": str(exc)}
        payment.save(update_fields=["status", "raw_response", "updated_at"])
        order.status = Order.Status.FAILED
        order.save(update_fields=["status", "updated_at"])
        messages.error(request, str(exc))
        logger.exception("Payment request failed for order %s", order.pk)
        return redirect("shop:payment_failed", order_id=order.pk)

    payment.authority = result.authority
    payment.status = Payment.Status.REDIRECTED
    payment.raw_response = result.raw
    payment.save(update_fields=["authority", "status", "raw_response", "updated_at"])
    return redirect(result.payment_url)


@require_GET
def payment_callback(request: HttpRequest) -> HttpResponse:
    authority = request.GET.get("Authority", "").strip()
    status = request.GET.get("Status", "").strip()
    if not authority:
        messages.error(request, "اطلاعات پرداخت ناقص است.")
        return redirect("shop:product_list")

    payment = (
        Payment.objects.select_related("order")
        .filter(authority=authority)
        .order_by("-created_at")
        .first()
    )
    if payment is None:
        messages.error(request, "پرداخت پیدا نشد.")
        return redirect("shop:product_list")

    order = payment.order
    if payment.status == Payment.Status.VERIFIED and order.status == Order.Status.PAID:
        return redirect("shop:payment_success", order_id=order.pk)

    if status != "OK":
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(pk=payment.pk)
            order = Order.objects.select_for_update().get(pk=order.pk)
            payment.status = Payment.Status.FAILED
            payment.raw_response = {**payment.raw_response, "callback_status": status}
            payment.save(update_fields=["status", "raw_response", "updated_at"])
            if order.status == Order.Status.PENDING_PAYMENT:
                order.status = Order.Status.FAILED
                order.save(update_fields=["status", "updated_at"])
        messages.error(request, "پرداخت لغو یا ناموفق بود.")
        return redirect("shop:payment_failed", order_id=order.pk)

    try:
        result = verify_payment(
            amount=toman_to_rial(payment.amount),
            authority=authority,
        )
    except ZarinpalError as exc:
        with transaction.atomic():
            payment = Payment.objects.select_for_update().get(pk=payment.pk)
            order = Order.objects.select_for_update().get(pk=order.pk)
            payment.status = Payment.Status.FAILED
            payment.raw_response = {**payment.raw_response, "verify_error": str(exc)}
            payment.save(update_fields=["status", "raw_response", "updated_at"])
            if order.status == Order.Status.PENDING_PAYMENT:
                order.status = Order.Status.FAILED
                order.save(update_fields=["status", "updated_at"])
        messages.error(request, str(exc))
        return redirect("shop:payment_failed", order_id=order.pk)

    with transaction.atomic():
        payment = Payment.objects.select_for_update().get(pk=payment.pk)
        order = Order.objects.select_for_update().get(pk=order.pk)
        if payment.status == Payment.Status.VERIFIED:
            return redirect("shop:payment_success", order_id=order.pk)
        payment.status = Payment.Status.VERIFIED
        payment.ref_id = result.ref_id
        payment.raw_response = result.raw
        payment.save(update_fields=["status", "ref_id", "raw_response", "updated_at"])
        order.status = Order.Status.PAID
        order.save(update_fields=["status", "updated_at"])

    from apps.shop.tasks import notify_order_paid

    notify_order_paid.delay(order.pk)
    messages.success(request, "پرداخت با موفقیت انجام شد.")
    return redirect("shop:payment_success", order_id=order.pk)


@login_required
@require_GET
def payment_success(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(
        Order.objects.prefetch_related("items", "payments"),
        pk=order_id,
        user=request.user,
    )
    return render(request, "shop/payment_success.html", {"order": order})


@login_required
@require_GET
def payment_failed(request: HttpRequest, order_id: int) -> HttpResponse:
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, "shop/payment_failed.html", {"order": order})


@require_GET
def wishlist(request: HttpRequest) -> HttpResponse:
    return render(request, "shop/wishlist.html")
