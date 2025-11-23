# Surveillance Tests

Surveillance 시스템의 pytest 테스트 코드입니다.

## 테스트 파일

### test_camera_controller.py
- `CameraController` 클래스의 모든 기능을 테스트합니다.
- 카메라 추가/삭제, 활성화/비활성화, 제어, 뷰 표시, 비밀번호 관리 등을 검증합니다.

### test_safehome_camera.py
- `SafeHomeCamera` 클래스의 모든 기능을 테스트합니다.
- 카메라 위치, ID, 줌, 팬, 비밀번호, 활성화 상태 등을 검증합니다.

### test_surveillance_integration.py
- Surveillance 시스템의 통합 테스트를 포함합니다.
- 여러 카메라 관리, 카메라 생명주기, 워크플로우 등을 검증합니다.

## 실행 방법

```bash
# 모든 surveillance 테스트 실행
pytest tests/surveillance_tests/

# 특정 테스트 파일 실행
pytest tests/surveillance_tests/test_camera_controller.py

# verbose 모드로 실행
pytest tests/surveillance_tests/ -v

# 특정 테스트 함수만 실행
pytest tests/surveillance_tests/test_camera_controller.py::TestCameraController::test_add_camera
```

## 테스트 커버리지

- CameraController: 카메라 관리, 제어, 뷰 표시, 비밀번호 관리
- SafeHomeCamera: 카메라 속성 관리, 줌/팬 제어, 비밀번호 관리
- 통합: 여러 카메라 동시 관리, 생명주기, 보안 기능

## 주의사항

- 일부 테스트는 실제 이미지 파일(`virtual_device_v3/camera*.jpg`)이 필요할 수 있습니다.
- 이미지가 없는 경우에도 테스트는 통과하지만, 뷰 표시 기능은 None을 반환할 수 있습니다.

