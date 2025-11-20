# domain/user_manager.py
# This module is now deprecated. Use auth.login_manager instead.
# Kept for backward compatibility with SystemController.

import sqlite3
from utils.constants import DB_FILE

class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        # Do not initialize DB here, as StorageManager handles schema

    def authenticate(self, user_id, password):
        """
        사용자 인증 로직 (기존 호환성 유지)
        새로운 스키마와 호환되도록 수정
        """
        try:
            self.cursor.execute("SELECT * FROM users WHERE user_id=? AND password=?", (user_id, password))
            result = self.cursor.fetchone()
            return result is not None
        except sqlite3.Error as e:
            print(f"[UserManager] Authentication error: {e}")
            return False

    def close(self):
        self.conn.close()