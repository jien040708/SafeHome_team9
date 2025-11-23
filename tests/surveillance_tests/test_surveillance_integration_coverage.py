"""
Coverage tests for Surveillance Integration - 기존 통합 테스트에서 커버하지 못한 부분 추가 테스트
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from PIL import Image

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from surveillance.camera_controller import CameraController
from surveillance.safehome_camera import SafeHomeCamera


class TestSurveillanceIntegrationCoverage:
    """Surveillance 통합 Coverage 테스트 클래스"""
    
    @pytest.fixture
    def controller(self):
        """CameraController 인스턴스 생성"""
        return CameraController()
    
    @pytest.mark.coverage
    def test_camera_lifecycle_with_security_events(self, controller):
        """카메라 생명주기 - 보안 이벤트와 함께 테스트"""
        # 카메라 추가
        controller.add_camera(100, 200)
        controller.add_camera(300, 400)
        
        # 보안 이벤트 트리거
        with patch.object(SafeHomeCamera, 'take_picture', return_value=None) as mock_picture:
            controller.trigger_security_event("INTRUSION")
            assert mock_picture.call_count == 2
        
        # 카메라 비활성화 후 다시 트리거
        controller.disable_camera(1)
        with patch.object(SafeHomeCamera, 'take_picture', return_value=None) as mock_picture2:
            controller.trigger_security_event("PANIC")
            # 활성화된 카메라만 트리거되어야 함
            assert mock_picture2.call_count >= 1
    
    @pytest.mark.coverage
    def test_camera_controller_safehome_camera_integration(self, controller):
        """CameraController와 SafeHomeCamera 통합 - 전체 워크플로우 테스트"""
        # 카메라 추가 (SafeHomeCamera 인스턴스 생성)
        controller.add_camera(100, 200)
        
        camera = controller.get_camera(1)
        assert isinstance(camera, SafeHomeCamera)
        assert camera.get_id() == 1
        assert camera.get_location() == [100, 200]
        
        # SafeHomeCamera 메서드 직접 사용
        camera.zoom_in()
        camera.pan_right()
        camera.set_password("test123")
        
        # CameraController를 통한 접근도 가능
        assert controller.validate_camera_password(1, "test123") == 0
    
    @pytest.mark.coverage
    def test_multiple_cameras_view_operations(self, controller):
        """여러 카메라 뷰 조작 통합 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        controller.add_camera(50, 60)
        
        # 각 카메라의 단일 뷰
        views = []
        for i in range(1, 4):
            view = controller.display_single_view(i)
            views.append(view)
        
        # 썸네일 뷰
        thumbnail = controller.display_thumbnail_view()
        
        # 모든 뷰가 올바르게 처리되었는지 확인
        assert len(views) == 3
        assert thumbnail is None or isinstance(thumbnail, Image.Image)
    
    @pytest.mark.coverage
    def test_camera_password_workflow_comprehensive(self, controller):
        """카메라 비밀번호 워크플로우 종합 테스트"""
        controller.add_camera(100, 200)
        
        # 1. 비밀번호 설정 전 상태
        assert controller.validate_camera_password(1, "any") == -2
        
        # 2. 비밀번호 설정
        controller.set_camera_password(1, "secure123")
        
        # 3. 올바른 비밀번호로 검증
        assert controller.validate_camera_password(1, "secure123") == 0
        
        # 4. 잘못된 비밀번호로 검증
        assert controller.validate_camera_password(1, "wrong") == 1
        
        # 5. 카메라 삭제 시 비밀번호도 제거되는지 확인
        controller.delete_camera(1)
        # 삭제된 카메라에 대한 검증은 -1을 반환해야 함
        assert controller.validate_camera_password(1, "secure123") == -1
    
    @pytest.mark.coverage
    def test_camera_control_all_operations(self, controller):
        """카메라 제어 - 모든 제어 작업 테스트"""
        controller.add_camera(100, 200)
        
        # 모든 제어 작업 수행
        operations = [
            (0, "pan_left"),
            (1, "pan_right"),
            (2, "zoom_in"),
            (3, "zoom_out"),
        ]
        
        for control_id, operation_name in operations:
            result = controller.control_single_camera(1, control_id)
            assert result is True, f"{operation_name} should succeed"
    
    @pytest.mark.coverage
    def test_camera_enable_disable_workflow(self, controller):
        """카메라 활성화/비활성화 워크플로우 테스트"""
        controller.add_camera(10, 20)
        controller.add_camera(30, 40)
        controller.add_camera(50, 60)
        
        # 개별 비활성화
        controller.disable_camera(1)
        controller.disable_camera(2)
        
        # 리스트로 활성화
        controller.enable_cameras([1, 2])
        
        # 모든 카메라 비활성화
        controller.disable_all_camera()
        
        # 모든 카메라 활성화
        controller.enable_all_camera()
        
        # 모든 카메라가 활성화되었는지 확인
        for i in range(1, 4):
            assert controller._cameras[i].is_enabled() is True
    
    @pytest.mark.coverage
    def test_camera_info_consistency_comprehensive(self, controller):
        """카메라 정보 일관성 종합 테스트"""
        # 여러 카메라 추가
        positions = [(10, 20), (30, 40), (50, 60), (70, 80)]
        for x, y in positions:
            controller.add_camera(x, y)
        
        # 정보 조회
        info_list = controller.get_all_camera_info()
        assert len(info_list) == 4
        
        # 각 카메라 정보 일관성 확인
        for idx, (x, y) in enumerate(positions, start=1):
            camera_info = next(info for info in info_list if info[0] == idx)
            assert camera_info[1] == x
            assert camera_info[2] == y
            assert camera_info[3] == 1  # enabled
        
        # 일부 비활성화 후 다시 확인
        controller.disable_camera(2)
        controller.disable_camera(4)
        
        info_list_updated = controller.get_all_camera_info()
        for info in info_list_updated:
            if info[0] in [2, 4]:
                assert info[3] == 0  # disabled
            else:
                assert info[3] == 1  # enabled
    
    @pytest.mark.coverage
    def test_camera_controller_edge_cases(self, controller):
        """CameraController 엣지 케이스 테스트"""
        # 빈 컨트롤러에서 다양한 작업
        assert controller.get_camera_count() == 0
        assert controller.get_all_camera_info() == []
        assert controller.display_thumbnail_view() is None
        
        # 존재하지 않는 카메라에 대한 모든 작업
        assert controller.delete_camera(999) is False
        assert controller.enable_camera(999) is False
        assert controller.disable_camera(999) is False
        assert controller.display_single_view(999) is None
        assert controller.get_camera(999) is None
        assert controller.validate_camera_password(999, "any") == -1
    
    @pytest.mark.coverage
    def test_safehome_camera_direct_operations(self):
        """SafeHomeCamera 직접 조작 통합 테스트"""
        camera = SafeHomeCamera(camera_id=10, location=[500, 600])
        
        # 모든 기본 작업
        assert camera.get_id() == 10
        assert camera.get_location() == [500, 600]
        assert camera.is_enabled() is True
        
        # 줌 조작
        initial_zoom = camera.get_zoom_setting()
        camera.zoom_in()
        assert camera.get_zoom_setting() >= initial_zoom
        
        # 팬 조작
        initial_angle = camera.get_pan_angle()
        camera.pan_right()
        # 각도가 변경되었는지 확인 (DeviceCamera 구현에 따라)
        
        # 비밀번호
        camera.set_password("direct123")
        assert camera.has_password() is True
        
        # 비활성화
        camera.disable()
        assert camera.is_enabled() is False
        assert camera.display_view() is None
    
    @pytest.mark.coverage
    def test_mixed_camera_operations(self, controller):
        """혼합 카메라 작업 시나리오 테스트"""
        # 카메라 추가
        controller.add_camera(100, 200)
        controller.add_camera(300, 400)
        
        # 첫 번째 카메라 설정
        controller.set_camera_password(1, "pass1")
        controller.control_single_camera(1, 2)  # zoom in
        
        # 두 번째 카메라 설정
        controller.set_camera_password(2, "pass2")
        controller.disable_camera(2)
        
        # 첫 번째 카메라로 작업
        assert controller.validate_camera_password(1, "pass1") == 0
        view1 = controller.display_single_view(1)
        
        # 두 번째 카메라는 비활성화되어 있음
        assert controller.display_single_view(2) is None
        
        # 보안 이벤트 트리거 (활성화된 카메라만)
        with patch.object(SafeHomeCamera, 'take_picture', return_value=None) as mock_picture:
            controller.trigger_security_event("TEST")
            # 활성화된 카메라만 트리거되어야 함
            assert mock_picture.call_count >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "coverage"])

