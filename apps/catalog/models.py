from __future__ import annotations

from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from apps.common.models import TimeStampedModel


class Category(TimeStampedModel):
    name = models.CharField("نام", max_length=120)
    slug = models.SlugField("اسلاگ", max_length=140, unique=True, allow_unicode=True)
    subtitle = models.CharField("زیرعنوان", max_length=200, blank=True)
    image = models.ImageField("تصویر", upload_to="categories/", blank=True)
    is_active = models.BooleanField("فعال", default=True)
    sort_order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ("sort_order", "name")
        verbose_name = "دسته"
        verbose_name_plural = "دسته‌ها"

    def __str__(self) -> str:
        return self.name

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Collection(TimeStampedModel):
    title = models.CharField("عنوان", max_length=120)
    slug = models.SlugField("اسلاگ", max_length=140, unique=True, allow_unicode=True)
    subtitle = models.CharField("زیرعنوان", max_length=200, blank=True)
    image = models.ImageField("تصویر", upload_to="collections/", blank=True)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ("title",)
        verbose_name = "کالکشن"
        verbose_name_plural = "کالکشن‌ها"

    def __str__(self) -> str:
        return self.title

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ProductQuerySet(models.QuerySet):
    def active(self) -> ProductQuerySet:
        return self.filter(is_active=True, category__is_active=True)

    def with_relations(self) -> ProductQuerySet:
        return self.select_related("category").prefetch_related(
            "images",
            "colors",
            "variants__color",
            "collections",
        )


class Product(TimeStampedModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
        verbose_name="دسته",
    )
    collections = models.ManyToManyField(
        Collection,
        blank=True,
        related_name="products",
        verbose_name="کالکشن‌ها",
    )
    name = models.CharField("نام", max_length=200)
    slug = models.SlugField("اسلاگ", max_length=220, unique=True, allow_unicode=True)
    description = models.TextField("توضیحات", blank=True)
    price = models.PositiveIntegerField(
        "قیمت (تومان)",
        validators=[MinValueValidator(1)],
        help_text="قیمت پایه؛ واریانت می‌تواند override کند",
    )
    sale_price = models.PositiveIntegerField(
        "قیمت تخفیف (تومان)",
        null=True,
        blank=True,
        validators=[MinValueValidator(1)],
    )
    stock = models.PositiveIntegerField(
        "موجودی پایه",
        default=0,
        help_text="اگر واریانت نباشد از این استفاده می‌شود",
    )
    image = models.ImageField("تصویر اصلی", upload_to="products/", blank=True)
    is_active = models.BooleanField("فعال", default=True)
    is_new = models.BooleanField("جدید", default=False)
    is_sale = models.BooleanField("تخفیف", default=False)
    best_seller = models.BooleanField("پرفروش", default=False)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ("name",)
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"
        indexes = [
            models.Index(fields=["is_active", "category"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self) -> str:
        return self.name

    def save(self, *args: object, **kwargs: object) -> None:
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if self.sale_price:
            self.is_sale = True
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("shop:product_detail", kwargs={"slug": self.slug})

    @property
    def effective_price(self) -> int:
        if self.sale_price and self.sale_price < self.price:
            return int(self.sale_price)
        return int(self.price)

    @property
    def is_on_sale(self) -> bool:
        return bool(self.sale_price and self.sale_price < self.price)

    @property
    def is_in_stock(self) -> bool:
        if self.variants.exists():
            return self.variants.filter(stock__gt=0).exists()
        return self.stock > 0

    def default_variant(self) -> ProductVariant | None:
        return (
            self.variants.filter(stock__gt=0).order_by("id").first()
            or self.variants.order_by("id").first()
        )

    def catalog_price(self) -> int:
        variants = self.variants.all()
        if not variants:
            return self.effective_price
        prices = [v.effective_price for v in variants if v.stock > 0] or [
            v.effective_price for v in variants
        ]
        return min(prices) if prices else self.effective_price


class ProductImage(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="محصول",
    )
    file = models.ImageField("فایل", upload_to="products/gallery/")
    alt_text = models.CharField("متن جایگزین", max_length=200, blank=True)
    sort_order = models.PositiveIntegerField("ترتیب", default=0)
    is_primary = models.BooleanField("اصلی", default=False)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "تصویر محصول"
        verbose_name_plural = "تصاویر محصول"

    def __str__(self) -> str:
        return f"{self.product_id} image #{self.pk}"


class ProductColor(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="colors",
        verbose_name="محصول",
    )
    name = models.CharField("نام", max_length=80)
    hex_code = models.CharField("کد رنگ", max_length=7, default="#14110F")
    sort_order = models.PositiveIntegerField("ترتیب", default=0)

    class Meta:
        ordering = ("sort_order", "id")
        unique_together = (("product", "name"),)
        verbose_name = "رنگ محصول"
        verbose_name_plural = "رنگ‌های محصول"

    def __str__(self) -> str:
        return f"{self.product_id}: {self.name}"


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
        verbose_name="محصول",
    )
    size = models.CharField("سایز / بسته", max_length=80)
    color = models.ForeignKey(
        ProductColor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="variants",
        verbose_name="رنگ",
    )
    price = models.PositiveIntegerField(
        "قیمت (تومان)",
        null=True,
        blank=True,
        help_text="خالی = ارث از محصول",
    )
    sale_price = models.PositiveIntegerField(
        "تخفیف (تومان)",
        null=True,
        blank=True,
    )
    stock = models.PositiveIntegerField("موجودی", default=10)
    sku = models.CharField("SKU", max_length=64, blank=True)

    class Meta:
        ordering = ("id",)
        unique_together = (("product", "size", "color"),)
        verbose_name = "واریانت"
        verbose_name_plural = "واریانت‌ها"

    def __str__(self) -> str:
        color = f" / {self.color.name}" if self.color_id else ""
        return f"{self.product.name} — {self.size}{color}"

    def get_base_price(self) -> int:
        return int(self.price) if self.price is not None else int(self.product.price)

    def get_sale_price(self) -> int | None:
        if self.sale_price is not None:
            return int(self.sale_price)
        if self.product.sale_price is not None:
            return int(self.product.sale_price)
        return None

    @property
    def effective_price(self) -> int:
        sale = self.get_sale_price()
        base = self.get_base_price()
        if sale is not None and sale < base:
            return sale
        return base

    @property
    def is_on_sale(self) -> bool:
        sale = self.get_sale_price()
        return bool(sale is not None and sale < self.get_base_price())

    @property
    def color_name(self) -> str:
        return self.color.name if self.color_id else ""


class HeroSlide(TimeStampedModel):
    badge = models.CharField("نشان", max_length=80, blank=True)
    headline = models.CharField("عنوان", max_length=200)
    headline_accent = models.CharField("تأکید عنوان", max_length=120, blank=True)
    subtitle = models.CharField("زیرعنوان", max_length=255, blank=True)
    cta_label = models.CharField("متن دکمه", max_length=80, default="مشاهده محصولات")
    cta_url = models.CharField("لینک دکمه", max_length=200, default="/shop/products/")
    image = models.ImageField("تصویر", upload_to="home/hero/", blank=True)
    theme = models.CharField(
        "تم",
        max_length=16,
        choices=(("dark", "تیره"), ("light", "روشن"), ("photo", "عکس")),
        default="light",
    )
    sort_order = models.PositiveIntegerField("ترتیب", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "اسلاید هیرو"
        verbose_name_plural = "اسلایدهای هیرو"

    def __str__(self) -> str:
        return self.headline


class SiteFeature(TimeStampedModel):
    title = models.CharField("عنوان", max_length=120)
    subtitle = models.CharField("زیرعنوان", max_length=200, blank=True)
    sort_order = models.PositiveIntegerField("ترتیب", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "ویژگی سایت"
        verbose_name_plural = "ویژگی‌های سایت"

    def __str__(self) -> str:
        return self.title


class Testimonial(TimeStampedModel):
    name = models.CharField("نام", max_length=80)
    text = models.TextField("متن")
    rating = models.PositiveSmallIntegerField("امتیاز", default=5)
    initials = models.CharField("حروف", max_length=4, blank=True)
    sort_order = models.PositiveIntegerField("ترتیب", default=0)
    is_active = models.BooleanField("فعال", default=True)

    class Meta:
        ordering = ("sort_order", "id")
        verbose_name = "نظر مشتری"
        verbose_name_plural = "نظرات مشتری"

    def __str__(self) -> str:
        return self.name
