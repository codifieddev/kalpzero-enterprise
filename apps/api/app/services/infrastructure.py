from urllib.parse import urlparse

from app.core.config import Settings
from app.db.mongo import describe_runtime_document_store
from app.db.redis import describe_ops_store


def _driver_label(url: str) -> str:
    parsed = urlparse(url)
    if "+" in parsed.scheme:
        return parsed.scheme.split("+", maxsplit=1)[0]
    return parsed.scheme


def get_storage_topology(settings: Settings) -> dict[str, object]:
    return {
        "control_plane": {
            "kind": "sql",
            "driver": _driver_label(settings.control_database_url),
            "purpose": [
                "agencies",
                "tenants",
                "auth",
                "rbac",
                "audit",
                "outbox",
                "transactional domains",
            ],
        },
        "runtime_documents": describe_runtime_document_store(settings),
        "ops_cache_queue": describe_ops_store(settings),
    }
