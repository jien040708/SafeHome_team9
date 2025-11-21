"""
웹 로그인 테스트 사용자 생성 스크립트
"""
from storage.storage_manager import StorageManager

def create_test_users():
    """테스트 사용자 생성"""
    storage = StorageManager()

    if not storage.connect():
        print("Failed to connect to database")
        return

    print("Creating web login test users...")

    # 테스트 사용자 1: admin
    success1 = storage.create_web_user(
        username='admin',
        first_password='password123',
        second_password='secure456',
        access_level=2
    )

    if success1:
        print("[OK] User 'admin' created successfully")
        print("  - First Password: password123")
        print("  - Second Password: secure456")
    else:
        print("[ERROR] Failed to create user 'admin' (may already exist)")

    # 테스트 사용자 2: homeowner
    success2 = storage.create_web_user(
        username='homeowner',
        first_password='first123',
        second_password='second456',
        access_level=1
    )

    if success2:
        print("[OK] User 'homeowner' created successfully")
        print("  - First Password: first123")
        print("  - Second Password: second456")
    else:
        print("[ERROR] Failed to create user 'homeowner' (may already exist)")

    print("\n" + "="*50)
    print("Test users created successfully!")
    print("You can now login at: http://localhost:5000/login")
    print("="*50)

    storage.disconnect()

if __name__ == '__main__':
    create_test_users()
