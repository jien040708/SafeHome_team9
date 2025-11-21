# security/interfaces.py

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, runtime_checkable, Optional, Set

from .events import SensorEvent
from .security_system import SecurityMode, AlarmState, IntrusionRecord


@runtime_checkable
class AuthContext(Protocol):
    """
    UC1에서 제공하는 인증 컨텍스트.
    Security 쪽에서는 '누가 인증된 상태인가?'만 알면 된다.
    """

    def require_authenticated_user(self) -> str:
        """
        현재 인증된 사용자의 ID/username을 반환.
        인증이 안 되어 있으면 예외를 던져야 한다.
        """
        ...


@runtime_checkable
class CameraGateway(Protocol):
    """
    UC3와 연결되는 카메라 게이트웨이.
    Security는 '침입 발생 → 카메라에게 알려라' 수준만 알면 된다.
    """

    def trigger_all(self, source: str) -> None:
        """
        모든 관련 카메라에 보안 이벤트를 알림.

        예시 source 값:
        - "INTRUSION"
        - "PANIC"
        """
        ...


@dataclass
class SecurityStatus:
    """
    UI/다른 서브시스템에 현재 보안 상태를 넘겨주는 DTO.
    """

    mode: SecurityMode
    alarm_state: AlarmState
    armed_zones: Set[str]
    entry_delay_deadline: Optional[datetime]
    monitoring_call_scheduled: bool


@runtime_checkable
class SecurityEventListener(Protocol):
    """
    UI/UC3가 Subscribe하는 보안 이벤트 리스너 인터페이스.
    """

    def on_status_changed(self, status: SecurityStatus) -> None:
        ...

    def on_intrusion_logged(self, record: IntrusionRecord) -> None:
        ...

    def on_entry_delay_started(self, event: SensorEvent, deadline: datetime) -> None:
        ...

    def on_alarm_activated(self, event: Optional[SensorEvent]) -> None:
        ...

    def on_alarm_cleared(self, cleared_by: str) -> None:
        ...
