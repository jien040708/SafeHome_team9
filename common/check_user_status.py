"""
사용자 계정 상태 확인 스크립트
"""
from storage.storage_manager import StorageManager
from datetime import datetime

storage = StorageManager()
storage.connect()

# 모든 사용자 조회
sql = """
    SELECT user_id, interface_type, failed_attempts, is_locked, locked_at, last_login_time
    FROM users
"""
users = storage.execute_query(sql)

print("="*80)
print("Current User Account Status")
print("="*80)

for user in users:
    print(f"\nUser: {user['user_id']} ({user['interface_type']})")
    print(f"  Failed attempts: {user['failed_attempts']}")
    print(f"  Is locked: {user['is_locked']}")
    locked_at = user['locked_at'] if user['locked_at'] else 'N/A'
    print(f"  Locked at: {locked_at}")
    last_login = user['last_login_time'] if user['last_login_time'] else 'N/A'
    print(f"  Last login: {last_login}")

    # 잠금 시간이 있으면 경과 시간 계산
    if user['locked_at']:
        try:
            locked_time = datetime.fromisoformat(user['locked_at'])
            current_time = datetime.now()
            elapsed = (current_time - locked_time).total_seconds()
            print(f"  Time since lock: {int(elapsed)} seconds")
        except:
            print(f"  Time since lock: Unable to parse")

# 시스템 설정 확인
sql = "SELECT system_lock_time FROM system_settings"
result = storage.execute_query(sql)
if result:
    print(f"\nSystem lock time: {result[0]['system_lock_time']} seconds")

storage.disconnect()
print("\n" + "="*80)
