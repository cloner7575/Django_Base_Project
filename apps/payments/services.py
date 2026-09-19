from __future__ import annotations

from django.db import transaction

from apps.catalog.models import ProductVariant
from apps.orders.models import Order
from apps.payments.models import Payment


@transaction.atomic
def mark_payment_verified(
    *, payment_id: int, ref_id: str, raw: dict[str, object]
) -> Order:
    """Idempotent: mark paid and decrement stock once."""
    payment = (
        Payment.objects.select_for_update().select_related("order").get(pk=payment_id)
    )
    order = (
        Order.objects.select_for_update()
        .prefetch_related("items")
        .get(pk=payment.order_id)
    )

    if payment.status == Payment.Status.VERIFIED and order.status == Order.Status.PAID:
        return order

    payment.status = Payment.Status.VERIFIED
    payment.ref_id = ref_id
    payment.raw_response = raw
    payment.save(update_fields=["status", "ref_id", "raw_response", "updated_at"])

    order.status = Order.Status.PAID
    order.save(update_fields=["status", "updated_at"])

    if not payment.stock_decremented:
        for item in order.items.all():
            if not item.variant_id_snapshot:
                continue
            variant = (
                ProductVariant.objects.select_for_update()
                .filter(pk=item.variant_id_snapshot)
                .first()
            )
            if variant is None:
                continue
            variant.stock = max(0, variant.stock - item.quantity)
            variant.save(update_fields=["stock", "updated_at"])
        payment.stock_decremented = True
        payment.save(update_fields=["stock_decremented", "updated_at"])

    return order
