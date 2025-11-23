from __future__ import annotations

from datetime import datetime
from typing import Optional

from domain.user_manager import UserManager
from security.events import SensorEvent, SensorStatus, SensorType
from security.security_system import SecurityMode, SecuritySystem
from utils.constants import MODE_AWAY, MODE_DISARMED, MODE_STAY


class SystemController:
    """Thin adapter between UI/UC1 authentication and the SecuritySystem."""

    def __init__(
        self,
        security_system: SecuritySystem,
        ui_app=None,
        user_manager: Optional[UserManager] = None,
    ):
        self.security_system = security_system
        self.ui_app = ui_app
        self.user_manager = user_manager or UserManager()
        self.authenticated_user: Optional[str] = None
        self.cameras = []  # 카메라 리스트 별도 관리

    def set_ui(self, ui_app):
        self.ui_app = ui_app

    def add_camera(self, camera):
        self.cameras.append(camera)

    def login(self, user_id, password):
        if self.user_manager.authenticate(user_id, password):
            self.authenticated_user = user_id
            print(f"[Controller] User '{user_id}' logged in.")
            return True
        return False

    def set_security_mode(self, mode_str):
        if not self.authenticated_user:
            print("[Error] Login required.")
            return False

        try:
            if mode_str == MODE_DISARMED:
                self.security_system.disarm(cleared_by=self.authenticated_user)
            elif mode_str == MODE_AWAY:
                self.security_system.arm(SecurityMode.AWAY)
            elif mode_str == MODE_STAY:
                self.security_system.arm(SecurityMode.STAY)
            else:
                print(f"[Error] Unsupported security mode: {mode_str}")
                return False
        except RuntimeError as exc:
            message = str(exc)
            print(f"[Controller] Failed to change mode: {message}")
            if self.ui_app:
                self.ui_app.show_alert(message)
                self.ui_app.add_log(message)
            return False

        mode_name = self.security_system.mode.name
        print(f"[Controller] State changed to: {mode_name}")
        if self.ui_app:
            self.ui_app.update_status_label(mode_name)
        return True

    def update_sensor_status(self, device_id, device_type, status):
        """Observer Pattern: 센서 신호 수신"""
        event = SensorEvent(
            sensor_id=device_id,
            zone_id=None,  # TODO: map device_id to a zone when available
            sensor_type=self._map_sensor_type(device_type),
            status=self._map_sensor_status(status),
            timestamp=datetime.utcnow(),
        )
        self.security_system.handle_sensor_event(event)
        if self.ui_app:
            self.ui_app.add_log(f"Sensor {device_id} -> {status}")

    def trigger_camera(self, trigger_source):
        """침입 발생 시 모든 카메라 촬영"""
        for cam in self.cameras:
            cam.take_picture()

    def _map_sensor_type(self, device_type: str) -> SensorType:
        if device_type == "Window/Door Sensor":
            return SensorType.DOOR
        if device_type == "Motion Detector":
            return SensorType.MOTION
        return SensorType.OTHER

    def _map_sensor_status(self, status: str) -> SensorStatus:
        if status == "Open":
            return SensorStatus.OPEN
        if status == "Motion Detected":
            return SensorStatus.MOTION_DETECTED
        return SensorStatus.NORMAL
