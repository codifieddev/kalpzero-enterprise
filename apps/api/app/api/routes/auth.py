from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.config import Settings, get_settings
from app.core.security import SessionContext, create_access_token, get_current_session
from app.db.session import get_db_session
from sqlalchemy import select
from app.db.models import TenantModel, UserModel
from app.schemas.requests import CreateCustomerRequest, LoginCustomerRequest, LoginRequest, MagicLoginRequest, RegisterRequest
from app.schemas.responses import LoginResponse, RegisterResponse, SessionResponse
from app.services.auth import (
    authenticate_customer,
    authenticate_user,
    create_customer,
    create_user,
)

router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(
    payload: RegisterRequest,
    response: Response,
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> RegisterResponse:
    user = create_user(db, payload)

    expires_at = datetime.now(tz=UTC) + timedelta(hours=8)

    token = create_access_token(
        id=user.id,
        email=user.email,
        tenant_id=user.tenant_id or "platform_control",
        role=user.role,
        settings=settings,
    )

    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1440 * 60,
        path="/",
    )

    return RegisterResponse(
        access_token=token,
        expires_at=expires_at.isoformat(),
        session={
            "email": user.email,
            "tenant_id": user.tenant_id or "platform_control",
            "role": user.role,
            "name": user.name,
            "isTenantOwner": user.istenantowner,
        },
    )


@router.post("/login", response_model=LoginResponse)
def login(
    response: Response,
    payload: LoginRequest,
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> LoginResponse:
    user = authenticate_user(db, payload.email, payload.password)
    print("user---", user)
    expires_at = datetime.now(tz=UTC) + timedelta(hours=8)
    token = create_access_token(
        id=user.id,
        email=user.email,
        tenant_id=user.tenant_id or "platform_control",
        role=user.role,
        settings=settings,
    )


    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1440 * 60,
        path="/",
    )

    return LoginResponse(
        access_token=token,
        expires_at=expires_at.isoformat(),
        session={
            "email": user.email,
            "tenant_id": user.tenant_id or "platform_control",
            "role": user.role,
            "name": user.name,
            "isTenantOwner": user.istenantowner,
        },
    )


@router.get("/me", response_model=SessionResponse)
def me(session: SessionContext = Depends(get_current_session)) -> SessionResponse:
    user = db.scalar(select(UserModel).where(UserModel.id == session.id))
    return SessionResponse(
        email=session.email,
        tenant_id=session.tenant_id,
        role=session.role,
        name=user.name,
        isTenantOwner=user.isTenantOwner,
    )


@router.post("/register/customer", response_model=RegisterResponse)
def register_customer(
    payload: CreateCustomerRequest,
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> RegisterResponse:

    customer = create_customer(db, payload)

    expires_at = datetime.now(tz=UTC) + timedelta(hours=8)
    token = create_access_token(
        user_id=customer.email,
        tenant_id=payload.tenant_slug,
        role=customer.role,
        settings=settings,
    )

    return RegisterResponse(
        access_token=token,
        expires_at=expires_at.isoformat(),
        session={
            "user_id": customer.email,
            "tenant_id": payload.tenant_slug,
            "role": customer.role,
        },
    )


@router.post("/login/customer", response_model=LoginResponse)
def login_customer(
    payload: LoginCustomerRequest,
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> LoginResponse:
    customer = authenticate_customer(
        db,
        tenant_slug=payload.tenant_slug,
        email=payload.email,
        password=payload.password,
    )

    expires_at = datetime.now(tz=UTC) + timedelta(hours=8)
    token = create_access_token(
        user_id=customer.email,
        tenant_id=payload.tenant_slug,
        role=customer.role,
        settings=settings,
    )

    return LoginResponse(
        access_token=token,
        expires_at=expires_at.isoformat(),
        session={
            "user_id": customer.email,
            "tenant_id": payload.tenant_slug,
            "role": customer.role,
        },
    )

@router.get("/magic/options")
def get_magic_options(
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
):
    if settings.env not in ["development", "testing"]:
        return {"users": []}

    # Fetch a few representative users
    users = db.scalars(
        select(UserModel)
        .where(UserModel.role.in_(["platform_admin", "tenant_admin"]))
        .limit(10)
    ).all()

    options = []
    for user in users:
        tenant_slug = None
        if user.tenant_id:
            tenant = db.get(TenantModel, user.tenant_id)
            tenant_slug = tenant.slug if tenant else None
        
        options.append({
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "name": user.name or user.email.split("@")[0].capitalize(),
            "tenant_slug": tenant_slug
        })

    return {"users": options}


@router.post("/magic/login", response_model=LoginResponse)
def magic_login(
    payload: MagicLoginRequest,
    response: Response,
    db: Session = Depends(get_db_session),
    settings: Settings = Depends(get_settings),
) -> LoginResponse:
    if settings.env not in ["development", "testing"]:
        raise HTTPException(status_code=403, detail="Magic login disabled in this environment")

    user = db.get(UserModel, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    expires_at = datetime.now(tz=UTC) + timedelta(hours=8)
    token = create_access_token(
        id=user.id,
        email=user.email,
        tenant_id=user.tenant_id or "platform_control",
        role=user.role,
        settings=settings,
    )

    response.set_cookie(
        key="auth_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=1440 * 60,
        path="/",
    )

    return LoginResponse(
        access_token=token,
        expires_at=expires_at.isoformat(),
        session={
            "email": user.email,
            "tenant_id": user.tenant_id or "platform_control",
            "role": user.role,
            "name": user.name,
            "isTenantOwner": user.istenantowner,
        },
    )
