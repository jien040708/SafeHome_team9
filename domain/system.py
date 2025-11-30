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
from utils.constants import STATE_OPEN, STATE_DETECTED
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
        self.alarms: List = []  # List of Alarm instances (composition: 1:*)
        self.security_listener = None
        self.camera_gateway = SystemCameraGateway(self)

        # UI 참조
        self.ui_app = None
        self._auth_service: Optional[AuthService] = None
        self._settings_service: Optional[SettingsService] = None

        # turn_on 완료 후 호출될 콜백 (디바이스 초기화 등)
        self.on_turn_on_complete = None

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

            # 3. Siren & Alarm initialization for SecuritySystem
            self.siren = Siren("MainSiren")
            
            # Initialize Alarm instances (composition: System has multiple Alarms)
            from security.security_system import Alarm
            # Create default alarms - can be configured later
            self.alarms = [
                Alarm(alarm_id=1, x_coord=100, y_coord=100),  # Main alarm
                Alarm(alarm_id=2, x_coord=200, y_coord=200),  # Secondary alarm
            ]

            def get_delay_time():
                settings = self.configuration_manager.get_system_setting()
                delay_seconds = max(settings.get_alarm_delay_time(), 0)
                return timedelta(seconds=delay_seconds)

            def call_monitoring_service(reason: str):
                message = f"[SecuritySystem] Monitoring service notified: {reason}"
                print(message)
                import sys
                sys.stdout.write(message + "\n")
                sys.stdout.flush()

            def activate_siren():
                # Activate siren
                if self.siren:
                    self.siren.activate()
                # Activate all alarms using Alarm class (ring all alarms)
                print(f"[System] Activating {len(self.alarms)} Alarm instance(s)...")
                for alarm in self.alarms:
                    if alarm:
                        alarm.ring_alarm(True)
                        print(f"[System] Alarm {alarm.get_id()} at {alarm.get_location()} is now ringing.")
                print("[SecuritySystem] Siren activated - Alarm is sounding!")
                import sys
                sys.stdout.write("[SecuritySystem] Siren activated - Alarm is sounding!\n")
                sys.stdout.flush()

            def deactivate_siren():
                # Deactivate siren
                if self.siren:
                    self.siren.deactivate()
                # Deactivate all alarms using Alarm class (silence all alarms)
                print(f"[System] Deactivating {len(self.alarms)} Alarm instance(s)...")
                for alarm in self.alarms:
                    if alarm:
                        alarm.ring_alarm(False)
                        print(f"[System] Alarm {alarm.get_id()} at {alarm.get_location()} is now silenced.")

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

            # turn_on 완료 콜백 호출 (디바이스 초기화 등)
            if self.on_turn_on_complete:
                try:
                    self.on_turn_on_complete()
                except Exception as callback_error:
                    print(f"[System] on_turn_on_complete callback error: {callback_error}")

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
        Sequence: Save Config -> Deactivate Sensors -> Disable Cameras ->
                  Deactivate Alarm -> Logout -> Log Event -> Disconnect DB
        """
        if self.system_state == SystemState.OFF:
            print("[System] System is already off.")
            return False

        print("[System] Shutting down SafeHome system...")
        self.system_state = SystemState.SHUTDOWN

        try:
            # 1. 설정 저장 (Save Configuration)
            if self.configuration_manager:
                settings = self.configuration_manager.get_system_setting()
                self.configuration_manager.update_system_settings(settings)
                print("[System] Configuration saved.")

            # 2. 센서 비활성화 (Deactivate Sensors)
            if self.sensors:
                for sensor in self.sensors:
                    if hasattr(sensor, 'deactivate'):
                        sensor.deactivate()
                print(f"[System] {len(self.sensors)} sensors deactivated.")

            # 3. 카메라 비활성화 (Disable All Cameras)
            if self.camera_controller:
                self.camera_controller.disable_all_camera()
                print("[System] All cameras disabled.")

            # Also deactivate cameras through system_controller if available
            if self.system_controller and hasattr(self.system_controller, 'cameras'):
                cameras = self.system_controller.cameras
                if cameras:
                    for camera in cameras:
                        if hasattr(camera, 'deactivate'):
                            camera.deactivate()

            # 4. 알람/사이렌 비활성화 (Deactivate Alarm)
            if self.siren:
                self.siren.deactivate()
                print("[System] Siren deactivated.")

            # Also deactivate security system alarm if active
            if self.security_system:
                try:
                    self.security_system.deactivate_alarm()
                except Exception:
                    pass  # Alarm might not be active

            # 5. 현재 사용자 로그아웃 (Logout User)
            if self.login_manager and self.login_manager.is_user_authenticated():
                self.logout()
                print("[System] User logged out.")

            # 6. 시스템 종료 로그 기록 (Log SYSTEM_SHUTDOWN Event)
            if self.log_manager:
                self.log_manager.log_event(
                    event_type="SYSTEM_SHUTDOWN",
                    description="SafeHome system shutting down"
                )
                print("[System] Shutdown event logged.")

            # 7. 데이터베이스 연결 종료 (Disconnect Database)
            if self.storage_manager:
                self.storage_manager.disconnect()
                print("[System] Database disconnected.")

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
    def reset(self) -> dict:
        """
        시스템 재시작 (Reset = Turn Off + Turn On)
        설정을 유지하면서 모든 컴포넌트를 재생성

        Returns:
            dict: {'success': bool, 'message': str, 'phase': int (optional)}
        """
        # 전제조건: 시스템이 켜져 있어야 함
        if self.system_state == SystemState.OFF:
            print("[System] Cannot reset: System is not running.")
            return {
                'success': False,
                'message': 'Cannot reset: System is not running',
                'phase': 0
            }

        print("[System] Resetting SafeHome system...")
        print("[System] Phase 1: Turning off...")

        # 리셋 시작 로그 (턴오프 전에 기록)
        if self.log_manager:
            self.log_manager.log_event(
                event_type="SYSTEM_RESET_START",
                description="System reset initiated - Phase 1: Turning off"
            )

        # ========================================
        # Phase 1: Turn Off the System
        # ========================================
        # turn_off()에서 설정 저장, 센서 비활성화, 카메라 비활성화,
        # 로그아웃, DB 연결 종료가 수행됨
        turn_off_result = self.turn_off()

        if not turn_off_result:
            print("[System] Reset failed: Could not turn off system (Phase 1)")
            return {
                'success': False,
                'message': 'Reset failed: Could not turn off system',
                'phase': 1
            }

        print("[System] Phase 1 complete: System turned off")

        # 잠시 대기 (컴포넌트 정리 시간)
        time.sleep(0.5)

        # ========================================
        # Phase 2: Turn On the System
        # ========================================
        print("[System] Phase 2: Turning on...")

        # turn_on()에서 모든 컴포넌트 재생성, 저장된 설정 로드가 수행됨
        turn_on_result = self.turn_on()

        if not turn_on_result:
            print("[System] Reset failed: Could not turn on system (Phase 2)")
            print("[System] WARNING: System remains in OFF state")
            return {
                'success': False,
                'message': 'Reset failed: Could not turn on system. System is OFF.',
                'phase': 2,
                'state': 'OFF'
            }

        print("[System] Phase 2 complete: System turned on")

        # ========================================
        # Phase 3: Reset Complete
        # ========================================
        # 리셋 완료 로그
        if self.log_manager:
            self.log_manager.log_event(
                event_type="SYSTEM_RESET_COMPLETE",
                description="System reset completed successfully"
            )

        print("[System] SafeHome system reset successfully.")
        print("[System] All settings preserved, all components recreated.")

        return {
            'success': True,
            'message': 'System reset successfully',
            'phase': 3
        }

    def reset_simple(self) -> bool:
        """
        간단한 리셋 (하위 호환용)
        :return: 성공 여부
        """
        result = self.reset()
        return result['success']

    # ========================================
    # Common Function 7: Change master password through control panel
    # ========================================
    def change_password(self, old_password: str, new_password: str) -> bool:
        """
        제어 패널을 통한 마스터 비밀번호 변경 (하위 호환용)
        :param old_password: 현재 비밀번호
        :param new_password: 새 비밀번호
        :return: 성공 여부
        """
        result = self.change_master_password(old_password, new_password, new_password)
        return result['success']

    def change_master_password(self, current_password: str, new_password: str,
                                confirm_password: str, max_reentry_tries: int = 3) -> dict:
        """
        제어 패널을 통한 마스터 비밀번호 변경 (상세 정보 반환)
        Common Function 7: Change Master Password Through Control Panel

        3단계 프로세스:
        - Phase 1: 현재 비밀번호 검증
        - Phase 2: 새 비밀번호 입력
        - Phase 3: 새 비밀번호 확인 및 저장

        :param current_password: 현재 비밀번호
        :param new_password: 새 비밀번호
        :param confirm_password: 새 비밀번호 확인
        :param max_reentry_tries: 최대 재시도 횟수 (기본: 3)
        :return: 변경 결과 딕셔너리
        """
        # 전제조건 1: 시스템이 켜져 있어야 함
        if self.system_state == SystemState.OFF:
            print("[System] System is off. Cannot change password.")
            return {
                'success': False,
                'message': 'System is off. Please turn on the system first.',
                'phase': 0,
                'error_type': 'SYSTEM_OFF'
            }

        # 전제조건 2: 시스템이 잠겨있지 않아야 함
        if self.system_state == SystemState.LOCKED:
            print("[System] System is locked. Cannot change password.")
            return {
                'success': False,
                'message': 'System is locked. Please contact administrator.',
                'phase': 0,
                'error_type': 'SYSTEM_LOCKED'
            }

        # 전제조건 3: 사용자가 로그인되어 있어야 함
        if not self.login_manager.is_user_authenticated():
            print("[System] Authentication required to change password.")
            return {
                'success': False,
                'message': 'Authentication required. Please login first.',
                'phase': 0,
                'error_type': 'NOT_AUTHENTICATED'
            }

        user = self.login_manager.get_current_user().get_username()

        # 비밀번호 변경 시도 로그
        self.log_manager.log_event(
            event_type="PASSWORD_CHANGE_START",
            description="Password change initiated",
            user_id=user
        )

        # LoginManager를 통한 비밀번호 변경
        result = self.login_manager.change_password_with_details(
            current_password, new_password, confirm_password, max_reentry_tries
        )

        if result['success']:
            # 성공 로그
            self.log_manager.log_event(
                event_type="PASSWORD_CHANGE_SUCCESS",
                description="User password changed successfully",
                user_id=user
            )
            print(f"[System] Password changed successfully for user '{user}'.")
        else:
            # 실패 로그
            error_type = result.get('error_type', 'UNKNOWN')
            phase = result.get('phase', 0)
            self.log_manager.log_event(
                event_type="PASSWORD_CHANGE_FAILED",
                description=f"Password change failed at phase {phase}: {error_type}",
                user_id=user
            )
            print(f"[System] Password change failed: {result['message']}")

        return result

    def validate_current_password_for_change(self, current_password: str) -> dict:
        """
        비밀번호 변경을 위한 현재 비밀번호 검증 (Phase 1)
        재시도 횟수 관리 포함

        :param current_password: 현재 비밀번호
        :return: 검증 결과 딕셔너리
        """
        if not self.login_manager.is_user_authenticated():
            return {
                'success': False,
                'message': 'Authentication required',
                'error_type': 'NOT_AUTHENTICATED'
            }

        result = self.login_manager.validate_current_password(current_password)

        user = self.login_manager.get_current_user().get_username()

        if result['success']:
            self.log_manager.log_event(
                event_type="PASSWORD_VERIFY_SUCCESS",
                description="Current password verified for password change",
                user_id=user
            )
        else:
            self.log_manager.log_event(
                event_type="PASSWORD_VERIFY_FAILED",
                description="Current password verification failed",
                user_id=user
            )

        return result

    def set_new_master_password(self, new_password: str, confirm_password: str) -> dict:
        """
        새 마스터 비밀번호 설정 (Phase 2-3)
        현재 비밀번호 검증 후 호출

        :param new_password: 새 비밀번호
        :param confirm_password: 새 비밀번호 확인
        :return: 설정 결과 딕셔너리
        """
        if not self.login_manager.is_user_authenticated():
            return {
                'success': False,
                'message': 'Authentication required',
                'error_type': 'NOT_AUTHENTICATED'
            }

        result = self.login_manager.set_new_password(new_password, confirm_password)

        user = self.login_manager.get_current_user().get_username()

        if result['success']:
            self.log_manager.log_event(
                event_type="PASSWORD_CHANGE_SUCCESS",
                description="New password set successfully",
                user_id=user
            )
        else:
            error_type = result.get('error_type', 'UNKNOWN')
            self.log_manager.log_event(
                event_type="PASSWORD_CHANGE_FAILED",
                description=f"Failed to set new password: {error_type}",
                user_id=user
            )

        return result

    def lock_account_after_failed_attempts(self, username: str, interface_type: str = 'control_panel') -> dict:
        """
        비밀번호 변경 시 재시도 횟수 초과로 인한 계정 잠금

        :param username: 사용자 ID
        :param interface_type: 인터페이스 타입
        :return: 잠금 결과 딕셔너리
        """
        # 계정 잠금
        success = self.storage_manager.lock_user_account(username, interface_type)

        if success:
            self.log_manager.log_event(
                event_type="ACCOUNT_LOCKED",
                description="Account locked due to too many failed password change attempts",
                user_id=username
            )

            # 사용자 로그아웃
            if self.login_manager.is_user_authenticated():
                self.logout()

            print(f"[System] Account '{username}' locked due to too many failed attempts.")

            return {
                'success': True,
                'message': 'Account locked due to too many failed attempts',
                'locked': True
            }
        else:
            return {
                'success': False,
                'message': 'Failed to lock account',
                'locked': False
            }

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
