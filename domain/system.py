"""
System - SafeHome 시스템 메인 클래스
전체 시스템의 생명주기, 컴포넌트 관리, 7가지 Common Functions 구현
"""
import time
from typing import Optional
from enum import Enum

from storage.storage_manager import StorageManager
from auth.login_manager import LoginManager
from event_logging.log_manager import LogManager
from config.configuration_manager import ConfigurationManager
from domain.system_controller import SystemController
from utils.constants import *
from domain.device_manager import DeviceManager


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

        self.device_manager = None
        self.sensors = []

        # UI 참조
        self.ui_app = None

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

        # LoginManager를 통한 인증
        result = self.login_manager.login_with_details(username, password, interface)

        if result['success']:
            # 로그 기록
            self.log_manager.log_event(
                event_type="LOGIN_SUCCESS",
                description=f"User logged in via {interface}",
                user_id=username
            )
            self.system_state = SystemState.ACTIVE

            # SystemController에도 인증 정보 전달 (기존 코드 호환)
            if self.system_controller:
                self.system_controller.authenticated_user = username

            print(f"[System] User '{username}' logged in successfully via {interface}.")
        else:
            # 로그 기록
            self.log_manager.log_event(
                event_type="LOGIN_FAILED",
                description=f"Failed login attempt via {interface}",
                user_id=username
            )
            print(f"[System] Login failed for user '{username}'.")

        return result

    def logout(self):
        """현재 사용자 로그아웃"""
        if self.login_manager.is_user_authenticated():
            user = self.login_manager.get_current_user().get_username()
            self.login_manager.logout()
            self.log_manager.log_event(
                event_type="LOGOUT",
                description="User logged out",
                user_id=user
            )
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
        if not self.login_manager.is_user_authenticated():
            print("[System] Authentication required to configure settings.")
            return False

        settings = self.configuration_manager.get_system_setting()

        if monitoring_phone:
            settings.set_monitoring_service_phone(monitoring_phone)
        if homeowner_phone:
            settings.set_homeowner_phone(homeowner_phone)
        if lock_time is not None:
            settings.set_system_lock_time(lock_time)
        if alarm_delay is not None:
            settings.set_alarm_delay_time(alarm_delay)

        success = self.configuration_manager.update_system_settings(settings)

        if success:
            user = self.login_manager.get_current_user().get_username()
            self.log_manager.log_event(
                event_type="CONFIG_UPDATE",
                description="System settings updated",
                user_id=user
            )
            print("[System] System settings configured successfully.")
        else:
            print("[System] Failed to configure system settings.")

        return success

    # ========================================
    # Common Function 4: Turn the system on
    # ========================================
    def turn_on(self) -> bool:
        """
        시스템 시작
        모든 컴포넌트 초기화 및 시작
        """
        if self.system_state != SystemState.OFF:
            print(f"[System] System is already {self.system_state.value}.")
            return False

        print("[System] Starting SafeHome system...")
        self.system_state = SystemState.INITIALIZING

        try:
            # 1. StorageManager 초기화 및 연결
            self.storage_manager = StorageManager()
            if not self.storage_manager.connect():
                raise Exception("Failed to connect to database.")

            # 2. ConfigurationManager 초기화
            self.configuration_manager = ConfigurationManager()
            self.configuration_manager.initialize_configuration()

            # 3. LoginManager 초기화
            self.login_manager = LoginManager()

            # 4. LogManager 초기화
            self.log_manager = LogManager()

            # 5. SystemController 초기화 (기존 로직 활용)
            self.system_controller = SystemController(ui_app=self.ui_app)

            # 6. 기본 관리자 계정 생성 (없으면)
            self._initialize_default_user()

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
            if self.system_controller and self.system_controller.siren:
                self.system_controller.siren.deactivate()

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
            'security_mode': self.system_controller.current_state.get_name() if self.system_controller else None
        }

    def set_ui(self, ui_app):
        """UI 앱 설정"""
        self.ui_app = ui_app
        if self.system_controller:
            self.system_controller.set_ui(ui_app)

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
