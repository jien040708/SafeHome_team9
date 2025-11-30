"""
Comprehensive tests for SecuritySystem to increase coverage.

Tests cover edge cases and less common code paths:
- Zone and sensor management
- Event listener callbacks
- Camera gateway integration
- Various security modes
- Error cases
- Helper methods
"""

from __future__ import annotations

from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock

from security.security_system import AlarmState, SecurityMode, SecuritySystem
from security.events import SensorEvent, SensorStatus, SensorType
from security.test_security_system import make_security_system


def test_register_sensor_without_zone():
    """Test registering a sensor without zone_id."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR)
    
    assert "sensor1" in system._sensor_types
    assert system._sensor_types["sensor1"] == SensorType.DOOR
    assert "sensor1" not in system._sensor_zones


def test_unassign_sensor():
    """Test unassigning a sensor from a zone."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.unassign_sensor("sensor1")
    
    assert "sensor1" not in system._sensor_zones
    assert "sensor1" not in system._zone_sensors.get("A", set())


def test_unassign_sensor_not_in_zone():
    """Test unassigning a sensor that is not in any zone."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR)
    # Should not raise error
    system.unassign_sensor("sensor1")


def test_unassign_sensor_removes_empty_zone():
    """Test that unassigning the last sensor in a zone removes the zone."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.unassign_sensor("sensor1")
    
    assert "A" not in system._zone_sensors


def test_remove_zone():
    """Test removing a zone."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.register_sensor("sensor2", SensorType.WINDOW, zone_id="A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    system.remove_zone("A")
    
    assert "A" not in system._zone_sensors
    assert "sensor1" not in system._sensor_zones
    assert "sensor2" not in system._sensor_zones
    assert "A" not in system._armed_zones


def test_set_event_listener():
    """Test setting an event listener."""
    system, _, _ = make_security_system()
    listener = Mock()
    
    system.set_event_listener(listener)
    
    assert system._listener is listener


def test_set_event_listener_to_none():
    """Test setting event listener to None."""
    system, _, _ = make_security_system()
    listener = Mock()
    system.set_event_listener(listener)
    assert system._listener is listener
    
    system.set_event_listener(None)
    assert system._listener is None


def test_arm_with_disarmed_mode_raises_error():
    """Test that arming with DISARMED mode raises ValueError."""
    system, _, _ = make_security_system()
    
    try:
        system.arm(SecurityMode.DISARMED)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "disarm" in str(e).lower()


def test_extended_travel_mode():
    """Test EXTENDED_TRAVEL mode arming and sensor triggering."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.register_sensor("sensor1", SensorType.MOTION, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    
    system.arm(SecurityMode.EXTENDED_TRAVEL, zones={"A"})
    assert system.mode is SecurityMode.EXTENDED_TRAVEL
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.MOTION,
        status=SensorStatus.MOTION_DETECTED,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_window_sensor_trigger():
    """Test window sensor triggering alarm."""
    system, monitoring, siren = make_security_system(delay_seconds=0)
    system.register_sensor("window1", SensorType.WINDOW, zone_id="A")
    system.assign_sensor_to_zone("window1", "A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="window1",
        zone_id="A",
        sensor_type=SensorType.WINDOW,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_camera_gateway_integration():
    """Test camera gateway integration when sensor triggers."""
    monitoring = Mock()
    siren = Mock()
    camera_gateway = Mock()
    
    def get_delay():
        return timedelta(seconds=0)
    
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
        camera_gateway=camera_gateway,
    )
    
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    camera_gateway.trigger_all.assert_called_once_with("INTRUSION")


def test_camera_gateway_in_panic():
    """Test camera gateway integration when panic button pressed."""
    monitoring = Mock()
    siren = Mock()
    camera_gateway = Mock()
    
    def get_delay():
        return timedelta(seconds=0)
    
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
        camera_gateway=camera_gateway,
    )
    
    system.trigger_panic()
    
    camera_gateway.trigger_all.assert_called_once_with("PANIC")


def test_event_listener_on_alarm_activated():
    """Test event listener callback when alarm is activated."""
    from datetime import timedelta
    from security.test_security_system import DummyMonitoring, DummySiren
    
    listener = Mock()
    monitoring = DummyMonitoring()
    siren = DummySiren()
    
    def get_delay():
        return timedelta(seconds=0)
    
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
        event_listener=listener,
    )
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    listener.on_alarm_activated.assert_called_once()
    listener.on_status_changed.assert_called()


def test_event_listener_on_alarm_cleared():
    """Test event listener callback when alarm is cleared."""
    from datetime import timedelta
    from security.test_security_system import DummyMonitoring, DummySiren
    
    listener = Mock()
    monitoring = DummyMonitoring()
    siren = DummySiren()
    
    def get_delay():
        return timedelta(seconds=0)
    
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
        event_listener=listener,
    )
    system.trigger_panic()
    
    system.clear_alarm(cleared_by="test_user")
    
    listener.on_alarm_cleared.assert_called_once_with("test_user")
    listener.on_status_changed.assert_called()


def test_event_listener_on_disarm():
    """Test event listener callback when system is disarmed."""
    from datetime import timedelta
    from security.test_security_system import DummyMonitoring, DummySiren
    
    listener = Mock()
    monitoring = DummyMonitoring()
    siren = DummySiren()
    
    def get_delay():
        return timedelta(seconds=0)
    
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
        event_listener=listener,
    )
    system.arm(SecurityMode.AWAY)
    system.trigger_panic()
    
    system.disarm(cleared_by="test_user")
    
    listener.on_alarm_cleared.assert_called_once_with("test_user")
    listener.on_status_changed.assert_called()


def test_event_listener_on_intrusion_logged():
    """Test event listener callback when intrusion is logged."""
    from datetime import timedelta
    from security.test_security_system import DummyMonitoring, DummySiren
    
    listener = Mock()
    monitoring = DummyMonitoring()
    siren = DummySiren()
    
    def get_delay():
        return timedelta(seconds=0)
    
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
        event_listener=listener,
    )
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    # Check that intrusion was logged
    logs = system.get_intrusion_logs()
    assert len(logs) > 0
    # Listener should have been called
    assert listener.on_intrusion_logged.call_count > 0


def test_entry_delay_retriggered():
    """Test ENTRY_DELAY state when sensor triggers again."""
    system, _, siren = make_security_system(delay_seconds=5)
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("sensor1", "A")
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    # First trigger (this should not happen with current implementation,
    # but test the code path if entry delay existed)
    # Actually, current code activates immediately, so this tests ALARM_ACTIVE retrigger
    event1 = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event1)
    
    # Second trigger while alarm is active
    event2 = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event2)
    
    # Should log ALARM_ALREADY_ACTIVE
    logs = system.get_intrusion_logs()
    alarm_logs = [log for log in logs if log.action == "ALARM_ALREADY_ACTIVE"]
    assert len(alarm_logs) > 0


def test_resolve_zone_with_event_zone_id():
    """Test _resolve_zone when event has zone_id."""
    system, _, _ = make_security_system()
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    
    zone = system._resolve_zone(event)
    assert zone == "A"


def test_resolve_zone_from_sensor_zones():
    """Test _resolve_zone when event zone_id is None but sensor is in zone."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    
    event = SensorEvent(
        sensor_id="sensor1",
        zone_id=None,
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    
    zone = system._resolve_zone(event)
    assert zone == "A"


def test_check_doors_windows_closed_no_zones():
    """Test _check_doors_and_windows_closed with no zones specified."""
    sensor_states = {
        "door1": SensorStatus.NORMAL,
        "window1": SensorStatus.NORMAL,
    }
    system, _, _ = make_security_system(sensor_states=sensor_states)
    system.register_sensor("door1", SensorType.DOOR)
    system.register_sensor("window1", SensorType.WINDOW)

    result = system._check_doors_and_windows_closed(set())
    assert result is True


def test_check_doors_windows_closed_with_open_window():
    """Test _check_doors_and_windows_closed with open window."""
    sensor_states = {
        "window1": SensorStatus.OPEN,
    }
    system, _, _ = make_security_system(sensor_states=sensor_states)
    system.register_sensor("window1", SensorType.WINDOW, zone_id="A")
    
    result = system._check_doors_and_windows_closed({"A"})
    assert result is False


def test_check_doors_windows_closed_ignores_motion_sensors():
    """Test _check_doors_and_windows_closed ignores motion sensors."""
    sensor_states = {
        "motion1": SensorStatus.MOTION_DETECTED,
    }
    system, _, _ = make_security_system(sensor_states=sensor_states)
    system.register_sensor("motion1", SensorType.MOTION, zone_id="A")
    
    result = system._check_doors_and_windows_closed({"A"})
    assert result is True  # Motion sensor should be ignored


def test_disarm_without_alarm_active():
    """Test disarming when no alarm is active."""
    system, _, siren = make_security_system()
    system.arm(SecurityMode.AWAY)
    
    system.disarm(cleared_by="test_user")
    
    assert system.mode is SecurityMode.DISARMED
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False


def test_get_status_returns_security_status():
    """Test get_status returns SecurityStatus object."""
    system, _, _ = make_security_system()
    system.arm(SecurityMode.AWAY)
    
    status = system.get_status()
    assert status is not None
    assert status.mode is SecurityMode.AWAY
    assert status.alarm_state is AlarmState.IDLE


def test_get_intrusion_logs():
    """Test get_intrusion_logs returns copy of logs."""
    system, _, _ = make_security_system()
    system.arm(SecurityMode.AWAY)
    system.disarm()
    
    logs1 = system.get_intrusion_logs()
    logs2 = system.get_intrusion_logs()
    
    assert logs1 is not logs2  # Should be different objects (copy)
    assert len(logs1) == len(logs2)


def test_arm_with_specific_zones():
    """Test arming with specific zones."""
    system, _, _ = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.register_sensor("sensor2", SensorType.DOOR, zone_id="B")
    
    system.arm(SecurityMode.AWAY, zones={"A"})
    
    assert "A" in system._armed_zones
    assert "B" not in system._armed_zones


def test_sensor_in_unarmed_zone_ignored():
    """Test that sensor in unarmed zone does not trigger alarm."""
    system, _, siren = make_security_system()
    system.register_sensor("sensor1", SensorType.DOOR, zone_id="A")
    system.register_sensor("sensor2", SensorType.DOOR, zone_id="B")
    system.arm(SecurityMode.AWAY, zones={"A"})  # Only arm zone A
    
    event = SensorEvent(
        sensor_id="sensor2",
        zone_id="B",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])

