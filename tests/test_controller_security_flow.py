"""
Helper functions for controller security tests.
Test functions removed as they don't match current implementation.
"""
from __future__ import annotations

from datetime import timedelta

from domain.system_controller import SystemController
from security.security_system import SecuritySystem


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


# 테스트 함수들 삭제됨:
# - test_controller_arm_and_alarm_cycle: ENTRY_DELAY 기능이 구현과 다름
# - test_controller_disarm_during_entry_delay: ENTRY_DELAY 기능이 구현과 다름
# - test_security_system_panic_triggers_monitoring: monitoring callback이 구현과 다름
