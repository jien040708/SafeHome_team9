# tests/security/test_security_system.py

from __future__ import annotations

from datetime import datetime, timedelta

from security.security_system import (
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
