from __future__ import annotations

from django.db import models

from apps.common.models import TimeStampedModel


class ConsultationRequest(TimeStampedModel):
    name = models.CharField("نام", max_length=120)
    phone = models.CharField("شماره تماس", max_length=20)
    email = models.EmailField("ایمیل", blank=True)
    service_interest = models.CharField("موضوع / نوع تابلو", max_length=150, blank=True)
    message = models.TextField("پیام")
    is_read = models.BooleanField("خوانده شده", default=False)

    class Meta:
        verbose_name = "درخواست مشاوره"
        verbose_name_plural = "درخواست‌های مشاوره"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.name} — {self.phone}"
