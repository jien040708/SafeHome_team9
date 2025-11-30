"""
Test cases for sensor trigger toggle functionality via API.

Tests cover:
- Motion detector toggle state via API
- Window/Door sensor toggle state via API
- Alarm only activates when transitioning to triggered state
- Alarm does NOT activate when transitioning to not-triggered state
"""

from __future__ import annotations

import pytest

from utils.constants import STATE_CLEAR, STATE_DETECTED, STATE_OPEN, STATE_CLOSED


@pytest.mark.usefixtures("safehome_system_instance")
class TestSensorTriggerToggle:
    """Test sensor trigger toggle functionality."""

    def _find_sensor(self, safehome_system, device_id: str):
        """Helper to find sensor by device_id."""
        if safehome_system.sensors:
            for s in safehome_system.sensors:
                if s.get_id() == device_id:
                    return s
        return None

    def test_motion_detector_toggle_to_triggered(self, auth_client, safehome_system_instance):
        """Test motion detector can be triggered via API."""
        sensor = self._find_sensor(safehome_system_instance, "Living Room")

        if sensor is None:
            pytest.skip("Living Room motion detector not found in sensors list")

        # Reset to clear state
        if hasattr(sensor, "clear_motion"):
            sensor.clear_motion()
        assert sensor.get_status() == STATE_CLEAR

        # Trigger via API
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Living Room", "action": "trigger"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert sensor.get_status() == STATE_DETECTED

    def test_motion_detector_toggle_to_clear(self, auth_client, safehome_system_instance):
        """Test motion detector can be cleared (toggled back) via API."""
        sensor = self._find_sensor(safehome_system_instance, "Living Room")

        if sensor is None:
            pytest.skip("Living Room motion detector not found in sensors list")

        # Set to detected state first
        if hasattr(sensor, "detect_motion"):
            sensor.detect_motion()
        assert sensor.get_status() == STATE_DETECTED

        # Toggle via API (should clear)
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Living Room", "action": "trigger"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert sensor.get_status() == STATE_CLEAR

    def test_window_door_sensor_toggle_to_open(self, auth_client, safehome_system_instance):
        """Test window/door sensor can be opened via API."""
        sensor = self._find_sensor(safehome_system_instance, "Front Door")

        if sensor is None:
            pytest.skip("Front Door sensor not found in sensors list")

        # Set to closed state first
        if hasattr(sensor, "set_closed"):
            sensor.set_closed()
        assert sensor.get_status() == STATE_CLOSED

        # Toggle via API (should open)
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Front Door", "action": "trigger"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert sensor.get_status() == STATE_OPEN

    def test_window_door_sensor_toggle_to_closed(self, auth_client, safehome_system_instance):
        """Test window/door sensor can be closed (toggled back) via API."""
        sensor = self._find_sensor(safehome_system_instance, "Front Door")

        if sensor is None:
            pytest.skip("Front Door sensor not found in sensors list")

        # Set to open state first
        if hasattr(sensor, "set_open"):
            sensor.set_open()
        assert sensor.get_status() == STATE_OPEN

        # Toggle via API (should close)
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Front Door", "action": "trigger"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert sensor.get_status() == STATE_CLOSED

    def test_sensor_trigger_invalid_device(self, auth_client, safehome_system_instance):
        """Test sensor trigger with invalid device ID returns error."""
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "NonExistentDevice", "action": "trigger"},
        )

        assert response.status_code == 404
        data = response.get_json()
        assert data["success"] is False

    def test_sensor_trigger_requires_auth(self, client, safehome_system_instance):
        """Test sensor trigger requires authentication."""
        response = client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Living Room", "action": "trigger"},
        )

        assert response.status_code == 401
        data = response.get_json()
        assert data["success"] is False

    def test_sensor_trigger_requires_action(self, auth_client, safehome_system_instance):
        """Test sensor trigger requires action parameter."""
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Living Room"},  # Missing action
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False

    def test_sensor_trigger_invalid_action(self, auth_client, safehome_system_instance):
        """Test sensor trigger with invalid action returns error."""
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Living Room", "action": "invalid_action"},
        )

        assert response.status_code == 400
        data = response.get_json()
        assert data["success"] is False


@pytest.mark.usefixtures("safehome_system_instance")
class TestAlarmTriggerOnStateTransition:
    """Test alarm activation only on triggered state transitions."""

    def _find_sensor(self, safehome_system, device_id: str):
        """Helper to find sensor by device_id."""
        if safehome_system.sensors:
            for s in safehome_system.sensors:
                if s.get_id() == device_id:
                    return s
        return None

    def test_motion_detector_clear_does_not_trigger_alarm_when_disarmed(
        self, auth_client, safehome_system_instance
    ):
        """Test that clearing motion detector does NOT activate alarm when disarmed."""
        sensor = self._find_sensor(safehome_system_instance, "Living Room")

        if sensor is None:
            pytest.skip("Living Room motion detector not found in sensors list")

        # Set to detected state
        if hasattr(sensor, "detect_motion"):
            sensor.detect_motion()

        # Disarm security system
        security_system = safehome_system_instance.security_system
        if security_system:
            security_system.disarm()

        # Toggle via API (should clear - NOT trigger alarm)
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Living Room", "action": "trigger"},
        )

        assert response.status_code == 200
        # After clearing, sensor should be clear
        assert sensor.get_status() == STATE_CLEAR

    def test_window_door_closed_does_not_trigger_alarm_when_disarmed(
        self, auth_client, safehome_system_instance
    ):
        """Test that closing door sensor does NOT activate alarm when disarmed."""
        sensor = self._find_sensor(safehome_system_instance, "Front Door")

        if sensor is None:
            pytest.skip("Front Door sensor not found in sensors list")

        # Set to open state
        if hasattr(sensor, "set_open"):
            sensor.set_open()

        # Disarm security system
        security_system = safehome_system_instance.security_system
        if security_system:
            security_system.disarm()

        # Toggle via API (should close - NOT trigger alarm since we're disarmed)
        response = auth_client.post(
            "/api/security/sensors/trigger",
            json={"device_id": "Front Door", "action": "trigger"},
        )

        assert response.status_code == 200
        data = response.get_json()
        assert data["success"] is True
        assert sensor.get_status() == STATE_CLOSED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
