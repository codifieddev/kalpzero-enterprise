from typing import Any
from app.repositories import themerepo

async def get_theme(db_name: str) -> list[dict[str, Any]]:
    return await themerepo.get_theme(db_name)


async def update_theme(db_name: str, id: str, data: dict[str, Any]) -> dict[str, Any] | None:
    return await themerepo.update_theme(db_name, id, data)
