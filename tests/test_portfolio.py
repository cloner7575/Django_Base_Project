import pytest
from django.urls import reverse

from apps.portfolio.models import ContactMessage


@pytest.mark.django_db
def test_home_renders_selected_work(client) -> None:
    response = client.get(reverse("portfolio:home"))
    assert response.status_code == 200
    html = response.content.decode()
    assert "RahatSell" in html
    assert "Bimtec" in html
    assert "Selected Work" in html
    assert 'id="contact"' in html
    assert "mrzjkb1375@gmail.com" in html
    assert "mohammad-zare-5b3630154" in html
    assert "github.com/cloner7575" in html
    assert "files/mrz-resume.pdf" in html


@pytest.mark.django_db
def test_case_study_pages_render(client) -> None:
    for slug in ("rahatsell", "bimtec", "insurance-api", "dev2dev"):
        response = client.get(reverse("portfolio:case_study", args=[slug]))
        assert response.status_code == 200
        assert "Architecture" in response.content.decode()


@pytest.mark.django_db
def test_unknown_case_study_is_404(client) -> None:
    response = client.get(reverse("portfolio:case_study", args=["missing"]))
    assert response.status_code == 404


@pytest.mark.django_db
def test_contact_form_persists_message(client) -> None:
    response = client.post(
        reverse("portfolio:contact"),
        {
            "name": "Alex Client",
            "email": "alex@example.com",
            "message": "We need a Django API for our product.",
        },
    )
    assert response.status_code == 302
    assert ContactMessage.objects.count() == 1
    message = ContactMessage.objects.get()
    assert message.email == "alex@example.com"
    assert "Django API" in message.message


@pytest.mark.django_db
def test_contact_form_rejects_invalid_payload(client) -> None:
    response = client.post(
        reverse("portfolio:contact"),
        {"name": "", "email": "not-an-email", "message": ""},
    )
    assert response.status_code == 400
    assert ContactMessage.objects.count() == 0


@pytest.mark.django_db
def test_home_query_budget(client, django_assert_num_queries) -> None:
    # Home is static content only — no ORM reads on the happy path.
    with django_assert_num_queries(0):
        response = client.get(reverse("portfolio:home"))
    assert response.status_code == 200
