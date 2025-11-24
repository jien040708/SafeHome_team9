"""
SafeHomeCamera - 개별 카메라 클래스
UML 다이어그램 기반 구현
"""
from typing import List, Optional
from PIL import Image
import sys
from pathlib import Path

from devices.camera import Camera as SensorCamera
from utils.constants import STATE_IDLE, VIRTUAL_DEVICE_DIR

# Add the appropriate virtual_device folder to sys.path for DeviceCamera import.
project_root = Path(__file__).parent.parent
virtual_device_path = project_root / VIRTUAL_DEVICE_DIR
if virtual_device_path.exists() and str(virtual_device_path) not in sys.path:
    sys.path.insert(0, str(virtual_device_path))

from device.device_camera import DeviceCamera as VirtualDeviceCamera


class SafeHomeCamera(SensorCamera):
    """
    SafeHome 시스템의 개별 카메라를 나타내는 클래스
    위치, 팬 각도, 줌 설정, 비밀번호 등을 관리
    DeviceCamera를 내부적으로 참조하여 실제 카메라 기능 제공
    """
    
    def __init__(self, camera_id: int, location: Optional[List[int]] = None):
        """
        SafeHomeCamera 초기화
        :param camera_id: 카메라 ID
        :param location: 위치 좌표 [x, y] 또는 None
        """
        super().__init__(device_id=f"Camera_{camera_id}")
        self._id: int = camera_id
        self._location: List[int] = location if location else [0, 0]
        self._has_password: bool = False
        self._password: str = ""
        self._enabled: bool = True
        self._zoom_level: int = 1
        self._pan_angle: float = 0.0

        # DeviceCamera 인스턴스 생성 및 ID 설정
        # 이미지 파일은 virtual_device 폴더에 있으므로 작업 디렉토리 변경 필요
        import os
        original_cwd = os.getcwd()
        try:
            virtual_device_dir = project_root / VIRTUAL_DEVICE_DIR
            if virtual_device_dir.exists():
                os.chdir(str(virtual_device_dir))

            self._device_camera: VirtualDeviceCamera = VirtualDeviceCamera()
            self._device_camera.set_id(camera_id)
        finally:
            # 원래 작업 디렉토리로 복원
            os.chdir(original_cwd)
    
    def get_location(self) -> List[int]:
        """
        카메라 위치 조회
        :return: 위치 좌표 [x, y]
        """
        return self._location.copy()
    
    def set_location(self, location: List[int]) -> bool:
        """
        카메라 위치 설정
        :param location: 위치 좌표 [x, y]
        :return: 성공 여부
        """
        if len(location) != 2:
            print(f"[SafeHomeCamera] Invalid location format: {location}")
            return False

        self._location = location[:2]  # x, y만 사용
        print(f"[SafeHomeCamera] Camera {self._id} location set to {self._location}")
        return True
    
    def get_id(self) -> int:
        """
        카메라 ID 조회
        :return: 카메라 ID
        """
        return self._id
    
    def set_id(self, camera_id: int) -> bool:
        """
        카메라 ID 설정
        :param camera_id: 새로운 카메라 ID
        :return: 성공 여부
        """
        if camera_id <= 0:
            print(f"[SafeHomeCamera] Invalid camera ID: {camera_id}")
            return False
        
        self._id = camera_id
        print(f"[SafeHomeCamera] Camera ID set to {camera_id}")
        return True
    
    def display_view(self) -> Optional[Image.Image]:
        """
        카메라 뷰 표시 (DeviceCamera를 통해 실제 이미지 가져오기)
        :return: 카메라 이미지 (PIL Image) 또는 None
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return None
        
        try:
            # DeviceCamera의 get_view() 메서드 사용
            return self._device_camera.get_view()
        except Exception as e:
            print(f"[SafeHomeCamera] Failed to display view: {e}")
            return None
    
    def zoom_in(self) -> bool:
        """
        줌 인 (DeviceCamera를 통해)
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False

        if self._zoom_level >= 10:
            return False
        self._zoom_level += 1
        try:
            self._device_camera.zoom_in()
        except Exception:
            pass
        return True

    def zoom_out(self) -> bool:
        """
        줌 아웃 (DeviceCamera를 통해)
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False

        if self._zoom_level <= 1:
            return False
        self._zoom_level -= 1
        try:
            self._device_camera.zoom_out()
        except Exception:
            pass
        return True
    
    def pan_left(self) -> bool:
        """
        팬 왼쪽으로 이동 (DeviceCamera를 통해)
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False

        if self._pan_angle <= -180.0:
            self._pan_angle = -180.0
            return True
        self._pan_angle = max(-180.0, self._pan_angle - 5.0)
        try:
            self._device_camera.pan_left()
        except Exception:
            pass
        return True

    def pan_right(self) -> bool:
        """
        팬 오른쪽으로 이동 (DeviceCamera를 통해)
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False

        if self._pan_angle >= 180.0:
            self._pan_angle = 180.0
            return True
        self._pan_angle = min(180.0, self._pan_angle + 5.0)
        try:
            self._device_camera.pan_right()
        except Exception:
            pass
        return True

    def stop_recording(self) -> None:
        """Stop recording and reset the base camera status."""
        self.status = STATE_IDLE.lower()
        print(f"[SafeHomeCamera] Camera {self._id} stopped recording")
    
    def get_password(self) -> str:
        """
        카메라 비밀번호 조회
        :return: 비밀번호 문자열
        """
        return self._password
    
    def set_password(self, password: str) -> bool:
        """
        카메라 비밀번호 설정
        :param password: 설정할 비밀번호
        :return: 성공 여부
        """
        if not password:
            print(f"[SafeHomeCamera] Password cannot be empty")
            return False
        
        self._password = password
        self._has_password = True
        print(f"[SafeHomeCamera] Camera {self._id} password set")
        return True
    
    def is_enabled(self) -> bool:
        """
        카메라 활성화 상태 조회
        :return: 활성화 여부
        """
        return self._enabled
    
    def enable(self) -> None:
        """
        카메라 활성화
        :return: None
        """
        self._enabled = True
        print(f"[SafeHomeCamera] Camera {self._id} enabled")
    
    def disable(self) -> None:
        """
        카메라 비활성화
        :return: None
        """
        self._enabled = False
        print(f"[SafeHomeCamera] Camera {self._id} disabled")
    
    def has_password(self) -> bool:
        """
        비밀번호 설정 여부 조회
        :return: 비밀번호 설정 여부
        """
        return self._has_password
    
    def save_info(self) -> bool:
        """
        카메라 정보 저장 (데이터베이스 또는 파일)
        :return: 성공 여부
        """
        try:
            # 실제 구현 시 StorageManager를 통해 데이터베이스에 저장
            # 여기서는 예시로 True 반환
            print(f"[SafeHomeCamera] Camera {self._id} info saved")
            return True
        except Exception as e:
            print(f"[SafeHomeCamera] Failed to save camera info: {e}")
            return False
    
    def get_pan_angle(self) -> float:
        """
        팬 각도 조회 (DeviceCamera에서)
        :return: 팬 각도
        """
        return float(self._pan_angle)

    def get_zoom_setting(self) -> int:
        """
        줌 설정 조회 (DeviceCamera에서)
        :return: 줌 레벨
        """
        return self._zoom_level
