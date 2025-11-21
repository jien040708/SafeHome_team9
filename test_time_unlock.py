"""
Time-Based Account Unlock Test
시간 기반 계정 잠금 해제 기능 테스트
"""
import time
from domain.system import System

def test_time_based_unlock():
    """시간 기반 잠금 해제 테스트"""
    print("=" * 70)
    print("Time-Based Account Unlock Test")
    print("=" * 70)
    print()

    # 1. 시스템 시작
    print("1. Starting system...")
    system = System()
    system.turn_on()
    print()

    # 2. 현재 시스템 설정 확인
    print("2. Checking system settings...")
    settings = system.configuration_manager.get_system_setting()
    lock_time = settings.get_system_lock_time()
    print(f"   System Lock Time: {lock_time} seconds")
    print()

    # 3. 잘못된 비밀번호로 5회 로그인 시도 (계정 잠금)
    print("3. Attempting login with wrong password (5 times)...")
    for i in range(5):
        result = system.login_with_details('admin', 'wrongpassword', interface='control_panel')
        print(f"   Attempt {i+1}: {result}")
        if result.get('locked'):
            print(f"   -> Account locked after {i+1} attempts!")
            break
    print()

    # 4. 즉시 로그인 시도 (잠금 상태 확인)
    print("4. Attempting login immediately (should be locked)...")
    result = system.login_with_details('admin', '1234', interface='control_panel')
    print(f"   Result: {result}")
    if result.get('locked'):
        remaining = result.get('remaining_time', 0)
        print(f"   -> Account is locked. Remaining time: {remaining} seconds")
    print()

    # 5. 잠금 시간 동안 대기
    print(f"5. Waiting for {lock_time} seconds for automatic unlock...")
    for i in range(lock_time):
        print(f"   {i+1}/{lock_time} seconds...", end='\r')
        time.sleep(1)
    print(f"   {lock_time}/{lock_time} seconds... Done!")
    print()

    # 6. 잠금 해제 후 로그인 시도
    print("6. Attempting login after lock time (should be unlocked)...")
    result = system.login_with_details('admin', '1234', interface='control_panel')
    print(f"   Result: {result}")
    if result.get('success'):
        print("   -> Login successful! Account automatically unlocked!")
    else:
        print(f"   -> Login failed: {result.get('message')}")
    print()

    # 7. 시스템 종료
    print("7. Shutting down system...")
    system.turn_off()
    print()

    print("=" * 70)
    print("Test completed!")
    print("=" * 70)

if __name__ == '__main__':
    test_time_based_unlock()
