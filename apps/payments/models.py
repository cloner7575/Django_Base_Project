from __future__ import annotations

from django.db import models

from apps.common.models import TimeStampedModel
from apps.orders.models import Order


class Payment(TimeStampedModel):
    class Status(models.TextChoices):
        INITIATED = "initiated", "آغاز‌شده"
        REDIRECTED = "redirected", "هدایت‌شده"
        VERIFIED = "verified", "تأیید‌شده"
        FAILED = "failed", "ناموفق"

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="سفارش",
    )
    authority = models.CharField("Authority", max_length=64, blank=True, db_index=True)
    ref_id = models.CharField("کد پیگیری", max_length=64, blank=True)
    amount = models.PositiveIntegerField("مبلغ (تومان)")
    status = models.CharField(
        "وضعیت",
        max_length=32,
        choices=Status.choices,
        default=Status.INITIATED,
        db_index=True,
    )
    raw_response = models.JSONField("پاسخ درگاه", default=dict, blank=True)
    stock_decremented = models.BooleanField("موجودی کسر شده", default=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self) -> str:
        return f"پرداخت سفارش #{self.order_id} ({self.status})"
