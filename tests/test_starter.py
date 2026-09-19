import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.mark.django_db
def test_user_model_is_custom() -> None:
    assert get_user_model()._meta.label == "accounts.User"


def test_health(client) -> None:
    response = client.get(reverse("common:health"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


@pytest.mark.django_db
def test_home_page_is_accessible(client) -> None:
    response = client.get(reverse("common:home"))
    assert response.status_code == 200
    html = response.content.decode()
    assert 'href="#main"' in html
    assert "<main" in html
    assert "رفتن به محتوا" in html
    assert 'lang="fa"' in html
    assert 'dir="rtl"' in html
    assert "محفل" in html
