from django.http import HttpRequest, HttpResponse, JsonResponse

from apps.catalog.views import home as catalog_home


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def home(request: HttpRequest) -> HttpResponse:
    return catalog_home(request)
