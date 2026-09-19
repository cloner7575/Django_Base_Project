from django.conf import settings
from django.http import HttpRequest


def site(request: HttpRequest) -> dict[str, str]:
    return {"SITE_NAME": getattr(settings, "SITE_NAME", "Core")}
