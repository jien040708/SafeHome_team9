"""
CameraController - 카메라 관리 및 제어 클래스
UML 다이어그램 기반 구현
"""
from typing import List, Optional, Dict
from PIL import Image
from surveillance.safehome_camera import SafeHomeCamera


class CameraController:
    """
    카메라 추가, 삭제, 활성화/비활성화, 제어, 뷰 표시 등을 관리하는 컨트롤러
    SafeHomeCamera 객체를 관리합니다.
    """
    
    def __init__(self):
        """CameraController 초기화"""
        self._next_camera_id: int = 1
        self._total_camera_number: int = 0
        self._cameras: Dict[int, SafeHomeCamera] = {}

        
    def add_camera(self, x_coord: int, y_coord: int) -> bool:
        """
        새 카메라 추가 (SafeHomeCamera 생성)
        :param x_coord: X 좌표
        :param y_coord: Y 좌표
        :return: 성공 여부
        """
        try:
            camera_id = self._next_camera_id
            camera = SafeHomeCamera(camera_id=camera_id, location=[x_coord, y_coord])
            
            self._cameras[camera_id] = camera
            
            self._next_camera_id += 1
            self._total_camera_number += 1
            
            print(f"[CameraController] Camera {camera_id} added at ({x_coord}, {y_coord})")
            return True
        except Exception as e:
            print(f"[CameraController] Failed to add camera: {e}")
            return False
    
    def delete_camera(self, camera_id: int) -> bool:
        """
        카메라 삭제
        :param camera_id: 삭제할 카메라 ID
        :return: 성공 여부
        """
        if camera_id not in self._cameras:
            print(f"[CameraController] Camera {camera_id} not found")
            return False
        
        try:
            camera = self._cameras[camera_id]
            # DeviceCamera 스레드 중지
            if hasattr(camera, '_device_camera') and hasattr(camera._device_camera, 'stop'):
                camera._device_camera.stop()
            
            del self._cameras[camera_id]
            self._total_camera_number -= 1
            print(f"[CameraController] Camera {camera_id} deleted")
            return True
        except Exception as e:
            print(f"[CameraController] Failed to delete camera {camera_id}: {e}")
            return False
    
    def enable_cameras(self, camera_id_list: List[int]) -> bool:
        """
        여러 카메라 활성화
        :param camera_id_list: 활성화할 카메라 ID 리스트
        :return: 성공 여부
        """
        success = True
        for camera_id in camera_id_list:
            if not self.enable_camera(camera_id):
                success = False
        return success
    
    def disable_cameras(self, camera_id_list: List[int]) -> bool:
        """
        여러 카메라 비활성화
        :param camera_id_list: 비활성화할 카메라 ID 리스트
        :return: 성공 여부
        """
        success = True
        for camera_id in camera_id_list:
            if not self.disable_camera(camera_id):
                success = False
        return success
    
    def enable_all_camera(self) -> bool:
        """
        모든 카메라 활성화
        :return: 성공 여부
        """
        success = True
        for camera_id in list(self._cameras.keys()):
            if not self.enable_camera(camera_id):
                success = False
        return success
    
    def disable_all_camera(self) -> bool:
        """
        모든 카메라 비활성화
        :return: 성공 여부
        """
        success = True
        for camera_id in list(self._cameras.keys()):
            if not self.disable_camera(camera_id):
                success = False
        return success
    
    def enable_camera(self, camera_id: int) -> bool:
        """
        단일 카메라 활성화
        :param camera_id: 활성화할 카메라 ID
        :return: 성공 여부
        """
        if camera_id not in self._cameras:
            print(f"[CameraController] Camera {camera_id} not found")
            return False
        
        self._cameras[camera_id].enable()
        return True
    
    def disable_camera(self, camera_id: int) -> bool:
        """
        단일 카메라 비활성화
        :param camera_id: 비활성화할 카메라 ID
        :return: 성공 여부
        """
        if camera_id not in self._cameras:
            print(f"[CameraController] Camera {camera_id} not found")
            return False
        
        self._cameras[camera_id].disable()
        return True
    
    def control_single_camera(self, camera_id: int, control_id: int) -> bool:
        """
        단일 카메라 제어
        :param camera_id: 카메라 ID
        :param control_id: 제어 ID (예: 0=팬 왼쪽, 1=팬 오른쪽, 2=줌 인, 3=줌 아웃 등)
        :return: 성공 여부
        """
        if camera_id not in self._cameras:
            print(f"[CameraController] Camera {camera_id} not found")
            return False
        
        camera = self._cameras[camera_id]
        if not camera.is_enabled():
            print(f"[CameraController] Camera {camera_id} is disabled")
            return False
        
        try:
            # control_id에 따른 제어 동작
            if control_id == 0:
                return camera.pan_left()
            elif control_id == 1:
                return camera.pan_right()
            elif control_id == 2:
                return camera.zoom_in()
            elif control_id == 3:
                return camera.zoom_out()
            else:
                print(f"[CameraController] Unknown control_id: {control_id}")
                return False
        except Exception as e:
            print(f"[CameraController] Failed to control camera {camera_id}: {e}")
            return False
    
    def display_thumbnail_view(self) -> Optional[Image.Image]:
        """
        모든 카메라의 썸네일 뷰 표시
        :return: 썸네일 이미지 (PIL Image) 또는 None
        """
        if self._total_camera_number == 0:
            print("[CameraController] No cameras available")
            return None
        
        try:
            from PIL import Image
            import os
            
            # 썸네일 그리드 크기 계산
            cols = min(3, self._total_camera_number)
            rows = (self._total_camera_number + cols - 1) // cols
            
            thumbnail_size = 300
            img = Image.new('RGB', (cols * thumbnail_size, rows * thumbnail_size), color='gray')
            
            # 각 카메라 썸네일 로드 및 배치
            for idx, (camera_id, camera) in enumerate(sorted(self._cameras.items())):
                row = idx // cols
                col = idx % cols
                x = col * thumbnail_size
                y = row * thumbnail_size
                
                # SafeHomeCamera의 display_view() 사용
                thumb_view = camera.display_view()
                if thumb_view:
                    thumb = thumb_view.resize((thumbnail_size, thumbnail_size), Image.LANCZOS)
                    img.paste(thumb, (x, y))
                else:
                    # 이미지가 없으면 검은색 박스
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([x, y, x + thumbnail_size, y + thumbnail_size], 
                                 fill='black', outline='white', width=2)
                    draw.text((x + thumbnail_size // 2, y + thumbnail_size // 2), 
                            f"Camera {camera_id}", fill='white', anchor='mm')
            
            return img
        except Exception as e:
            print(f"[CameraController] Failed to create thumbnail view: {e}")
            return None
    
    def display_single_view(self, camera_id: int) -> Optional[Image.Image]:
        """
        단일 카메라 뷰 표시 (SafeHomeCamera의 display_view() 사용)
        :param camera_id: 카메라 ID
        :return: 카메라 이미지 (PIL Image) 또는 None
        """
        if camera_id not in self._cameras:
            print(f"[CameraController] Camera {camera_id} not found")
            return None
        
        camera = self._cameras[camera_id]
        if not camera.is_enabled():
            print(f"[CameraController] Camera {camera_id} is disabled")
            return None
        
        return camera.display_view()
    
    def get_all_camera_info(self) -> List[List[int]]:
        """
        모든 카메라 정보 조회
        :return: 2D 정수 배열, 각 내부 배열은 [camera_id, x, y, enabled(0/1), ...] 형식
        """
        info_list = []
        for camera_id, camera in sorted(self._cameras.items()):
            location = camera.get_location()
            info_list.append([
                camera_id,
                location[0] if len(location) > 0 else 0,  # x
                location[1] if len(location) > 1 else 0,  # y
                1 if camera.is_enabled() else 0,  # enabled
                self._total_camera_number
            ])
        return info_list
    
    def set_camera_password(self, camera_id: int, input_password: str) -> None:
        """
        카메라 비밀번호 설정 (SafeHomeCamera의 set_password() 사용)
        :param camera_id: 카메라 ID
        :param input_password: 설정할 비밀번호
        :return: None
        """
        if camera_id not in self._cameras:
            print(f"[CameraController] Camera {camera_id} not found")
            return
        
        self._cameras[camera_id].set_password(input_password)
    
    def validate_camera_password(self, camera_id: int, input_password: str) -> int:
        """
        카메라 비밀번호 검증 (SafeHomeCamera의 password 사용)
        :param camera_id: 카메라 ID
        :param input_password: 입력한 비밀번호
        :return: 0=성공, 1=실패, -1=카메라 없음, -2=비밀번호 미설정
        """
        if camera_id not in self._cameras:
            return -1
        
        camera = self._cameras[camera_id]
        if not camera.has_password():
            return -2
        
        if camera.get_password() == input_password:
            return 0
        else:
            return 1
    
    def _delete_camera_password(self, camera_id: int) -> int:
        """
        카메라 비밀번호 삭제 (Private 메서드)
        :param camera_id: 카메라 ID
        :return: 0=성공, -1=카메라 없음, -2=비밀번호 없음
        """
        if camera_id not in self._cameras:
            return -1
        
        if camera_id not in self._camera_passwords:
            return -2
        
        del self._camera_passwords[camera_id]
        print(f"[CameraController] Password deleted for camera {camera_id}")
        return 0
    
    def trigger_security_event(self, source: str) -> None:
        """Capture images from enabled cameras for a security event."""
        if not getattr(self, '_cameras', None):
            print('[CameraController] No cameras to trigger')
            return

        print(f"[CameraController] Security event '{source}' captured by cameras")
        for camera_id, camera in self._cameras.items():
            # SafeHomeCamera의 is_enabled() 메서드를 사용하여 활성화 상태 확인
            if not camera.is_enabled():
                continue
            try:
                # SafeHomeCamera는 take_picture 메서드가 없을 수 있으므로
                # display_view를 호출하거나 예외 처리
                if hasattr(camera, 'take_picture'):
                    camera.take_picture()
                else:
                    # take_picture가 없으면 display_view를 호출하여 이미지 캡처
                    camera.display_view()
            except Exception as exc:
                print(f'[CameraController] Failed to capture camera {camera_id}: {exc}')

    def get_camera_count(self) -> int:
        """
        총 카메라 개수 조회 (헬퍼 메서드)
        :return: 총 카메라 개수
        """
        return self._total_camera_number
    
    def get_camera(self, camera_id: int) -> Optional[SafeHomeCamera]:
        """
        카메라 객체 조회 (헬퍼 메서드)
        :param camera_id: 카메라 ID
        :return: SafeHomeCamera 객체 또는 None
        """
        return self._cameras.get(camera_id)

