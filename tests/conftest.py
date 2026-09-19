import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username="ada",
        email="ada@example.com",
        password="pass-pass-pass",
    )
