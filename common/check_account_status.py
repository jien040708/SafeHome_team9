"""
Check Account Status
계정 상태 확인
"""
import sqlite3
from datetime import datetime

DB_FILE = 'safehome.db'

def check_account_status():
    """계정 상태 확인"""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        print("=" * 70)
        print("Account Status Check")
        print("=" * 70)
        print()

        # 모든 사용자 조회
        cursor.execute("""
            SELECT user_id, interface_type, is_locked, failed_attempts, locked_at
            FROM users
            ORDER BY user_id, interface_type
        """)

        rows = cursor.fetchall()

        for row in rows:
            print(f"User: {row['user_id']} ({row['interface_type']})")
            print(f"  is_locked: {row['is_locked']}")
            print(f"  failed_attempts: {row['failed_attempts']}")
            print(f"  locked_at: {row['locked_at']}")

            if row['locked_at']:
                # 시간 차이 계산
                locked_time = datetime.fromisoformat(row['locked_at'])
                current_time = datetime.now()
                elapsed = (current_time - locked_time).total_seconds()
                print(f"  elapsed_time: {elapsed:.1f} seconds")

            print()

        # 시스템 설정 확인
        cursor.execute("SELECT system_lock_time FROM system_settings")
        setting = cursor.fetchone()
        if setting:
            print(f"System Lock Time: {setting['system_lock_time']} seconds")
        print()

        conn.close()

    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    check_account_status()
