from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from apps.common.models import TimeStampedModel


class PostQuerySet(models.QuerySet["Post"]):
    def published(self) -> PostQuerySet:
        return self.filter(is_published=True, published_at__lte=timezone.now())


class Post(TimeStampedModel):
    title = models.CharField("عنوان", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, allow_unicode=True)
    excerpt = models.CharField("خلاصه", max_length=300, blank=True)
    body = models.TextField("متن")
    cover = models.ImageField("تصویر شاخص", upload_to="blog/covers/", blank=True)
    is_published = models.BooleanField("منتشر شده", default=False)
    published_at = models.DateTimeField("زمان انتشار", default=timezone.now)

    objects = PostQuerySet.as_manager()

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله‌ها"
        ordering = ["-published_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("blog:detail", kwargs={"slug": self.slug})
