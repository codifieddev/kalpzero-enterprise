from fastapi import APIRouter, Depends, HTTPException, status

from app.core.authz import require_permission
from app.core.security import SessionContext
from app.schemas.requests import SendWhatsAppCodeRequest
from app.services.errors import ValidationError
from app.services.messaging import build_whatsapp_manual_send_payload

router = APIRouter()


@router.post("/whatsapp/manual-send", status_code=status.HTTP_200_OK)
def whatsapp_manual_send(
    payload: SendWhatsAppCodeRequest,
    _: SessionContext = Depends(require_permission("messaging.whatsapp.compose")),
):
    try:
        return build_whatsapp_manual_send_payload(
            code=payload.code,
            sender_mobile_number=payload.sender_mobile_number,
            receiver_mobile_number=payload.receiver_mobile_number,
        )
    except ValidationError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc
