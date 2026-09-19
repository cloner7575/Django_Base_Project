from django.conf import settings
from django.http import HttpRequest


def site(request: HttpRequest) -> dict[str, str]:
    phone = getattr(settings, "CONTACT_PHONE", "09126655379")
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Core"),
        "TEXT_DIRECTION": getattr(settings, "TEXT_DIRECTION", "ltr"),
        "CONTACT_PHONE": phone,
        "CONTACT_PHONE_DISPLAY": getattr(
            settings, "CONTACT_PHONE_DISPLAY", "۰۹۱۲ ۶۶۵ ۵۳۷۹"
        ),
        "CONTACT_WHATSAPP": getattr(
            settings, "CONTACT_WHATSAPP", f"https://wa.me/98{phone.lstrip('0')}"
        ),
        "CONTACT_ADDRESS": getattr(settings, "CONTACT_ADDRESS", "رباط‌کریم، ایران"),
    }
