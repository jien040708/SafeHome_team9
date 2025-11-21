"""
Database Migration Script - Fix Time-Based Lock
이 스크립트는 users 테이블의 PRIMARY KEY를 (user_id, interface_type) 복합키로 변경합니다.
이를 통해 같은 사용자가 control_panel과 web_browser 두 인터페이스를 사용할 수 있게 됩니다.
"""
import sqlite3
from datetime import datetime

DB_FILE = 'safehome.db'

def migrate_database():
    """데이터베이스 마이그레이션 실행"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        print("[Migration] Starting database migration...")

        # 1. 기존 users 테이블 백업
        print("[Migration] Backing up existing users table...")
        cursor.execute("DROP TABLE IF EXISTS users_backup")
        cursor.execute("""
            CREATE TABLE users_backup AS
            SELECT * FROM users
        """)
        conn.commit()
        print("[Migration] Backup completed.")

        # 2. 기존 users 테이블 삭제
        print("[Migration] Dropping old users table...")
        cursor.execute("DROP TABLE IF EXISTS users")
        conn.commit()

        # 3. 새 users 테이블 생성 (복합 PRIMARY KEY)
        print("[Migration] Creating new users table with composite PRIMARY KEY...")
        cursor.execute("""
            CREATE TABLE users (
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
            )
        """)
        conn.commit()
        print("[Migration] New table created successfully.")

        # 4. 백업에서 데이터 복원
        print("[Migration] Restoring data from backup...")
        cursor.execute("""
            INSERT INTO users
            (user_id, interface_type, password, second_password, access_level,
             failed_attempts, is_locked, locked_at, last_login_time, created_at)
            SELECT user_id,
                   COALESCE(interface_type, 'control_panel') as interface_type,
                   password, second_password, access_level,
                   failed_attempts, is_locked, locked_at, last_login_time, created_at
            FROM users_backup
        """)
        conn.commit()

        # 5. 복원된 데이터 확인
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"[Migration] Restored {count} user records.")

        # 6. 백업 테이블 삭제 (선택사항)
        # cursor.execute("DROP TABLE users_backup")
        # conn.commit()
        # print("[Migration] Backup table removed.")

        print("[Migration] Migration completed successfully!")

        # 7. 현재 사용자 목록 출력
        print("\n[Migration] Current users in database:")
        cursor.execute("SELECT user_id, interface_type, is_locked, locked_at FROM users")
        for row in cursor.fetchall():
            print(f"  - {row[0]} ({row[1]}): locked={row[2]}, locked_at={row[3]}")

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"[Migration] Error during migration: {e}")
        return False

if __name__ == '__main__':
    print("=" * 60)
    print("Database Migration: Fix Time-Based Lock")
    print("=" * 60)
    print()

    result = migrate_database()

    if result:
        print("\n✓ Migration completed successfully!")
    else:
        print("\n✗ Migration failed. Check error messages above.")
