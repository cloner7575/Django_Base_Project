from django.urls import path

from apps.accounts.views import CustomerLoginView, CustomerLogoutView, register

app_name = "accounts"

urlpatterns = [
    path("login/", CustomerLoginView.as_view(), name="login"),
    path("logout/", CustomerLogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
]
