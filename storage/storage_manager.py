"""
StorageManager - 데이터베이스 접근 관리
JDBC 대신 sqlite3를 사용하여 데이터베이스 연결 및 쿼리 실행 관리
"""
import sqlite3
import threading
from typing import Optional, List, Tuple, Any
from utils.constants import DB_FILE


class StorageManager:
    """
    데이터베이스 연결 및 쿼리 실행을 관리하는 싱글톤 클래스
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection: Optional[sqlite3.Connection] = None
            self.initialized = True

    def connect(self) -> bool:
        """데이터베이스에 연결"""
        try:
            if self.connection is None:
                self.connection = sqlite3.connect(
                    DB_FILE,
                    check_same_thread=False,
                    timeout=10.0
                )
                self.connection.row_factory = sqlite3.Row  # 딕셔너리 형태로 결과 반환
                self.connection.execute("PRAGMA foreign_keys = ON;")
                print("[StorageManager] Database connected successfully.")
                self._initialize_schema()
                return True
            return True
        except sqlite3.Error as e:
            print(f"[StorageManager] Connection error: {e}")
            return False

    def disconnect(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
                print("[StorageManager] Database disconnected.")
            except sqlite3.Error as e:
                print(f"[StorageManager] Disconnect error: {e}")

    def _initialize_schema(self):
        """데이터베이스 스키마 초기화"""
        schema_sql = """
        -- Users table (확장) - 복합 PRIMARY KEY 사용
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT NOT NULL,
            interface_type TEXT NOT NULL DEFAULT 'control_panel',
            password TEXT NOT NULL,
            second_password TEXT,
            access_level INTEGER DEFAULT 1,
            failed_attempts INTEGER DEFAULT 0,
            is_locked BOOLEAN DEFAULT 0,
            locked_at TEXT,
            last_login_time TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, interface_type)
        );

        -- System settings table
        CREATE TABLE IF NOT EXISTS system_settings (
            setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
            monitoring_service_phone TEXT,
            homeowner_phone TEXT,
            system_lock_time INTEGER DEFAULT 30,
            alarm_delay_time INTEGER DEFAULT 60,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- Devices table (sensor catalog)
        CREATE TABLE IF NOT EXISTS devices (
            device_id TEXT PRIMARY KEY,
            device_type TEXT NOT NULL
        );

        -- Event logs table
        CREATE TABLE IF NOT EXISTS event_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            event_type TEXT NOT NULL,
            description TEXT,
            user_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        );

        -- Safety zones table (향후 확장용)
        CREATE TABLE IF NOT EXISTS safety_zones (
            zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
            zone_name TEXT NOT NULL,
            is_armed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        -- SafeHome modes table (향후 확장용)
        CREATE TABLE IF NOT EXISTS safehome_modes (
            mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode_name TEXT NOT NULL,
            description TEXT
        );

        -- Sensor-to-zone assignment table
        CREATE TABLE IF NOT EXISTS sensor_zone_assignments (
            device_id TEXT PRIMARY KEY,
            zone_id INTEGER NOT NULL,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (device_id) REFERENCES devices(device_id) ON DELETE CASCADE,
            FOREIGN KEY (zone_id) REFERENCES safety_zones(zone_id) ON DELETE CASCADE
        );
        """

        try:
            cursor = self.connection.cursor()
            cursor.executescript(schema_sql)
            self.connection.commit()

            # 기본 설정 데이터 삽입
            cursor.execute("SELECT COUNT(*) FROM system_settings")
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    INSERT INTO system_settings
                    (monitoring_service_phone, homeowner_phone, system_lock_time, alarm_delay_time)
                    VALUES (?, ?, ?, ?)
                """, ('911', '010-0000-0000', 30, 60))
                self.connection.commit()
                print("[StorageManager] Default system settings created.")

            # 기본 모드 데이터 삽입
            cursor.execute("SELECT COUNT(*) FROM safehome_modes")
            if cursor.fetchone()[0] == 0:
                modes = [
                    ('Disarmed', 'System is disarmed, all sensors inactive'),
                    ('Away', 'All sensors active, no one should be home'),
                    ('Stay', 'Perimeter sensors active, motion sensors inactive')
                ]
                cursor.executemany(
                    "INSERT INTO safehome_modes (mode_name, description) VALUES (?, ?)",
                    modes
                )
                self.connection.commit()
                print("[StorageManager] Default SafeHome modes created.")

            # 기본 사용자 데이터 삽입
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                users = [
                    # 관리자 계정 (제어판용)
                    ('admin', 'control_panel', '1234', None, 10, 0, 0, None, None),
                    # 일반 사용자 계정 (웹 브라우저용 - 이중 비밀번호)
                    ('homeowner', 'web_browser', 'first123', 'second456', 1, 0, 0, None, None)
                ]
                cursor.executemany("""
                    INSERT INTO users
                    (user_id, interface_type, password, second_password, access_level,
                     failed_attempts, is_locked, locked_at, last_login_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, users)
                self.connection.commit()
                print("[StorageManager] Default users created:")
                print("  - admin (control_panel): password='1234', access_level=10")
                print("  - homeowner (web_browser): password='first123', second_password='second456', access_level=1")

        except sqlite3.Error as e:
            print(f"[StorageManager] Schema initialization error: {e}")

    def execute_query(self, sql: str, params: Tuple = ()) -> Optional[List[sqlite3.Row]]:
        """
        SELECT 쿼리 실행
        :param sql: SQL 쿼리 문자열
        :param params: 파라미터 튜플
        :return: 결과 리스트 또는 None
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[StorageManager] Query error: {e}")
            return None

    def execute_update(self, sql: str, params: Tuple = ()) -> int:
        """
        INSERT, UPDATE, DELETE 쿼리 실행
        :param sql: SQL 쿼리 문자열
        :param params: 파라미터 튜플
        :return: 영향받은 행 수 또는 -1 (에러 시)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"[StorageManager] Update error: {e}")
            self.connection.rollback()
            return -1

    def execute_many(self, sql: str, params_list: List[Tuple]) -> int:
        """
        여러 개의 INSERT/UPDATE 실행 (배치)
        :param sql: SQL 쿼리 문자열
        :param params_list: 파라미터 튜플 리스트
        :return: 영향받은 총 행 수 또는 -1 (에러 시)
        """
        try:
            cursor = self.connection.cursor()
            cursor.executemany(sql, params_list)
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error as e:
            print(f"[StorageManager] Batch update error: {e}")
            self.connection.rollback()
            return -1

    def get_last_insert_id(self) -> int:
        """마지막 INSERT의 ID 반환"""
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            row = cursor.fetchone()
            return row[0] if row else -1
        except sqlite3.Error as e:
            print(f"[StorageManager] Get last insert ID error: {e}")
            return -1

    # Web Login Support Methods
    def get_user_by_username(self, username: str, interface_type: str = 'web_browser') -> Optional[dict]:
        """사용자 정보 조회 (웹 로그인용)"""
        sql = "SELECT * FROM users WHERE user_id = ? AND interface_type = ?"
        result = self.execute_query(sql, (username, interface_type))
        if result and len(result) > 0:
            return dict(result[0])
        return None

    def increment_failed_login_attempts(self, username: str, interface_type: str = 'web_browser') -> bool:
        """로그인 실패 횟수 증가"""
        sql = "UPDATE users SET failed_attempts = failed_attempts + 1 WHERE user_id = ? AND interface_type = ?"
        rows_affected = self.execute_update(sql, (username, interface_type))
        return rows_affected > 0

    def reset_failed_login_attempts(self, username: str, interface_type: str = 'web_browser') -> bool:
        """로그인 실패 횟수 리셋 및 잠금 해제"""
        sql = "UPDATE users SET failed_attempts = 0, is_locked = 0, locked_at = NULL WHERE user_id = ? AND interface_type = ?"
        rows_affected = self.execute_update(sql, (username, interface_type))
        return rows_affected > 0

    def lock_user_account(self, username: str, interface_type: str = 'web_browser') -> bool:
        """계정 잠금 (잠금 시작 시간 기록)"""
        from datetime import datetime
        sql = "UPDATE users SET is_locked = 1, locked_at = ? WHERE user_id = ? AND interface_type = ?"
        timestamp = datetime.now().isoformat()
        rows_affected = self.execute_update(sql, (timestamp, username, interface_type))
        return rows_affected > 0

    def update_last_login_time(self, username: str, interface_type: str = 'web_browser') -> bool:
        """마지막 로그인 시간 업데이트"""
        from datetime import datetime
        sql = "UPDATE users SET last_login_time = ? WHERE user_id = ? AND interface_type = ?"
        timestamp = datetime.now().isoformat()
        rows_affected = self.execute_update(sql, (timestamp, username, interface_type))
        return rows_affected > 0

    def create_web_user(self, username: str, first_password: str, second_password: str,
                        access_level: int = 1) -> bool:
        """웹 사용자 생성"""
        sql = """
        INSERT INTO users (user_id, password, second_password, interface_type, access_level)
        VALUES (?, ?, ?, 'web_browser', ?)
        """
        rows_affected = self.execute_update(sql, (username, first_password, second_password, access_level))
        return rows_affected > 0
