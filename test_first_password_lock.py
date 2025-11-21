"""
First Password 5회 실패 시 잠금 테스트
"""
from auth.login_manager import LoginManager
from storage.storage_manager import StorageManager

def test_first_password_lock():
    """First Password 5회 실패로 계정 잠금 테스트"""
    storage = StorageManager()
    storage.connect()

    login_manager = LoginManager()

    username = 'homeowner'
    wrong_password = 'wrong123'

    print("="*60)
    print("Testing First Password Lock (5 failed attempts)")
    print("="*60)

    # 계정 초기화
    print("\n1. Resetting account...")
    storage.reset_failed_login_attempts(username, 'web_browser')
    user = storage.get_user_by_username(username, 'web_browser')
    print(f"   Failed attempts: {user['failed_attempts']}")
    print(f"   Locked: {bool(user['is_locked'])}")

    # First password 5회 잘못 입력
    print("\n2. Attempting first password 5 times with wrong password...")
    for i in range(1, 6):
        print(f"\n   Attempt {i}:")
        result = login_manager.validate_first_password(
            username,
            wrong_password,
            'web_browser'
        )

        print(f"   - Success: {result['success']}")
        print(f"   - Message: {result['message']}")
        if 'tries' in result:
            print(f"   - Failed tries: {result['tries']}")
        if 'remaining' in result:
            print(f"   - Remaining: {result['remaining']}")
        if 'locked' in result and result['locked']:
            print(f"   - STATUS: ACCOUNT LOCKED!")

    # 최종 계정 상태 확인
    print("\n3. Final account status:")
    user = storage.get_user_by_username(username, 'web_browser')
    print(f"   Failed attempts: {user['failed_attempts']}")
    print(f"   Locked: {bool(user['is_locked'])}")
    print(f"   Locked at: {user.get('locked_at', 'N/A')}")

    # 올바른 first password로 시도
    print("\n4. Trying with CORRECT first password while locked:")
    correct_password = 'first123'
    result = login_manager.validate_first_password(
        username,
        correct_password,
        'web_browser'
    )
    print(f"   - Success: {result['success']}")
    print(f"   - Message: {result['message']}")

    print("\n" + "="*60)
    if user['is_locked']:
        print("[OK] First password lock is WORKING!")
        print("Account was locked after 5 failed first password attempts.")
    else:
        print("[ERROR] First password lock is NOT working!")
    print("="*60)

    # 계정 해제
    print("\nUnlocking account for future tests...")
    storage.reset_failed_login_attempts(username, 'web_browser')
    print("[OK] Account unlocked")

    storage.disconnect()

if __name__ == '__main__':
    test_first_password_lock()
