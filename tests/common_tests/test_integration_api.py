"""Integration-style tests for the configuration REST API."""

import pytest


@pytest.mark.usefixtures("safehome_system_instance")
def test_get_settings_requires_auth(client):
    response = client.get("/api/settings")
    assert response.status_code == 401
    payload = response.get_json()
    assert payload["success"] is False
    assert payload["message"] == "Authentication required"


@pytest.mark.usefixtures("safehome_system_instance")
def test_update_settings_requires_auth(client):
    response = client.put(
        "/api/settings",
        json={
            "monitoring_service_phone": "111-222-3333",
            "homeowner_phone": "444-555-6666",
            "system_lock_time": 30,
            "alarm_delay_time": 60,
        },
    )
    assert response.status_code == 401
    payload = response.get_json()
    assert payload["success"] is False
    assert payload["message"] == "Authentication required"


@pytest.mark.usefixtures("safehome_system_instance")
def test_update_settings_invalid_time_values(auth_client):
    invalid_payload = {
        "monitoring_service_phone": "111-222-3333",
        "homeowner_phone": "444-555-6666",
        "system_lock_time": 0,
        "alarm_delay_time": -5,
    }

    response = auth_client.put("/api/settings", json=invalid_payload)
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["success"] is False
    assert any("System lock time must be greater than 0" in err for err in payload["errors"])
    assert any("Alarm delay time must be non-negative" in err for err in payload["errors"])
