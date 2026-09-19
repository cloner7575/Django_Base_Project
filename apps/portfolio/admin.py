from django.contrib import admin

from apps.common.persian import format_jalali
from apps.portfolio.models import Category, Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_published",
        "is_featured",
        "created_jalali",
    )
    list_filter = ("is_published", "is_featured", "category")
    search_fields = ("title", "summary", "client_name")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ProjectImageInline]

    @admin.display(description="ایجاد")
    def created_jalali(self, obj: Project) -> str:
        return format_jalali(obj.created_at)
