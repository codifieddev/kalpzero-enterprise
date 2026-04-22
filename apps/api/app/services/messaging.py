import re
from urllib.parse import quote

from app.services.errors import ValidationError

_E164_MOBILE_PATTERN = re.compile(r"^\+[1-9]\d{7,14}$")
_SIX_DIGIT_CODE_PATTERN = re.compile(r"^\d{6}$")


def _normalize_mobile_number(value: str, *, field_name: str) -> str:
    normalized = re.sub(r"[\s().-]", "", value.strip())
    if normalized.startswith("00"):
        normalized = f"+{normalized[2:]}"
    if not _E164_MOBILE_PATTERN.fullmatch(normalized):
        raise ValidationError(f"{field_name} must use E.164 format, for example +919876543210.")
    return normalized


def _render_message(*, code: str) -> str:
    return f"{code} is your Kalp verification code."


def build_whatsapp_manual_send_payload(
    *,
    code: str,
    sender_mobile_number: str,
    receiver_mobile_number: str,
) -> dict[str, object]:
    if not _SIX_DIGIT_CODE_PATTERN.fullmatch(code):
        raise ValidationError("code must be a six-digit string.")

    normalized_sender = _normalize_mobile_number(sender_mobile_number, field_name="sender_mobile_number")
    normalized_receiver = _normalize_mobile_number(receiver_mobile_number, field_name="receiver_mobile_number")
    if normalized_sender == normalized_receiver:
        raise ValidationError("receiver_mobile_number must be different from sender_mobile_number.")

    message = _render_message(code=code)
    receiver_digits = normalized_receiver[1:]
    encoded_message = quote(message, safe="")

    return {
        "accepted": True,
        "channel": "whatsapp",
        "delivery_mode": "manual_send",
        "sender_mobile_number": normalized_sender,
        "receiver_mobile_number": normalized_receiver,
        "message": message,
        "whatsapp_url": f"https://wa.me/{receiver_digits}?text={encoded_message}",
        "whatsapp_app_url": f"whatsapp://send?phone={normalized_receiver}&text={encoded_message}",
        "manual_action_required": True,
        "instructions": "Open one of the WhatsApp links from the sender device and tap Send.",
    }
