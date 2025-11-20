"""
Log - 개별 이벤트 로그 정보 저장
시스템에서 발생하는 이벤트를 기록
"""
from datetime import datetime
from typing import Optional


class Log:
    """
    개별 이벤트 로그를 나타내는 클래스
    """

    def __init__(self, event_id: int = None, event_type: str = "",
                 description: str = "", date_time: datetime = None, user_id: str = None):
        self.event_id = event_id
        self.event_type = event_type
        self.description = description
        self.date_time = date_time if date_time else datetime.now()
        self.user_id = user_id

    # Getters
    def get_event_id(self) -> int:
        return self.event_id

    def get_event_type(self) -> str:
        return self.event_type

    def get_description(self) -> str:
        return self.description

    def get_date_time(self) -> datetime:
        return self.date_time

    def get_user_id(self) -> Optional[str]:
        return self.user_id

    # Setters
    def set_event_id(self, event_id: int):
        self.event_id = event_id

    def set_event_type(self, event_type: str):
        self.event_type = event_type

    def set_description(self, description: str):
        self.description = description

    def set_date_time(self, date_time: datetime):
        self.date_time = date_time

    def set_user_id(self, user_id: str):
        self.user_id = user_id

    def to_dict(self) -> dict:
        """로그를 딕셔너리로 변환"""
        return {
            'event_id': self.event_id,
            'event_type': self.event_type,
            'description': self.description,
            'date_time': self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': self.user_id
        }

    def __repr__(self):
        return (f"Log(id={self.event_id}, type={self.event_type}, "
                f"time={self.date_time.strftime('%Y-%m-%d %H:%M:%S')}, "
                f"user={self.user_id})")

    def __str__(self):
        time_str = self.date_time.strftime('%Y-%m-%d %H:%M:%S')
        user_str = f" [User: {self.user_id}]" if self.user_id else ""
        return f"[{time_str}] {self.event_type}: {self.description}{user_str}"
