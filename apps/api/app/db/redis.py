from functools import lru_cache

from redis import Redis

from app.core.config import Settings

OPS_CHANNELS = {
    "imports": "kz.imports",
    "publishing": "kz.publishing",
    "notifications": "kz.notifications",
    "rate_limits": "kz.rate_limits",
    "audit_outbox": "kz.audit.outbox",
}


@lru_cache
def get_redis_client(redis_url: str) -> Redis:
    return Redis.from_url(redis_url, decode_responses=True)


def describe_ops_store(settings: Settings) -> dict[str, object]:
    return {
        "kind": "redis",
        "driver": "redis",
        "configured": bool(settings.ops_redis_url),
        "channels": OPS_CHANNELS,
    }


def clear_redis_cache() -> None:
    get_redis_client.cache_clear()
