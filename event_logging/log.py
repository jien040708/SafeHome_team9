from __future__ import annotations

from datetime import datetime
from typing import Optional


class Log:
    """Value object for audit log records."""

    def __init__(
        self,
        event_id: Optional[int] = None,
        event_type: str = "",
        description: str = "",
        date_time: Optional[datetime] = None,
        user_id: Optional[str] = None,
        interface_type: str = "control_panel",
    ) -> None:
        self.event_id = event_id
        self.event_type = event_type
        self.description = description
        self.date_time = date_time if date_time else datetime.now()
        self.user_id = user_id
        self.interface_type = interface_type

    # Getters
    def get_event_id(self) -> Optional[int]:
        return self.event_id

    def get_event_type(self) -> str:
        return self.event_type

    def get_description(self) -> str:
        return self.description

    def get_date_time(self) -> datetime:
        return self.date_time

    def get_user_id(self) -> Optional[str]:
        return self.user_id

    def get_interface_type(self) -> str:
        return self.interface_type

    # Setters
    def set_event_id(self, event_id: int) -> None:
        self.event_id = event_id

    def set_event_type(self, event_type: str) -> None:
        self.event_type = event_type

    def set_description(self, description: str) -> None:
        self.description = description

    def set_date_time(self, date_time: datetime) -> None:
        self.date_time = date_time

    def set_user_id(self, user_id: Optional[str]) -> None:
        self.user_id = user_id

    def set_interface_type(self, interface_type: str) -> None:
        self.interface_type = interface_type

    def to_dict(self) -> dict:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "description": self.description,
            "date_time": self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
            "user_id": self.user_id,
            "interface_type": self.interface_type,
        }

    def __repr__(self) -> str:
        return (
            f"Log(id={self.event_id}, type={self.event_type}, "
            f"time={self.date_time.strftime('%Y-%m-%d %H:%M:%S')}, "
            f"user={self.user_id}, interface={self.interface_type})"
        )

    def __str__(self) -> str:
        time_str = self.date_time.strftime("%Y-%m-%d %H:%M:%S")
        user_str = f" [User: {self.user_id}]" if self.user_id else ""
        interface_str = f" [{self.interface_type}]" if self.interface_type else ""
        return f"[{time_str}] {self.event_type}: {self.description}{user_str}{interface_str}"
