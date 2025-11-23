"""
Admin 계정 잠금 해제 스크립트
"""
from storage.storage_manager import StorageManager
from auth.login_interface import LoginInterface

# StorageManager 연결
storage = StorageManager()
storage.connect()

# Admin 계정 로드 및 잠금 해제
login = LoginInterface()
if login.load('admin'):
    print(f"Current status:")
    print(f"  Failed attempts: {login.get_number_of_tries()}")
    print(f"  Locked: {login.is_locked()}")

    login.unlock()
    login.save()

    print("\nAdmin account unlocked successfully!")
    print(f"  Failed attempts: {login.get_number_of_tries()}")
    print(f"  Locked: {login.is_locked()}")
else:
    print("Admin account not found!")

storage.disconnect()
