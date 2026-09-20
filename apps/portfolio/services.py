import logging

from django.db import transaction

from apps.portfolio.models import ContactMessage

logger = logging.getLogger(__name__)


@transaction.atomic
def create_contact_message(*, name: str, email: str, message: str) -> ContactMessage:
    """Persist a validated contact submission."""
    contact = ContactMessage.objects.create(
        name=name.strip(),
        email=email.strip().lower(),
        message=message.strip(),
    )
    logger.info(
        "contact_message_created",
        extra={"contact_id": contact.pk, "email": contact.email},
    )
    return contact
