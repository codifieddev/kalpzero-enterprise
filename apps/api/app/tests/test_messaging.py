from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.tests._direct import ensure_project_python, run_current_test_file

ensure_project_python(__file__, is_main=__name__ == "__main__")

import pytest
from fastapi.testclient import TestClient

from app.tests.support import login


def test_whatsapp_send_requires_authentication(client: TestClient) -> None:
    response = client.post(
        "/messaging/whatsapp/manual-send",
        json={
            "code": "123456",
            "sender_mobile_number": "+919999999999",
            "receiver_mobile_number": "+919888888888",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Authentication required."


def test_whatsapp_send_rejects_matching_sender_and_receiver(
    client: TestClient,
) -> None:
    token = login(client, email="founder@kalpzero.com")

    response = client.post(
        "/messaging/whatsapp/manual-send",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "code": "123456",
            "sender_mobile_number": "+919777777777",
            "receiver_mobile_number": "+919777777777",
        },
    )

    assert response.status_code == 400
    assert "must be different" in response.json()["detail"]


def test_whatsapp_send_rejects_invalid_receiver_mobile_number(
    client: TestClient,
) -> None:
    token = login(client, email="founder@kalpzero.com")

    response = client.post(
        "/messaging/whatsapp/manual-send",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "code": "123456",
            "sender_mobile_number": "+919999999999",
            "receiver_mobile_number": "919876543210",
        },
    )

    assert response.status_code == 400
    assert "receiver_mobile_number must use E.164 format" in response.json()["detail"]


def test_whatsapp_send_returns_manual_send_links(
    client: TestClient,
) -> None:
    token = login(client, email="founder@kalpzero.com")

    response = client.post(
        "/messaging/whatsapp/manual-send",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "code": "123456",
            "sender_mobile_number": "+919999999999",
            "receiver_mobile_number": "+919888888888",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "accepted": True,
        "channel": "whatsapp",
        "delivery_mode": "manual_send",
        "sender_mobile_number": "+919999999999",
        "receiver_mobile_number": "+919888888888",
        "message": "123456 is your Kalp verification code.",
        "whatsapp_url": "https://wa.me/919888888888?text=123456%20is%20your%20Kalp%20verification%20code.",
        "whatsapp_app_url": "whatsapp://send?phone=+919888888888&text=123456%20is%20your%20Kalp%20verification%20code.",
        "manual_action_required": True,
        "instructions": "Open one of the WhatsApp links from the sender device and tap Send.",
    }


if __name__ == "__main__":
    raise SystemExit(run_current_test_file(__file__))
