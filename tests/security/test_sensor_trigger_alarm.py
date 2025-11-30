"""
Test cases for sensor trigger alarm functionality.

Tests cover:
- Sensor trigger activates alarm immediately
- Sensor trigger when system is DISARMED (should not activate)
- Sensor trigger when sensor is not armed (should not activate)
- Different sensor types triggering alarm
- Sensor status mapping for alarm activation
"""

from __future__ import annotations

from datetime import datetime

from domain.system_controller import SystemController
from security.security_system import AlarmState, SecurityMode
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


def test_sensor_trigger_immediate_alarm_activation():
    """Test that sensor trigger activates alarm immediately (no entry delay when delay is 0)."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    # Should immediately activate alarm (no entry delay when delay is 0)
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_sensor_trigger_disarmed_ignored():
    """Test that sensor trigger is ignored when system is DISARMED."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    # System is DISARMED
    assert system.mode is SecurityMode.DISARMED

    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    # Should not activate alarm
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False


def test_motion_sensor_trigger_activates_alarm():
    """Test that motion sensor trigger activates alarm when armed."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("motion1", SensorType.MOTION, zone_id="A")
    system.assign_sensor_to_zone("motion1", "A")

    event = SensorEvent(
        sensor_id="motion1",
        zone_id="A",
        sensor_type=SensorType.MOTION,
        status=SensorStatus.MOTION_DETECTED,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_door_sensor_trigger_activates_alarm():
    """Test that door sensor trigger activates alarm when armed."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_controller_update_sensor_status_triggers_alarm():
    """Test that SystemController.update_sensor_status triggers alarm when appropriate."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    controller = make_controller(system)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    # Update sensor status via controller
    controller.update_sensor_status("door1", "Window/Door Sensor", "Open")

    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_sensor_trigger_unarmed_zone_ignored():
    """Test that sensor trigger in unarmed zone is ignored."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.register_sensor("door-A", SensorType.DOOR, zone_id="A")
    system.register_sensor("door-B", SensorType.DOOR, zone_id="B")
    system.assign_sensor_to_zone("door-A", "A")
    system.assign_sensor_to_zone("door-B", "B")
    
    # Only arm zone A
    system.arm(SecurityMode.AWAY, zones={"A"})

    # Trigger sensor in unarmed zone B
    event = SensorEvent(
        sensor_id="door-B",
        zone_id="B",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    # Should not activate alarm
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False

    # Trigger sensor in armed zone A
    event = SensorEvent(
        sensor_id="door-A",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    # Should activate alarm
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_sensor_trigger_already_active_alarm():
    """Test that sensor trigger when alarm is already active is ignored."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")

    # First trigger
    event1 = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event1)
    assert system.alarm_state is AlarmState.ALARM_ACTIVE

    # Second trigger while alarm is already active
    event2 = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event2)

    # Should remain in ALARM_ACTIVE state
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

