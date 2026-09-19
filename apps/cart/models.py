from __future__ import annotations

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from apps.catalog.models import ProductVariant
from apps.common.models import TimeStampedModel


class Cart(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="cart",
        verbose_name="کاربر",
    )
    session_key = models.CharField(
        "کلید نشست",
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        verbose_name = "سبد"
        verbose_name_plural = "سبدها"

    def __str__(self) -> str:
        if self.user_id:
            return f"Cart user={self.user_id}"
        return f"Cart session={self.session_key}"


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="سبد",
    )
    variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name="cart_items",
        verbose_name="واریانت",
    )
    quantity = models.PositiveIntegerField(
        "تعداد",
        default=1,
        validators=[MinValueValidator(1)],
    )
    color_name = models.CharField("رنگ", max_length=80, blank=True)

    class Meta:
        unique_together = (("cart", "variant"),)
        verbose_name = "آیتم سبد"
        verbose_name_plural = "آیتم‌های سبد"

    def __str__(self) -> str:
        return f"{self.variant_id} × {self.quantity}"

    @property
    def unit_price(self) -> int:
        return self.variant.effective_price

    @property
    def line_total(self) -> int:
        return self.unit_price * self.quantity
