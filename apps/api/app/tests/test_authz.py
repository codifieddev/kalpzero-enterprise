import pytest
from fastapi import HTTPException

from app.core.authz import assert_permission_granted


def test_permission_registry_denies_unknown_permission() -> None:
    with pytest.raises(HTTPException) as exc_info:
        assert_permission_granted("unknown.permission", ["platform_admin"])

    assert exc_info.value.status_code == 403


def test_permission_registry_denies_missing_role_grant() -> None:
    with pytest.raises(HTTPException) as exc_info:
        assert_permission_granted("ai.runtime.read", ["operations_manager"])

    assert exc_info.value.status_code == 403


def test_permission_registry_allows_granted_operation() -> None:
    assert_permission_granted("commerce.catalog.read", ["tenant_admin"])
