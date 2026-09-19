"""Production. Requires DJANGO_SECRET_KEY and DJANGO_ALLOWED_HOSTS."""

import os

from core.settings.base import *  # noqa: F403
from core.settings.base import SECRET_KEY
from core.settings.env import get_list

DEBUG = False

if not SECRET_KEY or SECRET_KEY.startswith("django-insecure-"):
    raise ValueError("Set DJANGO_SECRET_KEY to a non-insecure value in production.")

ALLOWED_HOSTS = get_list("DJANGO_ALLOWED_HOSTS")
if not ALLOWED_HOSTS:
    raise ValueError("Set DJANGO_ALLOWED_HOSTS in production.")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

csrf_origins = get_list("DJANGO_CSRF_TRUSTED_ORIGINS")
if csrf_origins:
    CSRF_TRUSTED_ORIGINS = csrf_origins

MAILERS = {
    "default": {
        "BACKEND": os.getenv(
            "DJANGO_EMAIL_BACKEND",
            "django.core.mail.backends.smtp.EmailBackend",
        ),
    },
}
