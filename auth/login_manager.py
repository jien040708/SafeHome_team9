"""
LoginManager - 로그인 프로세스 관리
사용자 인증, 로그아웃, 비밀번호 변경 등의 로직을 담당
"""
from typing import Optional
from auth.login_interface import LoginInterface
from storage.storage_manager import StorageManager


class LoginManager:
    """
    로그인 프로세스를 총괄하는 매니저 클래스
    LoginInterface를 사용하여 실제 인증 로직 수행
    """

    def __init__(self):
        self.storage = StorageManager()
        self.current_user: Optional[LoginInterface] = None
        self.is_authenticated = False

    def login(self, username: str, password: str, interface: str = 'control_panel') -> bool:
        """
        사용자 로그인 시도 (하위 호환용 - bool 반환)
        :param username: 사용자 ID
        :param password: 비밀번호
        :param interface: 'control_panel' or 'web_browser'
        :return: 로그인 성공 여부
        """
        result = self.login_with_details(username, password, interface)
        return result['success']

    def login_with_details(self, username: str, password: str, interface: str = 'control_panel') -> dict:
        """
        사용자 로그인 시도 (상세 정보 반환)
        :param username: 사용자 ID
        :param password: 비밀번호
        :param interface: 'control_panel' or 'web_browser'
        :return: 로그인 결과 딕셔너리
        """
        MAX_ATTEMPTS = 5

        # LoginInterface 인스턴스 생성 및 사용자 정보 로드
        login_interface = LoginInterface(user_interface=interface)

        if not login_interface.load(username, interface_type=interface):
            print(f"[LoginManager] User '{username}' ({interface}) does not exist.")
            return {
                'success': False,
                'message': 'User not found',
                'user_exists': False
            }

        # 계정 잠금 확인 및 시간 기반 자동 해제 (웹 브라우저 로그인과 동일한 로직)
        if login_interface.is_locked():
            # StorageManager를 통해 사용자 정보 조회 (locked_at 포함)
            user_data = self.storage.get_user_by_username(username, interface)

            if user_data and user_data.get('is_locked'):
                # 시간 기반 자동 해제 확인
                unlock_result = self._check_and_unlock_if_time_passed(user_data, username, interface)

                if unlock_result['still_locked']:
                    # 아직 잠금 시간이 남아있음
                    print(f"[LoginManager] Account '{username}' is locked. {unlock_result.get('remaining_time', 0)} seconds remaining.")
                    return {
                        'success': False,
                        'message': unlock_result['message'],
                        'locked': True,
                        'tries': login_interface.get_number_of_tries(),
                        'remaining_time': unlock_result.get('remaining_time', 0)
                    }
                else:
                    # 잠금이 자동 해제됨 - LoginInterface도 다시 로드
                    login_interface.load(username, interface_type=interface)
                    print(f"[LoginManager] Account '{username}' ({interface}) automatically unlocked after lock period.")
            else:
                # locked_at 정보가 없는 경우 (영구 잠금으로 간주)
                print(f"[LoginManager] Account '{username}' is locked due to too many failed attempts.")
                return {
                    'success': False,
                    'message': 'Account is locked. Please contact administrator.',
                    'locked': True,
                    'tries': login_interface.get_number_of_tries()
                }

        # 자격 증명 검증
        if self.validate_credentials(login_interface, password):
            # 로그인 성공
            login_interface.reset_tries()
            login_interface.save()

            self.current_user = login_interface
            self.is_authenticated = True

            print(f"[LoginManager] User '{username}' logged in successfully via {interface}.")
            return {
                'success': True,
                'message': 'Login successful',
                'username': username,
                'access_level': login_interface.get_access_level()
            }
        else:
            # 로그인 실패
            login_interface.increment_tries()
            current_tries = login_interface.get_number_of_tries()
            remaining = MAX_ATTEMPTS - current_tries

            print(f"[LoginManager] Login failed for user '{username}'. "
                  f"Attempts: {current_tries}")

            # increment_tries()가 이미 5회 도달 시 계정을 잠그므로 여기서는 상태만 확인
            login_interface.save()

            # 5회 도달 시 잠금 메시지 반환 (remaining_time 포함)
            if current_tries >= MAX_ATTEMPTS:
                print(f"[LoginManager] Account '{username}' has been locked.")

                # 잠금 시간 계산 (방금 잠김)
                from config.system_settings import SystemSettings
                system_settings = SystemSettings()
                system_settings.load()
                lock_duration = system_settings.get_system_lock_time()

                return {
                    'success': False,
                    'message': 'Account locked due to too many failed attempts',
                    'locked': True,
                    'tries': current_tries,
                    'remaining_time': lock_duration  # 전체 잠금 시간 반환
                }

            return {
                'success': False,
                'message': 'Incorrect password',
                'tries': current_tries,
                'remaining': remaining,
                'locked': False
            }

    def logout(self):
        """현재 사용자 로그아웃"""
        if self.current_user:
            print(f"[LoginManager] User '{self.current_user.get_username()}' logged out.")
            self.current_user = None
            self.is_authenticated = False
        else:
            print("[LoginManager] No user is currently logged in.")

    def change_password(self, old_password: str, new_password: str) -> bool:
        """
        현재 로그인된 사용자의 비밀번호 변경 (하위 호환용)
        :param old_password: 현재 비밀번호
        :param new_password: 새 비밀번호
        :return: 성공 여부
        """
        result = self.change_password_with_details(old_password, new_password, new_password)
        return result['success']

    def change_password_with_details(self, current_password: str, new_password: str,
                                      confirm_password: str, max_reentry_tries: int = 3) -> dict:
        """
        마스터 비밀번호 변경 (상세 정보 반환)
        Common Function 7: Change Master Password Through Control Panel

        Phase 1: 현재 비밀번호 검증
        Phase 2: 새 비밀번호 입력
        Phase 3: 새 비밀번호 확인 및 저장

        :param current_password: 현재 비밀번호
        :param new_password: 새 비밀번호
        :param confirm_password: 새 비밀번호 확인
        :param max_reentry_tries: 최대 재시도 횟수 (기본: 3)
        :return: 변경 결과 딕셔너리
        """
        # 전제조건: 사용자가 로그인되어 있어야 함
        if not self.is_authenticated or not self.current_user:
            print("[LoginManager] No authenticated user to change password.")
            return {
                'success': False,
                'message': 'Authentication required. Please login first.',
                'phase': 0,
                'error_type': 'NOT_AUTHENTICATED'
            }

        username = self.current_user.get_username()
        interface_type = self.current_user.get_user_interface()

        # ========================================
        # Phase 1: 현재 비밀번호 검증
        # ========================================
        print(f"[LoginManager] Phase 1: Validating current password for user '{username}'")

        if not self.validate_credentials(self.current_user, current_password):
            print("[LoginManager] Current password is incorrect.")

            # 실패 횟수 증가 (재시도 로직은 호출자에서 관리)
            return {
                'success': False,
                'message': 'Current password is incorrect',
                'phase': 1,
                'error_type': 'INCORRECT_PASSWORD'
            }

        print("[LoginManager] Phase 1 complete: Current password verified")

        # ========================================
        # Phase 2 & 3: 새 비밀번호 검증 및 확인
        # ========================================
        print("[LoginManager] Phase 2-3: Validating new password")

        # 새 비밀번호와 확인 비밀번호 일치 확인
        if new_password != confirm_password:
            print("[LoginManager] New passwords do not match.")
            return {
                'success': False,
                'message': 'New passwords do not match. Please try again.',
                'phase': 3,
                'error_type': 'PASSWORD_MISMATCH'
            }

        # 새 비밀번호가 현재 비밀번호와 같은지 확인 (선택사항)
        if new_password == current_password:
            print("[LoginManager] New password cannot be the same as current password.")
            return {
                'success': False,
                'message': 'New password cannot be the same as current password.',
                'phase': 2,
                'error_type': 'SAME_PASSWORD'
            }

        # 새 비밀번호 정책 검증 (set_password에서 수행)
        if not self.current_user.set_password(new_password):
            print("[LoginManager] New password does not meet requirements.")
            return {
                'success': False,
                'message': 'New password does not meet security requirements.',
                'phase': 2,
                'error_type': 'WEAK_PASSWORD'
            }

        print("[LoginManager] Phase 2-3 complete: New password validated")

        # ========================================
        # 비밀번호 저장
        # ========================================
        print("[LoginManager] Saving new password to database")

        if self.current_user.save():
            print(f"[LoginManager] Password changed successfully for user '{username}'.")
            return {
                'success': True,
                'message': 'Password changed successfully',
                'phase': 3,
                'username': username
            }
        else:
            print("[LoginManager] Failed to save new password.")
            return {
                'success': False,
                'message': 'Failed to save new password. Please try again.',
                'phase': 3,
                'error_type': 'DATABASE_ERROR'
            }

    def validate_current_password(self, password: str) -> dict:
        """
        현재 비밀번호 검증 (비밀번호 변경 Phase 1용)
        :param password: 검증할 현재 비밀번호
        :return: 검증 결과 딕셔너리
        """
        if not self.is_authenticated or not self.current_user:
            return {
                'success': False,
                'message': 'Authentication required',
                'error_type': 'NOT_AUTHENTICATED'
            }

        if self.validate_credentials(self.current_user, password):
            return {
                'success': True,
                'message': 'Current password verified'
            }
        else:
            return {
                'success': False,
                'message': 'Current password is incorrect',
                'error_type': 'INCORRECT_PASSWORD'
            }

    def set_new_password(self, new_password: str, confirm_password: str) -> dict:
        """
        새 비밀번호 설정 (비밀번호 변경 Phase 2-3용)
        현재 비밀번호 검증 후 호출
        :param new_password: 새 비밀번호
        :param confirm_password: 새 비밀번호 확인
        :return: 설정 결과 딕셔너리
        """
        if not self.is_authenticated or not self.current_user:
            return {
                'success': False,
                'message': 'Authentication required',
                'error_type': 'NOT_AUTHENTICATED'
            }

        # 비밀번호 일치 확인
        if new_password != confirm_password:
            return {
                'success': False,
                'message': 'New passwords do not match',
                'error_type': 'PASSWORD_MISMATCH'
            }

        # 비밀번호 정책 검증 및 설정
        if not self.current_user.set_password(new_password):
            return {
                'success': False,
                'message': 'Password does not meet requirements',
                'error_type': 'WEAK_PASSWORD'
            }

        # 저장
        if self.current_user.save():
            return {
                'success': True,
                'message': 'Password changed successfully',
                'username': self.current_user.get_username()
            }
        else:
            return {
                'success': False,
                'message': 'Failed to save password',
                'error_type': 'DATABASE_ERROR'
            }

    def validate_credentials(self, login_interface: LoginInterface, password: str) -> bool:
        """
        자격 증명 검증 (간단한 평문 비교)
        실제 프로덕션에서는 해시 비교를 사용해야 함
        :param login_interface: LoginInterface 인스턴스
        :param password: 입력된 비밀번호
        :return: 일치 여부
        """
        return login_interface.get_password() == password

    def get_current_user(self) -> Optional[LoginInterface]:
        """현재 로그인된 사용자 반환"""
        return self.current_user

    def is_user_authenticated(self) -> bool:
        """사용자가 인증되었는지 확인"""
        return self.is_authenticated

    def create_user(self, username: str, password: str,
                    interface: str = 'control_panel', access_level: int = 1) -> bool:
        """
        새 사용자 생성 (관리자 기능)
        :param username: 사용자 ID
        :param password: 비밀번호
        :param interface: 인터페이스 유형
        :param access_level: 접근 권한 레벨
        :return: 성공 여부
        """
        login_interface = LoginInterface(username, password, interface, access_level)

        # 중복 확인
        if login_interface.load(username, interface_type=interface):
            print(f"[LoginManager] User '{username}' ({interface}) already exists.")
            return False

        # 비밀번호 검증
        if not login_interface.set_password(password):
            return False

        # 저장
        if login_interface.save():
            print(f"[LoginManager] User '{username}' created successfully.")
            return True
        else:
            print(f"[LoginManager] Failed to create user '{username}'.")
            return False

    def validate_first_password(self, username: str, password: str, interface_type: str = 'web_browser') -> dict:
        """
        First Password 검증 (웹 로그인용)
        :param username: 사용자 ID
        :param password: First Password
        :param interface_type: 'web_browser' or 'control_panel'
        :return: 검증 결과 딕셔너리
        """
        MAX_ATTEMPTS = 5

        # 사용자 조회
        user = self.storage.get_user_by_username(username, interface_type)

        if not user:
            return {
                'success': False,
                'message': 'User not found'
            }

        # 계정 잠금 확인 및 시간 기반 자동 해제
        if user['is_locked']:
            unlock_result = self._check_and_unlock_if_time_passed(user, username, interface_type)
            if unlock_result['still_locked']:
                return {
                    'success': False,
                    'message': unlock_result['message'],
                    'locked': True,
                    'remaining_time': unlock_result.get('remaining_time', 0)
                }
            # 잠금 해제되었으면 계속 진행

        # First password 검증 (password 필드 사용)
        if password == user['password']:
            # 성공 - 실패 카운터 리셋
            self.storage.reset_failed_login_attempts(username, interface_type)

            return {
                'success': True,
                'message': 'First password correct'
            }
        else:
            # 실패 - 카운터 증가
            self.storage.increment_failed_login_attempts(username, interface_type)

            # 현재 실패 횟수 조회
            user = self.storage.get_user_by_username(username, interface_type)
            new_count = user['failed_attempts']

            # 5회 도달 시 계정 잠금
            if new_count >= MAX_ATTEMPTS:
                self.storage.lock_user_account(username, interface_type)
                return {
                    'success': False,
                    'message': 'Account locked due to too many failed attempts',
                    'locked': True,
                    'tries': new_count
                }

            return {
                'success': False,
                'message': 'Incorrect first password',
                'tries': new_count,
                'remaining': MAX_ATTEMPTS - new_count
            }

    def validate_second_password(self, username: str, second_password: str, interface_type: str = 'web_browser') -> dict:
        """
        Second Password 검증 (웹 로그인용)
        :param username: 사용자 ID
        :param second_password: Second Password
        :param interface_type: 'web_browser' or 'control_panel'
        :return: 검증 결과 딕셔너리
        """
        MAX_ATTEMPTS = 5

        # 사용자 조회
        user = self.storage.get_user_by_username(username, interface_type)

        if not user:
            return {
                'success': False,
                'message': 'User not found'
            }

        # 계정 잠금 확인 및 시간 기반 자동 해제
        if user['is_locked']:
            unlock_result = self._check_and_unlock_if_time_passed(user, username, interface_type)
            if unlock_result['still_locked']:
                return {
                    'success': False,
                    'message': unlock_result['message'],
                    'locked': True,
                    'remaining_time': unlock_result.get('remaining_time', 0)
                }
            # 잠금 해제되었으면 계속 진행

        # Second password 검증
        if second_password == user['second_password']:
            # 성공 - 실패 카운터 리셋 및 로그인 시간 업데이트
            self.storage.reset_failed_login_attempts(username, interface_type)
            self.storage.update_last_login_time(username, interface_type)

            # 웹 로그인을 위한 인증 상태 업데이트
            # Note: 이 메서드는 주로 웹 세션 인증용이므로 self.current_user는 업데이트하지 않음

            return {
                'success': True,
                'message': 'Login successful',
                'username': username
            }
        else:
            # 실패 - 카운터 증가
            self.storage.increment_failed_login_attempts(username, interface_type)

            # 현재 실패 횟수 조회
            user = self.storage.get_user_by_username(username, interface_type)
            new_count = user['failed_attempts']

            # 5회 도달 시 계정 잠금
            if new_count >= MAX_ATTEMPTS:
                self.storage.lock_user_account(username, interface_type)
                return {
                    'success': False,
                    'message': 'Account locked due to too many failed attempts',
                    'locked': True,
                    'tries': new_count
                }

            return {
                'success': False,
                'message': 'Incorrect second password',
                'tries': new_count,
                'remaining': MAX_ATTEMPTS - new_count
            }

    def _check_and_unlock_if_time_passed(self, user: dict, username: str, interface_type: str) -> dict:
        """
        시간 기반 계정 잠금 해제 확인
        :param user: 사용자 정보 딕셔너리
        :param username: 사용자 ID
        :param interface_type: 인터페이스 타입
        :return: 잠금 상태 정보
        """
        from datetime import datetime, timedelta
        from config.configuration_manager import ConfigurationManager

        # 잠금 시간 확인
        locked_at = user.get('locked_at')
        if not locked_at:
            # locked_at이 없으면 영구 잠금으로 간주
            return {
                'still_locked': True,
                'message': 'Account is locked. Please contact administrator.'
            }

        try:
            # 잠금 시작 시간 파싱
            locked_time = datetime.fromisoformat(locked_at)
            current_time = datetime.now()
            elapsed_seconds = (current_time - locked_time).total_seconds()

            # 시스템 설정에서 잠금 시간 가져오기 (데이터베이스에서 직접 로드)
            from config.system_settings import SystemSettings
            system_settings = SystemSettings()
            system_settings.load()  # 데이터베이스에서 최신 설정 로드
            lock_duration = system_settings.get_system_lock_time()  # 초 단위

            if elapsed_seconds >= lock_duration:
                # 잠금 시간이 지났으면 자동 해제
                self.storage.reset_failed_login_attempts(username, interface_type)
                print(f"[LoginManager] Account '{username}' automatically unlocked after {lock_duration} seconds.")
                return {
                    'still_locked': False,
                    'message': 'Account unlocked automatically'
                }
            else:
                # 아직 잠금 시간이 남음
                remaining_seconds = int(lock_duration - elapsed_seconds)
                return {
                    'still_locked': True,
                    'message': f'Account is locked. Please try again in {remaining_seconds} seconds.',
                    'remaining_time': remaining_seconds
                }

        except (ValueError, AttributeError) as e:
            print(f"[LoginManager] Error parsing locked_at time: {e}")
            # 에러 발생 시 영구 잠금으로 간주
            return {
                'still_locked': True,
                'message': 'Account is locked. Please contact administrator.'
            }

    def __repr__(self):
        user = self.current_user.get_username() if self.current_user else 'None'
        return f"LoginManager(current_user={user}, authenticated={self.is_authenticated})"
