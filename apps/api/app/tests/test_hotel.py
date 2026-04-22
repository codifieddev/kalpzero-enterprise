from pathlib import Path
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.tests._direct import ensure_project_python, run_current_test_file

ensure_project_python(__file__, is_main=__name__ == "__main__")

from fastapi.testclient import TestClient

from app.tests.support import login, provision_tenant


def test_hotel_pack_supports_canonical_pms_flow(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_ops", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_ops")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Residency",
            "code": "KZR-IN-001",
            "city": "Jaipur",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    room_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Deluxe King",
            "code": "DLX-K",
            "occupancy": 2,
            "base_rate_minor": 950000,
            "currency": "INR",
        },
    )
    assert room_type_response.status_code == 201
    room_type_id = room_type_response.json()["id"]

    room_response = client.post(
        "/hotel/rooms",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_number": "201",
            "status": "available",
            "floor_label": "2",
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    reservation_response = client.post(
        "/hotel/reservations",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_id": room_id,
            "guest_customer_id": "cust_001",
            "guest_name": "Arjun Mehta",
            "check_in_date": "2026-04-10",
            "check_out_date": "2026-04-12",
            "total_amount_minor": 1900000,
            "currency": "INR",
            "adults": 2,
            "children": 0,
        },
    )
    assert reservation_response.status_code == 201
    reservation_id = reservation_response.json()["id"]
    assert reservation_response.json()["status"] == "reserved"

    conflict_response = client.post(
        "/hotel/reservations",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_id": room_id,
            "guest_customer_id": "cust_002",
            "guest_name": "Conflicting Guest",
            "check_in_date": "2026-04-11",
            "check_out_date": "2026-04-13",
            "total_amount_minor": 1900000,
            "currency": "INR",
            "adults": 2,
            "children": 0,
        },
    )
    assert conflict_response.status_code == 409

    check_in_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_in"},
    )
    assert check_in_response.status_code == 200
    assert check_in_response.json()["status"] == "checked_in"

    check_out_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_out"},
    )
    assert check_out_response.status_code == 200
    assert check_out_response.json()["status"] == "checked_out"

    housekeeping_response = client.get("/hotel/housekeeping/tasks", headers=headers)
    assert housekeeping_response.status_code == 200
    assert len(housekeeping_response.json()["tasks"]) == 1
    task_id = housekeeping_response.json()["tasks"][0]["id"]
    assert housekeeping_response.json()["tasks"][0]["status"] == "pending"

    room_dirty_response = client.get("/hotel/rooms", headers=headers)
    assert room_dirty_response.status_code == 200
    assert room_dirty_response.json()["rooms"][0]["status"] == "dirty"

    complete_housekeeping = client.patch(
        f"/hotel/housekeeping/tasks/{task_id}/status",
        headers=headers,
        json={"status": "completed"},
    )
    assert complete_housekeeping.status_code == 200
    assert complete_housekeeping.json()["status"] == "completed"

    maintenance_create = client.post(
        "/hotel/maintenance/tickets",
        headers=headers,
        json={
            "property_id": property_id,
            "room_id": room_id,
            "title": "Air conditioner service",
            "description": "Cooling issue after guest checkout.",
            "priority": "high",
        },
    )
    assert maintenance_create.status_code == 201
    ticket_id = maintenance_create.json()["id"]

    maintenance_resolve = client.patch(
        f"/hotel/maintenance/tickets/{ticket_id}/status",
        headers=headers,
        json={"status": "resolved"},
    )
    assert maintenance_resolve.status_code == 200
    assert maintenance_resolve.json()["status"] == "resolved"

    rooms_response = client.get("/hotel/rooms", headers=headers)
    overview_response = client.get("/hotel/overview", headers=headers)
    inventory_response = client.get("/hotel/inventory/summary", headers=headers)

    assert rooms_response.status_code == 200
    assert rooms_response.json()["rooms"][0]["status"] == "available"
    assert overview_response.status_code == 200
    assert overview_response.json()["properties"] == 1
    assert overview_response.json()["room_statuses"]["available"] == 1
    assert overview_response.json()["reservations"]["checked_out"] == 1
    assert overview_response.json()["housekeeping"]["completed"] == 1
    assert overview_response.json()["maintenance"]["resolved"] == 1
    assert inventory_response.status_code == 200
    assert inventory_response.json()["items"][0]["available_units"] == 1


def test_hotel_pack_supports_meal_plans_guest_profiles_and_late_room_assignment(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_extended", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_extended")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Suites",
            "code": "KZS-IN-001",
            "city": "Goa",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    room_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Executive Suite",
            "code": "EX-S",
            "category": "Suite",
            "bed_type": "King",
            "occupancy": 3,
            "room_size_sqm": 65,
            "base_rate_minor": 1850000,
            "extra_bed_price_minor": 250000,
            "refundable": True,
            "currency": "INR",
            "amenity_ids": ["wifi", "bathtub", "work_desk"],
        },
    )
    assert room_type_response.status_code == 201
    room_type_id = room_type_response.json()["id"]
    assert room_type_response.json()["category"] == "Suite"

    room_response = client.post(
        "/hotel/rooms",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_number": "701",
            "status": "available",
            "feature_tags": ["corner", "sea_view"],
            "notes": "VIP floor inventory",
            "floor_label": "7",
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]
    assert room_response.json()["sell_status"] == "sellable"
    assert room_response.json()["occupancy_status"] == "vacant"

    meal_plan_response = client.post(
        "/hotel/meal-plans",
        headers=headers,
        json={
            "property_id": property_id,
            "code": "MAP",
            "name": "Modified American Plan",
            "description": "Breakfast and dinner included.",
            "price_per_person_per_night_minor": 350000,
            "currency": "INR",
            "included_meals": ["Breakfast", "Dinner"],
            "is_active": True,
        },
    )
    assert meal_plan_response.status_code == 201
    meal_plan_id = meal_plan_response.json()["id"]

    guest_response = client.post(
        "/hotel/guests",
        headers=headers,
        json={
            "first_name": "Naina",
            "last_name": "Sharma",
            "email": "naina.sharma@example.com",
            "phone": "+919999999999",
            "nationality": "Indian",
            "loyalty_tier": "Gold",
            "vip": True,
            "preferred_room_type_id": room_type_id,
            "dietary_preference": "Vegetarian",
            "company_name": "KalpZero Ventures",
            "identity_document_number": "ID-998877",
            "notes": "Repeat guest with premium preferences",
        },
    )
    assert guest_response.status_code == 201
    guest_id = guest_response.json()["id"]

    reservation_response = client.post(
        "/hotel/reservations",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "meal_plan_id": meal_plan_id,
            "booking_source": "Website",
            "guest_customer_id": guest_id,
            "check_in_date": "2026-05-20",
            "check_out_date": "2026-05-23",
            "status": "pending",
            "special_requests": "Airport transfer and quiet room",
            "early_check_in": True,
            "late_check_out": False,
            "total_amount_minor": 6600000,
            "currency": "INR",
            "adults": 2,
            "children": 1,
        },
    )
    assert reservation_response.status_code == 201
    reservation_id = reservation_response.json()["id"]
    assert reservation_response.json()["room_id"] is None
    assert reservation_response.json()["guest_name"] == "Naina Sharma"
    assert reservation_response.json()["status"] == "pending"
    assert reservation_response.json()["booking_reference"].startswith("HK-")

    assign_response = client.patch(
        f"/hotel/reservations/{reservation_id}/assign-room",
        headers=headers,
        json={"room_id": room_id},
    )
    assert assign_response.status_code == 200
    assert assign_response.json()["room_id"] == room_id

    reserve_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "reserved"},
    )
    assert reserve_response.status_code == 200
    assert reserve_response.json()["status"] == "reserved"

    check_in_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_in"},
    )
    assert check_in_response.status_code == 200
    assert check_in_response.json()["actual_check_in_at"] is not None

    check_out_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_out"},
    )
    assert check_out_response.status_code == 200
    assert check_out_response.json()["actual_check_out_at"] is not None

    meal_plans_response = client.get("/hotel/meal-plans", headers=headers)
    guests_response = client.get("/hotel/guests", headers=headers)
    reservations_response = client.get("/hotel/reservations", headers=headers)
    rooms_response = client.get("/hotel/rooms", headers=headers)
    overview_response = client.get("/hotel/overview", headers=headers)

    assert meal_plans_response.status_code == 200
    assert guests_response.status_code == 200
    assert reservations_response.status_code == 200
    assert rooms_response.status_code == 200
    assert overview_response.status_code == 200
    assert len(meal_plans_response.json()["meal_plans"]) == 1
    assert len(guests_response.json()["guests"]) == 1
    assert reservations_response.json()["reservations"][0]["meal_plan_id"] == meal_plan_id
    assert rooms_response.json()["rooms"][0]["housekeeping_status"] == "dirty"
    assert overview_response.json()["meal_plans"] == 1
    assert overview_response.json()["guest_profiles"] == 1
    assert overview_response.json()["reservations"]["checked_out"] == 1


def test_hotel_pack_supports_rate_plans_and_availability_rules(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_revenue", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_revenue")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Revenue House",
            "code": "KZR-RM-001",
            "city": "Udaipur",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    room_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Premium Lake View",
            "code": "PRM-LV",
            "category": "Premium",
            "bed_type": "King",
            "occupancy": 2,
            "room_size_sqm": 48,
            "base_rate_minor": 2200000,
            "currency": "INR",
            "amenity_ids": ["wifi", "lake_view"],
        },
    )
    assert room_type_response.status_code == 201
    room_type_id = room_type_response.json()["id"]

    rate_plan_response = client.post(
        "/hotel/rate-plans",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "label": "BAR Flexible",
            "currency": "INR",
            "weekend_enabled": True,
            "weekend_rate_minor": 2450000,
            "seasonal_overrides": [
                {
                    "season_name": "Summer Peak",
                    "start_date": "2026-05-01",
                    "end_date": "2026-06-15",
                    "price_minor": 2750000,
                }
            ],
            "is_active": True,
        },
    )
    assert rate_plan_response.status_code == 201
    assert rate_plan_response.json()["label"] == "BAR Flexible"
    assert rate_plan_response.json()["weekend_enabled"] is True
    assert len(rate_plan_response.json()["seasonal_overrides"]) == 1

    availability_rule_response = client.post(
        "/hotel/availability-rules",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "total_units": 12,
            "available_units_snapshot": 9,
            "minimum_stay_nights": 2,
            "maximum_stay_nights": 10,
            "blackout_dates": ["2026-12-31"],
            "is_active": True,
        },
    )
    assert availability_rule_response.status_code == 201
    assert availability_rule_response.json()["total_units"] == 12
    assert availability_rule_response.json()["minimum_stay_nights"] == 2

    rate_plans_response = client.get("/hotel/rate-plans", headers=headers)
    availability_rules_response = client.get("/hotel/availability-rules", headers=headers)
    overview_response = client.get("/hotel/overview", headers=headers)

    assert rate_plans_response.status_code == 200
    assert availability_rules_response.status_code == 200
    assert overview_response.status_code == 200
    assert len(rate_plans_response.json()["rate_plans"]) == 1
    assert len(availability_rules_response.json()["availability_rules"]) == 1
    assert overview_response.json()["rate_plans"] == 1
    assert overview_response.json()["availability_rules"] == 1

    invalid_rate_plan_response = client.post(
        "/hotel/rate-plans",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "label": "Broken Season",
            "currency": "INR",
            "weekend_enabled": False,
            "seasonal_overrides": [
                {
                    "season_name": "Bad Range",
                    "start_date": "2026-08-10",
                    "end_date": "2026-08-10",
                    "price_minor": 2300000,
                }
            ],
            "is_active": True,
        },
    )
    assert invalid_rate_plan_response.status_code == 409

    invalid_availability_rule_response = client.post(
        "/hotel/availability-rules",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "total_units": 5,
            "available_units_snapshot": 6,
            "minimum_stay_nights": 1,
            "maximum_stay_nights": 5,
            "blackout_dates": [],
            "is_active": True,
        },
    )
    assert invalid_availability_rule_response.status_code == 409


def test_hotel_pack_supports_folio_payment_and_invoice_flow(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_finance", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_finance")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Grand",
            "code": "KZG-IN-001",
            "city": "Mumbai",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    room_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Business King",
            "code": "BUS-K",
            "occupancy": 2,
            "base_rate_minor": 4000000,
            "currency": "INR",
        },
    )
    assert room_type_response.status_code == 201
    room_type_id = room_type_response.json()["id"]

    room_response = client.post(
        "/hotel/rooms",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_number": "504",
            "status": "available",
            "floor_label": "5",
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    reservation_response = client.post(
        "/hotel/reservations",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_id": room_id,
            "guest_customer_id": "cust_fin_001",
            "guest_name": "Rohan Kapoor",
            "check_in_date": "2026-06-10",
            "check_out_date": "2026-06-12",
            "total_amount_minor": 4000000,
            "currency": "INR",
            "adults": 2,
            "children": 0,
        },
    )
    assert reservation_response.status_code == 201
    reservation_id = reservation_response.json()["id"]

    folios_response = client.get(f"/hotel/folios?reservation_id={reservation_id}", headers=headers)
    assert folios_response.status_code == 200
    assert len(folios_response.json()["folios"]) == 1
    folio_id = folios_response.json()["folios"][0]["id"]
    assert folios_response.json()["folios"][0]["total_minor"] == 4000000
    assert folios_response.json()["folios"][0]["balance_minor"] == 4000000

    folio_detail_response = client.get(f"/hotel/folios/{folio_id}", headers=headers)
    assert folio_detail_response.status_code == 200
    assert len(folio_detail_response.json()["charges"]) == 1
    assert folio_detail_response.json()["charges"][0]["category"] == "reservation_base"

    incidentals_response = client.post(
        f"/hotel/folios/{folio_id}/charges",
        headers=headers,
        json={
            "category": "incidental",
            "label": "Mini bar consumption",
            "service_date": "2026-06-11",
            "quantity": 1,
            "unit_amount_minor": 150000,
            "tax_amount_minor": 27000,
            "notes": "Soft drinks and snacks",
        },
    )
    assert incidentals_response.status_code == 201
    assert incidentals_response.json()["subtotal_minor"] == 4150000
    assert incidentals_response.json()["tax_minor"] == 27000
    assert incidentals_response.json()["total_minor"] == 4177000
    assert len(incidentals_response.json()["charges"]) == 2

    first_payment_response = client.post(
        f"/hotel/folios/{folio_id}/payments",
        headers=headers,
        json={
            "amount_minor": 2000000,
            "payment_method": "upi",
            "reference": "UPI-12345",
            "notes": "Advance received at front desk",
        },
    )
    assert first_payment_response.status_code == 201
    assert first_payment_response.json()["paid_minor"] == 2000000
    assert first_payment_response.json()["balance_minor"] == 2177000
    assert len(first_payment_response.json()["payments"]) == 1

    overpayment_response = client.post(
        f"/hotel/folios/{folio_id}/payments",
        headers=headers,
        json={
            "amount_minor": 3000000,
            "payment_method": "card",
        },
    )
    assert overpayment_response.status_code == 409

    second_payment_response = client.post(
        f"/hotel/folios/{folio_id}/payments",
        headers=headers,
        json={
            "amount_minor": 2177000,
            "payment_method": "card",
            "reference": "CARD-8899",
            "notes": "Final settlement",
        },
    )
    assert second_payment_response.status_code == 201
    assert second_payment_response.json()["paid_minor"] == 4177000
    assert second_payment_response.json()["balance_minor"] == 0
    assert len(second_payment_response.json()["payments"]) == 2

    check_in_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_in"},
    )
    assert check_in_response.status_code == 200

    check_out_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_out"},
    )
    assert check_out_response.status_code == 200

    close_folio_response = client.post(f"/hotel/folios/{folio_id}/close", headers=headers)
    assert close_folio_response.status_code == 200
    assert close_folio_response.json()["status"] == "closed"

    issue_invoice_response = client.post(f"/hotel/folios/{folio_id}/issue-invoice", headers=headers)
    assert issue_invoice_response.status_code == 200
    assert issue_invoice_response.json()["status"] == "invoiced"
    assert issue_invoice_response.json()["invoice_number"].startswith("INV-")
    assert issue_invoice_response.json()["invoice_issued_at"] is not None

    overview_response = client.get("/hotel/overview", headers=headers)
    assert overview_response.status_code == 200
    assert overview_response.json()["folios"] == 1
    assert overview_response.json()["payments"] == 2
    assert overview_response.json()["folio_statuses"]["invoiced"] == 1
    assert overview_response.json()["folio_balance_minor"] == 0
    assert overview_response.json()["payments_minor"] == 4177000


def test_hotel_pack_supports_staff_shifts_and_staff_assignment(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_staffing", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_staffing")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Operations Hub",
            "code": "KZO-IN-001",
            "city": "Pune",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    room_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Standard Twin",
            "code": "STD-T",
            "occupancy": 2,
            "base_rate_minor": 1800000,
            "currency": "INR",
        },
    )
    assert room_type_response.status_code == 201
    room_type_id = room_type_response.json()["id"]

    room_response = client.post(
        "/hotel/rooms",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_number": "305",
            "status": "available",
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    hk_staff_response = client.post(
        "/hotel/staff",
        headers=headers,
        json={
            "property_id": property_id,
            "staff_code": "HK-01",
            "first_name": "Asha",
            "last_name": "Patel",
            "role": "Housekeeping Supervisor",
            "department": "Housekeeping",
            "phone": "+919888888888",
            "email": "asha.patel@example.com",
            "employment_status": "active",
            "is_active": True,
        },
    )
    assert hk_staff_response.status_code == 201
    hk_staff_id = hk_staff_response.json()["id"]

    maintenance_staff_response = client.post(
        "/hotel/staff",
        headers=headers,
        json={
            "property_id": property_id,
            "staff_code": "ENG-01",
            "first_name": "Vikram",
            "last_name": "Rao",
            "role": "Maintenance Engineer",
            "department": "Engineering",
            "phone": "+919777777777",
            "email": "vikram.rao@example.com",
            "employment_status": "active",
            "is_active": True,
        },
    )
    assert maintenance_staff_response.status_code == 201
    maintenance_staff_id = maintenance_staff_response.json()["id"]

    shift_response = client.post(
        "/hotel/shifts",
        headers=headers,
        json={
            "property_id": property_id,
            "staff_member_id": hk_staff_id,
            "shift_date": "2026-07-10",
            "shift_kind": "morning",
            "start_time": "08:00",
            "end_time": "16:00",
            "status": "scheduled",
            "notes": "Standard housekeeping coverage",
        },
    )
    assert shift_response.status_code == 201
    assert shift_response.json()["staff_member_id"] == hk_staff_id

    housekeeping_response = client.post(
        "/hotel/housekeeping/tasks",
        headers=headers,
        json={
            "property_id": property_id,
            "room_id": room_id,
            "priority": "high",
            "notes": "Rush clean before VIP arrival",
            "assigned_staff_id": hk_staff_id,
        },
    )
    assert housekeeping_response.status_code == 201
    assert housekeeping_response.json()["assigned_staff_id"] == hk_staff_id
    assert housekeeping_response.json()["assigned_to"] == "Asha Patel"

    maintenance_response = client.post(
        "/hotel/maintenance/tickets",
        headers=headers,
        json={
            "property_id": property_id,
            "room_id": room_id,
            "title": "Bathroom fixture repair",
            "description": "Leaking faucet detected.",
            "priority": "medium",
            "assigned_staff_id": maintenance_staff_id,
        },
    )
    assert maintenance_response.status_code == 201
    assert maintenance_response.json()["assigned_staff_id"] == maintenance_staff_id
    assert maintenance_response.json()["assigned_to"] == "Vikram Rao"

    staff_list_response = client.get("/hotel/staff", headers=headers)
    shift_list_response = client.get("/hotel/shifts", headers=headers)
    overview_response = client.get("/hotel/overview", headers=headers)

    assert staff_list_response.status_code == 200
    assert shift_list_response.status_code == 200
    assert overview_response.status_code == 200
    assert len(staff_list_response.json()["staff_members"]) == 2
    assert len(shift_list_response.json()["shifts"]) == 1
    assert overview_response.json()["staff_members"] == 2
    assert overview_response.json()["shifts"] == 1


def test_hotel_pack_supports_refunds_and_night_audit(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_audit", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_audit")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Audit Stay",
            "code": "KZA-IN-001",
            "city": "Delhi",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    room_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Club Room",
            "code": "CLB-R",
            "occupancy": 2,
            "base_rate_minor": 3200000,
            "currency": "INR",
        },
    )
    assert room_type_response.status_code == 201
    room_type_id = room_type_response.json()["id"]

    room_response = client.post(
        "/hotel/rooms",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_number": "902",
            "status": "available",
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    reservation_response = client.post(
        "/hotel/reservations",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": room_type_id,
            "room_id": room_id,
            "guest_customer_id": "cust_audit_001",
            "guest_name": "Meera Iyer",
            "check_in_date": "2026-07-20",
            "check_out_date": "2026-07-22",
            "total_amount_minor": 3200000,
            "currency": "INR",
            "adults": 2,
            "children": 0,
        },
    )
    assert reservation_response.status_code == 201
    reservation_id = reservation_response.json()["id"]

    folios_response = client.get(f"/hotel/folios?reservation_id={reservation_id}", headers=headers)
    assert folios_response.status_code == 200
    folio_id = folios_response.json()["folios"][0]["id"]

    first_payment_response = client.post(
        f"/hotel/folios/{folio_id}/payments",
        headers=headers,
        json={
            "amount_minor": 3200000,
            "payment_method": "card",
            "reference": "CARD-AUDIT-1",
        },
    )
    assert first_payment_response.status_code == 201
    payment_id = first_payment_response.json()["payments"][0]["id"]

    refund_response = client.post(
        f"/hotel/folios/{folio_id}/refunds",
        headers=headers,
        json={
            "payment_id": payment_id,
            "amount_minor": 200000,
            "reason": "Courtesy adjustment",
            "reference": "RF-001",
        },
    )
    assert refund_response.status_code == 201
    assert refund_response.json()["paid_minor"] == 3000000
    assert refund_response.json()["balance_minor"] == 200000
    assert len(refund_response.json()["refunds"]) == 1

    second_payment_response = client.post(
        f"/hotel/folios/{folio_id}/payments",
        headers=headers,
        json={
            "amount_minor": 200000,
            "payment_method": "upi",
            "reference": "UPI-AUDIT-2",
        },
    )
    assert second_payment_response.status_code == 201
    assert second_payment_response.json()["balance_minor"] == 0

    check_in_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_in"},
    )
    assert check_in_response.status_code == 200

    check_out_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_out"},
    )
    assert check_out_response.status_code == 200

    night_audit_response = client.post(
        "/hotel/night-audits",
        headers=headers,
        json={
            "property_id": property_id,
            "audit_date": "2026-07-22",
        },
    )
    assert night_audit_response.status_code == 201
    assert night_audit_response.json()["status"] == "completed"
    assert night_audit_response.json()["report"]["open_folios_with_balance"] == 0

    duplicate_audit_response = client.post(
        "/hotel/night-audits",
        headers=headers,
        json={
            "property_id": property_id,
            "audit_date": "2026-07-22",
        },
    )
    assert duplicate_audit_response.status_code == 409

    refunds_response = client.get("/hotel/refunds", headers=headers)
    audits_response = client.get("/hotel/night-audits", headers=headers)
    overview_response = client.get("/hotel/overview", headers=headers)

    assert refunds_response.status_code == 200
    assert audits_response.status_code == 200
    assert overview_response.status_code == 200
    assert len(refunds_response.json()["refunds"]) == 1
    assert len(audits_response.json()["audits"]) == 1
    assert overview_response.json()["refunds"] == 1
    assert overview_response.json()["night_audits"] == 1
    assert overview_response.json()["refunds_minor"] == 200000


def test_hotel_pack_supports_stays_room_moves_guest_documents_and_reports(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_stays", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_stays")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Stay Ops",
            "code": "KZS-OPS-001",
            "city": "Bengaluru",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    standard_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Standard Queen",
            "code": "STD-Q",
            "occupancy": 2,
            "base_rate_minor": 2500000,
            "currency": "INR",
        },
    )
    assert standard_type_response.status_code == 201
    standard_type_id = standard_type_response.json()["id"]

    upgraded_type_response = client.post(
        "/hotel/room-types",
        headers=headers,
        json={
            "property_id": property_id,
            "name": "Premium Suite",
            "code": "PRM-S",
            "occupancy": 2,
            "base_rate_minor": 4200000,
            "currency": "INR",
        },
    )
    assert upgraded_type_response.status_code == 201
    upgraded_type_id = upgraded_type_response.json()["id"]

    room_1_response = client.post(
        "/hotel/rooms",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": standard_type_id,
            "room_number": "401",
            "status": "available",
        },
    )
    assert room_1_response.status_code == 201
    room_1_id = room_1_response.json()["id"]

    room_2_response = client.post(
        "/hotel/rooms",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": upgraded_type_id,
            "room_number": "801",
            "status": "available",
        },
    )
    assert room_2_response.status_code == 201
    room_2_id = room_2_response.json()["id"]

    guest_response = client.post(
        "/hotel/guests",
        headers=headers,
        json={
            "first_name": "Anika",
            "last_name": "Sen",
            "email": "anika.sen@example.com",
            "phone": "+919666666666",
        },
    )
    assert guest_response.status_code == 201
    guest_id = guest_response.json()["id"]

    guest_document_response = client.post(
        f"/hotel/guests/{guest_id}/documents",
        headers=headers,
        json={
            "document_kind": "passport",
            "document_number": "P1234567",
            "issuing_country": "India",
            "expires_on": "2031-01-01",
            "verification_status": "verified",
            "storage_key": "guest-docs/anika-passport.pdf",
            "notes": "Verified at check-in",
        },
    )
    assert guest_document_response.status_code == 201
    assert guest_document_response.json()["verification_status"] == "verified"

    reservation_response = client.post(
        "/hotel/reservations",
        headers=headers,
        json={
            "property_id": property_id,
            "room_type_id": standard_type_id,
            "room_id": room_1_id,
            "guest_customer_id": guest_id,
            "check_in_date": "2026-08-10",
            "check_out_date": "2026-08-13",
            "total_amount_minor": 7500000,
            "currency": "INR",
            "adults": 2,
            "children": 0,
        },
    )
    assert reservation_response.status_code == 201
    reservation_id = reservation_response.json()["id"]

    reserve_response = client.patch(
        f"/hotel/reservations/{reservation_id}/status",
        headers=headers,
        json={"status": "checked_in"},
    )
    assert reserve_response.status_code == 200

    stays_response = client.get("/hotel/stays", headers=headers)
    assert stays_response.status_code == 200
    assert len(stays_response.json()["stays"]) == 1
    stay_id = stays_response.json()["stays"][0]["id"]

    room_move_response = client.post(
        f"/hotel/stays/{stay_id}/room-moves",
        headers=headers,
        json={
            "to_room_id": room_2_id,
            "reason": "VIP upgrade",
        },
    )
    assert room_move_response.status_code == 200
    assert room_move_response.json()["room_id"] == room_2_id
    assert room_move_response.json()["room_type_id"] == upgraded_type_id
    assert len(room_move_response.json()["room_moves"]) == 1

    guest_documents_response = client.get(f"/hotel/guests/{guest_id}/documents", headers=headers)
    assert guest_documents_response.status_code == 200
    assert len(guest_documents_response.json()["documents"]) == 1

    report_response = client.get(
        f"/hotel/reports/summary?property_id={property_id}&from_date=2026-08-10&to_date=2026-08-13",
        headers=headers,
    )
    assert report_response.status_code == 200
    assert report_response.json()["stays"] == 1
    assert report_response.json()["room_moves"] == 1
    assert report_response.json()["reservations"] == 1


def test_hotel_pack_materializes_property_content_into_public_stay_page(client: TestClient) -> None:
    provision_tenant(client, tenant_slug="hotel_public", vertical_packs=["hotel"])
    tenant_token = login(client, email="ops@tenant.com", tenant_slug="hotel_public")
    headers = {"Authorization": f"Bearer {tenant_token}"}

    property_response = client.post(
        "/hotel/properties",
        headers=headers,
        json={
            "name": "KalpZero Heritage House",
            "code": "KZH-PUB-001",
            "city": "Udaipur",
            "country": "India",
            "timezone": "Asia/Kolkata",
        },
    )
    assert property_response.status_code == 201
    property_id = property_response.json()["id"]

    profile_response = client.put(
        "/hotel/property-profile",
        headers=headers,
        json={
            "property_id": property_id,
            "brand_name": "KalpZero Heritage House",
            "hero_title": "Lake-facing heritage hospitality",
            "hero_summary": "Boutique heritage stay in the old city.",
            "description": "A restored property with curated suites and local experiences.",
            "address_line_1": "Ambavgarh Main Road",
            "city": "Udaipur",
            "state": "Rajasthan",
            "country": "India",
            "contact_phone": "+919555555555",
            "contact_email": "stay@heritage.example.com",
            "website": "https://heritage.example.com",
            "check_in_time": "13:00",
            "check_out_time": "11:00",
            "star_rating": 4,
            "highlights": ["Lake views", "Rooftop dining"],
            "gallery_urls": ["https://example.com/1.jpg"],
            "policies": ["Government ID required"],
        },
    )
    assert profile_response.status_code == 200

    amenities_response = client.put(
        "/hotel/amenities",
        headers=headers,
        json={
            "property_id": property_id,
            "categories": [
                {
                    "key": "room",
                    "label": "Room Comfort",
                    "amenities": [
                        {"id": "wifi", "label": "Free Wi-Fi"},
                        {"id": "workspace", "label": "Workspace"},
                    ],
                }
            ],
        },
    )
    assert amenities_response.status_code == 200

    nearby_response = client.put(
        "/hotel/nearby",
        headers=headers,
        json={
            "property_id": property_id,
            "places": [
                {
                    "name": "City Palace",
                    "kind": "Attraction",
                    "distance_km": 1.8,
                    "travel_minutes": 8,
                    "summary": "Historic palace complex on the lakefront.",
                }
            ],
        },
    )
    assert nearby_response.status_code == 200

    public_response = client.get("/publishing/public/hotel_public/site?page_slug=stay")
    assert public_response.status_code == 200
    payload = public_response.json()

    block_ids = [block["id"] for block in payload["page"]["blocks"]]
    assert "hotel-profile" in block_ids
    assert "hotel-amenities" in block_ids
    assert "hotel-nearby" in block_ids
    assert any(card["title"] == "KalpZero Heritage House" for card in payload["discovery"]["cards"])


if __name__ == "__main__":
    raise SystemExit(run_current_test_file(__file__))
