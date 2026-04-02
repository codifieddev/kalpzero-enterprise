from sqlalchemy.orm import Session

from app.services.errors import NotFoundError
from app.services.platform import get_tenant_or_raise


def _tenant_exists(db: Session, tenant_id: str) -> bool:
    try:
        get_tenant_or_raise(db, tenant_slug=tenant_id)
        return True
    except NotFoundError:
        return False


def get_travel_overview(db: Session, tenant_id: str) -> dict[str, object]:
    return {
        "tenant_id": tenant_id,
        "tenant_exists": _tenant_exists(db, tenant_id),
        "package_count": 42,
        "scheduled_departures": 19,
        "lead_pipeline": {
            "new": 15,
            "qualified": 7,
            "proposal_sent": 3,
        },
    }


def get_publishing_overview(db: Session, tenant_id: str) -> dict[str, object]:
    return {
        "tenant_id": tenant_id,
        "tenant_exists": _tenant_exists(db, tenant_id),
        "domains": 2,
        "draft_pages": 11,
        "live_pages": 37,
        "seo_indexing_state": "ready",
    }


def get_ai_runtime(db: Session, tenant_id: str) -> dict[str, object]:
    return {
        "tenant_id": tenant_id,
        "tenant_exists": _tenant_exists(db, tenant_id),
        "provider": "openai",
        "policy": {
            "requires_human_approval": True,
            "pii_redaction_enabled": True,
            "usage_metering": "enabled",
        },
        "allowed_purposes": ["assistant", "knowledge_ingestion"],
    }
