from datetime import UTC, datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from app.core.config import Settings, get_settings

http_bearer = HTTPBearer(auto_error=False)
ALGORITHM = "HS256"


class TokenPayload(BaseModel):
    sub: str
    tenant_id: str
    roles: list[str]
    exp: int


class SessionContext(BaseModel):
    user_id: str
    tenant_id: str
    roles: list[str]


def create_access_token(
    *,
    user_id: str,
    tenant_id: str,
    roles: list[str],
    settings: Settings,
    expires_delta: timedelta = timedelta(hours=8),
) -> str:
    expire_at = datetime.now(tz=UTC) + expires_delta
    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "roles": roles,
        "exp": int(expire_at.timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=ALGORITHM)


def decode_access_token(token: str, settings: Settings) -> TokenPayload:
    try:
        raw_payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        ) from exc

    return TokenPayload(**raw_payload)


def get_current_session(
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
    settings: Settings = Depends(get_settings),
) -> SessionContext:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token required.",
        )

    payload = decode_access_token(credentials.credentials, settings)
    return SessionContext(user_id=payload.sub, tenant_id=payload.tenant_id, roles=payload.roles)
