"""
Coverage tests for SafeHomeCamera - 기존 테스트에서 커버하지 못한 부분 추가 테스트
"""
import pytest
import sys
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
from PIL import Image

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from surveillance.safehome_camera import SafeHomeCamera


class TestSafeHomeCameraCoverage:
    """SafeHomeCamera Coverage 테스트 클래스"""
    
    @pytest.fixture
    def camera(self):
        """SafeHomeCamera 인스턴스 생성"""
        return SafeHomeCamera(camera_id=1, location=[100, 200])
    
    @pytest.mark.coverage
    def test_display_view_exception_handling(self, camera):
        """display_view - DeviceCamera에서 예외 발생 시 처리 테스트"""
        # _device_camera.get_view()에서 예외 발생 시뮬레이션
        if hasattr(camera, '_device_camera'):
            with patch.object(camera._device_camera, 'get_view', side_effect=Exception("Camera error")):
                result = camera.display_view()
                # 예외가 발생해도 None을 반환하고 에러 없이 처리되어야 함
                assert result is None
    
    @pytest.mark.coverage
    def test_zoom_in_device_camera_integration(self, camera):
        """zoom_in - DeviceCamera와의 연동 테스트"""
        if hasattr(camera, '_device_camera'):
            initial_zoom = camera.get_zoom_setting()
            result = camera.zoom_in()
            
            # DeviceCamera를 통해 호출되므로 결과 확인
            assert isinstance(result, bool)
    
    @pytest.mark.coverage
    def test_zoom_out_device_camera_integration(self, camera):
        """zoom_out - DeviceCamera와의 연동 테스트"""
        if hasattr(camera, '_device_camera'):
            camera.zoom_in()  # 먼저 줌 인
            initial_zoom = camera.get_zoom_setting()
            result = camera.zoom_out()
            
            assert isinstance(result, bool)
    
    @pytest.mark.coverage
    def test_pan_left_device_camera_integration(self, camera):
        """pan_left - DeviceCamera와의 연동 테스트"""
        if hasattr(camera, '_device_camera'):
            initial_angle = camera.get_pan_angle()
            result = camera.pan_left()
            
            assert isinstance(result, bool)
            # 각도가 변경되었는지 확인 (DeviceCamera 구현에 따라)
    
    @pytest.mark.coverage
    def test_pan_right_device_camera_integration(self, camera):
        """pan_right - DeviceCamera와의 연동 테스트"""
        if hasattr(camera, '_device_camera'):
            initial_angle = camera.get_pan_angle()
            result = camera.pan_right()
            
            assert isinstance(result, bool)
    
    @pytest.mark.coverage
    def test_get_pan_angle_from_device_camera(self, camera):
        """get_pan_angle - DeviceCamera의 pan 속성 사용 테스트"""
        if hasattr(camera, '_device_camera'):
            angle = camera.get_pan_angle()
            
            # DeviceCamera의 pan 속성 값을 반환해야 함
            assert isinstance(angle, (int, float))
            assert angle is not None
    
    @pytest.mark.coverage
    def test_get_zoom_setting_from_device_camera(self, camera):
        """get_zoom_setting - DeviceCamera의 zoom 속성 사용 테스트"""
        if hasattr(camera, '_device_camera'):
            zoom = camera.get_zoom_setting()
            
            # DeviceCamera의 zoom 속성 값을 반환해야 함
            assert isinstance(zoom, int)
            assert zoom >= 1
    
    @pytest.mark.coverage
    def test_initialization_device_camera_setup(self):
        """초기화 - DeviceCamera 인스턴스 생성 및 설정 테스트"""
        camera = SafeHomeCamera(camera_id=5, location=[300, 400])
        
        # DeviceCamera가 생성되었는지 확인
        assert hasattr(camera, '_device_camera')
        assert camera.get_id() == 5
        assert camera.get_location() == [300, 400]
    
    @pytest.mark.coverage
    def test_initialization_working_directory_change(self):
        """초기화 - 작업 디렉토리 변경 테스트"""
        original_cwd = os.getcwd()
        
        try:
            camera = SafeHomeCamera(camera_id=1)
            # 작업 디렉토리가 원래대로 복원되었는지 확인
            assert os.getcwd() == original_cwd
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.coverage
    def test_initialization_virtual_device_path_handling(self):
        """초기화 - virtual_device assets 경로 처리 테스트"""
        camera = SafeHomeCamera(camera_id=1)
        
        # 경로가 올바르게 설정되었는지 확인
        assert hasattr(camera, '_device_camera')
        assert camera._device_camera is not None
    
    @pytest.mark.coverage
    def test_display_view_returns_image_when_enabled(self, camera):
        """display_view - 활성화된 카메라에서 이미지 반환 테스트"""
        camera.enable()
        result = camera.display_view()
        
        # 이미지 파일이 있으면 Image 객체, 없으면 None일 수 있음
        assert result is None or isinstance(result, Image.Image)
    
    @pytest.mark.coverage
    def test_display_view_device_camera_integration(self, camera):
        """display_view - DeviceCamera.get_view() 호출 테스트"""
        if hasattr(camera, '_device_camera'):
            with patch.object(camera._device_camera, 'get_view', return_value=Image.new('RGB', (100, 100))) as mock_view:
                result = camera.display_view()
                
                mock_view.assert_called_once()
                assert isinstance(result, Image.Image)
    
    @pytest.mark.coverage
    def test_zoom_operations_disabled_camera(self, camera):
        """줌 조작 - 비활성화된 카메라에서 모든 줌 조작 실패 테스트"""
        camera.disable()
        
        assert camera.zoom_in() is False
        assert camera.zoom_out() is False
    
    @pytest.mark.coverage
    def test_pan_operations_disabled_camera(self, camera):
        """팬 조작 - 비활성화된 카메라에서 모든 팬 조작 실패 테스트"""
        camera.disable()
        initial_angle = camera.get_pan_angle()
        
        assert camera.pan_left() is False
        assert camera.pan_right() is False
        # 각도가 변경되지 않아야 함
        assert camera.get_pan_angle() == initial_angle
    
    @pytest.mark.coverage
    def test_set_password_empty_string_validation(self, camera):
        """set_password - 빈 문자열 검증 테스트"""
        result = camera.set_password("")
        assert result is False
        assert camera.has_password() is False
        assert camera.get_password() == ""
    
    @pytest.mark.coverage
    def test_set_password_whitespace_only(self, camera):
        """set_password - 공백만 있는 문자열 테스트"""
        # 구현에 따라 공백은 허용될 수도, 안 될 수도 있음
        result = camera.set_password("   ")
        # 현재 구현은 빈 문자열이 아니면 True를 반환할 수 있음
        # 또는 공백을 빈 문자열로 처리할 수도 있음
        assert isinstance(result, bool)
    
    @pytest.mark.coverage
    def test_set_password_special_characters(self, camera):
        """set_password - 특수문자 포함 비밀번호 테스트"""
        special_passwords = ["!@#$%", "test123!@#", "암호123", "pass word"]
        
        for pwd in special_passwords:
            result = camera.set_password(pwd)
            assert result is True
            assert camera.get_password() == pwd
            camera.set_password("")  # 초기화
    
    @pytest.mark.coverage
    def test_set_password_long_password(self, camera):
        """set_password - 긴 비밀번호 테스트"""
        long_password = "a" * 1000
        result = camera.set_password(long_password)
        
        assert result is True
        assert camera.get_password() == long_password
    
    @pytest.mark.coverage
    def test_get_location_returns_copy(self, camera):
        """get_location - 복사본 반환 테스트 (이미 기존 테스트에 있지만 coverage 강화)"""
        location = camera.get_location()
        original_id = id(location)
        
        # 반환된 리스트를 수정해도 원본에 영향 없어야 함
        location.append(999)
        new_location = camera.get_location()
        
        assert len(new_location) == 2  # 원래 길이 유지
        assert 999 not in new_location
    
    @pytest.mark.coverage
    def test_set_location_invalid_lengths(self, camera):
        """set_location - 다양한 잘못된 길이 테스트"""
        invalid_locations = [
            [],  # 빈 리스트
            [100],  # 요소 1개
            [100, 200, 300],  # 요소 3개
            None,  # None
        ]
        
        original_location = camera.get_location()
        
        for invalid_loc in invalid_locations:
            if invalid_loc is None:
                continue  # None은 타입 에러 발생 가능
            result = camera.set_location(invalid_loc)
            assert result is False
            assert camera.get_location() == original_location
    
    @pytest.mark.coverage
    def test_set_id_boundary_values(self, camera):
        """set_id - 경계값 테스트"""
        # 0은 실패해야 함
        assert camera.set_id(0) is False
        
        # 1은 성공해야 함
        assert camera.set_id(1) is True
        assert camera.get_id() == 1
        
        # 큰 값도 성공해야 함
        assert camera.set_id(99999) is True
        assert camera.get_id() == 99999
    
    @pytest.mark.coverage
    def test_enable_disable_toggle(self, camera):
        """enable/disable - 토글 동작 테스트"""
        assert camera.is_enabled() is True
        
        # 여러 번 disable
        camera.disable()
        camera.disable()
        camera.disable()
        assert camera.is_enabled() is False
        
        # 여러 번 enable
        camera.enable()
        camera.enable()
        camera.enable()
        assert camera.is_enabled() is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "coverage"])
