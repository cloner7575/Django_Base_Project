from __future__ import annotations

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.contact.forms import ConsultationForm


@require_http_methods(["GET", "POST"])
def contact(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "درخواست شما ثبت شد. به‌زودی با شما تماس می‌گیریم.",
            )
            return redirect("contact:contact")
        messages.error(request, "لطفاً خطاهای فرم را برطرف کنید.")
    else:
        form = ConsultationForm()

    return render(request, "contact/contact.html", {"form": form})
