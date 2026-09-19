"""Isolated settings for pytest."""

from core.settings.base import *  # noqa: F403

DEBUG = False
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
MAILERS = {
    "default": {"BACKEND": "django.core.mail.backends.locmem.EmailBackend"},
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

SITE_NAME = "محصولات خانگی محفل"
LANGUAGE_CODE = "fa"
TEXT_DIRECTION = "rtl"
TIME_ZONE = "Asia/Tehran"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
ZARINPAL_MERCHANT_ID = "00000000-0000-0000-0000-000000000000"
ZARINPAL_SANDBOX = True
ZARINPAL_CALLBACK_URL = "http://testserver/shop/payment/callback/"
