"""
System - SafeHome 시스템 메인 클래스
전체 시스템의 생명주기, 컴포넌트 관리, 7가지 Common Functions 구현
"""
from __future__ import annotations
import time
from datetime import timedelta
from typing import Optional
from enum import Enum

from storage.storage_manager import StorageManager
from auth.login_manager import LoginManager
from event_logging.log_manager import LogManager
from config.configuration_manager import ConfigurationManager
from domain.system_controller import SystemController
from utils.constants import *
from domain.device_manager import DeviceManager
from devices.siren import Siren
from security.security_system import SecuritySystem
from security.events import SensorStatus
from surveillance.camera_controller import CameraController
from domain.services.auth_service import AuthService
from domain.services.settings_service import SettingsService


class SystemCameraGateway:
    """Adapter that forwards SecuritySystem triggers to UC3 components."""

    def __init__(self, system: "System") -> None:
        self._system = system

    def trigger_all(self, source: str) -> None:
        controller = getattr(self._system, "system_controller", None)
        if controller:
            try:
                controller.trigger_camera(source)
            except Exception as exc:  # pragma: no cover - defensive
                print(f"[SecurityCameraGateway] Controller trigger failed: {exc}")

        camera_controller = getattr(self._system, "camera_controller", None)
        if camera_controller and hasattr(camera_controller, "trigger_security_event"):
            try:
                camera_controller.trigger_security_event(source)
            except Exception as exc:  # pragma: no cover - defensive
                print(f"[SecurityCameraGateway] Camera controller trigger failed: {exc}")



class SystemState(Enum):
    """시스템 상태"""
    OFF = "Off"
    INITIALIZING = "Initializing"
    READY = "Ready"
    ACTIVE = "Active"
    LOCKED = "Locked"
    SHUTDOWN = "Shutdown"


class System:
    """
    SafeHome 시스템 메인 클래스
    모든 컴포넌트를 초기화하고 관리하며, Common Functions를 제공
    """

    def __init__(self):
        # 시스템 상태
        self.system_state = SystemState.OFF

        # 핵심 컴포넌트
        self.storage_manager: Optional[StorageManager] = None
        self.login_manager: Optional[LoginManager] = None
        self.log_manager: Optional[LogManager] = None
        self.configuration_manager: Optional[ConfigurationManager] = None
        self.system_controller: Optional[SystemController] = None
        self.security_system: Optional[SecuritySystem] = None
        self.camera_controller: Optional[CameraController] = None

        self.device_manager = None
        self.sensors = []
        self.siren: Optional[Siren] = None
        self.security_listener = None
        self.camera_gateway = SystemCameraGateway(self)

        # UI ??
        self.ui_app = None
        self._auth_service: Optional[AuthService] = None
        self._settings_service: Optional[SettingsService] = None

    # ========================================
    # Common Function 1 & 2: Login (Control Panel / Web Browser)
    # ========================================
    def login(self, username: str, password: str, interface: str = 'control_panel') -> bool:
        """
        제어 패널 또는 웹 브라우저를 통한 로그인 (하위 호환용)
        :param username: 사용자 ID
        :param password: 비밀번호
        :param interface: 'control_panel' or 'web_browser'
        :return: 로그인 성공 여부
        """
        result = self.login_with_details(username, password, interface)
        return result['success']

    def login_with_details(self, username: str, password: str, interface: str = 'control_panel') -> dict:
        """
        제어 패널 또는 웹 브라우저를 통한 로그인 (상세 정보 반환)
        :param username: 사용자 ID
        :param password: 비밀번호
        :param interface: 'control_panel' or 'web_browser'
        :return: 로그인 결과 딕셔너리
        """
        if self.system_state == SystemState.OFF:
            print("[System] System is off. Please turn on the system first.")
            return {
                'success': False,
                'message': 'System is off. Please turn on the system first.',
                'system_off': True
            }

        if self.system_state == SystemState.LOCKED:
            print("[System] System is locked.")
            return {
                'success': False,
                'message': 'System is locked. Please contact administrator.',
                'system_locked': True
            }

        auth_service = self._get_auth_service()
        if not auth_service:
            print("[System] Authentication service unavailable.")
            return {
                'success': False,
                'message': 'Authentication service unavailable.'
            }

        result = auth_service.login(username, password, interface)

        if result.get('success'):
            self.system_state = SystemState.ACTIVE

            if self.system_controller:
                self.system_controller.authenticated_user = username

            print(f"[System] User '{username}' logged in successfully via {interface}.")
        else:
            print(f"[System] Login failed for user '{username}'.")

        return result

    def logout(self):
        """현재 사용자 로그아웃"""
        auth_service = self._get_auth_service()
        if not auth_service:
            return

        user = auth_service.logout()
        if user:
            self.system_state = SystemState.READY
            print(f"[System] User '{user}' logged out.")

    # ========================================
    # Common Function 3: Configure System Setting
    # ========================================
    def configure_system_setting(self, monitoring_phone: str = None,
                                  homeowner_phone: str = None,
                                  lock_time: int = None,
                                  alarm_delay: int = None) -> bool:
        """
        시스템 설정 구성
        :param monitoring_phone: 모니터링 서비스 전화번호
        :param homeowner_phone: 집주인 전화번호
        :param lock_time: 시스템 잠금 시간 (초)
        :param alarm_delay: 알람 지연 시간 (초)
        :return: 성공 여부
        """
        settings_service = self._get_settings_service()
        if not settings_service:
            print("[System] Settings service unavailable.")
            return False

        result = settings_service.update_settings(
            monitoring_phone=monitoring_phone,
            homeowner_phone=homeowner_phone,
            lock_time=lock_time,
            alarm_delay=alarm_delay,
        )

        if result.success:
            print("[System] System settings configured successfully.")
        else:
            print(f"[System] Failed to configure system settings: {result.message}")

        return result.success

    # ========================================
    # Common Function 4: Turn the system on
    # ========================================
    def turn_on(self) -> bool:
        """
        ??? ??
        ?? ???? ??? ? ??
        """
        if self.system_state != SystemState.OFF:
            print(f"[System] System is already {self.system_state.value}.")
            return False

        print("[System] Starting SafeHome system...")
        self.system_state = SystemState.INITIALIZING

        try:
            # 1. StorageManager ??? ? ??
            self.storage_manager = StorageManager()
            if not self.storage_manager.connect():
                raise Exception("Failed to connect to database.")

            # 2. ConfigurationManager ???
            self.configuration_manager = ConfigurationManager()
            self.configuration_manager.initialize_configuration()

            # 3. Siren ? SecuritySystem ???
            self.siren = Siren("MainSiren")

            def get_delay_time():
                settings = self.configuration_manager.get_system_setting()
                delay_seconds = max(settings.get_alarm_delay_time(), 0)
                return timedelta(seconds=delay_seconds)

            def call_monitoring_service(reason: str):
                print(f"[SecuritySystem] Monitoring service notified: {reason}")

            def activate_siren():
                if self.siren:
                    self.siren.activate()

            def deactivate_siren():
                if self.siren:
                    self.siren.deactivate()

            def get_monitored_sensors_state():
                states = {}
                for sensor in self.sensors:
                    get_id = getattr(sensor, "get_id", None)
                    get_status = getattr(sensor, "get_status", None)
                    if not get_id or not get_status:
                        continue
                    raw_status = get_status()
                    if raw_status == STATE_OPEN:
                        mapped = SensorStatus.OPEN
                    elif raw_status == STATE_DETECTED:
                        mapped = SensorStatus.MOTION_DETECTED
                    else:
                        mapped = SensorStatus.NORMAL
                    states[get_id()] = mapped
                return states

            self.security_system = SecuritySystem(
                get_delay_time=get_delay_time,
                call_monitoring_service=call_monitoring_service,
                activate_siren=activate_siren,
                deactivate_siren=deactivate_siren,
                get_monitored_sensors_state=get_monitored_sensors_state,
                camera_gateway=self.camera_gateway,
            )
            self.configuration_manager.configure_security_system(self.security_system)
            self._attach_security_listener()

            # 4. LoginManager ???
            self.login_manager = LoginManager()

            # 5. LogManager ???
            self.log_manager = LogManager()

            # 6. SystemController ??? (?? ?? ??)
            self.system_controller = SystemController(
                security_system=self.security_system,
                ui_app=self.ui_app
            )

            # 6. CameraController 초기화
            self.camera_controller = CameraController()

            # 7. 기본 관리자 계정 생성 (없으면)
            self._initialize_default_user()
            self._refresh_services()

            # 시스템 시작 로그
            self.log_manager.log_event(
                event_type="SYSTEM_START",
                description="SafeHome system started successfully"
            )

            self.system_state = SystemState.READY
            print("[System] SafeHome system is now READY.")
            return True

        except Exception as e:
            print(f"[System] Failed to start system: {e}")
            self.system_state = SystemState.OFF
            return False

    # ========================================
    # Common Function 5: Turn the system off
    # ========================================
    def turn_off(self) -> bool:
        """
        시스템 종료
        모든 컴포넌트를 안전하게 종료
        """
        if self.system_state == SystemState.OFF:
            print("[System] System is already off.")
            return False

        print("[System] Shutting down SafeHome system...")
        self.system_state = SystemState.SHUTDOWN

        try:
            # 시스템 종료 로그 (종료 전 기록)
            if self.log_manager:
                self.log_manager.log_event(
                    event_type="SYSTEM_SHUTDOWN",
                    description="SafeHome system shutting down"
                )

            # 1. 현재 사용자 로그아웃
            if self.login_manager and self.login_manager.is_user_authenticated():
                self.logout()

            # 2. 센서 비활성화 (SystemController를 통해)
            if self.system_controller:
                # 센서 비활성화 로직 (필요 시 추가)
                pass

            # 3. 카메라 비활성화
            if self.system_controller and self.system_controller.cameras:
                for camera in self.system_controller.cameras:
                    camera.deactivate() if hasattr(camera, 'deactivate') else None

            # 4. 알람 비활성화
            if self.siren:
                self.siren.deactivate()

            # 5. 데이터베이스 연결 종료
            if self.storage_manager:
                self.storage_manager.disconnect()

            self.system_state = SystemState.OFF
            print("[System] SafeHome system is now OFF.")
            return True

        except Exception as e:
            print(f"[System] Error during shutdown: {e}")
            self.system_state = SystemState.OFF
            return False

    # ========================================
    # Common Function 6: Reset the system
    # ========================================
    def reset(self) -> bool:
        """
        시스템 재시작
        현재 상태를 저장하고 시스템을 재시작
        """
        print("[System] Resetting SafeHome system...")

        # 현재 설정 백업 (필요 시)
        current_settings = None
        if self.configuration_manager:
            current_settings = self.configuration_manager.get_system_setting()

        # 시스템 종료
        if not self.turn_off():
            print("[System] Failed to turn off system during reset.")
            return False

        # 잠시 대기
        time.sleep(1)

        # 시스템 시작
        if not self.turn_on():
            print("[System] Failed to turn on system during reset.")
            return False

        # 설정 복원 (필요 시)
        if current_settings:
            self.configuration_manager.update_system_settings(current_settings)

        print("[System] SafeHome system reset successfully.")
        return True

    # ========================================
    # Common Function 7: Change master password through control panel
    # ========================================
    def change_password(self, old_password: str, new_password: str) -> bool:
        """
        제어 패널을 통한 마스터 비밀번호 변경
        :param old_password: 현재 비밀번호
        :param new_password: 새 비밀번호
        :return: 성공 여부
        """
        if not self.login_manager.is_user_authenticated():
            print("[System] Authentication required to change password.")
            return False

        success = self.login_manager.change_password(old_password, new_password)

        if success:
            user = self.login_manager.get_current_user().get_username()
            self.log_manager.log_event(
                event_type="PASSWORD_CHANGE",
                description="User password changed successfully",
                user_id=user
            )
            print(f"[System] Password changed successfully for user '{user}'.")
        else:
            print("[System] Failed to change password.")

        return success

    # ========================================
    # 추가 메서드
    # ========================================
    def lock_system(self):
        """시스템 잠금 (로그인 차단)"""
        self.system_state = SystemState.LOCKED
        print("[System] System locked.")

    def unlock_system(self):
        """시스템 잠금 해제"""
        if self.system_state == SystemState.LOCKED:
            self.system_state = SystemState.READY
            print("[System] System unlocked.")

    def get_system_status(self) -> dict:
        """현재 시스템 상태 정보 반환"""
        return {
            'state': self.system_state.value,
            'authenticated': self.login_manager.is_user_authenticated() if self.login_manager else False,
            'current_user': self.login_manager.get_current_user().get_username() if self.login_manager and self.login_manager.is_user_authenticated() else None,
            'security_mode': self.security_system.mode.name if self.security_system else None
        }

    def set_ui(self, ui_app):
        """UI ?? ??"""
        self.ui_app = ui_app
        if self.system_controller:
            self.system_controller.set_ui(ui_app)
        self._attach_security_listener()

    def _attach_security_listener(self):
        """Create or update the Tkinter listener for security events."""
        if not (self.security_system and self.ui_app):
            return
        from ui.main_window import TkSecurityListener
        self.security_listener = TkSecurityListener(self.ui_app)
        self.security_system.set_event_listener(self.security_listener)

    def _get_auth_service(self) -> Optional[AuthService]:
        if not self._auth_service and self.login_manager and self.log_manager:
            self._auth_service = AuthService(self.login_manager, self.log_manager)
        return self._auth_service

    def _get_settings_service(self) -> Optional[SettingsService]:
        if (not self._settings_service and self.configuration_manager
                and self.login_manager and self.log_manager):
            self._settings_service = SettingsService(
                self.configuration_manager,
                self.login_manager,
                self.log_manager,
            )
        return self._settings_service

    def _refresh_services(self):
        """Recreate service layer instances after dependency changes."""
        self._auth_service = None
        self._settings_service = None
        self._get_auth_service()
        self._get_settings_service()

    def _initialize_default_user(self):
        """기본 관리자 계정 생성"""
        from auth.login_interface import LoginInterface

        # admin 계정이 존재하는지 확인 (control_panel 인터페이스)
        login_interface = LoginInterface(user_interface='control_panel')
        if not login_interface.load('admin', interface_type='control_panel'):
            # admin 계정 생성
            success = self.login_manager.create_user(
                username='admin',
                password='1234',
                interface='control_panel',
                access_level=10  # 최고 권한
            )
            if success:
                print("[System] Default admin account created (admin/1234).")

    def __repr__(self):
        return f"System(state={self.system_state.value})"
