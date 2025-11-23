"""
계정 잠금 기능 테스트 스크립트
"""
from auth.login_manager import LoginManager
from storage.storage_manager import StorageManager

def test_account_lock():
    """5회 실패 후 계정 잠금 테스트"""
    storage = StorageManager()
    storage.connect()

    login_manager = LoginManager()

    username = 'homeowner'
    correct_first = 'first123'
    wrong_first = 'wrong_password'

    print("="*60)
    print("Testing Account Lock Feature")
    print("="*60)

    # 먼저 계정 상태 확인 및 초기화
    print("\n1. Resetting account state...")
    storage.reset_failed_login_attempts(username, 'web_browser')
    user = storage.get_user_by_username(username, 'web_browser')
    print(f"   Current failed attempts: {user['failed_attempts']}")
    print(f"   Account locked: {user['is_locked']}")

    # 5회 잘못된 비밀번호로 시도
    print("\n2. Testing 5 failed login attempts...")
    for i in range(1, 6):
        print(f"\n   Attempt {i}:")
        result = login_manager.validate_first_password(
            username,
            wrong_first,
            'web_browser'
        )

        print(f"   - Success: {result['success']}")
        print(f"   - Message: {result['message']}")
        if 'tries' in result:
            print(f"   - Failed tries: {result['tries']}")
        if 'remaining' in result:
            print(f"   - Remaining attempts: {result['remaining']}")
        if 'locked' in result and result['locked']:
            print(f"   - Account is LOCKED!")

    # 계정 상태 확인
    print("\n3. Checking account state after 5 failures...")
    user = storage.get_user_by_username(username, 'web_browser')
    print(f"   Failed attempts: {user['failed_attempts']}")
    print(f"   Account locked: {bool(user['is_locked'])}")

    # 잠긴 계정으로 올바른 비밀번호 시도
    print("\n4. Trying with CORRECT password on locked account...")
    result = login_manager.validate_first_password(
        username,
        correct_first,
        'web_browser'
    )
    print(f"   - Success: {result['success']}")
    print(f"   - Message: {result['message']}")
    if 'locked' in result:
        print(f"   - Locked: {result['locked']}")

    print("\n" + "="*60)
    if user['is_locked']:
        print("✓ Account lock feature is WORKING correctly!")
        print("\nTo unlock the account, run:")
        print(f"  python -c \"from storage.storage_manager import StorageManager; s=StorageManager(); s.connect(); s.reset_failed_login_attempts('{username}', 'web_browser')\"")
    else:
        print("✗ Account lock feature is NOT working!")
    print("="*60)

    storage.disconnect()

if __name__ == '__main__':
    test_account_lock()
