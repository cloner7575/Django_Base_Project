from django.contrib import admin

from apps.blog.models import Post
from apps.common.persian import format_jalali


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "published_jalali")
    list_filter = ("is_published",)
    search_fields = ("title", "excerpt", "body")
    prepopulated_fields = {"slug": ("title",)}

    @admin.display(description="انتشار")
    def published_jalali(self, obj: Post) -> str:
        return format_jalali(obj.published_at)
