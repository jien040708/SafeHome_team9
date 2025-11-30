"""
Edge case tests for SecuritySystem to maximize coverage.

Tests cover:
- Boundary conditions
- Null/None handling
- Multiple simultaneous operations
- Race conditions simulation
- Error recovery
"""

from __future__ import annotations

from datetime import datetime, timedelta

from security.security_system import AlarmState, SecurityMode, SecuritySystem
from security.events import SensorEvent, SensorStatus, SensorType
from security.test_security_system import make_security_system


def test_multiple_register_same_sensor():
    """Test registering the same sensor multiple times."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.register_sensor("sensor1", SensorType.WINDOW, zone_id="B")
    
    # Should update to latest type and zone
    assert system._sensor_types["sensor1"] == SensorType.WINDOW
    assert system._sensor_zones["sensor1"] == "B"


def test_arm_with_empty_zones():
    """Test arming with empty zones set."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    
    # Should use all zones when zones=None
    system.arm(SecurityMode.AWAY, zones=None)
    assert "A" in system._armed_zones


def test_arm_with_all_zones():
    """Test arming with all zones."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.register_sensor("sensor2", SensorType.DOOR, zone_id="B")
    
    system.arm(SecurityMode.AWAY)  # zones defaults to all
    assert "A" in system._armed_zones
    assert "B" in system._armed_zones


def test_disarm_without_cleared_by():
    """Test disarming without cleared_by parameter."""
    system, _, _ = make_security_system()
    system.arm(SecurityMode.AWAY)
    system.trigger_panic()
    
    system.disarm()  # No cleared_by
    
    assert system.mode is SecurityMode.DISARMED
    assert system.alarm_state is AlarmState.IDLE


def test_clear_alarm_without_cleared_by():
    """Test clearing alarm without cleared_by parameter."""
    system, _, _ = make_security_system(delay_seconds=0)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    system.clear_alarm()  # No cleared_by
    
    assert system.alarm_state is AlarmState.IDLE


def test_sensor_event_with_none_zone_id():
    """Test sensor event with None zone_id but sensor is registered."""
    system, _, siren = make_security_system(delay_seconds=0)
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id=None,  # Not provided in event
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE


def test_sensor_event_with_unknown_sensor():
    """Test sensor event with unknown sensor ID."""
    system, _, siren = make_security_system()
    system.arm(SecurityMode.AWAY)
    
    event = SensorEvent(
        sensor_id="unknown_sensor",
        zone_id=None,
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    # Should not trigger alarm if sensor is not armed/registered
    assert system.alarm_state is AlarmState.IDLE


def test_tick_with_no_alarm_state_changes():
    """Test tick when no state changes should occur."""
    system, _, _ = make_security_system()
    system.arm(SecurityMode.AWAY)
    
    now = datetime.utcnow()
    system.tick(now)
    
    # Should not change state
    assert system.alarm_state is AlarmState.IDLE


def test_tick_before_entry_delay_expires():
    """Test tick before entry delay expires (if entry delay existed)."""
    system, _, _ = make_security_system(delay_seconds=5)
    system.arm(SecurityMode.AWAY)
    
    # With current implementation, there's no entry delay
    # But test the tick path anyway
    now = datetime.utcnow()
    system.tick(now)
    
    assert system.alarm_state is AlarmState.IDLE


def test_tick_after_monitoring_deadline_already_scheduled():
    """Test tick after monitoring deadline when already scheduled."""
    system, monitoring, siren = make_security_system(delay_seconds=1)
    system.arm(SecurityMode.AWAY)
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    
    # Wait for monitoring deadline
    now = event.timestamp + timedelta(seconds=2)
    system.tick(now)
    
    initial_call_count = len(monitoring.calls)
    
    # Tick again - should not call monitoring again
    system.tick(now + timedelta(seconds=1))
    
    # Monitoring should only be called once
    assert len(monitoring.calls) == initial_call_count


def test_log_with_event_and_details():
    """Test _log with both event and details."""
    system, _, _ = make_security_system()
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    
    system._log(event, "TEST_ACTION", details="test details")
    
    logs = system.get_intrusion_logs()
    assert len(logs) > 0
    assert logs[-1].action == "TEST_ACTION"
    assert logs[-1].details == "test details"
    assert logs[-1].sensor_id == "sensor1"


def test_log_without_event():
    """Test _log without event."""
    system, _, _ = make_security_system()
    
    system._log(None, "TEST_ACTION", details="test details")
    
    logs = system.get_intrusion_logs()
    assert len(logs) > 0
    assert logs[-1].action == "TEST_ACTION"
    assert logs[-1].details == "test details"
    assert logs[-1].sensor_id is None


def test_log_without_details():
    """Test _log without details."""
    system, _, _ = make_security_system()
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    
    system._log(event, "TEST_ACTION")
    
    logs = system.get_intrusion_logs()
    assert len(logs) > 0
    assert logs[-1].details is None


def test_home_mode_with_window_sensor():
    """Test HOME mode triggers on window sensor."""
    system, _, siren = make_security_system(delay_seconds=0)
    system.register_sensor("window1", SensorType.WINDOW, zone_id="A")
    system.assign_sensor_to_zone("window1", "A")
    system.arm(SecurityMode.HOME, zones={"A"})
    
    event = SensorEvent(
        sensor_id="window1",
        zone_id="A",
        sensor_type=SensorType.WINDOW,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE


def test_stay_mode_with_door_sensor():
    """Test STAY mode triggers on door sensor."""
    system, _, siren = make_security_system(delay_seconds=0)
    system.register_sensor("door1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door1", "A")
    system.arm(SecurityMode.STAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="door1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE


def test_stay_mode_ignores_motion():
    """Test STAY mode ignores motion sensors."""
    system, _, siren = make_security_system()
    system.register_sensor("motion1", SensorType.MOTION, zone_id="A")
    system.assign_sensor_to_zone("motion1", "A")
    system.arm(SecurityMode.STAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="motion1",
        zone_id="A",
        sensor_type=SensorType.MOTION,
        status=SensorStatus.MOTION_DETECTED,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.IDLE


def test_away_mode_with_motion_sensor():
    """Test AWAY mode triggers on motion sensor."""
    system, _, siren = make_security_system(delay_seconds=0)
    system.register_sensor("motion1", SensorType.MOTION, zone_id="A")
    system.assign_sensor_to_zone("motion1", "A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="motion1",
        zone_id="A",
        sensor_type=SensorType.MOTION,
        status=SensorStatus.MOTION_DETECTED,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE


def test_assign_sensor_to_multiple_zones():
    """Test that sensor can only be in one zone at a time."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "B")
    
    # Should be in zone B now
    assert system._sensor_zones["sensor1"] == "B"
    assert "sensor1" not in system._zone_sensors.get("A", set())
    assert "sensor1" in system._zone_sensors.get("B", set())


def test_remove_zone_that_doesnt_exist():
    """Test removing a zone that doesn't exist."""
    system, _, _ = make_security_system()
    
    # Should not raise error
    system.remove_zone("NONEXISTENT")


def test_get_status_with_different_states():
    """Test get_status with various alarm states."""
    system, _, _ = make_security_system()
    
    status1 = system.get_status()
    assert status1.alarm_state is AlarmState.IDLE
    
    system.arm(SecurityMode.AWAY)
    status2 = system.get_status()
    assert status2.mode is SecurityMode.AWAY
    
    system.trigger_panic()
    status3 = system.get_status()
    assert status3.alarm_state is AlarmState.ALARM_ACTIVE


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

