from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.authz import require_permission
from app.core.security import SessionContext
from app.db.session import get_db_session
from app.services.bootstrap import get_ai_runtime

router = APIRouter()


@router.get("/runtime")
def ai_runtime(
    session: SessionContext = Depends(require_permission("ai.runtime.read")),
    db: Session = Depends(get_db_session),
):
    return get_ai_runtime(db, session.tenant_id)
