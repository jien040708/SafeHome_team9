"""
Integration tests for surveillance system
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from surveillance.camera_controller import CameraController
from surveillance.safehome_camera import SafeHomeCamera
from devices.camera import Camera


class TestSurveillanceIntegration:
    """Surveillance 시스템 통합 테스트"""
    
    @pytest.fixture
    def controller(self):
        """CameraController 인스턴스 생성"""
        return CameraController()
    
    def test_camera_lifecycle(self, controller):
        """카메라 전체 생명주기 테스트"""
        # 1. 카메라 추가
        assert controller.add_camera(100, 200) is True
        assert controller.get_camera_count() == 1
        
        # 2. 카메라 정보 확인
        camera = controller.get_camera(1)
        assert camera is not None
        assert isinstance(camera, Camera)
        
        # 3. 카메라 비밀번호 설정
        controller.set_camera_password(1, "test123")
        assert controller.validate_camera_password(1, "test123") == 0
        
        # 4. 카메라 활성화/비활성화
        controller.disable_camera(1)
        assert controller._camera_info[1]['enabled'] is False
        assert controller.display_single_view(1) is None  # 비활성화 시 뷰 없음
        
        controller.enable_camera(1)
        assert controller._camera_info[1]['enabled'] is True
        
        # 5. 카메라 제어
        assert controller.control_single_camera(1, 0) is True  # 촬영
        assert controller.control_single_camera(1, 1) is True  # 녹화 시작
        
        # 6. 카메라 삭제
        assert controller.delete_camera(1) is True
        assert controller.get_camera_count() == 0
        assert controller.get_camera(1) is None
    
    def test_multiple_cameras_management(self, controller):
        """여러 카메라 관리 테스트"""
        # 여러 카메라 추가
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        controller.add_camera(50, 60)
        
        assert controller.get_camera_count() == 3
        
        # 모든 카메라 비밀번호 설정
        controller.set_camera_password(1, "pass1")
        controller.set_camera_password(2, "pass2")
        controller.set_camera_password(3, "pass3")
        
        # 비밀번호 검증
        assert controller.validate_camera_password(1, "pass1") == 0
        assert controller.validate_camera_password(2, "pass2") == 0
        assert controller.validate_camera_password(3, "pass3") == 0
        
        # 일부 카메라 비활성화
        controller.disable_cameras([1, 2])
        assert controller._camera_info[1]['enabled'] is False
        assert controller._camera_info[2]['enabled'] is False
        assert controller._camera_info[3]['enabled'] is True
        
        # 모든 카메라 활성화
        controller.enable_all_camera()
        assert all(info['enabled'] for info in controller._camera_info.values())
        
        # 일부 카메라 삭제
        controller.delete_camera(2)
        assert controller.get_camera_count() == 2
        assert 2 not in controller._cameras
        assert 2 not in controller._camera_passwords
    
    def test_camera_view_integration(self, controller):
        """카메라 뷰 통합 테스트"""
        # 카메라 추가
        controller.add_camera(100, 200)
        controller.add_camera(300, 400)
        
        # 단일 뷰 표시
        view1 = controller.display_single_view(1)
        view2 = controller.display_single_view(2)
        # 이미지가 없을 수도 있지만 None이 아닐 수도 있음
        # (이미지 파일 존재 여부에 따라)
        
        # 썸네일 뷰 표시
        thumbnail = controller.display_thumbnail_view()
        # 카메라가 있으므로 None이 아니어야 함 (이미지 파일이 있다면)
        
        # 비활성화된 카메라는 뷰 표시 안 됨
        controller.disable_camera(1)
        assert controller.display_single_view(1) is None
    
    def test_camera_control_workflow(self, controller):
        """카메라 제어 워크플로우 테스트"""
        controller.add_camera(100, 200)
        
        # 1. 촬영
        assert controller.control_single_camera(1, 0) is True
        
        # 2. 녹화 시작
        assert controller.control_single_camera(1, 1) is True
        assert controller._cameras[1].status == "Recording"
        
        # 3. 녹화 중지
        assert controller.control_single_camera(1, 2) is True
        assert controller._cameras[1].status == "idle"
        
        # 비활성화된 카메라는 제어 불가
        controller.disable_camera(1)
        assert controller.control_single_camera(1, 0) is False
    
    def test_camera_password_security(self, controller):
        """카메라 비밀번호 보안 테스트"""
        controller.add_camera(100, 200)
        
        # 비밀번호 설정 전 검증
        assert controller.validate_camera_password(1, "any") == -2  # 비밀번호 미설정
        
        # 비밀번호 설정
        controller.set_camera_password(1, "secure123")
        
        # 올바른 비밀번호
        assert controller.validate_camera_password(1, "secure123") == 0
        
        # 잘못된 비밀번호
        assert controller.validate_camera_password(1, "wrong") == 1
        
        # 존재하지 않는 카메라
        assert controller.validate_camera_password(999, "any") == -1
        
        # 카메라 삭제 시 비밀번호도 삭제되는지 확인
        controller.delete_camera(1)
        assert 1 not in controller._camera_passwords
    
    def test_camera_info_consistency(self, controller):
        """카메라 정보 일관성 테스트"""
        # 카메라 추가
        controller.add_camera(150, 250)
        controller.add_camera(350, 450)
        
        # 정보 조회
        info_list = controller.get_all_camera_info()
        assert len(info_list) == 2
        
        # 각 카메라의 정보 확인
        for info in info_list:
            camera_id = info[0]
            assert camera_id in controller._cameras
            assert camera_id in controller._camera_info
            assert info[1] == controller._camera_info[camera_id]['x']
            assert info[2] == controller._camera_info[camera_id]['y']
            assert info[3] == (1 if controller._camera_info[camera_id]['enabled'] else 0)
        
        # 카메라 비활성화 후 정보 업데이트 확인
        controller.disable_camera(1)
        info_list_updated = controller.get_all_camera_info()
        assert info_list_updated[0][3] == 0  # 비활성화됨
    
    def test_camera_controller_with_safehome_camera(self):
        """CameraController와 SafeHomeCamera 통합 테스트"""
        # SafeHomeCamera는 별도 클래스이지만, 
        # CameraController는 Camera 객체를 사용함을 확인
        controller = CameraController()
        controller.add_camera(100, 200)
        
        camera = controller.get_camera(1)
        assert isinstance(camera, Camera)
        assert isinstance(camera, SafeHomeCamera)

        # SafeHomeCamera는 독립적으로 사용 가능
        safehome_cam = SafeHomeCamera(camera_id=99, location=[500, 600])
        assert safehome_cam.get_id() == 99
        assert safehome_cam.get_location() == [500, 600]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
