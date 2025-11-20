"""
ConfigurationManager - 시스템 설정 관리
SystemSettings, SafeHomeMode, SafetyZone 정보를 총괄 관리
"""
from typing import List, Optional
from config.system_settings import SystemSettings
from storage.storage_manager import StorageManager
from utils.constants import MODE_DISARMED, MODE_AWAY, MODE_STAY


class SafeHomeMode:
    """SafeHome 모드 정보"""
    def __init__(self, mode_id: int, mode_name: str, description: str):
        self.mode_id = mode_id
        self.mode_name = mode_name
        self.description = description

    def __repr__(self):
        return f"SafeHomeMode(id={self.mode_id}, name={self.mode_name})"


class SafetyZone:
    """안전 구역 정보"""
    def __init__(self, zone_id: int, zone_name: str, is_armed: bool):
        self.zone_id = zone_id
        self.zone_name = zone_name
        self.is_armed = is_armed

    def arm(self):
        self.is_armed = True

    def disarm(self):
        self.is_armed = False

    def __repr__(self):
        armed_status = "Armed" if self.is_armed else "Disarmed"
        return f"SafetyZone(id={self.zone_id}, name={self.zone_name}, {armed_status})"


class ConfigurationManager:
    """
    시스템 전체 구성 정보를 관리하는 매니저 클래스
    """

    def __init__(self):
        self.system_settings = SystemSettings()
        self.safehome_modes: List[SafeHomeMode] = []
        self.safety_zones: List[SafetyZone] = []
        self.current_mode_name: str = MODE_DISARMED
        self.storage = StorageManager()

    def initialize_configuration(self) -> bool:
        """
        시스템 구성 초기화
        데이터베이스에서 모든 설정 정보를 로드
        """
        print("[ConfigurationManager] Initializing configuration...")

        # 시스템 설정 로드
        self.system_settings.load()

        # SafeHome 모드 로드
        self._load_safehome_modes()

        # Safety Zone 로드
        self._load_safety_zones()

        print("[ConfigurationManager] Configuration initialized successfully.")
        return True

    def _load_safehome_modes(self):
        """데이터베이스에서 SafeHome 모드 목록 로드"""
        sql = "SELECT mode_id, mode_name, description FROM safehome_modes"
        result = self.storage.execute_query(sql)

        self.safehome_modes.clear()
        if result:
            for row in result:
                mode = SafeHomeMode(
                    mode_id=row['mode_id'],
                    mode_name=row['mode_name'],
                    description=row['description']
                )
                self.safehome_modes.append(mode)
            print(f"[ConfigurationManager] Loaded {len(self.safehome_modes)} SafeHome modes.")

    def _load_safety_zones(self):
        """데이터베이스에서 Safety Zone 목록 로드"""
        sql = "SELECT zone_id, zone_name, is_armed FROM safety_zones"
        result = self.storage.execute_query(sql)

        self.safety_zones.clear()
        if result:
            for row in result:
                zone = SafetyZone(
                    zone_id=row['zone_id'],
                    zone_name=row['zone_name'],
                    is_armed=bool(row['is_armed'])
                )
                self.safety_zones.append(zone)
            print(f"[ConfigurationManager] Loaded {len(self.safety_zones)} safety zones.")

    def update_system_settings(self, settings: SystemSettings) -> bool:
        """
        시스템 설정 업데이트
        :param settings: 새 SystemSettings 객체
        :return: 성공 여부
        """
        self.system_settings = settings
        return self.system_settings.save()

    def update_safehome_mode(self, mode_name: str) -> bool:
        """
        현재 SafeHome 모드 변경
        :param mode_name: 모드 이름 (Disarmed, Away, Stay 등)
        :return: 성공 여부
        """
        # 유효한 모드인지 확인
        valid_modes = [m.mode_name for m in self.safehome_modes]
        if mode_name in valid_modes:
            self.current_mode_name = mode_name
            print(f"[ConfigurationManager] SafeHome mode changed to: {mode_name}")
            return True
        else:
            print(f"[ConfigurationManager] Invalid mode name: {mode_name}")
            return False

    def modify_safety_zone(self, zone_id: int, zone_name: str = None, is_armed: bool = None) -> bool:
        """
        Safety Zone 정보 수정
        :param zone_id: 구역 ID
        :param zone_name: 새 구역 이름 (optional)
        :param is_armed: 무장 여부 (optional)
        :return: 성공 여부
        """
        zone = self.get_safety_zone_by_id(zone_id)
        if not zone:
            print(f"[ConfigurationManager] Safety zone {zone_id} not found.")
            return False

        # 수정 사항 적용
        if zone_name:
            zone.zone_name = zone_name
        if is_armed is not None:
            if is_armed:
                zone.arm()
            else:
                zone.disarm()

        # 데이터베이스 업데이트
        sql = "UPDATE safety_zones SET zone_name = ?, is_armed = ? WHERE zone_id = ?"
        rows = self.storage.execute_update(sql, (zone.zone_name, int(zone.is_armed), zone_id))

        if rows > 0:
            print(f"[ConfigurationManager] Safety zone {zone_id} updated.")
            return True
        else:
            print(f"[ConfigurationManager] Failed to update safety zone {zone_id}.")
            return False

    def add_safety_zone(self, zone_name: str) -> bool:
        """
        새 Safety Zone 추가
        :param zone_name: 구역 이름
        :return: 성공 여부
        """
        sql = "INSERT INTO safety_zones (zone_name, is_armed) VALUES (?, 0)"
        rows = self.storage.execute_update(sql, (zone_name,))

        if rows > 0:
            zone_id = self.storage.get_last_insert_id()
            new_zone = SafetyZone(zone_id, zone_name, False)
            self.safety_zones.append(new_zone)
            print(f"[ConfigurationManager] Safety zone '{zone_name}' added.")
            return True
        else:
            print(f"[ConfigurationManager] Failed to add safety zone '{zone_name}'.")
            return False

    def delete_safety_zone(self, zone_id: int) -> bool:
        """
        Safety Zone 삭제
        :param zone_id: 구역 ID
        :return: 성공 여부
        """
        sql = "DELETE FROM safety_zones WHERE zone_id = ?"
        rows = self.storage.execute_update(sql, (zone_id,))

        if rows > 0:
            self.safety_zones = [z for z in self.safety_zones if z.zone_id != zone_id]
            print(f"[ConfigurationManager] Safety zone {zone_id} deleted.")
            return True
        else:
            print(f"[ConfigurationManager] Failed to delete safety zone {zone_id}.")
            return False

    # Getters
    def get_system_setting(self) -> SystemSettings:
        """현재 시스템 설정 반환"""
        return self.system_settings

    def get_current_safehome_mode(self) -> str:
        """현재 SafeHome 모드 이름 반환"""
        return self.current_mode_name

    def get_safehome_modes(self) -> List[SafeHomeMode]:
        """모든 SafeHome 모드 목록 반환"""
        return self.safehome_modes

    def get_safety_zone_info(self) -> List[SafetyZone]:
        """모든 Safety Zone 정보 반환"""
        return self.safety_zones

    def get_safety_zone_by_id(self, zone_id: int) -> Optional[SafetyZone]:
        """특정 ID의 Safety Zone 반환"""
        for zone in self.safety_zones:
            if zone.zone_id == zone_id:
                return zone
        return None

    def __repr__(self):
        return (f"ConfigurationManager(current_mode={self.current_mode_name}, "
                f"zones={len(self.safety_zones)}, modes={len(self.safehome_modes)})")
