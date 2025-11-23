from __future__ import annotations

from datetime import timedelta

import pytest

import storage.storage_manager as storage_mod
from config.configuration_manager import ConfigurationManager
from security.security_system import SecuritySystem


@pytest.fixture(autouse=True)
def isolated_storage(tmp_path, monkeypatch):
    """Provide a throwaway SQLite database for each test."""
    test_db = tmp_path / "test_safehome.db"
    monkeypatch.setattr(storage_mod, "DB_FILE", str(test_db))
    storage_mod.StorageManager._instance = None
    manager = storage_mod.StorageManager()
    assert manager.connect()
    yield
    manager.disconnect()
    storage_mod.StorageManager._instance = None


def make_security_system() -> SecuritySystem:
    """Create a minimal SecuritySystem with dummy callbacks."""

    def get_delay():
        return timedelta(seconds=1)

    def call_monitoring(reason: str):
        return None

    def activate():
        return None

    def deactivate():
        return None

    def get_states():
        return {}

    return SecuritySystem(
        get_delay_time=get_delay,
        call_monitoring_service=call_monitoring,
        activate_siren=activate,
        deactivate_siren=deactivate,
        get_monitored_sensors_state=get_states,
    )


def test_security_system_tracks_explicit_zone_assignments():
    cm = ConfigurationManager()
    assert cm.initialize_configuration()
    cm.add_safety_zone("Entryway")
    zone_id = cm.safety_zones[-1].zone_id
    assert cm.assign_sensor_to_zone("Front Door", zone_id)

    sec = make_security_system()
    cm.configure_security_system(sec)
    assert sec._sensor_zones.get("Front Door") == str(zone_id)  # pylint: disable=protected-access

    cm.remove_sensor_assignment("Front Door")
    assert "Front Door" not in sec._sensor_zones  # pylint: disable=protected-access
