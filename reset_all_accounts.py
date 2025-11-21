"""
모든 계정 잠금 해제 및 시스템 설정 복구
"""
from storage.storage_manager import StorageManager
from auth.login_interface import LoginInterface

storage = StorageManager()
storage.connect()

print("="*60)
print("Resetting All Accounts")
print("="*60)

# 모든 사용자 조회
sql = "SELECT user_id FROM users"
users = storage.execute_query(sql)

for user in users:
    username = user['user_id']
    login = LoginInterface()
    if login.load(username):
        print(f"\nUser: {username}")
        print(f"  Before - Failed attempts: {login.get_number_of_tries()}, Locked: {login.is_locked()}")

        login.unlock()
        login.save()

        print(f"  After  - Failed attempts: {login.get_number_of_tries()}, Locked: {login.is_locked()}")

# 시스템 잠금 시간을 30초로 복구
print("\n" + "="*60)
print("Restoring system lock time to 30 seconds...")
storage.execute_update("UPDATE system_settings SET system_lock_time = 30")
print("System lock time restored to 30 seconds")

storage.disconnect()

print("\n" + "="*60)
print("All accounts unlocked successfully!")
print("="*60)
