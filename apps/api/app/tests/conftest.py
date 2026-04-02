import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.mongo import clear_mongo_cache
from app.db.redis import clear_redis_cache
from app.db.session import clear_db_caches


def _set_default_env(db_path: Path) -> None:
    os.environ["KALPZERO_ENV"] = "test"
    os.environ["KALPZERO_APP_NAME"] = "KalpZero Enterprise API Test"
    os.environ["KALPZERO_REGION"] = "in"
    os.environ["KALPZERO_JWT_SECRET"] = "test-secret-value-with-32-characters!!"
    os.environ["KALPZERO_ENCRYPTION_KEY"] = "test-encryption-key-with-32-chars!"
    os.environ["KALPZERO_CONTROL_DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["KALPZERO_RUNTIME_MONGO_URL"] = "mongodb://localhost:27017/test"
    os.environ["KALPZERO_RUNTIME_DOC_STORE_MODE"] = "memory"
    os.environ["KALPZERO_RUNTIME_MONGO_DB"] = "kalpzero_runtime_test"
    os.environ["KALPZERO_AI_MONGO_DB"] = "kalpzero_ai_test"
    os.environ["KALPZERO_OPS_REDIS_URL"] = "redis://localhost:6379/0"
    os.environ["KALPZERO_PUBLIC_WEB_URL"] = "http://localhost:3000"
    os.environ["KALPZERO_PUBLIC_API_URL"] = "http://localhost:8000"


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    db_path = tmp_path / "kalpzero-enterprise-test.db"
    _set_default_env(db_path)
    get_settings.cache_clear()
    clear_db_caches()
    clear_mongo_cache()
    clear_redis_cache()
    from app.main import create_app

    with TestClient(create_app()) as test_client:
        yield test_client

    get_settings.cache_clear()
    clear_db_caches()
    clear_mongo_cache()
    clear_redis_cache()
