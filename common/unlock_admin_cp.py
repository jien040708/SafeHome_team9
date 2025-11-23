"""
Unlock Admin Account (Control Panel)
admin 계정 (control_panel) 잠금 해제
"""
import sqlite3

DB_FILE = 'safehome.db'

def unlock_admin():
    """admin 계정 잠금 해제"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        print("Unlocking admin account (control_panel)...")

        # admin 계정 잠금 해제 및 실패 횟수 리셋
        cursor.execute("""
            UPDATE users
            SET is_locked = 0, failed_attempts = 0, locked_at = NULL
            WHERE user_id = 'admin' AND interface_type = 'control_panel'
        """)

        conn.commit()

        # 결과 확인
        cursor.execute("""
            SELECT user_id, interface_type, is_locked, failed_attempts, locked_at
            FROM users
            WHERE user_id = 'admin' AND interface_type = 'control_panel'
        """)

        row = cursor.fetchone()
        if row:
            print(f"Admin account status:")
            print(f"  user_id: {row[0]}")
            print(f"  interface_type: {row[1]}")
            print(f"  is_locked: {row[2]}")
            print(f"  failed_attempts: {row[3]}")
            print(f"  locked_at: {row[4]}")
            print("\nAdmin account unlocked successfully!")
        else:
            print("Admin account not found!")

        conn.close()

    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    unlock_admin()
