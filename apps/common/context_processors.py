from django.conf import settings
from django.http import HttpRequest
from django.utils.translation import get_language

from apps.portfolio.content import EMAIL, GITHUB_URL, LINKEDIN_URL, resume_url

_RTL_LANGS = frozenset({"ar", "fa", "he", "ur"})


def site(request: HttpRequest) -> dict[str, str]:
    """Expose site identity, direction, and public contact links."""
    lang = (get_language() or settings.LANGUAGE_CODE).split("-", maxsplit=1)[0]
    direction = "rtl" if lang.lower() in _RTL_LANGS else "ltr"
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "Core"),
        "TEXT_DIRECTION": direction,
        "github_url": GITHUB_URL,
        "linkedin_url": LINKEDIN_URL,
        "contact_email": EMAIL,
        "resume_url": resume_url(),
    }
