from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser
from django.db import transaction
from django.http import HttpRequest

from apps.shop.cart import Cart
from apps.shop.models import Order, OrderItem, ProductVariant


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
    cart = Cart(request)
    if cart.is_empty:
        raise CheckoutError("سبد خرید خالی است.")

    variant_ids = [int(vid) for vid in cart.items]
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

    for variant_id_str, quantity in cart.items.items():
        variant_id = int(variant_id_str)
        variant = variants.get(variant_id)
        if variant is None or not variant.product.is_active:
            raise CheckoutError("یکی از محصولات دیگر موجود نیست.")
        if variant.stock < quantity:
            raise CheckoutError(f"موجودی «{variant.product.name}» کافی نیست.")

        unit = variant.effective_price
        OrderItem.objects.create(
            order=order,
            product=variant.product,
            product_name=variant.product.name,
            size=variant.size,
            color_name=variant.color_name,
            unit_price=unit,
            quantity=quantity,
        )
        variant.stock -= quantity
        variant.save(update_fields=["stock", "updated_at"])

    order.recalculate_total()
    cart.clear()
    return order
