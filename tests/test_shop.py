from __future__ import annotations

from unittest.mock import patch

import pytest
from django.contrib.sessions.backends.db import SessionStore
from django.core.management import call_command
from django.test import Client, RequestFactory
from django.urls import reverse

from apps.cart import services as cart_services
from apps.cart.models import Cart, CartItem
from apps.catalog.adapters import ensure_default_variant
from apps.catalog.models import Category, Product
from apps.orders.models import Order, OrderItem
from apps.orders.services import create_order_from_cart
from apps.payments.models import Payment
from apps.payments.zarinpal import PaymentRequestResult, PaymentVerifyResult


@pytest.fixture
def category(db) -> Category:
    return Category.objects.create(name="شمع", slug="shama")


@pytest.fixture
def product(category: Category) -> Product:
    product = Product.objects.create(
        category=category,
        name="شمع معطر وانیل",
        slug="sham-vanilla",
        description="شمع سویا",
        price=150000,
        stock=10,
        is_active=True,
    )
    ensure_default_variant(product)
    return product


def _authed_request(user):
    factory = RequestFactory()
    request = factory.get("/")
    request.user = user
    request.session = SessionStore()
    request.session.create()
    return request


@pytest.mark.django_db
def test_product_list_renders(client: Client, product: Product) -> None:
    response = client.get(reverse("shop:product_list"))
    assert response.status_code == 200
    assert product.name in response.content.decode()
    assert "catalog-sort" in response.content.decode()


@pytest.mark.django_db
def test_checkout_service_keeps_stock(user, product: Product) -> None:
    request = _authed_request(user)
    variant = product.default_variant()
    assert variant is not None
    stock_before = variant.stock
    cart, _ = Cart.objects.get_or_create(user=user, defaults={"session_key": None})
    CartItem.objects.create(cart=cart, variant=variant, quantity=2)

    order = create_order_from_cart(
        request=request,
        user=user,
        full_name="علی صفری",
        phone="09120000000",
        address="تهران",
    )
    assert order.total_amount == 300000
    assert order.items.count() == 1
    variant.refresh_from_db()
    assert variant.stock == stock_before
    assert cart_services.is_empty(request)


@pytest.mark.django_db
def test_checkout_redirects_to_zarinpal(client: Client, user, product: Product) -> None:
    client.force_login(user)
    variant = product.default_variant()
    assert variant is not None
    client.post(
        reverse("shop:cart_add", kwargs={"slug": product.slug}),
        {"quantity": 2, "variant_id": variant.pk},
    )
    with patch(
        "apps.orders.views.request_payment",
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
    variant.refresh_from_db()
    assert variant.stock == 10


@pytest.mark.django_db
def test_payment_callback_decrements_stock_once(
    client: Client, user, product: Product
) -> None:
    variant = product.default_variant()
    assert variant is not None
    stock_before = variant.stock
    order = Order.objects.create(
        user=user,
        full_name="علی",
        phone="0912",
        address="تهران",
        total_amount=product.price,
        status=Order.Status.PENDING_PAYMENT,
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        variant_id_snapshot=variant.pk,
        product_name=product.name,
        size=variant.size,
        unit_price=product.price,
        quantity=2,
    )
    Payment.objects.create(
        order=order,
        amount=order.total_amount,
        authority="AUTH123",
        status=Payment.Status.REDIRECTED,
    )

    with (
        patch(
            "apps.orders.views.verify_payment",
            return_value=PaymentVerifyResult(
                ref_id="999",
                raw={"data": {"code": 100, "ref_id": 999}},
            ),
        ),
        patch("apps.payments.tasks.notify_order_paid.delay") as notify,
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
    variant.refresh_from_db()
    assert variant.stock == stock_before - 2


@pytest.mark.django_db
def test_home_has_mobile_nav(client: Client, product: Product) -> None:
    response = client.get(reverse("common:home"))
    html = response.content.decode()
    assert "mobile-nav-bar" in html
    assert response.status_code == 200


@pytest.mark.django_db
def test_pdp_has_fitile_structure(client: Client, product: Product) -> None:
    response = client.get(reverse("shop:product_detail", kwargs={"slug": product.slug}))
    html = response.content.decode()
    assert response.status_code == 200
    assert "productDetailPage" in html
    assert "fitile-mobile-cta" in html


@pytest.mark.django_db
def test_panel_requires_staff(client: Client, user) -> None:
    client.force_login(user)
    response = client.get(reverse("panel:dashboard"))
    assert response.status_code in (302, 403)


@pytest.mark.django_db
def test_seed_shop_creates_variants() -> None:
    call_command("seed_shop")
    assert Product.objects.count() >= 10
    assert Product.objects.filter(slug="sham-vanilla").exists()
    product = Product.objects.get(slug="sham-vanilla")
    assert product.variants.count() >= 1


@pytest.mark.django_db
def test_guest_cart_merge_on_login(user, product: Product) -> None:
    factory = RequestFactory()
    guest = factory.get("/")
    guest.user = type("Anon", (), {"is_authenticated": False})()
    guest.session = SessionStore()
    guest.session.create()

    variant = product.default_variant()
    assert variant is not None
    cart_services.add_item(guest, variant, 1)

    authed = factory.get("/")
    authed.user = user
    authed.session = guest.session
    cart_services.merge_guest_cart(authed)
    assert Cart.objects.filter(user=user).exists()
    assert CartItem.objects.filter(cart__user=user, variant=variant).exists()
