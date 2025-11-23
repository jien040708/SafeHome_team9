"""
데이터베이스에 locked_at 컬럼 추가
시간 기반 계정 잠금을 위한 마이그레이션
"""
import sqlite3
from utils.constants import DB_FILE

def add_locked_at_column():
    """locked_at 컬럼 추가"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        print("Adding locked_at column to users table...")

        # users 테이블 구조 확인
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]

        # locked_at 컬럼 추가
        if 'locked_at' not in columns:
            cursor.execute("ALTER TABLE users ADD COLUMN locked_at TEXT")
            conn.commit()
            print("[OK] Column 'locked_at' added successfully")
        else:
            print("[INFO] Column 'locked_at' already exists")

        print("\n" + "="*50)
        print("Migration completed!")
        print("="*50)

        conn.close()

    except sqlite3.Error as e:
        print(f"[ERROR] Migration failed: {e}")

if __name__ == '__main__':
    add_locked_at_column()
