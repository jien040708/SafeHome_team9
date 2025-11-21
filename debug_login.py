"""
로그인 시도 시 자세한 디버깅 정보 출력
"""
from domain.system import System
from datetime import datetime
import time

print("="*60)
print("Debug: Time-Based Unlock Test")
print("="*60)

# 시스템 초기화
system = System()
system.turn_on()

username = 'admin'
password = '1234'

print(f"\n현재 시간: {datetime.now().isoformat()}")

# 5번 틀려서 잠금
print("\n1단계: 5번 틀려서 계정 잠금...")
for i in range(1, 6):
    result = system.login_with_details(username, 'wrong', 'control_panel')
    print(f"   시도 {i}: {result.get('message', 'N/A')}")

print("\n2단계: 즉시 로그인 시도 (실패해야 함)...")
result = system.login_with_details(username, password, 'control_panel')
print(f"   결과: {result}")
if 'remaining_time' in result:
    print(f"   남은 시간: {result['remaining_time']}초")

print("\n3단계: 30초 대기 중...")
time.sleep(31)

print(f"\n4단계: 30초 후 로그인 시도...")
print(f"현재 시간: {datetime.now().isoformat()}")
result = system.login_with_details(username, password, 'control_panel')
print(f"   결과: {result}")

if result['success']:
    print("\n[성공] 30초 후 자동 해제되어 로그인 성공!")
else:
    print("\n[실패] 30초 후에도 로그인 실패!")
    print(f"   메시지: {result.get('message', 'N/A')}")
    if 'remaining_time' in result:
        print(f"   남은 시간: {result['remaining_time']}초")

system.turn_off()
print("\n" + "="*60)
