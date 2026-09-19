"""Isolated settings for pytest."""

from pathlib import Path

from core.settings.base import *  # noqa: F403
from core.settings.base import BASE_DIR

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
MAILERS = {
    "default": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend"},
}
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": Path(BASE_DIR) / "test.sqlite3",
    }
}
SITE_NAME = "تابلوسازی سپهراد"
LANGUAGE_CODE = "fa"
TEXT_DIRECTION = "rtl"
TIME_ZONE = "Asia/Tehran"
