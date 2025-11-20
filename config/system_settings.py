"""
SystemSettings - 시스템 전역 설정 관리
모니터링 서비스 전화번호, 집주인 전화번호, 시스템 잠금 시간, 알람 지연 시간 등
"""
from storage.storage_manager import StorageManager
from typing import Optional


class SystemSettings:
    """
    시스템 전역 설정을 관리하는 클래스
    데이터베이스와 연동하여 설정 정보를 저장/로드
    """

    def __init__(self):
        self.monitoring_service_phone: str = "911"
        self.homeowner_phone: str = "010-0000-0000"
        self.system_lock_time: int = 30  # 초 단위
        self.alarm_delay_time: int = 60  # 초 단위
        self.storage = StorageManager()

    # Getters
    def get_monitoring_service_phone(self) -> str:
        return self.monitoring_service_phone

    def get_homeowner_phone(self) -> str:
        return self.homeowner_phone

    def get_system_lock_time(self) -> int:
        return self.system_lock_time

    def get_alarm_delay_time(self) -> int:
        return self.alarm_delay_time

    # Setters
    def set_monitoring_service_phone(self, phone: str):
        """모니터링 서비스 전화번호 설정"""
        if self._validate_phone(phone):
            self.monitoring_service_phone = phone
        else:
            print("[SystemSettings] Invalid phone number format.")

    def set_homeowner_phone(self, phone: str):
        """집주인 전화번호 설정"""
        if self._validate_phone(phone):
            self.homeowner_phone = phone
        else:
            print("[SystemSettings] Invalid phone number format.")

    def set_system_lock_time(self, seconds: int):
        """시스템 잠금 시간 설정 (초)"""
        if seconds > 0:
            self.system_lock_time = seconds
        else:
            print("[SystemSettings] System lock time must be positive.")

    def set_alarm_delay_time(self, seconds: int):
        """알람 지연 시간 설정 (초)"""
        if seconds >= 0:
            self.alarm_delay_time = seconds
        else:
            print("[SystemSettings] Alarm delay time must be non-negative.")

    def _validate_phone(self, phone: str) -> bool:
        """
        전화번호 형식 간단 검증
        실제로는 더 정교한 검증 필요
        """
        # 숫자와 하이픈만 포함되어 있는지 확인
        import re
        pattern = r'^[\d\-+() ]+$'
        return bool(re.match(pattern, phone)) and len(phone) >= 3

    def load(self) -> bool:
        """
        데이터베이스에서 시스템 설정 로드
        :return: 성공 여부
        """
        sql = """
            SELECT monitoring_service_phone, homeowner_phone,
                   system_lock_time, alarm_delay_time
            FROM system_settings
            ORDER BY setting_id DESC
            LIMIT 1
        """
        result = self.storage.execute_query(sql)

        if result and len(result) > 0:
            row = result[0]
            self.monitoring_service_phone = row['monitoring_service_phone']
            self.homeowner_phone = row['homeowner_phone']
            self.system_lock_time = row['system_lock_time']
            self.alarm_delay_time = row['alarm_delay_time']
            print("[SystemSettings] Settings loaded successfully.")
            return True
        else:
            print("[SystemSettings] No settings found in database, using defaults.")
            return False

    def save(self) -> bool:
        """
        현재 시스템 설정을 데이터베이스에 저장
        기존 설정을 업데이트하거나 새로 삽입
        :return: 성공 여부
        """
        # 기존 설정 확인
        check_sql = "SELECT setting_id FROM system_settings LIMIT 1"
        result = self.storage.execute_query(check_sql)

        if result and len(result) > 0:
            # UPDATE
            sql = """
                UPDATE system_settings
                SET monitoring_service_phone = ?,
                    homeowner_phone = ?,
                    system_lock_time = ?,
                    alarm_delay_time = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE setting_id = (SELECT setting_id FROM system_settings LIMIT 1)
            """
        else:
            # INSERT
            sql = """
                INSERT INTO system_settings
                (monitoring_service_phone, homeowner_phone, system_lock_time, alarm_delay_time)
                VALUES (?, ?, ?, ?)
            """

        rows = self.storage.execute_update(
            sql,
            (self.monitoring_service_phone, self.homeowner_phone,
             self.system_lock_time, self.alarm_delay_time)
        )

        if rows > 0:
            print("[SystemSettings] Settings saved successfully.")
            return True
        else:
            print("[SystemSettings] Failed to save settings.")
            return False

    def __repr__(self):
        return (f"SystemSettings(monitoring={self.monitoring_service_phone}, "
                f"homeowner={self.homeowner_phone}, "
                f"lock_time={self.system_lock_time}s, "
                f"alarm_delay={self.alarm_delay_time}s)")
