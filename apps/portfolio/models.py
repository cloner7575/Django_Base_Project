from __future__ import annotations

from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.common.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField("نام", max_length=100)
    slug = models.SlugField("اسلاگ", max_length=120, unique=True, allow_unicode=True)

    class Meta:
        verbose_name = "دسته نمونه کار"
        verbose_name_plural = "دسته‌های نمونه کار"
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class ProjectQuerySet(models.QuerySet["Project"]):
    def published(self) -> ProjectQuerySet:
        return self.filter(is_published=True)

    def featured(self) -> ProjectQuerySet:
        return self.published().filter(is_featured=True)


class Project(TimeStampedModel):
    title = models.CharField("عنوان", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, allow_unicode=True)
    summary = models.CharField("خلاصه", max_length=300, blank=True)
    description = models.TextField("توضیحات", blank=True)
    cover = models.ImageField("تصویر شاخص", upload_to="portfolio/covers/", blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="projects",
        verbose_name="دسته",
    )
    client_name = models.CharField("نام مشتری", max_length=120, blank=True)
    is_published = models.BooleanField("منتشر شده", default=True)
    is_featured = models.BooleanField("ویژه صفحه اصلی", default=False)

    objects = ProjectQuerySet.as_manager()

    class Meta:
        verbose_name = "نمونه کار"
        verbose_name_plural = "نمونه کارها"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("portfolio:detail", kwargs={"slug": self.slug})


class ProjectImage(TimeStampedModel):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="پروژه",
    )
    image = models.ImageField("تصویر", upload_to="portfolio/gallery/")
    alt_text = models.CharField("متن جایگزین", max_length=200, blank=True)
    sort_order = models.PositiveSmallIntegerField("ترتیب", default=0)

    class Meta:
        verbose_name = "تصویر نمونه کار"
        verbose_name_plural = "تصاویر نمونه کار"
        ordering = ["sort_order", "id"]

    def __str__(self) -> str:
        return self.alt_text or f"تصویر {self.pk}"
