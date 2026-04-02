from fastapi.testclient import TestClient

from app.tests.support import login, provision_tenant


def test_travel_pack_supports_packages_departures_and_leads(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="travel_ops", vertical_packs=["travel"], bypass_onboarding_gate=True)
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="travel_ops")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    package_response = client.post(
        "/travel/packages",
        headers=headers,
        json={
            "code": "GOA-ESC-01",
            "slug": "goa-escape",
            "title": "Goa Escape",
            "summary": "Beach escape with curated stays and activities.",
            "origin_city": "Delhi",
            "destination_city": "Goa",
            "destination_country": "India",
            "duration_days": 4,
            "base_price_minor": 4599000,
            "currency": "INR",
            "status": "active",
            "itinerary_days": [
                {
                    "day_number": 1,
                    "title": "Arrival and transfer",
                    "summary": "Arrival in Goa, hotel check-in, and sunset leisure.",
                    "hotel_ref_id": "hotel_goa_01",
                    "activity_ref_ids": [],
                    "transfer_ref_ids": ["transfer_airport_hotel"],
                },
                {
                    "day_number": 2,
                    "title": "North Goa exploration",
                    "summary": "Guided sightseeing with beach and fort visits.",
                    "hotel_ref_id": "hotel_goa_01",
                    "activity_ref_ids": ["activity_beach_hop", "activity_fort_visit"],
                    "transfer_ref_ids": ["transfer_sightseeing"],
                },
            ],
        },
    )
    assert package_response.status_code == 201
    package_id = package_response.json()["id"]
    assert len(package_response.json()["itinerary_days"]) == 2

    departure_response = client.post(
        "/travel/departures",
        headers=headers,
        json={
            "package_id": package_id,
            "departure_date": "2026-05-10",
            "return_date": "2026-05-13",
            "seats_total": 24,
            "seats_available": 24,
            "price_override_minor": 4899000,
            "status": "scheduled",
        },
    )
    assert departure_response.status_code == 201
    departure_id = departure_response.json()["id"]
    assert departure_response.json()["status"] == "scheduled"

    lead_response = client.post(
        "/travel/leads",
        headers=headers,
        json={
            "source": "instagram",
            "interested_package_id": package_id,
            "departure_id": departure_id,
            "customer_id": "cust_travel_001",
            "contact_name": "Naina Sharma",
            "contact_phone": "+919999999999",
            "travelers_count": 2,
            "desired_departure_date": "2026-05-10",
            "budget_minor": 5000000,
            "currency": "INR",
            "status": "new",
            "notes": "Interested in premium room upgrade.",
        },
    )
    assert lead_response.status_code == 201
    lead_id = lead_response.json()["id"]
    assert lead_response.json()["status"] == "new"

    qualify_response = client.patch(
        f"/travel/leads/{lead_id}/status",
        headers=headers,
        json={"status": "qualified"},
    )
    assert qualify_response.status_code == 200
    assert qualify_response.json()["status"] == "qualified"

    close_departure = client.patch(
        f"/travel/departures/{departure_id}/status",
        headers=headers,
        json={"status": "closed"},
    )
    assert close_departure.status_code == 200
    assert close_departure.json()["status"] == "closed"

    packages_response = client.get("/travel/packages", headers=headers)
    departures_response = client.get("/travel/departures", headers=headers)
    leads_response = client.get("/travel/leads", headers=headers)
    overview_response = client.get("/travel/overview", headers=headers)
    adapter_response = client.get("/travel/legacy/plan", headers=headers)
    outbox_response = client.get("/platform/outbox", headers=headers)

    assert packages_response.status_code == 200
    assert departures_response.status_code == 200
    assert leads_response.status_code == 200
    assert overview_response.status_code == 200
    assert adapter_response.status_code == 200
    assert outbox_response.status_code == 200
    assert overview_response.json()["packages"] == 1
    assert overview_response.json()["departures"]["closed"] == 1
    assert overview_response.json()["lead_pipeline"]["qualified"] == 1
    assert adapter_response.json()["adapter_id"] == "legacy-kalpzero-travel"
    assert any(event["event_name"] == "travel.lead.updated" for event in outbox_response.json()["events"])
