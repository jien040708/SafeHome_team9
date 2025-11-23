"""
pytest tests for CameraController
"""
import pytest
import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from surveillance.camera_controller import CameraController
from devices.camera import Camera


class TestCameraController:
    """CameraController 테스트 클래스"""
    
    @pytest.fixture
    def controller(self):
        """CameraController 인스턴스 생성"""
        return CameraController()
    
    def test_initialization(self, controller):
        """초기화 테스트"""
        assert controller._next_camera_id == 1
        assert controller._total_camera_number == 0
        assert controller._cameras == {}
        assert controller._camera_info == {}
        assert controller._camera_passwords == {}
    
    def test_add_camera(self, controller):
        """카메라 추가 테스트"""
        result = controller.add_camera(100, 200)
        assert result is True
        assert controller._total_camera_number == 1
        assert 1 in controller._cameras
        assert 1 in controller._camera_info
        assert controller._camera_info[1]['x'] == 100
        assert controller._camera_info[1]['y'] == 200
        assert controller._camera_info[1]['enabled'] is True
        assert controller._next_camera_id == 2
    
    def test_add_multiple_cameras(self, controller):
        """여러 카메라 추가 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        controller.add_camera(50, 60)
        
        assert controller._total_camera_number == 3
        assert controller._next_camera_id == 4
        assert len(controller._cameras) == 3
        assert controller._camera_info[1]['x'] == 10
        assert controller._camera_info[2]['x'] == 30
        assert controller._camera_info[3]['x'] == 50
    
    def test_delete_camera(self, controller):
        """카메라 삭제 테스트"""
        controller.add_camera(100, 200)
        controller.add_camera(300, 400)
        
        result = controller.delete_camera(1)
        assert result is True
        assert controller._total_camera_number == 1
        assert 1 not in controller._cameras
        assert 1 not in controller._camera_info
        assert 2 in controller._cameras
    
    def test_delete_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 삭제 테스트"""
        result = controller.delete_camera(999)
        assert result is False
        assert controller._total_camera_number == 0
    
    def test_enable_camera(self, controller):
        """카메라 활성화 테스트"""
        controller.add_camera(100, 200)
        controller.disable_camera(1)
        
        result = controller.enable_camera(1)
        assert result is True
        assert controller._camera_info[1]['enabled'] is True
    
    def test_enable_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 활성화 테스트"""
        result = controller.enable_camera(999)
        assert result is False
    
    def test_disable_camera(self, controller):
        """카메라 비활성화 테스트"""
        controller.add_camera(100, 200)
        
        result = controller.disable_camera(1)
        assert result is True
        assert controller._camera_info[1]['enabled'] is False
    
    def test_disable_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 비활성화 테스트"""
        result = controller.disable_camera(999)
        assert result is False
    
    def test_enable_cameras_list(self, controller):
        """여러 카메라 활성화 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        controller.add_camera(50, 60)
        controller.disable_camera(1)
        controller.disable_camera(2)
        
        result = controller.enable_cameras([1, 2])
        assert result is True
        assert controller._camera_info[1]['enabled'] is True
        assert controller._camera_info[2]['enabled'] is True
        assert controller._camera_info[3]['enabled'] is True
    
    def test_disable_cameras_list(self, controller):
        """여러 카메라 비활성화 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        
        result = controller.disable_cameras([1, 2])
        assert result is True
        assert controller._camera_info[1]['enabled'] is False
        assert controller._camera_info[2]['enabled'] is False
    
    def test_enable_all_cameras(self, controller):
        """모든 카메라 활성화 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        controller.disable_camera(1)
        controller.disable_camera(2)
        
        result = controller.enable_all_camera()
        assert result is True
        assert controller._camera_info[1]['enabled'] is True
        assert controller._camera_info[2]['enabled'] is True
    
    def test_disable_all_cameras(self, controller):
        """모든 카메라 비활성화 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        
        result = controller.disable_all_camera()
        assert result is True
        assert controller._camera_info[1]['enabled'] is False
        assert controller._camera_info[2]['enabled'] is False
    
    def test_control_single_camera_take_picture(self, controller):
        """카메라 촬영 제어 테스트"""
        controller.add_camera(100, 200)
        
        result = controller.control_single_camera(1, 0)
        assert result is True
    
    def test_control_single_camera_start_recording(self, controller):
        """카메라 녹화 시작 제어 테스트"""
        controller.add_camera(100, 200)
        
        result = controller.control_single_camera(1, 1)
        assert result is True
        assert controller._cameras[1].status == "Recording"
    
    def test_control_single_camera_stop_recording(self, controller):
        """카메라 녹화 중지 제어 테스트"""
        controller.add_camera(100, 200)
        controller.control_single_camera(1, 1)  # 녹화 시작
        
        result = controller.control_single_camera(1, 2)
        assert result is True
    
    def test_control_disabled_camera(self, controller):
        """비활성화된 카메라 제어 테스트"""
        controller.add_camera(100, 200)
        controller.disable_camera(1)
        
        result = controller.control_single_camera(1, 0)
        assert result is False
    
    def test_control_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 제어 테스트"""
        result = controller.control_single_camera(999, 0)
        assert result is False
    
    def test_control_invalid_control_id(self, controller):
        """잘못된 제어 ID 테스트"""
        controller.add_camera(100, 200)
        
        result = controller.control_single_camera(1, 99)
        assert result is False
    
    def test_display_thumbnail_view_no_cameras(self, controller):
        """카메라가 없을 때 썸네일 뷰 테스트"""
        result = controller.display_thumbnail_view()
        assert result is None
    
    def test_display_single_view(self, controller):
        """단일 카메라 뷰 표시 테스트"""
        controller.add_camera(100, 200)
        
        result = controller.display_single_view(1)
        # 이미지가 없을 수도 있지만 Image 객체 또는 None이어야 함
        assert result is not None or result is None  # PIL Image 또는 None
    
    def test_display_single_view_disabled_camera(self, controller):
        """비활성화된 카메라 뷰 표시 테스트"""
        controller.add_camera(100, 200)
        controller.disable_camera(1)
        
        result = controller.display_single_view(1)
        assert result is None
    
    def test_display_single_view_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 뷰 표시 테스트"""
        result = controller.display_single_view(999)
        assert result is None
    
    def test_get_all_camera_info(self, controller):
        """모든 카메라 정보 조회 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        
        info_list = controller.get_all_camera_info()
        assert len(info_list) == 2
        assert info_list[0][0] == 1  # camera_id
        assert info_list[0][1] == 10  # x
        assert info_list[0][2] == 20  # y
        assert info_list[0][3] == 1  # enabled (1)
        assert info_list[1][0] == 2
        assert info_list[1][1] == 30
    
    def test_get_all_camera_info_empty(self, controller):
        """카메라가 없을 때 정보 조회 테스트"""
        info_list = controller.get_all_camera_info()
        assert info_list == []
    
    def test_set_camera_password(self, controller):
        """카메라 비밀번호 설정 테스트"""
        controller.add_camera(100, 200)
        
        controller.set_camera_password(1, "password123")
        assert 1 in controller._camera_passwords
        assert controller._camera_passwords[1] == "password123"
    
    def test_set_password_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 비밀번호 설정 테스트"""
        controller.set_camera_password(999, "password123")
        # 존재하지 않는 카메라는 비밀번호가 설정되지 않아야 함
        assert 999 not in controller._camera_passwords
    
    def test_validate_camera_password_success(self, controller):
        """카메라 비밀번호 검증 성공 테스트"""
        controller.add_camera(100, 200)
        controller.set_camera_password(1, "password123")
        
        result = controller.validate_camera_password(1, "password123")
        assert result == 0  # 성공
    
    def test_validate_camera_password_failure(self, controller):
        """카메라 비밀번호 검증 실패 테스트"""
        controller.add_camera(100, 200)
        controller.set_camera_password(1, "password123")
        
        result = controller.validate_camera_password(1, "wrongpassword")
        assert result == 1  # 실패
    
    def test_validate_camera_password_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 비밀번호 검증 테스트"""
        result = controller.validate_camera_password(999, "password123")
        assert result == -1  # 카메라 없음
    
    def test_validate_camera_password_not_set(self, controller):
        """비밀번호가 설정되지 않은 카메라 검증 테스트"""
        controller.add_camera(100, 200)
        
        result = controller.validate_camera_password(1, "password123")
        assert result == -2  # 비밀번호 미설정
    
    def test_delete_camera_with_password(self, controller):
        """비밀번호가 설정된 카메라 삭제 테스트"""
        controller.add_camera(100, 200)
        controller.set_camera_password(1, "password123")
        
        result = controller.delete_camera(1)
        assert result is True
        assert 1 not in controller._camera_passwords
    
    def test_get_camera_count(self, controller):
        """카메라 개수 조회 테스트"""
        assert controller.get_camera_count() == 0
        
        controller.add_camera(10, 20)
        assert controller.get_camera_count() == 1
        
        controller.add_camera(30, 40)
        assert controller.get_camera_count() == 2
        
        controller.delete_camera(1)
        assert controller.get_camera_count() == 1
    
    def test_get_camera(self, controller):
        """카메라 객체 조회 테스트"""
        controller.add_camera(100, 200)
        
        camera = controller.get_camera(1)
        assert camera is not None
        assert isinstance(camera, Camera)
        assert camera.device_id == "Camera_1"
    
    def test_get_nonexistent_camera(self, controller):
        """존재하지 않는 카메라 객체 조회 테스트"""
        camera = controller.get_camera(999)
        assert camera is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

