from __future__ import annotations

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from apps.cart import services as cart_services
from apps.catalog.forms import CheckoutForm
from apps.common.persian import toman_to_rial
from apps.orders.models import Order
from apps.orders.services import CheckoutError, create_order_from_cart
from apps.payments.models import Payment
from apps.payments.services import mark_payment_verified
from apps.payments.zarinpal import ZarinpalError, request_payment, verify_payment

logger = logging.getLogger(__name__)


@login_required
@require_http_methods(["GET", "POST"])
def checkout(request: HttpRequest) -> HttpResponse:
    if cart_services.is_empty(request):
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
            "lines": cart_services.lines(request),
            "total": cart_services.cart_subtotal(request),
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
            description=f"سفارش #{order.pk} — فیتیله شاپ",
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
        if payment.status == Payment.Status.VERIFIED:
            return redirect("shop:payment_success", order_id=payment.order_id)
        order = mark_payment_verified(
            payment_id=payment.pk,
            ref_id=result.ref_id,
            raw=result.raw,
        )

    from apps.payments.tasks import notify_order_paid

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
