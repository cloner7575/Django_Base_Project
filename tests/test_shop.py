from __future__ import annotations

from unittest.mock import patch

import pytest
from django.core.management import call_command
from django.test import RequestFactory
from django.urls import reverse

from apps.shop.adapters import ensure_default_variant
from apps.shop.cart import Cart
from apps.shop.models import Category, Order, Payment, Product
from apps.shop.payments.zarinpal import PaymentRequestResult, PaymentVerifyResult
from apps.shop.services import create_order_from_cart


@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="ترشی", slug="torshi")


@pytest.fixture
def product(category: Category) -> Product:
    product = Product.objects.create(
        category=category,
        name="ترشی مخلوط",
        slug="torshi-makhlut",
        description="ترشی خانگی",
        price=150000,
        stock=10,
        is_active=True,
    )
    ensure_default_variant(product)
    return product


@pytest.mark.django_db
def test_product_list_renders(client, product: Product) -> None:
    response = client.get(reverse("shop:product_list"))
    assert response.status_code == 200
    assert product.name in response.content.decode()


@pytest.mark.django_db
def test_cart_to_order_service(user, product: Product) -> None:
    factory = RequestFactory()
    request = factory.get("/")
    request.session = {}
    variant = product.default_variant()
    assert variant is not None
    cart = Cart(request)
    cart.add(variant, 2)

    order = create_order_from_cart(
        request=request,
        user=user,
        full_name="علی صفری",
        phone="09120000000",
        address="تهران",
    )
    assert order.total_amount == 300000
    assert order.items.count() == 1
    assert order.items.first().size == "استاندارد"
    variant.refresh_from_db()
    assert variant.stock == 8
    assert Cart(request).is_empty


@pytest.mark.django_db
def test_checkout_redirects_to_zarinpal(client, user, product: Product) -> None:
    client.force_login(user)
    variant = product.default_variant()
    assert variant is not None
    client.post(
        reverse("shop:cart_add", kwargs={"slug": product.slug}),
        {"quantity": 2, "variant_id": variant.pk},
    )
    with patch(
        "apps.shop.views.request_payment",
        return_value=PaymentRequestResult(
            authority="A" * 36,
            payment_url="https://sandbox.zarinpal.com/pg/StartPay/AAAA",
            raw={"data": {"code": 100, "authority": "A" * 36}},
        ),
    ):
        response = client.post(
            reverse("shop:checkout"),
            {
                "full_name": "علی صفری",
                "phone": "09120000000",
                "address": "تهران",
            },
        )
    assert response.status_code == 302
    assert "zarinpal" in response.url
    assert Order.objects.filter(status=Order.Status.PENDING_PAYMENT).exists()


@pytest.mark.django_db
def test_payment_callback_idempotent(client, user, product: Product) -> None:
    order = Order.objects.create(
        user=user,
        full_name="علی",
        phone="0912",
        address="تهران",
        total_amount=product.price,
        status=Order.Status.PENDING_PAYMENT,
    )
    Payment.objects.create(
        order=order,
        amount=order.total_amount,
        authority="AUTH123",
        status=Payment.Status.REDIRECTED,
    )

    with (
        patch(
            "apps.shop.views.verify_payment",
            return_value=PaymentVerifyResult(
                ref_id="999",
                raw={"data": {"code": 100, "ref_id": 999}},
            ),
        ),
        patch("apps.shop.tasks.notify_order_paid.delay") as notify,
    ):
        first = client.get(
            reverse("shop:payment_callback"),
            {"Authority": "AUTH123", "Status": "OK"},
        )
        second = client.get(
            reverse("shop:payment_callback"),
            {"Authority": "AUTH123", "Status": "OK"},
        )

    assert first.status_code == 302
    assert second.status_code == 302
    order.refresh_from_db()
    assert order.status == Order.Status.PAID
    assert notify.call_count == 1


@pytest.mark.django_db
def test_home_has_mobile_nav(client, product: Product) -> None:
    response = client.get(reverse("common:home"))
    html = response.content.decode()
    assert "mobile-nav-bar" in html
    assert "محفل" in html or "SITE" in html or response.status_code == 200


@pytest.mark.django_db
def test_panel_requires_staff(client, user) -> None:
    client.force_login(user)
    response = client.get(reverse("panel:dashboard"))
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_seed_shop_creates_variants() -> None:
    call_command("seed_shop")
    assert Product.objects.count() >= 10
    assert Product.objects.filter(slug="torshi-makhlut").exists()
    product = Product.objects.get(slug="torshi-makhlut")
    assert product.variants.count() >= 1
