"""
데이터베이스 마이그레이션 스크립트
기존 users 테이블에 second_password, last_login_time 컬럼 추가
"""
import sqlite3
from utils.constants import DB_FILE

def migrate_database():
    """데이터베이스 스키마 마이그레이션"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        print("Starting database migration...")

        # users 테이블 구조 확인
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        print(f"Current columns: {columns}")

        # second_password 컬럼 추가
        if 'second_password' not in columns:
            print("Adding 'second_password' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN second_password TEXT")
            print("[OK] Column 'second_password' added")
        else:
            print("[INFO] Column 'second_password' already exists")

        # last_login_time 컬럼 추가
        if 'last_login_time' not in columns:
            print("Adding 'last_login_time' column...")
            cursor.execute("ALTER TABLE users ADD COLUMN last_login_time TEXT")
            print("[OK] Column 'last_login_time' added")
        else:
            print("[INFO] Column 'last_login_time' already exists")

        conn.commit()
        print("\n" + "="*50)
        print("Database migration completed successfully!")
        print("="*50)

        conn.close()

    except sqlite3.Error as e:
        print(f"[ERROR] Migration failed: {e}")

if __name__ == '__main__':
    migrate_database()
