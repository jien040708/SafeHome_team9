from __future__ import annotations

from datetime import datetime, timedelta

from domain.system_controller import SystemController
from security.events import SensorEvent, SensorStatus, SensorType
from security.security_system import AlarmState, SecuritySystem
from utils.constants import MODE_AWAY, MODE_DISARMED, MODE_STAY


class StubUserManager:
    def authenticate(self, *_args, **_kwargs):
        return True


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


def make_security_system(delay_seconds: int = 2):
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


def make_controller(security_system: SecuritySystem) -> SystemController:
    controller = SystemController(
        security_system=security_system,
        user_manager=StubUserManager(),
    )
    controller.authenticated_user = "tester"
    return controller


def test_controller_arm_and_alarm_cycle():
    system, monitoring, siren = make_security_system(delay_seconds=1)
    controller = make_controller(system)

    system.register_sensor("door-1", SensorType.DOOR, zone_id="A")
    assert controller.set_security_mode(MODE_AWAY)

    event = SensorEvent(
        sensor_id="door-1",
        zone_id="A",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    assert system.alarm_state is AlarmState.ENTRY_DELAY

    system.tick(event.timestamp + timedelta(seconds=2))
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True
    assert monitoring.calls == ["INTRUSION_ALARM"]


def test_controller_disarm_during_entry_delay():
    system, monitoring, siren = make_security_system(delay_seconds=3)
    controller = make_controller(system)

    system.register_sensor("door-2", SensorType.DOOR, zone_id="B")
    assert controller.set_security_mode(MODE_STAY)

    event = SensorEvent(
        sensor_id="door-2",
        zone_id="B",
        sensor_type=SensorType.DOOR,
        status=SensorStatus.OPEN,
        timestamp=datetime.utcnow(),
    )
    system.handle_sensor_event(event)
    assert system.alarm_state is AlarmState.ENTRY_DELAY

    assert controller.set_security_mode(MODE_DISARMED)
    assert system.alarm_state is AlarmState.IDLE
    assert siren.active is False
    assert monitoring.calls == []


def test_security_system_panic_triggers_monitoring():
    system, monitoring, siren = make_security_system()
    system.trigger_panic()
    assert system.alarm_state is AlarmState.ALARM_ACTIVE
    assert siren.active is True
    assert monitoring.calls == ["PANIC"]
