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
        self.last_error_message: Optional[str] = None

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
        self.last_error_message = None

        if not self.authenticated_user:
            print("[Error] Login required.")
            self.last_error_message = "Login required"
            return False

        try:
            if mode_str == MODE_DISARMED:
                self.security_system.disarm(cleared_by=self.authenticated_user)
            elif mode_str == MODE_AWAY:
                self.security_system.arm(SecurityMode.AWAY)
            elif mode_str == MODE_STAY:
                self.security_system.arm(SecurityMode.STAY)
            else:
                message = f"Unsupported security mode: {mode_str}"
                print(f"[Error] {message}")
                self.last_error_message = message
                return False
        except RuntimeError as exc:
            message = str(exc)
            self.last_error_message = message
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

    def clear_alarm(self) -> bool:
        """Clear the alarm without disarming the system."""
        if not self.authenticated_user:
            print("[Error] Login required to clear alarm.")
            if self.ui_app:
                self.ui_app.show_alert("Login required to clear alarm")
            return False

        try:
            self.security_system.clear_alarm(cleared_by=self.authenticated_user)
            print(f"[Controller] Alarm cleared by {self.authenticated_user}")
            if self.ui_app:
                self.ui_app.add_log(f"Alarm cleared by {self.authenticated_user}")
                # Update status display
                status = self.security_system.get_status()
                if status:
                    mode_name = status.mode.name
                    self.ui_app.update_status_label(mode_name, status.armed_zones)
            return True
        except Exception as exc:
            message = str(exc)
            print(f"[Controller] Failed to clear alarm: {message}")
            if self.ui_app:
                self.ui_app.show_alert(message)
                self.ui_app.add_log(message)
            return False

    def trigger_panic(self) -> bool:
        """Trigger panic alarm immediately, regardless of system state."""
        if not self.authenticated_user:
            print("[Error] Login required to trigger panic alarm.")
            if self.ui_app:
                self.ui_app.show_alert("Login required to trigger panic alarm")
            return False

        try:
            self.security_system.trigger_panic()
            print(f"[Controller] Panic alarm triggered by {self.authenticated_user}")
            if self.ui_app:
                self.ui_app.add_log(f"Panic alarm triggered by {self.authenticated_user}")
                self.ui_app.show_alert("PANIC ALARM ACTIVATED!")
                # Update status display
                status = self.security_system.get_status()
                if status:
                    mode_name = status.mode.name
                    self.ui_app.update_status_label(mode_name, status.armed_zones)
            return True
        except Exception as exc:
            message = str(exc)
            print(f"[Controller] Failed to trigger panic alarm: {message}")
            if self.ui_app:
                self.ui_app.show_alert(message)
                self.ui_app.add_log(message)
            return False

    def update_sensor_status(self, device_id, device_type, status):
        """Observer Pattern: 센서 신호 수신"""
        sensor_type_enum = self._map_sensor_type(device_type)
        sensor_status_enum = self._map_sensor_status(status, sensor_type_enum)
        
        print(f"[Controller] Sensor status update: {device_id} ({device_type}) -> {status} (mapped: {sensor_status_enum.name})")
        
        event = SensorEvent(
            sensor_id=device_id,
            zone_id=None,  # TODO: map device_id to a zone when available
            sensor_type=sensor_type_enum,
            status=sensor_status_enum,
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

    def _map_sensor_status(self, status: str, sensor_type: SensorType) -> SensorStatus:
        """Map string status to SensorStatus enum, considering sensor type."""
        if status == "Open":
            return SensorStatus.OPEN
        if status == "Motion Detected":
            return SensorStatus.MOTION_DETECTED
        if status == "Triggered":
            # Map "Triggered" based on sensor type
            if sensor_type in (SensorType.DOOR, SensorType.WINDOW):
                return SensorStatus.OPEN
            elif sensor_type == SensorType.MOTION:
                return SensorStatus.MOTION_DETECTED
            else:
                # For other sensors (e.g., camera), treat as OPEN for alarm purposes
                return SensorStatus.OPEN
        if status == "Recording":
            # Camera recording should trigger alarm
            return SensorStatus.OPEN  # Treat as triggering event
        return SensorStatus.NORMAL
