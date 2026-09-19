from django.urls import path

from apps.cart import views as cart_views
from apps.catalog import views as catalog_views
from apps.orders import views as order_views

app_name = "shop"

urlpatterns = [
    path("products/", catalog_views.product_list, name="product_list"),
    path("products/<slug:slug>/", catalog_views.product_detail, name="product_detail"),
    path("wishlist/", catalog_views.wishlist, name="wishlist"),
    path("cart/", cart_views.cart_detail, name="cart_detail"),
    path("cart/api/", cart_views.cart_api, name="cart_api"),
    path("cart/add/<slug:slug>/", cart_views.cart_add, name="cart_add"),
    path(
        "cart/update/<int:variant_id>/",
        cart_views.cart_update,
        name="cart_update",
    ),
    path(
        "cart/remove/<int:variant_id>/",
        cart_views.cart_remove,
        name="cart_remove",
    ),
    path("checkout/", order_views.checkout, name="checkout"),
    path("payment/callback/", order_views.payment_callback, name="payment_callback"),
    path(
        "payment/success/<int:order_id>/",
        order_views.payment_success,
        name="payment_success",
    ),
    path(
        "payment/failed/<int:order_id>/",
        order_views.payment_failed,
        name="payment_failed",
    ),
]
