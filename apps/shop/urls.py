from django.urls import path

from apps.shop import views

app_name = "shop"

urlpatterns = [
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/api/", views.cart_api, name="cart_api"),
    path("cart/add/<slug:slug>/", views.cart_add, name="cart_add"),
    path(
        "cart/update/<int:variant_id>/",
        views.cart_update,
        name="cart_update",
    ),
    path(
        "cart/remove/<int:variant_id>/",
        views.cart_remove,
        name="cart_remove",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("payment/callback/", views.payment_callback, name="payment_callback"),
    path(
        "payment/success/<int:order_id>/",
        views.payment_success,
        name="payment_success",
    ),
    path(
        "payment/failed/<int:order_id>/",
        views.payment_failed,
        name="payment_failed",
    ),
]
