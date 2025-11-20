"""
LoginInterface - 사용자별 로그인 정보 관리
각 사용자의 자격 증명, 인터페이스 유형, 접근 권한 등을 관리
"""
from datetime import datetime
from typing import Optional
from storage.storage_manager import StorageManager


class PasswordProperties:
    """비밀번호 정책 관리"""
    def __init__(self, min_length=4, require_special=False, require_digit=False):
        self.min_length = min_length
        self.require_special = require_special
        self.require_digit = require_digit

    def validate(self, password: str) -> bool:
        """비밀번호가 정책을 만족하는지 검증"""
        if len(password) < self.min_length:
            return False
        if self.require_digit and not any(c.isdigit() for c in password):
            return False
        if self.require_special and not any(not c.isalnum() for c in password):
            return False
        return True


class LoginInterface:
    """
    사용자별 로그인 정보 관리 클래스
    데이터베이스와 연동하여 사용자 정보를 CRUD
    """
    MAX_LOGIN_ATTEMPTS = 5

    def __init__(self, user_id: str = None, password: str = None,
                 user_interface: str = 'control_panel', access_level: int = 1):
        self.user_id = user_id
        self.password = password
        self.user_interface = user_interface  # 'control_panel' or 'web_browser'
        self.access_level = access_level
        self.password_properties = PasswordProperties()
        self.number_of_tries = 0
        self.storage = StorageManager()

    # Getters
    def get_username(self) -> str:
        return self.user_id

    def get_password(self) -> str:
        return self.password

    def get_user_interface(self) -> str:
        return self.user_interface

    def get_access_level(self) -> int:
        return self.access_level

    def get_number_of_tries(self) -> int:
        return self.number_of_tries

    # Setters
    def set_username(self, username: str):
        self.user_id = username

    def set_password(self, password: str):
        """비밀번호 정책 검증 후 설정"""
        if self.password_properties.validate(password):
            self.password = password
            return True
        else:
            print("[LoginInterface] Password does not meet requirements.")
            return False

    def set_user_interface(self, interface: str):
        if interface in ['control_panel', 'web_browser']:
            self.user_interface = interface
        else:
            print("[LoginInterface] Invalid interface type.")

    def set_access_level(self, level: int):
        self.access_level = level

    def increment_tries(self):
        """로그인 실패 시도 횟수 증가"""
        self.number_of_tries += 1
        if self.number_of_tries >= self.MAX_LOGIN_ATTEMPTS:
            self._lock_account()

    def reset_tries(self):
        """로그인 성공 시 시도 횟수 초기화"""
        self.number_of_tries = 0
        self._unlock_account()

    def _lock_account(self):
        """계정 잠금"""
        sql = "UPDATE users SET is_locked = 1, failed_attempts = ? WHERE user_id = ?"
        self.storage.execute_update(sql, (self.number_of_tries, self.user_id))
        print(f"[LoginInterface] Account '{self.user_id}' has been locked.")

    def _unlock_account(self):
        """계정 잠금 해제"""
        sql = "UPDATE users SET is_locked = 0, failed_attempts = 0 WHERE user_id = ?"
        self.storage.execute_update(sql, (self.user_id,))

    def is_locked(self) -> bool:
        """계정이 잠겨있는지 확인"""
        sql = "SELECT is_locked FROM users WHERE user_id = ?"
        result = self.storage.execute_query(sql, (self.user_id,))
        if result and len(result) > 0:
            return bool(result[0]['is_locked'])
        return False

    def load(self, user_id: str) -> bool:
        """
        데이터베이스에서 사용자 정보 로드
        :param user_id: 로드할 사용자 ID
        :return: 성공 여부
        """
        sql = """
            SELECT user_id, password, interface_type, access_level, failed_attempts, is_locked
            FROM users WHERE user_id = ?
        """
        result = self.storage.execute_query(sql, (user_id,))

        if result and len(result) > 0:
            row = result[0]
            self.user_id = row['user_id']
            self.password = row['password']
            self.user_interface = row['interface_type']
            self.access_level = row['access_level']
            self.number_of_tries = row['failed_attempts']
            return True
        else:
            print(f"[LoginInterface] User '{user_id}' not found.")
            return False

    def save(self) -> bool:
        """
        현재 사용자 정보를 데이터베이스에 저장 (INSERT or UPDATE)
        :return: 성공 여부
        """
        # 기존 사용자 확인
        check_sql = "SELECT user_id FROM users WHERE user_id = ?"
        result = self.storage.execute_query(check_sql, (self.user_id,))

        if result and len(result) > 0:
            # UPDATE
            sql = """
                UPDATE users
                SET password = ?, interface_type = ?, access_level = ?,
                    failed_attempts = ?
                WHERE user_id = ?
            """
            rows = self.storage.execute_update(
                sql,
                (self.password, self.user_interface, self.access_level,
                 self.number_of_tries, self.user_id)
            )
        else:
            # INSERT
            sql = """
                INSERT INTO users (user_id, password, interface_type, access_level, failed_attempts)
                VALUES (?, ?, ?, ?, ?)
            """
            rows = self.storage.execute_update(
                sql,
                (self.user_id, self.password, self.user_interface,
                 self.access_level, self.number_of_tries)
            )

        if rows > 0:
            print(f"[LoginInterface] User '{self.user_id}' saved successfully.")
            return True
        else:
            print(f"[LoginInterface] Failed to save user '{self.user_id}'.")
            return False

    def delete(self) -> bool:
        """사용자 삭제"""
        sql = "DELETE FROM users WHERE user_id = ?"
        rows = self.storage.execute_update(sql, (self.user_id,))
        return rows > 0

    def __repr__(self):
        return (f"LoginInterface(user_id={self.user_id}, interface={self.user_interface}, "
                f"access_level={self.access_level}, tries={self.number_of_tries})")
