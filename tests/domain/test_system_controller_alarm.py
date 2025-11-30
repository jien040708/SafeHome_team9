"""
Test cases for SystemController alarm and sensor trigger functionality.

Tests cover:
- SystemController.update_sensor_status with different sensor statuses
- SystemController._map_sensor_status mapping
- SystemController.trigger_panic
- SystemController.clear_alarm
"""

from __future__ import annotations

from datetime import datetime

from domain.system_controller import SystemController
from security.events import SensorEvent, SensorStatus, SensorType
from security.security_system import AlarmState, SecurityMode
from tests.test_controller_security_flow import make_controller

def make_security_system(delay_seconds: int = 0):
    """Helper to create security system for testing."""
    from datetime import timedelta
    from security.security_system import SecuritySystem
    
    class DummyMonitoring:
        def __init__(self):
            self.calls = []
        def __call__(self, reason: str):
            self.calls.append(reason)
    
    class DummySiren:
        def __init__(self):
            self.active = False
        def activate(self):
            self.active = True
        def deactivate(self):
            self.active = False
    
    monitoring = DummyMonitoring()
    siren = DummySiren()
    
    def get_delay():
        return timedelta(seconds=delay_seconds)
    
    def call_monitoring(reason: str):
        monitoring(reason)
    
    def activate_siren():
        siren.activate()
    
    def deactivate_siren():
        siren.deactivate()
    
    def get_states():
        return {}
    
    system = SecuritySystem(
        get_delay_time=get_delay,
        call_monitoring_service=call_monitoring,
        activate_siren=activate_siren,
        deactivate_siren=deactivate_siren,
        get_monitored_sensors_state=get_states,
    )
    return system, monitoring, siren


def test_map_sensor_status_open():
    """Test _map_sensor_status maps 'Open' correctly."""
    system, _, _ = make_security_system()
    controller = make_controller(system)
    
    status = controller._map_sensor_status("Open", SensorType.DOOR)
    assert status == SensorStatus.OPEN


def test_map_sensor_status_motion_detected():
    """Test _map_sensor_status maps 'Motion Detected' correctly."""
    system, _, _ = make_security_system()
    controller = make_controller(system)
    
    status = controller._map_sensor_status("Motion Detected", SensorType.MOTION)
    assert status == SensorStatus.MOTION_DETECTED


def test_map_sensor_status_triggered_door():
    """Test _map_sensor_status maps 'Triggered' for door sensor to OPEN."""
    system, _, _ = make_security_system()
    controller = make_controller(system)
    
    status = controller._map_sensor_status("Triggered", SensorType.DOOR)
    assert status == SensorStatus.OPEN


def test_map_sensor_status_triggered_motion():
    """Test _map_sensor_status maps 'Triggered' for motion sensor to MOTION_DETECTED."""
    system, _, _ = make_security_system()
    controller = make_controller(system)
    
    status = controller._map_sensor_status("Triggered", SensorType.MOTION)
    assert status == SensorStatus.MOTION_DETECTED


def test_map_sensor_status_triggered_other():
    """Test _map_sensor_status maps 'Triggered' for other sensors to OPEN."""
    system, _, _ = make_security_system()
    controller = make_controller(system)
    
    status = controller._map_sensor_status("Triggered", SensorType.OTHER)
    assert status == SensorStatus.OPEN


def test_map_sensor_status_recording():
    """Test _map_sensor_status maps 'Recording' to OPEN (alarm trigger)."""
    system, _, _ = make_security_system()
    controller = make_controller(system)
    
    status = controller._map_sensor_status("Recording", SensorType.OTHER)
    assert status == SensorStatus.OPEN


def test_map_sensor_status_normal():
    """Test _map_sensor_status maps unknown status to NORMAL."""
    system, _, _ = make_security_system()
    controller = make_controller(system)
    
    status = controller._map_sensor_status("UnknownStatus", SensorType.OTHER)
    assert status == SensorStatus.NORMAL


def test_controller_trigger_panic():
    """Test SystemController.trigger_panic activates alarm."""
    system, monitoring, siren = make_security_system()
    controller = make_controller(system)
    
    result = controller.trigger_panic()
    
    assert result is True
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_controller_trigger_panic_without_auth():
    """Test SystemController.trigger_panic fails without authentication."""
    system, _, _ = make_security_system()
    controller = SystemController(
        security_system=system,
        user_manager=None,
    )
    controller.authenticated_user = None
    
    result = controller.trigger_panic()
    
    assert result is False


def test_controller_update_sensor_status_triggered():
    """Test update_sensor_status with 'Triggered' status triggers alarm."""
    system, _, siren = make_security_system(delay_seconds=0)
    controller = make_controller(system)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    
    controller.update_sensor_status("sensor1", "Window/Door Sensor", "Triggered")
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_controller_update_sensor_status_recording():
    """Test update_sensor_status with 'Recording' status triggers alarm."""
    system, _, siren = make_security_system(delay_seconds=0)
    controller = make_controller(system)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("camera1", SensorType.OTHER, zone_id="A")
    system.assign_sensor_to_zone("camera1", "A")
    
    controller.update_sensor_status("camera1", "Camera", "Recording")
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

