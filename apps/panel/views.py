from __future__ import annotations

from datetime import timedelta

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Count, Q, Sum
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView

from apps.catalog.models import Product, ProductVariant
from apps.common.persian import format_jalali, format_toman
from apps.orders.models import Order


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("panel:login")

    def test_func(self) -> bool:
        user = self.request.user
        return bool(user.is_authenticated and user.is_staff)

    def handle_no_permission(self) -> HttpResponse:
        if self.request.user.is_authenticated:
            return redirect("common:home")
        return super().handle_no_permission()


class PanelLoginView(LoginView):
    template_name = "panel/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):  # type: ignore[no-untyped-def]
        response = super().form_valid(form)
        if not self.request.user.is_staff:
            from django.contrib.auth import logout

            logout(self.request)
            form.add_error(None, "فقط کارکنان می‌توانند وارد پنل شوند.")
            return self.form_invalid(form)
        return response

    def get_success_url(self) -> str:
        return str(reverse_lazy("panel:dashboard"))


class PanelLogoutView(LogoutView):
    next_page = reverse_lazy("panel:login")


class DashboardView(StaffRequiredMixin, TemplateView):
    template_name = "panel/dashboard.html"

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        paid = Order.objects.filter(status=Order.Status.PAID)
        today_sales = (
            paid.filter(created_at__date=today).aggregate(s=Sum("total_amount"))["s"]
            or 0
        )
        week_start = today - timedelta(days=6)
        week_sales = (
            paid.filter(created_at__date__gte=week_start).aggregate(
                s=Sum("total_amount")
            )["s"]
            or 0
        )
        pending = Order.objects.filter(status=Order.Status.PENDING_PAYMENT).count()
        today_orders = Order.objects.filter(created_at__date=today).count()
        low_stock = ProductVariant.objects.filter(stock__gt=0, stock__lt=3).count()
        no_image = (
            Product.objects.filter(Q(image="") | Q(image__isnull=True))
            .annotate(img_count=Count("images"))
            .filter(img_count=0)
            .count()
        )
        context.update(
            {
                "panel_section": "dashboard",
                "kpi_today": format_toman(today_sales),
                "kpi_week": format_toman(week_sales),
                "kpi_pending": pending,
                "kpi_today_orders": today_orders,
                "low_stock": low_stock,
                "no_image": no_image,
                "recent_orders": Order.objects.select_related("user").order_by(
                    "-created_at"
                )[:8],
                "format_jalali": format_jalali,
                "format_toman": format_toman,
            }
        )
        return context


class OrderListView(StaffRequiredMixin, ListView):
    model = Order
    template_name = "panel/orders.html"
    context_object_name = "orders"
    paginate_by = 20

    def get_queryset(self):  # type: ignore[no-untyped-def]
        qs = Order.objects.select_related("user").order_by("-created_at")
        tab = self.request.GET.get("tab", "action")
        if tab == "payment":
            qs = qs.filter(status=Order.Status.PENDING_PAYMENT)
        elif tab == "done":
            qs = qs.filter(status=Order.Status.PAID)
        elif tab == "failed":
            qs = qs.filter(status__in=[Order.Status.FAILED, Order.Status.CANCELLED])
        elif tab == "action":
            qs = qs.filter(status__in=[Order.Status.PENDING_PAYMENT, Order.Status.PAID])
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(
                Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(id__icontains=q)
            )
        return qs

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["panel_section"] = "orders"
        context["tab"] = self.request.GET.get("tab", "action")
        context["format_toman"] = format_toman
        context["format_jalali"] = format_jalali
        return context


class ProductListView(StaffRequiredMixin, ListView):
    model = Product
    template_name = "panel/products.html"
    context_object_name = "products"
    paginate_by = 20

    def get_queryset(self):  # type: ignore[no-untyped-def]
        qs = Product.objects.select_related("category").prefetch_related("variants")
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(slug__icontains=q))
        if self.request.GET.get("low"):
            qs = qs.filter(variants__stock__gt=0, variants__stock__lt=3).distinct()
        return qs.order_by("name")

    def get_context_data(self, **kwargs: object) -> dict[str, object]:
        context = super().get_context_data(**kwargs)
        context["panel_section"] = "products"
        context["format_toman"] = format_toman
        return context


class OrderDetailView(StaffRequiredMixin, View):
    def get(self, request: HttpRequest, pk: int) -> HttpResponse:
        order = get_object_or_404(
            Order.objects.prefetch_related("items", "payments"),
            pk=pk,
        )
        return render(
            request,
            "panel/order_detail.html",
            {
                "order": order,
                "panel_section": "orders",
                "format_toman": format_toman,
                "format_jalali": format_jalali,
            },
        )

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        order = get_object_or_404(Order, pk=pk)
        new_status = request.POST.get("status", "").strip()
        if new_status in Order.Status.values:
            order.status = new_status
            order.save(update_fields=["status", "updated_at"])
        return redirect("panel:order_detail", pk=pk)
