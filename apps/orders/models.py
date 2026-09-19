from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum

from apps.catalog.models import Product
from apps.common.models import TimeStampedModel


class Order(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING_PAYMENT = "pending_payment", "در انتظار پرداخت"
        PAID = "paid", "پرداخت‌شده"
        FAILED = "failed", "ناموفق"
        CANCELLED = "cancelled", "لغو‌شده"
        FULFILLED = "fulfilled", "ارسال‌شده"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name="کاربر",
    )
    full_name = models.CharField("نام گیرنده", max_length=200)
    phone = models.CharField("تلفن", max_length=20)
    address = models.TextField("آدرس")
    total_amount = models.PositiveIntegerField("مبلغ کل (تومان)", default=0)
    status = models.CharField(
        "وضعیت",
        max_length=32,
        choices=Status.choices,
        default=Status.PENDING_PAYMENT,
        db_index=True,
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"

    def __str__(self) -> str:
        return f"سفارش #{self.pk}"

    def recalculate_total(self) -> None:
        total = self.items.aggregate(s=Sum("line_total"))["s"] or 0
        self.total_amount = int(total)
        self.save(update_fields=["total_amount", "updated_at"])


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سفارش",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="محصول",
        null=True,
        blank=True,
    )
    variant_id_snapshot = models.PositiveIntegerField(
        "واریانت",
        null=True,
        blank=True,
        help_text="برای کسر موجودی پس از پرداخت",
    )
    product_name = models.CharField("نام محصول", max_length=200)
    size = models.CharField("سایز", max_length=80, blank=True)
    color_name = models.CharField("رنگ", max_length=80, blank=True)
    unit_price = models.PositiveIntegerField("قیمت واحد (تومان)")
    quantity = models.PositiveIntegerField(
        "تعداد",
        validators=[MinValueValidator(1)],
    )
    line_total = models.PositiveIntegerField("جمع ردیف (تومان)")

    class Meta:
        verbose_name = "آیتم سفارش"
        verbose_name_plural = "آیتم‌های سفارش"

    def __str__(self) -> str:
        return f"{self.product_name} × {self.quantity}"

    def save(self, *args: object, **kwargs: object) -> None:
        self.line_total = int(self.unit_price) * int(self.quantity)
        super().save(*args, **kwargs)
