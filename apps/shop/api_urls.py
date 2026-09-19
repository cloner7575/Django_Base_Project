from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.shop.api import CategoryViewSet, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="api-category")
router.register("products", ProductViewSet, basename="api-product")
router.register("orders", OrderViewSet, basename="api-order")

urlpatterns = [
    path("", include(router.urls)),
]
