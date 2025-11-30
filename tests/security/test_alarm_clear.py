"""
Test cases for alarm clear functionality.

Tests cover:
- clear_alarm() method in SecuritySystem
- clear_alarm() method in SystemController
- Alarm state transitions when clearing
- Alarm instances deactivation when clearing
"""

from __future__ import annotations

from datetime import datetime, timedelta

from domain.system_controller import SystemController
from security.security_system import AlarmState, SecurityMode, SecuritySystem
from security.events import SensorEvent, SensorStatus, SensorType
from tests.test_controller_security_flow import make_controller

def make_security_system(delay_seconds: int = 0):
    """Helper to create security system for testing."""
    from datetime import timedelta
    from security.security_system import SecuritySystem
    from security.events import SensorStatus
    
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


class DummyAlarm:
    """Dummy alarm for testing."""
    def __init__(self, alarm_id: int):
        self.alarm_id = alarm_id
        self.ringing = False

    def ring_alarm(self, status_value: bool) -> None:
        self.ringing = status_value


def test_clear_alarm_from_active_state():
    """Test clearing alarm when alarm is active."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    # Trigger alarm
    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    assert system.alarm_state is AlarmState.ALARM_ACTIVE

    # Clear alarm
    system.clear_alarm(cleared_by="test_user")

    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False
    assert system._alarm_started_at is None
    assert system._monitoring_deadline is None
    assert system._monitoring_call_scheduled is False


def test_clear_alarm_from_idle_state():
    """Test clearing alarm when no alarm is active (should do nothing)."""
    system, monitoring, siren = make_security_system()
    
    # Try to clear when no alarm
    initial_state = system.alarm_state
    system.clear_alarm(cleared_by="test_user")

    # Should remain in IDLE state
    assert system.alarm_state is AlarmState.IDLE
    assert system.alarm_state == initial_state
    assert siren.active is False


def test_clear_alarm_keeps_system_armed():
    """Test that clearing alarm does not disarm the system."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    # Trigger alarm
    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert system.mode is SecurityMode.AWAY

    # Clear alarm
    system.clear_alarm(cleared_by="test_user")

    # System should still be armed
    assert system.mode is SecurityMode.AWAY
    assert system.alarm_state is AlarmState.IDLE


def test_controller_clear_alarm_with_authentication():
    """Test SystemController clear_alarm with authenticated user."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    controller = make_controller(system)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    # Trigger alarm
    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    assert system.alarm_state is AlarmState.ALARM_ACTIVE

    # Clear alarm via controller
    result = controller.clear_alarm()
    
    assert result is True
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False


def test_controller_clear_alarm_without_authentication():
    """Test SystemController clear_alarm fails without authentication."""
    system, monitoring, siren = make_security_system()
    controller = SystemController(
        security_system=system,
        user_manager=None,
    )
    controller.authenticated_user = None  # Not authenticated

    # Try to clear alarm
    result = controller.clear_alarm()
    
    assert result is False
    # Alarm state should remain unchanged


def test_clear_alarm_after_panic():
    """Test clearing alarm after panic button is pressed."""
    system, monitoring, siren = make_security_system()

    # Trigger panic
    system.trigger_panic()
    assert system.alarm_state is AlarmState.ALARM_ACTIVE

    # Clear alarm
    system.clear_alarm(cleared_by="test_user")

    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False


def test_clear_alarm_logs_event():
    """Test that clearing alarm logs the event."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    # Trigger alarm
    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    initial_log_count = len(system.get_intrusion_logs())

    # Clear alarm
    system.clear_alarm(cleared_by="test_user")

    logs = system.get_intrusion_logs()
    assert len(logs) > initial_log_count
    
    # Find the ALARM_CLEARED log
    cleared_logs = [log for log in logs if log.action == "ALARM_CLEARED"]
    assert len(cleared_logs) > 0
    assert "test_user" in (cleared_logs[0].details or "")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

