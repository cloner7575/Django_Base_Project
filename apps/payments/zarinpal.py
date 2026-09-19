from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from dataclasses import dataclass

from django.conf import settings

logger = logging.getLogger(__name__)


class ZarinpalError(Exception):
    """Gateway request or verify failed."""


@dataclass(frozen=True)
class PaymentRequestResult:
    authority: str
    payment_url: str
    raw: dict[str, object]


@dataclass(frozen=True)
class PaymentVerifyResult:
    ref_id: str
    raw: dict[str, object]


def _base_url() -> str:
    if getattr(settings, "ZARINPAL_SANDBOX", True):
        return "https://sandbox.zarinpal.com"
    return "https://payment.zarinpal.com"


def _merchant_id() -> str:
    merchant = getattr(settings, "ZARINPAL_MERCHANT_ID", "").strip()
    if not merchant:
        raise ZarinpalError("شناسه درگاه تنظیم نشده است.")
    return merchant


def _post_json(path: str, payload: dict[str, object]) -> dict[str, object]:
    url = f"{_base_url()}{path}"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        logger.exception("Zarinpal HTTP error: %s", body)
        raise ZarinpalError("خطا در ارتباط با درگاه پرداخت.") from exc
    except urllib.error.URLError as exc:
        logger.exception("Zarinpal connection error")
        raise ZarinpalError("درگاه پرداخت در دسترس نیست.") from exc

    try:
        parsed: dict[str, object] = json.loads(body)
    except json.JSONDecodeError as exc:
        logger.exception("Zarinpal invalid JSON: %s", body)
        raise ZarinpalError("پاسخ نامعتبر از درگاه پرداخت.") from exc
    return parsed


def request_payment(
    *, amount: int, description: str, callback_url: str
) -> PaymentRequestResult:
    payload = {
        "merchant_id": _merchant_id(),
        "amount": amount,
        "callback_url": callback_url,
        "description": description,
    }
    raw = _post_json("/pg/v4/payment/request.json", payload)
    data = raw.get("data") or {}
    errors = raw.get("errors")
    if not isinstance(data, dict):
        raise ZarinpalError("درخواست پرداخت ناموفق بود.")
    code = data.get("code")
    authority = data.get("authority")
    if code != 100 or not authority:
        logger.error("Zarinpal request failed: %s errors=%s", raw, errors)
        raise ZarinpalError("درخواست پرداخت ناموفق بود.")
    payment_url = f"{_base_url()}/pg/StartPay/{authority}"
    return PaymentRequestResult(
        authority=str(authority), payment_url=payment_url, raw=raw
    )


def verify_payment(*, amount: int, authority: str) -> PaymentVerifyResult:
    payload = {
        "merchant_id": _merchant_id(),
        "amount": amount,
        "authority": authority,
    }
    raw = _post_json("/pg/v4/payment/verify.json", payload)
    data = raw.get("data") or {}
    if not isinstance(data, dict):
        raise ZarinpalError("تأیید پرداخت ناموفق بود.")
    code = data.get("code")
    if code not in (100, 101):
        logger.error("Zarinpal verify failed: %s", raw)
        raise ZarinpalError("تأیید پرداخت ناموفق بود.")
    ref_id = str(data.get("ref_id") or "")
    return PaymentVerifyResult(ref_id=ref_id, raw=raw)
