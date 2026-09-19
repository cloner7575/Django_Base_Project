import pytest
from django.urls import reverse

from apps.blog.models import Post
from apps.contact.models import ConsultationRequest
from apps.portfolio.models import Category, Project


@pytest.mark.django_db
def test_home_page_shows_brand(client) -> None:
    response = client.get(reverse("common:home"))
    assert response.status_code == 200
    html = response.content.decode()
    assert "تابلوسازی سپهراد" in html
    assert 'dir="rtl"' in html
    assert "رفتن به محتوا" in html
    assert 'href="#main"' in html


@pytest.mark.django_db
def test_portfolio_list_and_detail(client) -> None:
    category = Category.objects.create(name="نئون", slug="neon")
    project = Project.objects.create(
        title="تابلو کافه",
        slug="cafe-neon",
        summary="نئون سفارشی",
        category=category,
        is_published=True,
    )
    list_response = client.get(reverse("portfolio:list"))
    assert list_response.status_code == 200
    assert "تابلو کافه" in list_response.content.decode()

    filtered = client.get(reverse("portfolio:list"), {"category": "neon"})
    assert filtered.status_code == 200
    assert "تابلو کافه" in filtered.content.decode()

    detail = client.get(reverse("portfolio:detail", kwargs={"slug": project.slug}))
    assert detail.status_code == 200
    assert "تابلو کافه" in detail.content.decode()


@pytest.mark.django_db
def test_blog_list_and_detail(client) -> None:
    post = Post.objects.create(
        title="ساخت نئون در خانه",
        slug="neon-home",
        excerpt="راهنمای شروع",
        body="متن آموزش نمونه.",
        is_published=True,
    )
    list_response = client.get(reverse("blog:list"))
    assert list_response.status_code == 200
    assert post.title in list_response.content.decode()

    detail = client.get(reverse("blog:detail", kwargs={"slug": post.slug}))
    assert detail.status_code == 200
    assert "متن آموزش نمونه" in detail.content.decode()


@pytest.mark.django_db
def test_contact_form_requires_csrf(client) -> None:
    csrf_client = client
    csrf_client.handler.enforce_csrf_checks = True
    response = csrf_client.post(
        reverse("contact:contact"),
        {
            "name": "علی",
            "phone": "09121234567",
            "email": "",
            "service_interest": "نئون",
            "message": "سلام، قیمت می‌خواهم.",
        },
    )
    assert response.status_code == 403
    assert ConsultationRequest.objects.count() == 0


@pytest.mark.django_db
def test_contact_form_creates_lead(client) -> None:
    response = client.post(
        reverse("contact:contact"),
        {
            "name": "علی",
            "phone": "09121234567",
            "email": "ali@example.com",
            "service_interest": "نئون",
            "message": "سلام، قیمت می‌خواهم.",
        },
        follow=True,
    )
    assert response.status_code == 200
    assert ConsultationRequest.objects.count() == 1
    lead = ConsultationRequest.objects.get()
    assert lead.name == "علی"
    assert lead.phone == "09121234567"
    assert "ثبت شد" in response.content.decode()
