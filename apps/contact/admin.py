from django.contrib import admin

from apps.common.persian import format_jalali
from apps.contact.models import ConsultationRequest


@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "service_interest",
        "is_read",
        "created_jalali",
    )
    list_filter = ("is_read",)
    search_fields = ("name", "phone", "email", "message")
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="ثبت")
    def created_jalali(self, obj: ConsultationRequest) -> str:
        return format_jalali(obj.created_at, "%Y/%m/%d %H:%M")
