from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.tests._direct import ensure_project_python, run_current_test_file

ensure_project_python(__file__, is_main=__name__ == "__main__")

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


if __name__ == "__main__":
    raise SystemExit(run_current_test_file(__file__))
