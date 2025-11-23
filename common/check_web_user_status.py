"""
웹 사용자 상태 확인
"""
from storage.storage_manager import StorageManager

storage = StorageManager()
storage.connect()

user = storage.get_user_by_username('homeowner', 'web_browser')

if user:
    print("Web User Status:")
    print(f"  Username: {user['user_id']}")
    print(f"  Failed attempts: {user['failed_attempts']}")
    print(f"  Is locked: {bool(user['is_locked'])}")
    print(f"  Locked at: {user.get('locked_at', 'N/A')}")
    print(f"  Interface type: {user.get('interface_type', 'N/A')}")
else:
    print("User not found")

storage.disconnect()
