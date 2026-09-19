from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import transaction
from django.http import HttpRequest

from apps.cart import services as cart_services
from apps.catalog.models import ProductVariant
from apps.orders.models import Order, OrderItem


class CheckoutError(Exception):
    """Raised when checkout cannot proceed."""


@transaction.atomic
def create_order_from_cart(
    *,
    request: HttpRequest,
    user: AbstractBaseUser,
    full_name: str,
    phone: str,
    address: str,
) -> Order:
    """Create order + snapshots. Does NOT decrement stock (that happens on paid)."""
    if cart_services.is_empty(request):
        raise CheckoutError("سبد خرید خالی است.")

    cart_lines = cart_services.lines(request)
    variant_ids = [int(line["variant"].pk) for line in cart_lines]  # type: ignore[union-attr]
    variants = {
        v.pk: v
        for v in ProductVariant.objects.select_for_update()
        .select_related("product", "color")
        .filter(pk__in=variant_ids)
    }

    order = Order.objects.create(
        user=user,
        full_name=full_name,
        phone=phone,
        address=address,
        status=Order.Status.PENDING_PAYMENT,
    )

    for line in cart_lines:
        variant = line["variant"]
        quantity = int(line["quantity"])  # type: ignore[arg-type]
        assert hasattr(variant, "pk")
        locked = variants.get(variant.pk)
        if locked is None or not locked.product.is_active:
            raise CheckoutError("یکی از محصولات دیگر موجود نیست.")
        if locked.stock < quantity:
            raise CheckoutError(f"موجودی «{locked.product.name}» کافی نیست.")

        unit = locked.effective_price
        OrderItem.objects.create(
            order=order,
            product=locked.product,
            variant_id_snapshot=locked.pk,
            product_name=locked.product.name,
            size=locked.size,
            color_name=locked.color_name,
            unit_price=unit,
            quantity=quantity,
        )

    order.recalculate_total()
    cart_services.clear_cart(request)
    return order
