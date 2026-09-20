"""API wiring.

Versions are URL namespaces (`api:v1:...`), which is what DRF's
`NamespaceVersioning` reads. Adding v2 means a second `include()` here, not a
rewrite of every app.
"""

from django.urls import include, path

v1_patterns = [
    path("", include("apps.common.api_urls")),
    path("accounts/", include("apps.accounts.api_urls")),
]

app_name = "api"

urlpatterns = [
    path("v1/", include((v1_patterns, "v1"), namespace="v1")),
]
