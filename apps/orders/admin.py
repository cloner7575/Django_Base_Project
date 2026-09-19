from django.contrib import admin

from apps.common.persian import format_jalali, format_toman
from apps.orders.models import Order, OrderItem
from apps.payments.models import Payment


def jalali_created(obj: object) -> str:
    return format_jalali(obj.created_at, "%Y/%m/%d %H:%M")


jalali_created.short_description = "ایجاد (جلالی)"  # type: ignore[attr-defined]


def total_toman(obj: Order) -> str:
    return format_toman(obj.total_amount)


total_toman.short_description = "مبلغ کل"  # type: ignore[attr-defined]


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product",
        "variant_id_snapshot",
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
    readonly_fields = (
        "authority",
        "ref_id",
        "amount",
        "status",
        "stock_decremented",
        "created_at",
    )
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
