from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from apps.common.htmx import is_htmx
from apps.common.services import database_status


def health(request: HttpRequest) -> JsonResponse:
    """Machine-readable probe. 503 when a dependency is down."""
    reachable, database = database_status()
    return JsonResponse(
        {"status": "ok" if reachable else "degraded", "database": database},
        status=200 if reachable else 503,
    )


def health_panel(request: HttpRequest) -> HttpResponse:
    """HTMX fragment for the same probe. Direct hits go back to the page."""
    if not is_htmx(request):
        return redirect("portfolio:home")

    reachable, database = database_status()
    return render(
        request,
        "partials/_health.html",
        {"reachable": reachable, "database": database},
        status=200 if reachable else 503,
    )
