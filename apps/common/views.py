from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render


def health(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"status": "ok"})


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "pages/home.html")
