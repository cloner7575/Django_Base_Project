import pytest
from django.core.management import call_command

from apps.blog.models import Post
from apps.contact.models import ConsultationRequest
from apps.portfolio.models import Category, Project


@pytest.mark.django_db
def test_seed_sepehrad_creates_demo_content() -> None:
    call_command("seed_sepehrad")

    assert Category.objects.count() >= 4
    assert Project.objects.published().count() >= 6
    assert Project.objects.featured().count() >= 4
    assert Post.objects.published().count() >= 3
    assert ConsultationRequest.objects.exists()

    assert Project.objects.filter(slug="neon-cafe-robat-karim").exists()
    assert Post.objects.filter(slug="learning-how-to-make-a-neon-sign-at-home").exists()


@pytest.mark.django_db
def test_seed_sepehrad_is_idempotent() -> None:
    call_command("seed_sepehrad")
    call_command("seed_sepehrad")

    assert Project.objects.filter(slug="neon-cafe-robat-karim").count() == 1
    assert (
        Post.objects.filter(slug="learning-how-to-make-a-neon-sign-at-home").count()
        == 1
    )
