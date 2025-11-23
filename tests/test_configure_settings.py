import pytest

from config.system_settings import SystemSettings


DEFAULT_SETTINGS = {
    "monitoring_service_phone": "911",
    "homeowner_phone": "010-0000-0000",
    "system_lock_time": 30,
    "alarm_delay_time": 60,
}


@pytest.fixture(autouse=True)
def reset_system_settings(safehome_system_instance):
    """Ensure every test starts with a known SystemSettings state."""
    settings = safehome_system_instance.configuration_manager.get_system_setting()
    settings.set_monitoring_service_phone(DEFAULT_SETTINGS["monitoring_service_phone"])
    settings.set_homeowner_phone(DEFAULT_SETTINGS["homeowner_phone"])
    settings.set_system_lock_time(DEFAULT_SETTINGS["system_lock_time"])
    settings.set_alarm_delay_time(DEFAULT_SETTINGS["alarm_delay_time"])
    settings.save()
    yield


def _db_settings_snapshot():
    db_settings = SystemSettings()
    db_settings.load()
    return {
        "monitoring_service_phone": db_settings.get_monitoring_service_phone(),
        "homeowner_phone": db_settings.get_homeowner_phone(),
        "system_lock_time": db_settings.get_system_lock_time(),
        "alarm_delay_time": db_settings.get_alarm_delay_time(),
    }


def test_get_settings(auth_client):
    response = auth_client.get("/api/settings")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True
    assert payload["settings"] == DEFAULT_SETTINGS


def test_update_settings_valid(auth_client):
    new_values = {
        "monitoring_service_phone": "111-222-3333",
        "homeowner_phone": "444-555-6666",
        "system_lock_time": 45,
        "alarm_delay_time": 90,
    }

    response = auth_client.put("/api/settings", json=new_values)
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["success"] is True

    stored = _db_settings_snapshot()
    assert stored == new_values


def test_update_settings_invalid_phone(auth_client):
    invalid_payload = {
        "monitoring_service_phone": "invalid-phone",
        "homeowner_phone": "444-555-6666",
        "system_lock_time": 30,
        "alarm_delay_time": 60,
    }

    response = auth_client.put("/api/settings", json=invalid_payload)
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["success"] is False
    assert any(
        "Invalid monitoring service phone format" in err for err in payload["errors"]
    )
    assert _db_settings_snapshot() == DEFAULT_SETTINGS


def test_update_settings_invalid_time(auth_client):
    invalid_payload = {
        "monitoring_service_phone": "111-222-3333",
        "homeowner_phone": "444-555-6666",
        "system_lock_time": 0,
        "alarm_delay_time": -10,
    }

    response = auth_client.put("/api/settings", json=invalid_payload)
    assert response.status_code == 400
    payload = response.get_json()
    assert payload["success"] is False
    assert any("System lock time must be greater than 0" in err for err in payload["errors"])
    assert any("Alarm delay time must be non-negative" in err for err in payload["errors"])
    assert _db_settings_snapshot() == DEFAULT_SETTINGS


def test_verify_final_settings_reflect_db(auth_client, safehome_system_instance):
    settings = safehome_system_instance.configuration_manager.get_system_setting()
    settings.set_monitoring_service_phone("222-333-4444")
    settings.set_homeowner_phone("555-666-7777")
    settings.set_system_lock_time(25)
    settings.set_alarm_delay_time(15)
    settings.save()

    response = auth_client.get("/api/settings")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["settings"] == _db_settings_snapshot()
