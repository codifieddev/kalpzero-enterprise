import pytest

from app.core.config import Settings


def test_settings_reject_short_jwt_secret() -> None:
    with pytest.raises(ValueError):
        Settings(
            jwt_secret="short-secret",
            encryption_key="x" * 32,
            control_database_url="sqlite:///./kalpzero-enterprise-test.db",
            runtime_mongo_url="mongodb://localhost:27017/test",
            runtime_mongo_db="kalpzero_runtime_test",
            ai_mongo_db="kalpzero_ai_test",
            ops_redis_url="redis://localhost:6379/0",
            public_web_url="http://localhost:3000",
            public_api_url="http://localhost:8000",
        )


def test_settings_accept_strong_secrets() -> None:
    settings = Settings(
        jwt_secret="test-secret-value-with-32-characters!!",
        encryption_key="test-encryption-key-with-32-chars!",
        control_database_url="sqlite:///./kalpzero-enterprise-test.db",
        runtime_mongo_url="mongodb://localhost:27017/test",
        runtime_mongo_db="kalpzero_runtime_test",
        ai_mongo_db="kalpzero_ai_test",
        ops_redis_url="redis://localhost:6379/0",
        public_web_url="http://localhost:3000",
        public_api_url="http://localhost:8000",
    )

    assert settings.jwt_secret.startswith("test-secret")
    assert settings.database_url.startswith("sqlite")
