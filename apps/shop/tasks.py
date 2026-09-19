from __future__ import annotations

import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from apps.common.persian import format_jalali, format_toman
from apps.shop.models import Order

logger = logging.getLogger(__name__)


@shared_task(bind=True, autoretry_for=(OSError,), retry_backoff=True, max_retries=5)
def notify_order_paid(self, order_id: int) -> None:
    order = (
        Order.objects.select_related("user")
        .prefetch_related("items")
        .filter(pk=order_id, status=Order.Status.PAID)
        .first()
    )
    if order is None:
        logger.info("notify_order_paid skipped; order %s not paid", order_id)
        return

    subject = f"سفارش #{order.pk} پرداخت شد — محصولات خانگی محفل"
    lines = [
        f"سفارش #{order.pk}",
        f"گیرنده: {order.full_name}",
        f"تلفن: {order.phone}",
        f"مبلغ: {format_toman(order.total_amount)}",
        f"تاریخ: {format_jalali(order.created_at, '%Y/%m/%d %H:%M')}",
        "",
        "اقلام:",
    ]
    for item in order.items.all():
        lines.append(f"- {item.product_name} × {item.quantity}")
    body = "\n".join(lines)

    logger.info("Order %s paid notification\n%s", order.pk, body)

    recipient = getattr(order.user, "email", "") or ""
    if recipient:
        send_mail(
            subject,
            body,
            getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@mahfel.local"),
            [recipient],
            fail_silently=False,
        )
