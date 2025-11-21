"""
Set System Lock Time
시스템 잠금 시간 설정
"""
import sqlite3

DB_FILE = 'safehome.db'

def set_lock_time(seconds):
    """시스템 잠금 시간 설정"""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        print(f"Setting system lock time to {seconds} seconds...")

        cursor.execute("""
            UPDATE system_settings
            SET system_lock_time = ?
        """, (seconds,))

        conn.commit()

        # 결과 확인
        cursor.execute("SELECT system_lock_time FROM system_settings")
        row = cursor.fetchone()
        if row:
            print(f"System lock time set to: {row[0]} seconds")
        else:
            print("Failed to set system lock time!")

        conn.close()

    except sqlite3.Error as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    set_lock_time(10)  # 10초로 설정
