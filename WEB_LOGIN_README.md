# SafeHome - Web Browser Login Feature

## 개요
SafeHome 시스템에 2단계 비밀번호 인증을 사용한 웹 브라우저 로그인 기능이 추가되었습니다.

## 주요 기능

### 1. 2단계 비밀번호 인증
- **First Password**: 첫 번째 인증 단계
- **Second Password**: 두 번째 인증 단계
- 두 단계 모두 통과해야 로그인 완료

### 2. 보안 기능
- **로그인 실패 제한**: 5회 실패 시 계정 자동 잠금
- **세션 기반 인증**: Flask session을 사용한 안전한 세션 관리
- **이벤트 로깅**: 모든 로그인 시도 및 실패 기록

### 3. 사용자 인터페이스
- 반응형 웹 디자인
- 직관적인 2단계 로그인 프로세스
- 실시간 오류 메시지 및 피드백
- 대시보드에서 시스템 상태 확인 및 제어

## 설치 및 설정

### 1. 데이터베이스 마이그레이션
기존 데이터베이스가 있는 경우, 먼저 마이그레이션을 실행하세요:

```bash
python migrate_database.py
```

이 스크립트는 `users` 테이블에 다음 컬럼을 추가합니다:
- `second_password`: 두 번째 비밀번호
- `last_login_time`: 마지막 로그인 시간

### 2. 웹 사용자 생성
테스트용 웹 사용자를 생성합니다:

```bash
python create_web_user.py
```

이 스크립트는 다음 사용자를 생성합니다:
- **Username**: `homeowner`
  - First Password: `first123`
  - Second Password: `second456`
  - Access Level: 1

### 3. 시스템 실행
SafeHome 시스템을 실행합니다:

```bash
python main.py
```

시스템이 시작되면 다음과 같은 메시지가 표시됩니다:
```
==================================================
SafeHome System Started Successfully!
Control Panel: Running on Tkinter window
Web Interface: http://localhost:5000
==================================================
```

## 사용 방법

### 웹 브라우저 로그인

1. **웹 브라우저에서 접속**
   ```
   http://localhost:5000/login
   ```

2. **First Password 입력**
   - Username: `homeowner`
   - First Password: `first123`
   - "Login" 버튼 클릭

3. **Second Password 입력**
   - First Password가 정확하면 Second Password 입력 화면이 표시됩니다
   - Second Password: `second456`
   - "Submit" 버튼 클릭

4. **대시보드 접속**
   - 로그인 성공 시 자동으로 대시보드로 리다이렉트됩니다
   - 시스템 상태 확인 및 보안 모드 제어 가능

### 로그아웃
대시보드 우측 상단의 "Logout" 버튼을 클릭합니다.

## API 엔드포인트

### 인증 관련

#### `POST /api/login/first`
First Password 검증

**Request Body:**
```json
{
  "username": "homeowner",
  "password": "first123"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "First password correct"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "message": "Incorrect first password",
  "tries": 1,
  "remaining": 4
}
```

#### `POST /api/login/second`
Second Password 검증

**Request Body:**
```json
{
  "second_password": "second456"
}
```

**Success Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "redirect": "/dashboard"
}
```

**Error Response (401):**
```json
{
  "success": false,
  "message": "Incorrect second password",
  "tries": 1,
  "remaining": 4
}
```

### 페이지 라우트

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | 메인 페이지 (로그인 상태에 따라 리다이렉트) |
| `/login` | GET | 로그인 페이지 |
| `/dashboard` | GET | 대시보드 (로그인 필요) |
| `/logout` | GET | 로그아웃 |
| `/arm` | GET | 시스템 Arm Away |
| `/disarm` | GET | 시스템 Disarm |
| `/status` | GET | 시스템 상태 조회 |

## 데이터베이스 스키마

### users 테이블 (업데이트)

```sql
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL,             -- First Password
    second_password TEXT,               -- Second Password (새로 추가)
    interface_type TEXT DEFAULT 'control_panel',
    access_level INTEGER DEFAULT 1,
    failed_attempts INTEGER DEFAULT 0,
    is_locked BOOLEAN DEFAULT 0,
    last_login_time TEXT,               -- 새로 추가
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 보안 고려사항

### 현재 구현
- 평문 비밀번호 저장 (개발/테스트용)
- 세션 기반 인증
- 로그인 실패 5회 시 계정 잠금
- 모든 인증 시도 로깅

### 향후 개선 사항
1. **비밀번호 해싱**: BCrypt 또는 Argon2 사용
2. **HTTPS**: SSL/TLS 인증서 적용
3. **CSRF 보호**: Flask-WTF 사용
4. **Rate Limiting**: IP 기반 요청 제한
5. **2FA**: TOTP 기반 이중 인증 추가

## 트러블슈팅

### 문제: "Account is locked" 메시지
**해결**: 데이터베이스에서 직접 계정 잠금 해제
```sql
UPDATE users
SET is_locked = 0, failed_attempts = 0
WHERE user_id = 'homeowner' AND interface_type = 'web_browser';
```

### 문제: "User not found"
**해결**: 웹 사용자가 생성되지 않았을 수 있습니다
```bash
python create_web_user.py
```

### 문제: "System not available"
**해결**: SafeHome 시스템이 실행 중인지 확인
```bash
python main.py
```

### 문제: 세션이 유지되지 않음
**해결**: 브라우저 쿠키 설정 확인 또는 시크릿 키 재설정

## 파일 구조

```
SafeHome_team9/
├── main.py                          # Flask 라우트 및 웹 서버 (업데이트)
├── migrate_database.py              # 데이터베이스 마이그레이션 스크립트
├── create_web_user.py               # 웹 사용자 생성 스크립트
│
├── storage/
│   └── storage_manager.py           # 웹 로그인 메서드 추가
│
├── auth/
│   └── login_manager.py             # 2단계 인증 메서드 추가
│
├── templates/                       # Flask 템플릿 (새로 생성)
│   ├── login.html                   # 로그인 페이지
│   └── dashboard.html               # 대시보드 페이지
│
└── safehome.db                      # SQLite 데이터베이스
```

## 테스트 시나리오

### 시나리오 1: 정상 로그인
1. `http://localhost:5000/login` 접속
2. Username: `homeowner`, First Password: `first123` 입력
3. Second Password: `second456` 입력
4. 대시보드 접속 확인

### 시나리오 2: First Password 실패
1. 잘못된 First Password 입력 (예: `wrong123`)
2. 오류 메시지 및 남은 시도 횟수 확인
3. 5회 실패 시 계정 잠금 확인

### 시나리오 3: Second Password 실패
1. First Password 정상 입력
2. 잘못된 Second Password 입력
3. 오류 메시지 확인
4. 5회 실패 시 계정 잠금 확인

### 시나리오 4: 세션 유지
1. 정상 로그인
2. 대시보드에서 시스템 제어 (Arm/Disarm)
3. 새로고침 후에도 로그인 상태 유지 확인

### 시나리오 5: 로그아웃
1. 대시보드에서 "Logout" 클릭
2. 로그인 페이지로 리다이렉트 확인
3. 수동으로 `/dashboard` 접근 시 로그인 페이지로 리다이렉트 확인

## 기술 스택

| 구분 | 기술 |
|-----|-----|
| **백엔드** | Python 3.x, Flask |
| **프론트엔드** | HTML5, CSS3, JavaScript (Vanilla) |
| **데이터베이스** | SQLite 3 |
| **인증** | Flask Session |
| **디자인** | Responsive CSS (Gradient UI) |

## 개발자 정보

- **구현 일자**: 2025-11-21
- **버전**: 1.0
- **Common Function**: Log onto the system through Web browser

## 참고 문서

- [IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md) - 전체 시스템 구현 요약
- Flask Documentation: https://flask.palletsprojects.com/
- SQLite Documentation: https://www.sqlite.org/docs.html
