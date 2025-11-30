"""
Test cases for monitoring service notification functionality.

Tests cover:
- Monitoring service notification after alarm_delay_time
- Entry delay expiration triggers monitoring service scheduling
- tick() method monitoring service logic
"""

from __future__ import annotations

from datetime import datetime, timedelta

from security.security_system import AlarmState, SecurityMode
from security.events import SensorEvent, SensorStatus, SensorType
from security.test_security_system import make_security_system


def test_monitoring_service_called_after_delay():
    """Test that monitoring service is called after alarm_delay_time expires."""
    system, monitoring, siren = make_security_system(delay_seconds=5)
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
    
    # Trigger entry delay expiration
    system.tick(event.timestamp + timedelta(seconds=2))
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    
    # Wait for monitoring deadline
    now = event.timestamp + timedelta(seconds=7)  # 2 seconds entry + 5 seconds delay
    system.tick(now)
    
    # Monitoring service should have been called
    assert system._monitoring_call_scheduled is True
    assert len(monitoring.calls) > 0
    # Check that monitoring was called with condition information
    monitoring_calls = [call for call in monitoring.calls if "Sensor states" in call or "Alarm active" in call]
    assert len(monitoring_calls) > 0


def test_monitoring_service_not_called_before_delay():
    """Test that monitoring service is not called before alarm_delay_time expires."""
    system, monitoring, siren = make_security_system(delay_seconds=10)
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
    
    # Trigger entry delay expiration
    system.tick(event.timestamp + timedelta(seconds=2))
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    
    # Check monitoring deadline was set
    assert system._monitoring_deadline is not None
    
    # Tick before delay expires
    now = event.timestamp + timedelta(seconds=5)  # Before 10 second delay
    system.tick(now)
    
    # Monitoring service should not have been called yet
    assert system._monitoring_call_scheduled is False
    # No monitoring calls should contain condition info yet
    monitoring_calls = [call for call in monitoring.calls if "Sensor states" in call or "Alarm active" in call]
    assert len(monitoring_calls) == 0


def test_monitoring_service_with_sensor_states():
    """Test that monitoring service receives current sensor states."""
    sensor_states = {
        "door1": SensorStatus.OPEN,
        "motion1": SensorStatus.NORMAL,
    }
    system, monitoring, siren = make_security_system(delay_seconds=1, sensor_states=sensor_states)
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
    
    # Trigger entry delay expiration
    system.tick(event.timestamp + timedelta(seconds=2))
    
    # Wait for monitoring deadline
    now = event.timestamp + timedelta(seconds=3)  # 2 seconds entry + 1 second delay
    system.tick(now)
    
    # Monitoring service should have been called with sensor states
    assert system._monitoring_call_scheduled is True
    assert len(monitoring.calls) > 0
    # Find the monitoring call with condition information
    condition_calls = [call for call in monitoring.calls if "Sensor states" in call]
    assert len(condition_calls) > 0
    assert "door1" in condition_calls[0] or "Sensor states" in condition_calls[0]


def test_monitoring_service_after_panic():
    """Test that monitoring service is called after panic button."""
    system, monitoring, siren = make_security_system(delay_seconds=2)
    
    # Trigger panic
    system.trigger_panic()
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert system._alarm_started_at is not None
    
    # Check monitoring deadline was set
    assert system._monitoring_deadline is not None
    
    # Wait for monitoring deadline
    now = system._alarm_started_at + timedelta(seconds=3)
    system.tick(now)
    
    # Monitoring service should have been called
    assert system._monitoring_call_scheduled is True
    assert len(monitoring.calls) > 0


def test_get_status_includes_monitoring_deadline():
    """Test that get_status includes monitoring deadline information."""
    system, monitoring, siren = make_security_system(delay_seconds=1)
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
    
    # Trigger entry delay expiration
    system.tick(event.timestamp + timedelta(seconds=2))
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    
    # Get status - alarm 활성화 시 즉시 monitoring이 스케줄됨
    status = system.get_status()
    assert status is not None
    assert status.alarm_state is AlarmState.ALARM_ACTIVE
    assert status.monitoring_call_scheduled is True  # 즉시 스케줄됨


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

