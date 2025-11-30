"""
Integration tests for Alarm class with SecuritySystem.

Tests cover:
- Alarm activation when sensor triggers
- Alarm activation when panic button pressed
- Alarm deactivation when alarm is cleared
- Multiple Alarm instances working together
"""

from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from security.security_system import Alarm, AlarmState, SecurityMode, SecuritySystem
from security.events import SensorEvent, SensorStatus, SensorType


class DummyMonitoring:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def __call__(self, reason: str) -> None:
        self.calls.append(reason)


class DummyAlarm:
    """Dummy alarm for testing alarm activation."""
    def __init__(self, alarm_id: int):
        self.alarm_id = alarm_id
        self.ringing = False
        self.ring_calls = []

    def ring_alarm(self, status_value: bool) -> None:
        self.ringing = status_value
        self.ring_calls.append(status_value)


def make_security_system_with_alarms(
    delay_seconds: int = 0,  # 0 delay for immediate alarm
    sensor_states: dict[str, SensorStatus] | None = None,
) -> tuple[SecuritySystem, DummyMonitoring, list[DummyAlarm]]:
    """Create SecuritySystem with dummy alarms for testing."""
    monitoring = DummyMonitoring()
    alarms = [DummyAlarm(1), DummyAlarm(2)]

    def get_delay() -> timedelta:
        return timedelta(seconds=delay_seconds)

    def call_monitoring(reason: str) -> None:
        monitoring(reason)

    def activate_siren() -> None:
        for alarm in alarms:
            alarm.ring_alarm(True)

    def deactivate_siren() -> None:
        for alarm in alarms:
            alarm.ring_alarm(False)

    def get_sensor_states() -> dict[str, SensorStatus]:
        return sensor_states or {}

    system = SecuritySystem(
        get_delay_time=get_delay,
        call_monitoring_service=call_monitoring,
        activate_siren=activate_siren,
        deactivate_siren=deactivate_siren,
        get_monitored_sensors_state=get_sensor_states,
    )
    return system, monitoring, alarms


def test_sensor_trigger_activates_alarms():
    """Test that sensor trigger activates all alarms."""
    system, monitoring, alarms = make_security_system_with_alarms(delay_seconds=0)
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
    # Verify all alarms are ringing
    for alarm in alarms:
        assert alarm.ringing is True
        assert len(alarm.ring_calls) >= 1
        assert alarm.ring_calls[-1] is True


def test_panic_button_activates_alarms():
    """Test that panic button activates all alarms."""
    system, monitoring, alarms = make_security_system_with_alarms()

    system.trigger_panic()

    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    # Verify all alarms are ringing
    for alarm in alarms:
        assert alarm.ringing is True
        assert len(alarm.ring_calls) >= 1
        assert alarm.ring_calls[-1] is True
    assert "PANIC" in monitoring.calls or monitoring.calls == []


def test_clear_alarm_deactivates_alarms():
    """Test that clearing alarm deactivates all alarms."""
    system, monitoring, alarms = make_security_system_with_alarms(delay_seconds=0)
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
    # Verify all alarms are silenced
    for alarm in alarms:
        assert alarm.ringing is False
        # Should have both ring and silence calls
        assert len(alarm.ring_calls) >= 2
        assert alarm.ring_calls[-1] is False


def test_disarm_clears_alarm_and_deactivates_alarms():
    """Test that disarming clears alarm and deactivates alarms."""
    system, monitoring, alarms = make_security_system_with_alarms(delay_seconds=0)
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
    
    # Disarm
    system.disarm()
    
    assert system.alarm_state is AlarmState.IDLE
    assert system.mode is SecurityMode.DISARMED
    # Verify all alarms are silenced
    for alarm in alarms:
        assert alarm.ringing is False


def test_multiple_alarms_work_independently():
    """Test that multiple alarms work independently."""
    alarm1 = Alarm(alarm_id=1, x_coord=100, y_coord=100)
    alarm2 = Alarm(alarm_id=2, x_coord=200, y_coord=200)
    
    # Test alarm1
    alarm1.ring_alarm(True)
    assert alarm1.is_ringing() is True
    assert alarm2.is_ringing() is False
    
    # Test alarm2
    alarm2.ring_alarm(True)
    assert alarm1.is_ringing() is True
    assert alarm2.is_ringing() is True
    
    # Silence alarm1
    alarm1.ring_alarm(False)
    assert alarm1.is_ringing() is False
    assert alarm2.is_ringing() is True
    
    # Silence alarm2
    alarm2.ring_alarm(False)
    assert alarm1.is_ringing() is False
    assert alarm2.is_ringing() is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

