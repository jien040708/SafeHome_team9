"""
Control Panel Login 기능 테스트 스크립트
"""
from domain.system import System
from auth.login_interface import LoginInterface


def test_control_panel_login():
    """제어 패널 로그인 기능 테스트"""
    print("="*60)
    print("Testing Control Panel Login Feature")
    print("="*60)

    # 시스템 초기화
    print("\n1. Initializing system...")
    system = System()
    if not system.turn_on():
        print("[ERROR] Failed to start system.")
        return

    # 테스트 사용자 생성
    print("\n2. Creating test user...")
    username = 'testuser'
    password = 'test1234'

    # 기존 사용자 삭제 (있으면)
    login_interface = LoginInterface()
    if login_interface.load(username):
        print(f"   User '{username}' already exists. Resetting...")
        login_interface.reset_tries()
        login_interface.unlock()
        login_interface.save()
    else:
        # 새 사용자 생성
        success = system.login_manager.create_user(
            username=username,
            password=password,
            interface='control_panel',
            access_level=1
        )
        if success:
            print(f"   Test user '{username}' created successfully.")
        else:
            print(f"   [ERROR] Failed to create test user.")
            return

    # 테스트 1: 정상 로그인
    print("\n3. Test 1: Successful Login")
    result = system.login_with_details(username, password, 'control_panel')
    print(f"   Result: {result}")
    assert result['success'] == True, "Login should succeed"
    assert result['message'] == 'Login successful', "Message should be 'Login successful'"
    print("   [OK] Test 1 PASSED")

    # 로그아웃
    system.logout()

    # 테스트 2: 잘못된 비밀번호 (1회)
    print("\n4. Test 2: Incorrect Password (Attempt 1)")
    result = system.login_with_details(username, 'wrongpass', 'control_panel')
    print(f"   Result: {result}")
    assert result['success'] == False, "Login should fail"
    assert result['tries'] == 1, "Tries should be 1"
    assert result['remaining'] == 4, "Remaining should be 4"
    print("   [OK] Test 2 PASSED")

    # 테스트 3: 연속 실패 (2-4회)
    print("\n5. Test 3: Multiple Failed Attempts (2-4)")
    for i in range(2, 5):
        result = system.login_with_details(username, 'wrongpass', 'control_panel')
        print(f"   Attempt {i}: tries={result['tries']}, remaining={result['remaining']}")
        assert result['tries'] == i, f"Tries should be {i}"
        assert result['remaining'] == 5 - i, f"Remaining should be {5 - i}"
    print("   [OK] Test 3 PASSED")

    # 테스트 4: 5회 실패 후 계정 잠금
    print("\n6. Test 4: Account Lock After 5th Failure")
    result = system.login_with_details(username, 'wrongpass', 'control_panel')
    print(f"   Result: {result}")
    assert result['success'] == False, "Login should fail"
    assert result['locked'] == True, "Account should be locked"
    assert result['tries'] == 5, "Tries should be 5"
    print("   [OK] Test 4 PASSED")

    # 테스트 5: 잠긴 계정으로 올바른 비밀번호 시도
    print("\n7. Test 5: Locked Account with Correct Password")
    result = system.login_with_details(username, password, 'control_panel')
    print(f"   Result: {result}")
    assert result['success'] == False, "Login should fail"
    assert result['locked'] == True, "Account should still be locked"
    print("   [OK] Test 5 PASSED")

    # 테스트 6: 계정 잠금 해제 후 로그인
    print("\n8. Test 6: Login After Unlocking Account")
    # 계정 잠금 해제
    login_interface = LoginInterface()
    login_interface.load(username)
    login_interface.reset_tries()
    login_interface.unlock()
    login_interface.save()
    print("   Account unlocked.")

    result = system.login_with_details(username, password, 'control_panel')
    print(f"   Result: {result}")
    assert result['success'] == True, "Login should succeed after unlock"
    print("   [OK] Test 6 PASSED")

    # 시스템 종료
    print("\n9. Shutting down system...")
    system.turn_off()

    print("\n" + "="*60)
    print("All tests PASSED!")
    print("="*60)


if __name__ == '__main__':
    test_control_panel_login()
