# SafeHome System - Common Functions 구현 완료 보고서

## 📋 프로젝트 개요
SafeHome 홈 자동화 보안 시스템의 7가지 Common Functions를 Python으로 구현했습니다.

**기술 스택:**
- Language: Python 3
- Database: SQLite (safehome.db)
- GUI: Tkinter
- Web Framework: Flask
- Architecture: MVC Pattern with State Pattern

---

## ✅ 구현된 7가지 Common Functions

### 1. Log onto the system through control panel
**구현 위치:** `domain/system.py:login()`, `ui/main_window.py:LoginView`

**기능:**
- Tkinter GUI를 통한 로그인
- LoginManager를 통한 인증 처리
- 로그인 실패 횟수 추적 (최대 5회)
- 계정 잠금 기능

**테스트 방법:**
```bash
python main.py
# GUI에서 Login 화면
# ID: admin
# Password: 1234
```

**구현 클래스:**
- `auth/login_manager.py:LoginManager`
- `auth/login_interface.py:LoginInterface`

---

### 2. Log onto the system through web browser
**구현 위치:** `main.py:app routes`

**기능:**
- Flask 웹 서버를 통한 로그인 확인
- 제어 패널에서 로그인한 사용자 정보를 웹에서도 공유

**테스트 방법:**
```bash
# 1. 제어 패널에서 로그인
# 2. 웹 브라우저에서 http://localhost:5000 접속
# 3. 로그인 상태 확인
```

**웹 인터페이스 라우트:**
- `/` - 홈 페이지 (시스템 상태 표시)
- `/arm` - 시스템 무장 (Away 모드)
- `/disarm` - 시스템 해제
- `/status` - 시스템 상세 정보

---

### 3. Configure system setting
**구현 위치:** `domain/system.py:configure_system_setting()`, `ui/main_window.py:MonitoringView`

**기능:**
- 모니터링 서비스 전화번호 설정
- 집주인 전화번호 설정
- 시스템 잠금 시간 설정 (초)
- 알람 지연 시간 설정 (초)

**테스트 방법:**
```bash
# GUI에서:
# 1. 로그인
# 2. CONFIGURE 버튼 클릭
# 3. "System Settings" 탭 선택
# 4. 설정 값 변경 후 "Save Settings" 클릭
```

**구현 클래스:**
- `config/system_settings.py:SystemSettings`
- `config/configuration_manager.py:ConfigurationManager`

**데이터베이스 테이블:** `system_settings`

---

### 4. Turn the system on
**구현 위치:** `domain/system.py:turn_on()`, `main.py:main()`

**기능:**
1. StorageManager 초기화 및 데이터베이스 연결
2. ConfigurationManager 초기화 (설정 로드)
3. LoginManager 초기화
4. LogManager 초기화
5. SystemController 초기화
6. 기본 admin 계정 생성 (없으면)
7. 시스템 시작 로그 기록

**실행:**
```bash
python main.py
# 자동으로 시스템이 시작됨
```

**로그 출력 예시:**
```
[System] Starting SafeHome system...
[StorageManager] Database connected successfully.
[ConfigurationManager] Configuration initialized successfully.
[System] Default admin account created (admin/1234).
[System] SafeHome system is now READY.
```

---

### 5. Turn the system off
**구현 위치:** `domain/system.py:turn_off()`, `main.py:main()`

**기능:**
1. 현재 사용자 로그아웃
2. 센서 비활성화
3. 카메라 비활성화
4. 알람 비활성화
5. 데이터베이스 연결 종료
6. 시스템 종료 로그 기록

**실행:**
```bash
# main.py의 finally 블록에서 자동으로 실행됨
# 또는 프로그램 종료 시 (Ctrl+C, 창 닫기)
```

---

### 6. Reset the system
**구현 위치:** `domain/system.py:reset()`, `ui/main_window.py:MonitoringView`

**기능:**
1. 현재 설정 백업
2. 시스템 종료 (turn_off)
3. 잠시 대기 (1초)
4. 시스템 시작 (turn_on)
5. 설정 복원

**테스트 방법:**
```bash
# GUI에서:
# 1. 로그인
# 2. CONFIGURE 버튼 클릭
# 3. "System Control" 탭 선택
# 4. "Reset System" 버튼 클릭
# 5. 확인 다이얼로그에서 "Yes" 선택
```

**프로그래밍 방식:**
```python
system = System()
system.turn_on()
# ... 작업 수행 ...
system.reset()  # 시스템 재시작
```

---

### 7. Change master password through control panel
**구현 위치:** `domain/system.py:change_password()`, `ui/main_window.py:MonitoringView`

**기능:**
- 현재 비밀번호 확인
- 새 비밀번호 검증 (최소 4자)
- 비밀번호 정책 검사 (PasswordProperties)
- 데이터베이스 업데이트
- 비밀번호 변경 로그 기록

**테스트 방법:**
```bash
# GUI에서:
# 1. 로그인 (admin/1234)
# 2. CONFIGURE 버튼 클릭
# 3. "Change Password" 탭 선택
# 4. Current Password: 1234
# 5. New Password: admin123
# 6. Confirm New Password: admin123
# 7. "Change Password" 버튼 클릭
# 8. 로그아웃 후 새 비밀번호로 로그인 테스트
```

**구현 클래스:**
- `auth/login_manager.py:LoginManager.change_password()`
- `auth/login_interface.py:PasswordProperties`

---

## 🗂️ 프로젝트 구조

```
SafeHome_team9/
├── main.py                        # 메인 진입점 (Flask + Tkinter)
├── safehome.db                    # SQLite 데이터베이스
│
├── domain/                        # 도메인 로직
│   ├── system.py                  # System 메인 클래스 (7 Common Functions)
│   ├── system_controller.py      # 시스템 제어 (기존)
│   ├── system_states.py           # State Pattern (Disarmed, Away, Stay)
│   └── user_manager.py            # 사용자 관리 (Deprecated)
│
├── storage/                       # 데이터베이스 관리
│   └── storage_manager.py         # StorageManager (싱글톤)
│
├── auth/                          # 인증 및 권한
│   ├── login_manager.py           # LoginManager
│   └── login_interface.py         # LoginInterface, PasswordProperties
│
├── config/                        # 설정 관리
│   ├── system_settings.py         # SystemSettings
│   └── configuration_manager.py   # ConfigurationManager
│
├── event_logging/                 # 이벤트 로깅 (logging과 구분)
│   ├── log.py                     # Log 클래스
│   └── log_manager.py             # LogManager
│
├── ui/                            # 사용자 인터페이스
│   └── main_window.py             # Tkinter GUI (5개 페이지)
│
├── devices/                       # 디바이스 (센서, 카메라 등)
│   ├── device_base.py
│   ├── windoor_sensor.py
│   ├── motion_detector.py
│   ├── camera.py
│   └── siren.py
│
└── utils/                         # 유틸리티
    └── constants.py               # 상수 정의
```

---

## 💾 데이터베이스 스키마

### users 테이블
```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    interface_type TEXT DEFAULT 'control_panel',
    access_level INTEGER DEFAULT 1,
    failed_attempts INTEGER DEFAULT 0,
    is_locked BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### system_settings 테이블
```sql
CREATE TABLE system_settings (
    setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    monitoring_service_phone TEXT,
    homeowner_phone TEXT,
    system_lock_time INTEGER DEFAULT 30,
    alarm_delay_time INTEGER DEFAULT 60,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### event_logs 테이블
```sql
CREATE TABLE event_logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    event_type TEXT NOT NULL,
    description TEXT,
    user_id TEXT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### safety_zones 테이블
```sql
CREATE TABLE safety_zones (
    zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_name TEXT NOT NULL,
    is_armed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### safehome_modes 테이블
```sql
CREATE TABLE safehome_modes (
    mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
    mode_name TEXT NOT NULL,
    description TEXT
);
```

**기본 데이터:**
- Disarmed, Away, Stay 모드
- 기본 시스템 설정 (911, 010-0000-0000, 30초, 60초)
- admin 계정 (admin/1234)

---

## 🔑 주요 클래스 및 메서드

### System 클래스 (domain/system.py)
시스템의 중심 클래스로 모든 Common Functions를 제공합니다.

```python
class System:
    def turn_on() -> bool           # Common Function 4
    def turn_off() -> bool          # Common Function 5
    def reset() -> bool             # Common Function 6

    def login(username, password, interface) -> bool    # Common Function 1 & 2
    def logout()
    def change_password(old, new) -> bool               # Common Function 7

    def configure_system_setting(...) -> bool           # Common Function 3
    def lock_system()
    def unlock_system()
    def get_system_status() -> dict
```

### LoginManager 클래스 (auth/login_manager.py)
```python
class LoginManager:
    def login(username, password, interface) -> bool
    def logout()
    def change_password(old_password, new_password) -> bool
    def validate_credentials(login_interface, password) -> bool
    def create_user(username, password, interface, access_level) -> bool
```

### LogManager 클래스 (event_logging/log_manager.py)
```python
class LogManager:
    def save_log(log: Log) -> bool
    def log_event(event_type, description, user_id) -> bool
    def get_log_list(limit) -> List[Log]
    def get_logs_by_date_range(start, end) -> List[Log]
    def get_logs_by_type(event_type) -> List[Log]
```

---

## 🧪 테스트 시나리오

### 시나리오 1: 전체 시스템 생명주기
```bash
# 1. 시스템 시작
python main.py

# 2. 로그인
# GUI: ID=admin, Password=1234

# 3. 시스템 설정 변경
# GUI: CONFIGURE → System Settings → 값 변경 → Save

# 4. 비밀번호 변경
# GUI: CONFIGURE → Change Password → 변경

# 5. 보안 모드 변경
# GUI: SURVEILLANCE → Arm Away

# 6. 시스템 재시작
# GUI: CONFIGURE → System Control → Reset System

# 7. 시스템 종료
# 창 닫기
```

### 시나리오 2: 로그인 실패 및 계정 잠금
```bash
# 1. 시스템 시작
# 2. 잘못된 비밀번호로 5회 로그인 시도
# 3. 계정 잠금 확인
# 4. 데이터베이스에서 is_locked 확인
sqlite3 safehome.db "SELECT * FROM users WHERE user_id='admin'"
```

### 시나리오 3: 이벤트 로그 확인
```python
from event_logging.log_manager import LogManager

log_manager = LogManager()
logs = log_manager.get_log_list(limit=10)
for log in logs:
    print(log)
```

---

## 📊 이벤트 로그 타입

시스템에서 기록되는 주요 이벤트 타입:

| Event Type | Description |
|------------|-------------|
| `SYSTEM_START` | 시스템 시작 |
| `SYSTEM_SHUTDOWN` | 시스템 종료 |
| `LOGIN_SUCCESS` | 로그인 성공 |
| `LOGIN_FAILED` | 로그인 실패 |
| `LOGOUT` | 로그아웃 |
| `PASSWORD_CHANGE` | 비밀번호 변경 |
| `CONFIG_UPDATE` | 시스템 설정 변경 |

---

## 🚀 실행 방법

### 1. 의존성 설치
```bash
pip install flask pillow
```

### 2. 시스템 실행
```bash
cd "C:\Users\louis\Desktop\kaist\25 fall\소공개\SafeHome_team9"
python main.py
```

### 3. 접속
- **Control Panel:** 자동으로 Tkinter 창이 열림
- **Web Interface:** http://localhost:5000

### 4. 기본 로그인 정보
- **Username:** admin
- **Password:** 1234

---

## 🎯 구현 특징

### 1. 디자인 패턴
- **Singleton Pattern:** StorageManager (데이터베이스 연결 관리)
- **State Pattern:** SecurityState (Disarmed, Away, Stay)
- **Observer Pattern:** 센서 → SystemController
- **MVC Pattern:** UI와 비즈니스 로직 분리

### 2. 보안 기능
- 로그인 실패 횟수 제한 (5회)
- 계정 자동 잠금
- 비밀번호 정책 검증
- 모든 중요 이벤트 로깅

### 3. 확장성
- 모듈화된 구조 (각 기능별 독립 모듈)
- 플러그인 가능한 센서 및 디바이스
- 데이터베이스 스키마 확장 가능
- 새로운 SafeHome 모드 추가 가능

### 4. 호환성
- 기존 SystemController 코드와 호환
- 기존 UI 구조 유지
- 점진적 마이그레이션 가능

---

## 📝 향후 개선 사항

### 단기 개선
1. 비밀번호 해싱 (BCrypt)
2. 웹 인터페이스 로그인 기능 추가
3. Safety Zone CRUD 기능 구현
4. 이벤트 로그 UI 추가

### 중기 개선
1. 다중 사용자 권한 관리
2. 이메일/SMS 알림 기능
3. 카메라 스트리밍
4. 센서 데이터 시각화

### 장기 개선
1. 클라우드 백업
2. 모바일 앱 연동
3. AI 기반 침입 감지
4. 음성 제어

---

## ✅ 체크리스트

- [x] StorageManager 구현
- [x] LoginInterface 및 LoginManager 구현
- [x] SystemSettings 및 ConfigurationManager 구현
- [x] LogManager 및 Log 클래스 구현
- [x] System 메인 클래스 구현
- [x] 7가지 Common Functions 구현
- [x] UI 통합
- [x] 기존 코드와 호환성 유지
- [x] 데이터베이스 스키마 설계
- [x] 초기 데이터 생성
- [x] 테스트 및 디버깅
- [x] 문서화

---

## 📞 문의

구현 관련 문의사항이 있으시면 프로젝트 저장소의 이슈 트래커를 이용해주세요.

---

**구현 완료일:** 2025-11-20
**버전:** 1.0
**개발자:** SafeHome Team 9
