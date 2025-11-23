"""
pytest tests for SafeHomeCamera
"""
import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from surveillance.safehome_camera import SafeHomeCamera
from PIL import Image


class TestSafeHomeCamera:
    """SafeHomeCamera 테스트 클래스"""
    
    @pytest.fixture
    def camera(self):
        """SafeHomeCamera 인스턴스 생성"""
        return SafeHomeCamera(camera_id=1, location=[100, 200])
    
    def test_initialization_with_location(self):
        """위치와 함께 초기화 테스트"""
        camera = SafeHomeCamera(camera_id=1, location=[100, 200])
        assert camera.get_id() == 1
        assert camera.get_location() == [100, 200]
        assert camera.get_pan_angle() == 0.0
        assert camera.get_zoom_setting() == 1
        assert camera.is_enabled() is True
        assert camera.has_password() is False
    
    def test_initialization_without_location(self):
        """위치 없이 초기화 테스트"""
        camera = SafeHomeCamera(camera_id=2)
        assert camera.get_id() == 2
        assert camera.get_location() == [0, 0]
    
    def test_get_location(self, camera):
        """위치 조회 테스트"""
        location = camera.get_location()
        assert location == [100, 200]
        # 복사본이 반환되는지 확인
        location[0] = 999
        assert camera.get_location() == [100, 200]
    
    def test_set_location(self, camera):
        """위치 설정 테스트"""
        result = camera.set_location([300, 400])
        assert result is True
        assert camera.get_location() == [300, 400]
    
    def test_set_invalid_location(self, camera):
        """잘못된 위치 설정 테스트"""
        result = camera.set_location([100])  # y 좌표 없음
        assert result is False
        assert camera.get_location() == [100, 200]  # 원래 값 유지
    
    def test_get_id(self, camera):
        """ID 조회 테스트"""
        assert camera.get_id() == 1
    
    def test_set_id(self, camera):
        """ID 설정 테스트"""
        result = camera.set_id(5)
        assert result is True
        assert camera.get_id() == 5
    
    def test_set_invalid_id(self, camera):
        """잘못된 ID 설정 테스트"""
        result = camera.set_id(0)
        assert result is False
        assert camera.get_id() == 1  # 원래 값 유지
        
        result = camera.set_id(-1)
        assert result is False
    
    def test_display_view(self, camera):
        """뷰 표시 테스트"""
        result = camera.display_view()
        assert result is not None
        assert isinstance(result, Image.Image)
    
    def test_display_view_disabled_camera(self, camera):
        """비활성화된 카메라 뷰 표시 테스트"""
        camera.disable()
        result = camera.display_view()
        assert result is None
    
    def test_zoom_in(self, camera):
        """줌 인 테스트"""
        initial_zoom = camera.get_zoom_setting()
        result = camera.zoom_in()
        assert result is True
        assert camera.get_zoom_setting() == initial_zoom + 1
    
    def test_zoom_in_max(self, camera):
        """최대 줌 인 테스트"""
        # 최대 줌까지 증가
        for _ in range(10):
            camera.zoom_in()
        
        # 이미 최대 줌인 상태에서 다시 줌 인 시도
        result = camera.zoom_in()
        assert result is False
        assert camera.get_zoom_setting() == 10  # 최대 줌 레벨
    
    def test_zoom_in_disabled_camera(self, camera):
        """비활성화된 카메라 줌 인 테스트"""
        camera.disable()
        initial_zoom = camera.get_zoom_setting()
        result = camera.zoom_in()
        assert result is False
        assert camera.get_zoom_setting() == initial_zoom
    
    def test_zoom_out(self, camera):
        """줌 아웃 테스트"""
        camera.zoom_in()  # 먼저 줌 인
        initial_zoom = camera.get_zoom_setting()
        result = camera.zoom_out()
        assert result is True
        assert camera.get_zoom_setting() == initial_zoom - 1
    
    def test_zoom_out_min(self, camera):
        """최소 줌 아웃 테스트"""
        # 이미 최소 줌인 상태
        result = camera.zoom_out()
        assert result is False
        assert camera.get_zoom_setting() == 1  # 최소 줌 레벨
    
    def test_zoom_out_disabled_camera(self, camera):
        """비활성화된 카메라 줌 아웃 테스트"""
        camera.zoom_in()
        camera.disable()
        initial_zoom = camera.get_zoom_setting()
        result = camera.zoom_out()
        assert result is False
        assert camera.get_zoom_setting() == initial_zoom
    
    def test_pan_left(self, camera):
        """팬 왼쪽 이동 테스트"""
        initial_angle = camera.get_pan_angle()
        result = camera.pan_left()
        assert result is True
        assert camera.get_pan_angle() == initial_angle - 5.0
    
    def test_pan_left_limit(self, camera):
        """팬 왼쪽 최대 한계 테스트"""
        # -180도까지 이동
        for _ in range(37):  # 37 * 5 = 185도, -180도에서 멈춤
            camera.pan_left()
        
        angle = camera.get_pan_angle()
        assert angle == -180.0
        result = camera.pan_left()
        assert result is True
        assert camera.get_pan_angle() == -180.0  # 더 이상 감소하지 않음
    
    def test_pan_left_disabled_camera(self, camera):
        """비활성화된 카메라 팬 왼쪽 이동 테스트"""
        camera.disable()
        initial_angle = camera.get_pan_angle()
        result = camera.pan_left()
        assert result is False
        assert camera.get_pan_angle() == initial_angle
    
    def test_pan_right(self, camera):
        """팬 오른쪽 이동 테스트"""
        initial_angle = camera.get_pan_angle()
        result = camera.pan_right()
        assert result is True
        assert camera.get_pan_angle() == initial_angle + 5.0
    
    def test_pan_right_limit(self, camera):
        """팬 오른쪽 최대 한계 테스트"""
        # 180도까지 이동
        for _ in range(37):  # 37 * 5 = 185도, 180도에서 멈춤
            camera.pan_right()
        
        angle = camera.get_pan_angle()
        assert angle == 180.0
        result = camera.pan_right()
        assert result is True
        assert camera.get_pan_angle() == 180.0  # 더 이상 증가하지 않음
    
    def test_pan_right_disabled_camera(self, camera):
        """비활성화된 카메라 팬 오른쪽 이동 테스트"""
        camera.disable()
        initial_angle = camera.get_pan_angle()
        result = camera.pan_right()
        assert result is False
        assert camera.get_pan_angle() == initial_angle
    
    def test_get_password_not_set(self, camera):
        """비밀번호가 설정되지 않았을 때 조회 테스트"""
        password = camera.get_password()
        assert password == ""
    
    def test_set_password(self, camera):
        """비밀번호 설정 테스트"""
        result = camera.set_password("mypassword123")
        assert result is True
        assert camera.get_password() == "mypassword123"
        assert camera.has_password() is True
    
    def test_set_empty_password(self, camera):
        """빈 비밀번호 설정 테스트"""
        result = camera.set_password("")
        assert result is False
        assert camera.has_password() is False
    
    def test_has_password(self, camera):
        """비밀번호 설정 여부 조회 테스트"""
        assert camera.has_password() is False
        
        camera.set_password("password123")
        assert camera.has_password() is True
    
    def test_is_enabled(self, camera):
        """활성화 상태 조회 테스트"""
        assert camera.is_enabled() is True
        
        camera.disable()
        assert camera.is_enabled() is False
        
        camera.enable()
        assert camera.is_enabled() is True
    
    def test_enable(self, camera):
        """카메라 활성화 테스트"""
        camera.disable()
        assert camera.is_enabled() is False
        
        camera.enable()
        assert camera.is_enabled() is True
    
    def test_disable(self, camera):
        """카메라 비활성화 테스트"""
        assert camera.is_enabled() is True
        
        camera.disable()
        assert camera.is_enabled() is False
    
    def test_save_info(self, camera):
        """카메라 정보 저장 테스트"""
        result = camera.save_info()
        assert result is True
    
    def test_get_pan_angle(self, camera):
        """팬 각도 조회 테스트"""
        assert camera.get_pan_angle() == 0.0
        
        camera.pan_right()
        assert camera.get_pan_angle() == 5.0
        
        camera.pan_left()
        camera.pan_left()
        assert camera.get_pan_angle() == -5.0
    
    def test_get_zoom_setting(self, camera):
        """줌 설정 조회 테스트"""
        assert camera.get_zoom_setting() == 1
        
        camera.zoom_in()
        assert camera.get_zoom_setting() == 2
        
        camera.zoom_out()
        assert camera.get_zoom_setting() == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

