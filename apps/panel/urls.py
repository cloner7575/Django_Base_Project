from django.urls import path

from apps.panel.views import (
    DashboardView,
    OrderDetailView,
    OrderListView,
    PanelLoginView,
    PanelLogoutView,
    ProductListView,
)

app_name = "panel"

urlpatterns = [
    path("login/", PanelLoginView.as_view(), name="login"),
    path("logout/", PanelLogoutView.as_view(), name="logout"),
    path("", DashboardView.as_view(), name="dashboard"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("products/", ProductListView.as_view(), name="products"),
]
