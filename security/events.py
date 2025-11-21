# safehome/security/events.py
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class SensorType(Enum):
    """Type of sensor in the security system."""
    DOOR = auto()
    WINDOW = auto()
    MOTION = auto()
    OTHER = auto()


class SensorStatus(Enum):
    """Current status of a sensor."""
    NORMAL = auto()
    OPEN = auto()          # For door/window
    MOTION_DETECTED = auto()
    TAMPERED = auto()


@dataclass
class SensorEvent:
    """
    Domain event representing a sensor change reported by the system.

    This is independent from UI/virtual device details and can be used
    for unit tests and pure domain logic.
    """
    sensor_id: str
    zone_id: str | None
    sensor_type: SensorType
    status: SensorStatus
    timestamp: datetime
