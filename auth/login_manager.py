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
        사용자 로그인 시도
        :param username: 사용자 ID
        :param password: 비밀번호
        :param interface: 'control_panel' or 'web_browser'
        :return: 로그인 성공 여부
        """
        # LoginInterface 인스턴스 생성 및 사용자 정보 로드
        login_interface = LoginInterface()

        if not login_interface.load(username):
            print(f"[LoginManager] User '{username}' does not exist.")
            return False

        # 계정 잠금 확인
        if login_interface.is_locked():
            print(f"[LoginManager] Account '{username}' is locked due to too many failed attempts.")
            return False

        # 자격 증명 검증
        if self.validate_credentials(login_interface, password):
            # 로그인 성공
            login_interface.reset_tries()
            login_interface.save()

            self.current_user = login_interface
            self.is_authenticated = True

            print(f"[LoginManager] User '{username}' logged in successfully via {interface}.")
            return True
        else:
            # 로그인 실패
            login_interface.increment_tries()
            login_interface.save()

            print(f"[LoginManager] Login failed for user '{username}'. "
                  f"Attempts: {login_interface.get_number_of_tries()}")
            return False

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
        현재 로그인된 사용자의 비밀번호 변경
        :param old_password: 현재 비밀번호
        :param new_password: 새 비밀번호
        :return: 성공 여부
        """
        if not self.is_authenticated or not self.current_user:
            print("[LoginManager] No authenticated user to change password.")
            return False

        # 디버깅: 현재 사용자 정보 출력
        print(f"[DEBUG] Current user: {self.current_user.get_username()}")
        print(f"[DEBUG] Stored password: {self.current_user.get_password()}")
        print(f"[DEBUG] Input old password: {old_password}")

        # 현재 비밀번호 확인
        if not self.validate_credentials(self.current_user, old_password):
            print("[LoginManager] Old password is incorrect.")
            return False

        # 새 비밀번호 설정 (정책 검증 포함)
        if not self.current_user.set_password(new_password):
            print("[LoginManager] New password does not meet requirements.")
            return False

        # 데이터베이스에 저장
        if self.current_user.save():
            print(f"[LoginManager] Password changed successfully for user '{self.current_user.get_username()}'.")
            return True
        else:
            print("[LoginManager] Failed to save new password.")
            return False

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
        if login_interface.load(username):
            print(f"[LoginManager] User '{username}' already exists.")
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

    def __repr__(self):
        user = self.current_user.get_username() if self.current_user else 'None'
        return f"LoginManager(current_user={user}, authenticated={self.is_authenticated})"
