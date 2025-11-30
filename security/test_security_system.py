# tests/security/test_security_system.py

from __future__ import annotations

from datetime import datetime, timedelta

from security.security_system import (
    Alarm,
    AlarmState,
    SecurityMode,
    SecuritySystem,
)
from security.events import (
    SensorEvent,
    SensorStatus,
    SensorType,
)


class DummyMonitoring:
    def __init__(self) -> None:
        self.calls: list[str] = []

    def __call__(self, reason: str) -> None:
        self.calls.append(reason)


class DummySiren:
    def __init__(self) -> None:
        self.active = False

    def activate(self) -> None:
        self.active = True

    def deactivate(self) -> None:
        self.active = False


def make_security_system(
    delay_seconds: int = 30,
    sensor_states: dict[str, SensorStatus] | None = None,
) -> tuple[SecuritySystem, DummyMonitoring, DummySiren]:
    monitoring = DummyMonitoring()
    siren = DummySiren()

    def get_delay() -> timedelta:
        return timedelta(seconds=delay_seconds)

    def call_monitoring(reason: str) -> None:
        monitoring(reason)

    def activate_siren() -> None:
        siren.activate()

    def deactivate_siren() -> None:
        siren.deactivate()

    def get_sensor_states() -> dict[str, SensorStatus]:
        return sensor_states or {}

    system = SecuritySystem(
        get_delay_time=get_delay,
        call_monitoring_service=call_monitoring,
        activate_siren=activate_siren,
        deactivate_siren=deactivate_siren,
        get_monitored_sensors_state=get_sensor_states,
    )
    return system, monitoring, siren


def test_arm_disarm_basic():
    # TODO: Codex will help fill this test and additional ones.
    system, monitoring, siren = make_security_system()
    system.arm(SecurityMode.AWAY)
    assert system.mode is SecurityMode.AWAY

    system.disarm()
    assert system.mode is SecurityMode.DISARMED
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False
    assert monitoring.calls == []


def test_entry_delay_disarm_prevents_alarm():
    system, monitoring, siren = make_security_system(delay_seconds=5)
    system.arm(SecurityMode.AWAY)

    event = SensorEvent(
        sensor_id="door1",
        zone_id=None,
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    assert system.alarm_state is AlarmState.ENTRY_DELAY
    assert siren.active is False
    assert monitoring.calls == []

    system.disarm(cleared_by="tester")

    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False
    assert monitoring.calls == []


def test_entry_delay_expires_triggers_alarm():
    system, monitoring, siren = make_security_system(delay_seconds=1)
    system.arm(SecurityMode.AWAY)

    event = SensorEvent(
        sensor_id="door1",
        zone_id=None,
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)

    system.tick(event.timestamp + timedelta(seconds=2))

    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True
    assert monitoring.calls == ["INTRUSION_ALARM"]


def test_home_mode_door_triggers_delay_but_motion_ignored():
    system, monitoring, siren = make_security_system(delay_seconds=5)
    system.register_sensor("front-door", SensorType.DOOR, zone_id="A")
    system.register_sensor("hall-motion", SensorType.MOTION, zone_id="A")
    system.assign_sensor_to_zone("front-door", "A")
    system.assign_sensor_to_zone("hall-motion", "A")

    system.arm(SecurityMode.HOME, zones={"A"})

    door_event = SensorEvent(
        sensor_id="front-door",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(door_event)
    assert system.alarm_state is AlarmState.ENTRY_DELAY

    motion_event = SensorEvent(
        sensor_id="hall-motion",
        zone_id="A",
        sensor_type=SensorType.MOTION,
        status=SensorStatus.MOTION_DETECTED,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(motion_event)
    assert system.alarm_state is AlarmState.ENTRY_DELAY
    assert monitoring.calls == []
    assert siren.active is False


def test_home_mode_motion_ignored():
    system, monitoring, siren = make_security_system(delay_seconds=5)
    system.register_sensor("hall-motion", SensorType.MOTION, zone_id="A")
    system.assign_sensor_to_zone("hall-motion", "A")

    system.arm(SecurityMode.STAY, zones={"A"})

    motion_event = SensorEvent(
        sensor_id="hall-motion",
        zone_id="A",
        sensor_type=SensorType.MOTION,
        status=SensorStatus.MOTION_DETECTED,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(motion_event)
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False
    assert monitoring.calls == []


def test_away_mode_motion_triggers_entry_delay_and_alarm():
    system, monitoring, siren = make_security_system(delay_seconds=1)
    system.register_sensor("hall-motion", SensorType.MOTION, zone_id="A")
    system.assign_sensor_to_zone("hall-motion", "A")

    system.arm(SecurityMode.AWAY, zones={"A"})

    event = SensorEvent(
        sensor_id="hall-motion",
        zone_id="A",
        sensor_type=SensorType.MOTION,
        status=SensorStatus.MOTION_DETECTED,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    assert system.alarm_state is AlarmState.ENTRY_DELAY

    system.tick(event.timestamp + timedelta(seconds=2))
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True
    assert monitoring.calls == ["INTRUSION_ALARM"]


def test_zone_specific_arming_blocks_other_zones():
    system, monitoring, siren = make_security_system(delay_seconds=1)
    system.register_sensor("door-A", SensorType.DOOR, zone_id="A")
    system.register_sensor("door-B", SensorType.DOOR, zone_id="B")
    system.assign_sensor_to_zone("door-A", "A")
    system.assign_sensor_to_zone("door-B", "B")

    system.arm(SecurityMode.AWAY, zones={"A"})

    off_zone_event = SensorEvent(
        sensor_id="door-B",
        zone_id="B",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(off_zone_event)
    assert system.alarm_state is AlarmState.IDLE

    on_zone_event = SensorEvent(
        sensor_id="door-A",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(on_zone_event)
    assert system.alarm_state is AlarmState.ENTRY_DELAY

    system.tick(on_zone_event.timestamp + timedelta(seconds=2))
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True


def test_readiness_check_blocks_arming_when_door_open():
    sensor_states = {"door-A": SensorStatus.OPEN}
    system, monitoring, siren = make_security_system(sensor_states=sensor_states)
    system.register_sensor("door-A", SensorType.DOOR, zone_id="A")
    system.assign_sensor_to_zone("door-A", "A")

    try:
        system.arm(SecurityMode.AWAY, zones={"A"})
    except RuntimeError:
        pass
    else:
        raise AssertionError("Arming should fail when door is open")

    assert system.mode is SecurityMode.DISARMED
    assert siren.active is False
    assert monitoring.calls == []


def test_trigger_panic_from_disarmed():
    system, monitoring, siren = make_security_system()

    system.trigger_panic()

    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True
    assert monitoring.calls == ["PANIC"]


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


def test_sensor_trigger_immediate_alarm_no_delay():
    """Test that sensor trigger activates alarm immediately when delay is 0."""
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


def test_alarm_class_basic_functionality():
    """Test Alarm class basic functionality."""
    alarm = Alarm(alarm_id=1, x_coord=100, y_coord=200)
    assert alarm.get_id() == 1
    assert alarm.get_location() == (100, 200)
    assert alarm.is_ringing() is False

    alarm.ring_alarm(True)
    assert alarm.is_ringing() is True

    alarm.ring_alarm(False)
    assert alarm.is_ringing() is False

    assert alarm.set_id(5) is True
    assert alarm.get_id() == 5

    assert alarm.set_id(-1) is False
    assert alarm.get_id() == 5  # Should remain unchanged
