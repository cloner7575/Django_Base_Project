from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Project user. Keep AUTH_USER_MODEL pointing here in every derived project."""

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self) -> str:
        return self.get_username()
