from django.http import HttpRequest, HttpResponse, JsonResponse

from apps.shop.views import home as shop_home


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def home(request: HttpRequest) -> HttpResponse:
    return shop_home(request)
