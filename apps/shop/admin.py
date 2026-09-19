from django.contrib import admin

from apps.common.persian import format_jalali, format_toman
from apps.shop.models import (
    Category,
    Collection,
    HeroSlide,
    Order,
    OrderItem,
    Payment,
    Product,
    ProductColor,
    ProductImage,
    ProductVariant,
    SiteFeature,
    Testimonial,
)


def jalali_created(obj: object) -> str:
    return format_jalali(obj.created_at, "%Y/%m/%d %H:%M")


jalali_created.short_description = "ایجاد (جلالی)"  # type: ignore[attr-defined]


def price_toman(obj: Product) -> str:
    return format_toman(obj.catalog_price())


price_toman.short_description = "قیمت"  # type: ignore[attr-defined]


def total_toman(obj: Order) -> str:
    return format_toman(obj.total_amount)


total_toman.short_description = "مبلغ کل"  # type: ignore[attr-defined]


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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product",
        "product_name",
        "size",
        "color_name",
        "unit_price",
        "quantity",
        "line_total",
    )
    can_delete = False


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    readonly_fields = ("authority", "ref_id", "amount", "status", "created_at")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "full_name",
        "phone",
        total_toman,
        "status",
        jalali_created,
    )
    list_filter = ("status",)
    search_fields = ("full_name", "phone", "user__username")
    list_select_related = ("user",)
    inlines = (OrderItemInline, PaymentInline)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "authority", "amount", "status", jalali_created)
    list_filter = ("status",)


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("headline", "theme", "sort_order", "is_active")


@admin.register(SiteFeature)
class SiteFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "sort_order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("name", "rating", "sort_order", "is_active")
