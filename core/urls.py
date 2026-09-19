from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path


def admin_to_panel(request):  # type: ignore[no-untyped-def]
    return redirect("panel:dashboard")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("panel/", include("apps.panel.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("shop/", include("apps.catalog.storefront_urls")),
    path("api/", include("apps.catalog.api_urls")),
    path("", include("apps.common.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
