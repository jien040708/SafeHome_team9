"""
시간 기반 계정 잠금 테스트 스크립트
"""
import time
from auth.login_manager import LoginManager
from storage.storage_manager import StorageManager
from config.configuration_manager import ConfigurationManager

def test_time_based_lock():
    """시간 기반 계정 잠금 및 자동 해제 테스트"""
    storage = StorageManager()
    storage.connect()

    login_manager = LoginManager()
    config_manager = ConfigurationManager()

    username = 'homeowner'
    correct_first = 'first123'
    wrong_first = 'wrong_password'

    print("="*60)
    print("Testing Time-Based Account Lock Feature")
    print("="*60)

    # 시스템 설정 확인
    system_settings = config_manager.get_system_setting()
    lock_time = system_settings.get_system_lock_time()
    print(f"\nSystem lock time: {lock_time} seconds")

    # 테스트를 위해 잠금 시간을 10초로 임시 변경
    print("\nSetting lock time to 10 seconds for testing...")
    system_settings.set_system_lock_time(10)
    system_settings.save()
    print("[OK] Lock time set to 10 seconds")

    # 계정 초기화
    print("\n1. Resetting account state...")
    storage.reset_failed_login_attempts(username, 'web_browser')
    user = storage.get_user_by_username(username, 'web_browser')
    print(f"   Failed attempts: {user['failed_attempts']}")
    print(f"   Account locked: {user['is_locked']}")

    # 5회 실패로 계정 잠금
    print("\n2. Locking account with 5 failed attempts...")
    for i in range(5):
        login_manager.validate_first_password(username, wrong_first, 'web_browser')

    user = storage.get_user_by_username(username, 'web_browser')
    print(f"   Account locked: {bool(user['is_locked'])}")
    print(f"   Locked at: {user.get('locked_at', 'N/A')}")

    # 잠긴 상태에서 로그인 시도
    print("\n3. Trying to login while locked...")
    result = login_manager.validate_first_password(username, correct_first, 'web_browser')
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    if 'remaining_time' in result:
        print(f"   Remaining time: {result['remaining_time']} seconds")

    # 5초 대기
    print("\n4. Waiting 5 seconds (lock is 10 seconds)...")
    time.sleep(5)

    # 다시 시도 (아직 잠김)
    print("\n5. Trying again after 5 seconds...")
    result = login_manager.validate_first_password(username, correct_first, 'web_browser')
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")
    if 'remaining_time' in result:
        print(f"   Remaining time: {result['remaining_time']} seconds")

    # 6초 더 대기 (총 11초)
    print("\n6. Waiting 6 more seconds (total 11 seconds)...")
    time.sleep(6)

    # 잠금 시간이 지난 후 시도
    print("\n7. Trying after lock time has passed (11 seconds total)...")
    result = login_manager.validate_first_password(username, correct_first, 'web_browser')
    print(f"   Success: {result['success']}")
    print(f"   Message: {result['message']}")

    # 계정 상태 확인
    user = storage.get_user_by_username(username, 'web_browser')
    print(f"\n8. Final account state:")
    print(f"   Failed attempts: {user['failed_attempts']}")
    print(f"   Account locked: {bool(user['is_locked'])}")
    print(f"   Locked at: {user.get('locked_at', 'N/A')}")

    # 시스템 설정 복원
    print(f"\n9. Restoring original lock time ({lock_time} seconds)...")
    system_settings.set_system_lock_time(lock_time)
    system_settings.save()

    print("\n" + "="*60)
    if result['success']:
        print("[OK] Time-based lock feature is WORKING correctly!")
        print("Account was automatically unlocked after the lock time passed.")
    else:
        print("[ERROR] Time-based lock feature is NOT working!")
    print("="*60)

    storage.disconnect()

if __name__ == '__main__':
    test_time_based_lock()
