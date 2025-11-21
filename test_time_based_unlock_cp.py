"""
Control Panel 시간 기반 계정 잠금 해제 테스트
"""
from domain.system import System
from auth.login_interface import LoginInterface
from storage.storage_manager import StorageManager
from datetime import datetime, timedelta
import time


def test_time_based_unlock():
    """시간 기반 자동 잠금 해제 테스트"""
    print("="*60)
    print("Testing Time-Based Account Unlock (Control Panel)")
    print("="*60)

    # 시스템 초기화
    print("\n1. Initializing system...")
    system = System()
    if not system.turn_on():
        print("[ERROR] Failed to start system.")
        return

    # 테스트 사용자 생성/초기화
    print("\n2. Setting up test user...")
    username = 'testuser'
    password = 'test1234'

    login_interface = LoginInterface()
    if login_interface.load(username):
        print(f"   Resetting user '{username}'...")
        login_interface.unlock()
        login_interface.save()
    else:
        system.login_manager.create_user(
            username=username,
            password=password,
            interface='control_panel',
            access_level=1
        )
        print(f"   User '{username}' created.")

    # 시스템 잠금 시간 설정 (테스트용으로 짧게 설정 - 5초)
    # 직접 데이터베이스에 설정 (인증 불필요)
    print("\n3. Setting lock time to 5 seconds for testing...")
    storage = StorageManager()
    storage.connect()
    storage.execute_update("UPDATE system_settings SET system_lock_time = 5")
    # Don't disconnect - other components need to use the same storage instance
    print("   Lock time set to 5 seconds")

    # 5회 실패로 계정 잠금
    print("\n4. Locking account with 5 failed attempts...")
    for i in range(1, 6):
        result = system.login_with_details(username, 'wrongpass', 'control_panel')
        print(f"   Attempt {i}: {result.get('message', 'N/A')}")

    # 계정이 잠겼는지 확인
    login_interface.load(username)
    if login_interface.is_locked():
        print("   [OK] Account is locked")
    else:
        print("   [ERROR] Account should be locked!")
        return

    # 즉시 로그인 시도 (실패해야 함)
    print("\n5. Trying to login immediately (should fail)...")
    result = system.login_with_details(username, password, 'control_panel')
    print(f"   Result: {result}")

    if result['success']:
        print("   [ERROR] Login should fail while locked!")
        return
    else:
        remaining = result.get('remaining_time', 0)
        print(f"   [OK] Login rejected. Remaining time: {remaining} seconds")

    # 잠금 시간 대기
    print(f"\n6. Waiting for lock time to pass (5 seconds)...")
    time.sleep(6)  # 5초 + 여유 1초

    # 자동 해제 후 로그인 시도 (성공해야 함)
    print("\n7. Trying to login after lock time (should succeed)...")
    result = system.login_with_details(username, password, 'control_panel')
    print(f"   Result: {result}")

    if result['success']:
        print("   [OK] Login successful after automatic unlock!")
    else:
        print(f"   [ERROR] Login should succeed after lock time!")
        print(f"   Message: {result.get('message', 'N/A')}")
        return

    # 계정 상태 확인
    user_data = storage.get_user_by_username(username, 'control_panel')
    print(f"\n8. Final account state:")
    print(f"   Failed attempts: {user_data['failed_attempts']}")
    print(f"   Is locked: {user_data['is_locked']}")
    print(f"   Locked at: {user_data.get('locked_at', 'N/A')}")

    # 시스템 종료
    print("\n9. Shutting down system...")
    system.turn_off()

    # Cleanup - disconnect storage
    storage.disconnect()

    print("\n" + "="*60)
    print("Time-based unlock test PASSED!")
    print("="*60)


if __name__ == '__main__':
    test_time_based_unlock()
