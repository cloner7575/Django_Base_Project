import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command

from apps.shop.models import Category, Product


@pytest.mark.django_db
def test_seed_shop_creates_catalog() -> None:
    call_command("seed_shop")
    assert Category.objects.count() == 4
    assert Product.objects.count() >= 10
    call_command("seed_shop")
    assert Category.objects.count() == 4


@pytest.mark.django_db
def test_seed_shop_with_demo_user() -> None:
    call_command("seed_shop", with_demo_user=True)
    user = get_user_model().objects.get(username="demo")
    assert user.check_password("demo-pass-123")
