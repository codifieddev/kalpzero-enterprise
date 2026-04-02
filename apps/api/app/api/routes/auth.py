from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.core.security import SessionContext, create_access_token, get_current_session
from app.schemas.requests import LoginRequest
from app.schemas.responses import LoginResponse, SessionResponse

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, settings: Settings = Depends(get_settings)) -> LoginResponse:
    roles = ["tenant_admin"]
    tenant_id = payload.tenant_slug or "tenant_demo"
    if payload.email.endswith("@kalpzero.com"):
        roles = ["platform_admin"]
        tenant_id = payload.tenant_slug or "platform_control"

    expires_at = datetime.now(tz=UTC) + timedelta(hours=8)
    token = create_access_token(
        user_id=payload.email,
        tenant_id=tenant_id,
        roles=roles,
        settings=settings,
    )
    return LoginResponse(
        access_token=token,
        expires_at=expires_at.isoformat(),
        session={
            "user_id": payload.email,
            "tenant_id": tenant_id,
            "roles": roles,
        },
    )


@router.get("/me", response_model=SessionResponse)
def me(session: SessionContext = Depends(get_current_session)) -> SessionResponse:
    return SessionResponse(
        user_id=session.user_id,
        tenant_id=session.tenant_id,
        roles=session.roles,
    )
