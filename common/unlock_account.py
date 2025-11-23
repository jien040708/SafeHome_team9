"""
계정 잠금 해제 스크립트
"""
from storage.storage_manager import StorageManager

def unlock_account(username, interface_type='web_browser'):
    """계정 잠금 해제"""
    storage = StorageManager()
    storage.connect()

    # 현재 상태 확인
    user = storage.get_user_by_username(username, interface_type)

    if not user:
        print(f"[ERROR] User '{username}' not found")
        storage.disconnect()
        return

    print(f"User: {username}")
    print(f"Interface: {interface_type}")
    print(f"Failed attempts: {user['failed_attempts']}")
    print(f"Locked: {bool(user['is_locked'])}")
    print()

    if user['is_locked']:
        # 잠금 해제
        success = storage.reset_failed_login_attempts(username, interface_type)

        if success:
            print("[OK] Account unlocked successfully!")
            print("The user can now login again.")
        else:
            print("[ERROR] Failed to unlock account")
    else:
        print("[INFO] Account is not locked")

    storage.disconnect()

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Usage: python unlock_account.py <username> [interface_type]")
        print("Example: python unlock_account.py homeowner web_browser")
        sys.exit(1)

    username = sys.argv[1]
    interface_type = sys.argv[2] if len(sys.argv) > 2 else 'web_browser'

    unlock_account(username, interface_type)
