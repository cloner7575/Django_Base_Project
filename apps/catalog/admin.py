from django.contrib import admin

from apps.catalog.models import (
    Category,
    Collection,
    HeroSlide,
    Product,
    ProductColor,
    ProductImage,
    ProductVariant,
    SiteFeature,
    Testimonial,
)
from apps.common.persian import format_jalali, format_toman


def jalali_created(obj: object) -> str:
    return format_jalali(obj.created_at, "%Y/%m/%d %H:%M")


jalali_created.short_description = "ایجاد (جلالی)"  # type: ignore[attr-defined]


def price_toman(obj: Product) -> str:
    return format_toman(obj.catalog_price())


price_toman.short_description = "قیمت"  # type: ignore[attr-defined]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 0


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    autocomplete_fields = ("color",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "sort_order")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "slug")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        price_toman,
        "is_active",
        "is_new",
        "is_sale",
        "best_seller",
    )
    list_filter = ("is_active", "is_new", "is_sale", "best_seller", "category")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("category",)
    filter_horizontal = ("collections",)
    inlines = (ProductImageInline, ProductColorInline, ProductVariantInline)
    list_select_related = ("category",)


@admin.register(ProductColor)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ("name", "product", "hex_code")
    search_fields = ("name", "product__name")
    autocomplete_fields = ("product",)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("headline", "theme", "sort_order", "is_active")


@admin.register(SiteFeature)
class SiteFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "sort_order", "is_active")
