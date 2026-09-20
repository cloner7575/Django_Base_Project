from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.models import TimeStampedModel


class ContactMessage(TimeStampedModel):
    """Inbound message from the public contact form."""

    name = models.CharField(_("name"), max_length=120)
    email = models.EmailField(_("email"))
    message = models.TextField(_("message"), max_length=5000)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("contact message")
        verbose_name_plural = _("contact messages")

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"
