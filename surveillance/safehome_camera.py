"""
SafeHomeCamera - 개별 카메라 클래스
UML 다이어그램 기반 구현
"""
from typing import List, Optional
from PIL import Image


class SafeHomeCamera:
    """
    SafeHome 시스템의 개별 카메라를 나타내는 클래스
    위치, 팬 각도, 줌 설정, 비밀번호 등을 관리
    """
    
    def __init__(self, camera_id: int, location: Optional[List[int]] = None):
        """
        SafeHomeCamera 초기화
        :param camera_id: 카메라 ID
        :param location: 위치 좌표 [x, y] 또는 None
        """
        self._id: int = camera_id
        self._location: List[int] = location if location else [0, 0]
        self._pan_angle: float = 0.0
        self._zoom_setting: int = 1  # 기본 줌 레벨
        self._has_password: bool = False
        self._password: str = ""
        self._enabled: bool = True
    
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
        if len(location) < 2:
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
        카메라 뷰 표시
        :return: 카메라 이미지 (PIL Image) 또는 None
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return None
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # 실제 구현 시 카메라 하드웨어에서 이미지를 가져와야 함
            # 여기서는 예시로 카메라 정보가 표시된 이미지 생성
            img = Image.new('RGB', (800, 600), color='black')
            draw = ImageDraw.Draw(img)
            
            # 카메라 정보 표시
            info_text = [
                f"Camera ID: {self._id}",
                f"Location: {self._location}",
                f"Pan Angle: {self._pan_angle}°",
                f"Zoom: {self._zoom_setting}x"
            ]
            
            y_offset = 50
            for line in info_text:
                draw.text((50, y_offset), line, fill='white')
                y_offset += 30
            
            return img
        except Exception as e:
            print(f"[SafeHomeCamera] Failed to display view: {e}")
            return None
    
    def zoom_in(self) -> bool:
        """
        줌 인
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False
        
        max_zoom = 10  # 최대 줌 레벨
        if self._zoom_setting < max_zoom:
            self._zoom_setting += 1
            print(f"[SafeHomeCamera] Camera {self._id} zoom in to {self._zoom_setting}x")
            return True
        else:
            print(f"[SafeHomeCamera] Camera {self._id} already at max zoom")
            return False
    
    def zoom_out(self) -> bool:
        """
        줌 아웃
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False
        
        min_zoom = 1  # 최소 줌 레벨
        if self._zoom_setting > min_zoom:
            self._zoom_setting -= 1
            print(f"[SafeHomeCamera] Camera {self._id} zoom out to {self._zoom_setting}x")
            return True
        else:
            print(f"[SafeHomeCamera] Camera {self._id} already at min zoom")
            return False
    
    def pan_left(self) -> bool:
        """
        팬 왼쪽으로 이동
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False
        
        self._pan_angle -= 5.0  # 5도씩 이동
        if self._pan_angle < -180:
            self._pan_angle = -180
        
        print(f"[SafeHomeCamera] Camera {self._id} panned left to {self._pan_angle}°")
        return True
    
    def pan_right(self) -> bool:
        """
        팬 오른쪽으로 이동
        :return: 성공 여부
        """
        if not self._enabled:
            print(f"[SafeHomeCamera] Camera {self._id} is disabled")
            return False
        
        self._pan_angle += 5.0  # 5도씩 이동
        if self._pan_angle > 180:
            self._pan_angle = 180
        
        print(f"[SafeHomeCamera] Camera {self._id} panned right to {self._pan_angle}°")
        return True
    
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
        팬 각도 조회 (헬퍼 메서드)
        :return: 팬 각도
        """
        return self._pan_angle
    
    def get_zoom_setting(self) -> int:
        """
        줌 설정 조회 (헬퍼 메서드)
        :return: 줌 레벨
        """
        return self._zoom_setting

