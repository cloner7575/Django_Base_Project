"""Local development. Default for manage.py and runserver."""

from core.settings.base import *  # noqa: F403

DEBUG = True

ALLOWED_HOSTS = get_list(  # noqa: F405
    "DJANGO_ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "[::1]"],
)

INTERNAL_IPS = ["127.0.0.1"]
