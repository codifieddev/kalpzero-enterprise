import json
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


def _redact_headers(headers: dict[str, object] | None) -> dict[str, object]:
    if not headers:
        return {}

    redacted: dict[str, object] = {}
    for key, value in headers.items():
        if key.lower() == "authorization" and isinstance(value, str) and len(value) > 20:
            redacted[key] = f"{value[:16]}..."
        else:
            redacted[key] = value
    return redacted


def _attach_verbose_http_logging(test_client: TestClient) -> None:
    if os.environ.get("KALPZERO_TEST_VERBOSE_HTTP") != "1":
        return

    original_request = test_client.request

    def verbose_request(method: str, url: str, *args, **kwargs):
        print(f"\n>>> {method.upper()} {url}")
        if kwargs.get("params"):
            print("params:", json.dumps(kwargs["params"], indent=2, default=str))
        if kwargs.get("headers"):
            print("headers:", json.dumps(_redact_headers(kwargs["headers"]), indent=2, default=str))
        if "json" in kwargs and kwargs["json"] is not None:
            print("json:", json.dumps(kwargs["json"], indent=2, default=str))

        response = original_request(method, url, *args, **kwargs)

        print(f"<<< {response.status_code} {url}")
        content_type = response.headers.get("content-type", "")
        if "application/json" in content_type:
            try:
                print(json.dumps(response.json(), indent=2, default=str))
            except ValueError:
                print(response.text)
        else:
            body = response.text
            if len(body) > 1200:
                body = f"{body[:1200]}... [truncated]"
            print(body)

        return response

    test_client.request = verbose_request  # type: ignore[method-assign]


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
        _attach_verbose_http_logging(test_client)
        yield test_client

    get_settings.cache_clear()
    clear_db_caches()
    clear_mongo_cache()
    clear_redis_cache()
