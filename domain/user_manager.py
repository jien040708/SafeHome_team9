# domain/user_manager.py
import sqlite3
from utils.constants import DB_FILE

class UserManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._initialize_db()

    def _initialize_db(self):
        """DB 테이블 생성 및 초기 관리자 계정 설정"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                password TEXT
            )
        """)
        self.conn.commit()
        
        # 초기 관리자 계정 추가 (없으면 생성)
        self.cursor.execute("SELECT * FROM users WHERE user_id='admin'")
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT INTO users VALUES ('admin', '1234')")
            self.conn.commit()
            print("[DB] Admin account initialized.")

    def authenticate(self, user_id, password):
        """사용자 인증 로직"""
        self.cursor.execute("SELECT * FROM users WHERE user_id=? AND password=?", (user_id, password))
        result = self.cursor.fetchone()
        return result is not None

    def close(self):
        self.conn.close()