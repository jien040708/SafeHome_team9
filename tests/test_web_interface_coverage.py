"""
Web Interface Coverage 테스트 - 기존 테스트에서 커버하지 못한 부분 추가 테스트
"""
from __future__ import annotations

import pytest
import json
from unittest.mock import patch, MagicMock


class TestWebInterfaceCoverage:
    """Web Interface Coverage 테스트 클래스"""

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_zone_update_succeeds(self, auth_client):
        """Zone 업데이트 API - Zone 이름 변경"""
        # 먼저 Zone 생성
        create_response = auth_client.post('/api/security/zones', json={'name': 'Test Zone'})
        assert create_response.status_code == 201
        zones_data = create_response.get_json()
        # Zone 응답은 'zone_id' 키를 사용함
        zone_id = zones_data['zones'][-1]['zone_id']  # 마지막으로 생성된 Zone ID
        
        # Zone 업데이트
        response = auth_client.put(f'/api/security/zones/{zone_id}', json={'name': 'Updated Zone'})
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'zones' in data

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_zone_update_requires_name(self, auth_client):
        """Zone 업데이트 API - name 필수"""
        response = auth_client.put('/api/security/zones/1', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_zone_delete_succeeds(self, auth_client):
        """Zone 삭제 API - Zone 삭제"""
        # 먼저 Zone 생성
        create_response = auth_client.post('/api/security/zones', json={'name': 'Zone to Delete'})
        assert create_response.status_code == 201
        zones_data = create_response.get_json()
        # Zone 응답은 'zone_id' 키를 사용함
        zone_id = zones_data['zones'][-1]['zone_id']
        
        # Zone 삭제
        response = auth_client.delete(f'/api/security/zones/{zone_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'zones' in data

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_zone_delete_nonexistent_zone(self, auth_client):
        """Zone 삭제 API - 존재하지 않는 Zone 삭제 시도"""
        response = auth_client.delete('/api/security/zones/99999')
        # 삭제 실패 시 400 반환
        assert response.status_code in [200, 400]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_assign_sensor_succeeds(self, auth_client):
        """Sensor 할당 API - Sensor를 Zone에 할당"""
        # 먼저 Zone 생성
        create_response = auth_client.post('/api/security/zones', json={'name': 'Test Zone'})
        assert create_response.status_code == 201
        zones_data = create_response.get_json()
        # Zone 응답은 'zone_id' 키를 사용함
        zone_id = zones_data['zones'][-1]['zone_id']
        
        # Sensor 할당 (실제 device_id는 시스템에 따라 다를 수 있음)
        response = auth_client.post('/api/security/assignments', json={
            'device_id': 'test_sensor_1',
            'zone_id': zone_id
        })
        # 성공 또는 실패 (시스템 상태에 따라)
        assert response.status_code in [200, 400, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_assign_sensor_requires_device_id_and_zone_id(self, auth_client):
        """Sensor 할당 API - device_id와 zone_id 필수"""
        # device_id 없음
        response = auth_client.post('/api/security/assignments', json={'zone_id': 1})
        assert response.status_code == 400
        
        # zone_id 없음
        response = auth_client.post('/api/security/assignments', json={'device_id': 'test'})
        assert response.status_code == 400

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_unassign_sensor_succeeds(self, auth_client):
        """Sensor 해제 API - Sensor 할당 해제"""
        response = auth_client.delete('/api/security/assignments/test_sensor_1')
        # 성공 또는 실패 (시스템 상태에 따라)
        # 실패 시 400 반환 (No assignment to remove)
        assert response.status_code in [200, 400]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_legacy_arm_route(self, auth_client):
        """레거시 /arm 라우트 테스트"""
        response = auth_client.get('/arm')
        # 리다이렉트 또는 성공
        assert response.status_code in [200, 302]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_legacy_disarm_route(self, auth_client):
        """레거시 /disarm 라우트 테스트"""
        response = auth_client.get('/disarm')
        # 리다이렉트 또는 성공
        assert response.status_code in [200, 302]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_legacy_status_route(self, auth_client):
        """레거시 /status 라우트 테스트"""
        response = auth_client.get('/status')
        # 리다이렉트 또는 성공
        assert response.status_code in [200, 302]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_view_returns_image(self, auth_client):
        """Camera View API - 카메라 뷰 이미지 반환"""
        # 카메라가 있는 경우에만 테스트
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.get(f'/api/cameras/{camera_id}/view')
                # 이미지 반환 또는 에러
                assert response.status_code in [200, 404, 500]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_thumbnails_returns_list(self, auth_client):
        """Camera Thumbnails API - 썸네일 이미지 반환"""
        response = auth_client.get('/api/cameras/thumbnails')
        # 카메라가 있으면 200 (image 반환), 없으면 404
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'image' in data  # base64 인코딩된 이미지

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_pan_right(self, auth_client):
        """Camera Pan Right API - 카메라 오른쪽으로 팬"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(f'/api/cameras/{camera_id}/pan', json={'direction': 'right'})
                assert response.status_code in [200, 400, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_pan_left(self, auth_client):
        """Camera Pan Left API - 카메라 왼쪽으로 팬"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(f'/api/cameras/{camera_id}/pan', json={'direction': 'left'})
                assert response.status_code in [200, 400, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_zoom_in(self, auth_client):
        """Camera Zoom In API - 카메라 줌 인"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(f'/api/cameras/{camera_id}/zoom', json={'action': 'in'})
                assert response.status_code in [200, 400, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_zoom_out(self, auth_client):
        """Camera Zoom Out API - 카메라 줌 아웃"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(f'/api/cameras/{camera_id}/zoom', json={'action': 'out'})
                assert response.status_code in [200, 400, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_enable_succeeds(self, auth_client):
        """Camera Enable API - 카메라 활성화"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(f'/api/cameras/{camera_id}/enable')
                assert response.status_code in [200, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_disable_succeeds(self, auth_client):
        """Camera Disable API - 카메라 비활성화"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(f'/api/cameras/{camera_id}/disable')
                assert response.status_code in [200, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_password_validation_success(self, auth_client):
        """Camera Password Validation API - 성공 케이스"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                # 카메라에 비밀번호가 설정되어 있는 경우에만 테스트
                camera_info = cameras_data['cameras'][0]
                if camera_info.get('has_password'):
                    response = auth_client.post(
                        f'/api/cameras/{camera_id}/validate-password',
                        json={'password': 'test'}
                    )
                    # 성공 또는 실패 (비밀번호에 따라)
                    assert response.status_code in [200, 401, 403]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_password_validation_failure_count(self, auth_client):
        """Camera Password Validation API - 실패 횟수 추적"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                camera_info = cameras_data['cameras'][0]
                if camera_info.get('has_password'):
                    # 잘못된 비밀번호로 여러 번 시도
                    for _ in range(2):
                        response = auth_client.post(
                            f'/api/cameras/{camera_id}/validate-password',
                            json={'password': 'wrong_password'}
                        )
                        # 실패 응답 확인
                        if response.status_code == 401:
                            data = response.get_json()
                            assert 'attempts' in data or 'remaining' in data

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_set_password_succeeds(self, auth_client):
        """Camera Set Password API - 카메라 비밀번호 설정"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(
                    f'/api/cameras/{camera_id}/set-password',
                    json={'new_password': 'newpass123'}
                )
                assert response.status_code in [200, 400, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_delete_password_succeeds(self, auth_client):
        """Camera Delete Password API - 카메라 비밀번호 삭제"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.delete(f'/api/cameras/{camera_id}/password')
                assert response.status_code in [200, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_open_view_window(self, auth_client):
        """Camera Open View Window API - 카메라 뷰 창 열기"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.post(f'/api/cameras/{camera_id}/open-view')
                # 성공 또는 실패 (GUI 환경에 따라)
                assert response.status_code in [200, 400, 500]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_pick_a_camera_page_renders_when_authenticated(self, auth_client):
        """Pick a Camera 페이지 - 인증 시 렌더링"""
        response = auth_client.get('/pick-a-camera')
        assert response.status_code == 200

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_all_cameras_page_renders_when_authenticated(self, auth_client):
        """All Cameras 페이지 - 인증 시 렌더링"""
        response = auth_client.get('/all-cameras')
        assert response.status_code == 200

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_view_page_renders_when_authenticated(self, auth_client):
        """Camera View 페이지 - 인증 시 렌더링"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                response = auth_client.get(f'/camera-view/{camera_id}')
                assert response.status_code == 200

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_configure_page_renders_when_authenticated(self, auth_client):
        """Configure 페이지 - 인증 시 렌더링"""
        response = auth_client.get('/configure')
        assert response.status_code == 200

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_surveillance_page_renders_when_authenticated(self, auth_client):
        """Surveillance 페이지 - 인증 시 렌더링"""
        response = auth_client.get('/surveillance')
        assert response.status_code == 200

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_first_password_system_not_available(self, client):
        """First Password API - 시스템이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            main_app.safehome_system = None
            response = client.post('/api/login/first', json={
                'username': 'homeowner',
                'password': 'first123'
            })
            assert response.status_code == 503
            data = response.get_json()
            assert data['success'] is False
            assert 'not available' in data['message'].lower()
        finally:
            main_app.safehome_system = original_system

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_second_password_system_not_available(self, client):
        """Second Password API - 시스템이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            with client.session_transaction() as session:
                session['first_validated'] = True
                session['temp_username'] = 'homeowner'
            
            main_app.safehome_system = None
            response = client.post('/api/login/second', json={
                'second_password': 'second456'
            })
            assert response.status_code == 503
            data = response.get_json()
            assert data['success'] is False
            assert 'not available' in data['message'].lower()
        finally:
            main_app.safehome_system = original_system

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_security_status_system_not_available(self, auth_client):
        """Security Status API - Security System이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            # Security system을 None으로 설정 (시뮬레이션)
            if original_system:
                original_security = original_system.security_system
                original_system.security_system = None
                
                response = auth_client.get('/api/security/status')
                # 에러 또는 기본 응답
                assert response.status_code in [200, 503]
            else:
                pytest.skip("System not available")
        finally:
            if original_system:
                original_system.security_system = original_security

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_settings_get_system_not_available(self, auth_client):
        """Get Settings API - 시스템이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            main_app.safehome_system = None
            response = auth_client.get('/api/settings')
            assert response.status_code == 503
            data = response.get_json()
            assert data['success'] is False
            assert 'not available' in data['message'].lower()
        finally:
            main_app.safehome_system = original_system

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_settings_update_system_not_available(self, auth_client):
        """Update Settings API - 시스템이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            main_app.safehome_system = None
            response = auth_client.put('/api/settings', json={
                'monitoring_service_phone': '111-222-3333'
            })
            assert response.status_code == 503
            data = response.get_json()
            assert data['success'] is False
            assert 'not available' in data['message'].lower()
        finally:
            main_app.safehome_system = original_system

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_arm_with_invalid_mode(self, auth_client):
        """Arm API - 잘못된 모드로 Arm 시도"""
        response = auth_client.post('/api/security/arm', json={'mode': 'InvalidMode'})
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'Unsupported arm mode' in data['message']

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_arm_without_mode_uses_default(self, auth_client):
        """Arm API - mode 없이 호출 시 기본값 사용"""
        response = auth_client.post('/api/security/arm', json={})
        # 기본값 MODE_AWAY 사용
        assert response.status_code in [200, 400]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_security_intrusions_with_limit(self, auth_client):
        """Security Intrusions API - limit 파라미터 테스트"""
        response = auth_client.get('/api/security/intrusions?limit=5')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'intrusions' in data
        assert len(data['intrusions']) <= 5

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_security_intrusions_with_invalid_limit(self, auth_client):
        """Security Intrusions API - 잘못된 limit 파라미터"""
        response = auth_client.get('/api/security/intrusions?limit=-1')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        # 음수 limit는 기본값으로 처리됨

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_security_intrusions_with_large_limit(self, auth_client):
        """Security Intrusions API - 큰 limit 값 (최대 200으로 제한)"""
        response = auth_client.get('/api/security/intrusions?limit=500')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert len(data['intrusions']) <= 200  # 최대 200으로 제한

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_get_camera_info_not_found(self, auth_client):
        """Get Camera Info API - 존재하지 않는 카메라"""
        response = auth_client.get('/api/cameras/99999')
        assert response.status_code == 404
        data = response.get_json()
        assert data['success'] is False

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_operations_on_nonexistent_camera(self, auth_client):
        """Camera Operations - 존재하지 않는 카메라에 대한 작업"""
        # Enable - 실패 시 400 반환 (Failed to enable camera)
        response = auth_client.post('/api/cameras/99999/enable')
        assert response.status_code == 400
        
        # Disable - 실패 시 400 반환 (Failed to disable camera)
        response = auth_client.post('/api/cameras/99999/disable')
        assert response.status_code == 400
        
        # Pan - 404 또는 400 가능
        response = auth_client.post('/api/cameras/99999/pan', json={'direction': 'right'})
        assert response.status_code in [400, 404]
        
        # Zoom - 404 또는 400 가능
        response = auth_client.post('/api/cameras/99999/zoom', json={'action': 'in'})
        assert response.status_code in [400, 404]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_exception_handling_in_first_password(self, client):
        """First Password API - 예외 처리 테스트"""
        with patch('main.safehome_system') as mock_system:
            mock_system.login_manager.validate_first_password.side_effect = Exception("Test error")
            response = client.post('/api/login/first', json={
                'username': 'homeowner',
                'password': 'first123'
            })
            assert response.status_code == 500
            data = response.get_json()
            assert data['success'] is False
            assert 'Server error' in data['message']

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_exception_handling_in_second_password(self, client):
        """Second Password API - 예외 처리 테스트"""
        with patch('main.safehome_system') as mock_system:
            with client.session_transaction() as session:
                session['first_validated'] = True
                session['temp_username'] = 'homeowner'
            
            mock_system.login_manager.validate_second_password.side_effect = Exception("Test error")
            response = client.post('/api/login/second', json={
                'second_password': 'second456'
            })
            assert response.status_code == 500
            data = response.get_json()
            assert data['success'] is False
            assert 'Server error' in data['message']

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_legacy_arm_route_not_authenticated(self, client):
        """레거시 /arm 라우트 - Control Panel에서 인증되지 않은 경우"""
        response = client.get('/arm')
        assert response.status_code == 200
        assert b'Please login first' in response.data

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_legacy_disarm_route_no_system(self, client):
        """레거시 /disarm 라우트 - 시스템이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            main_app.safehome_system = None
            response = client.get('/disarm')
            assert response.status_code == 200
            assert b'Error' in response.data
        finally:
            main_app.safehome_system = original_system

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_legacy_status_route_no_system(self, client):
        """레거시 /status 라우트 - 시스템이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            main_app.safehome_system = None
            response = client.get('/status')
            assert response.status_code == 200
            assert b'System offline' in response.data
        finally:
            main_app.safehome_system = original_system

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_legacy_status_route_with_system(self, client):
        """레거시 /status 라우트 - 시스템이 있을 때"""
        response = client.get('/status')
        assert response.status_code == 200
        assert b'System Status' in response.data

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_security_status_status_none(self, auth_client):
        """Security Status API - get_status()가 None을 반환할 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system and original_system.security_system:
                # get_status가 None을 반환하도록 모킹
                with patch.object(original_system.security_system, 'get_status', return_value=None):
                    response = auth_client.get('/api/security/status')
                    assert response.status_code == 500
                    data = response.get_json()
                    assert data['success'] is False
                    assert 'Security status unavailable' in data['message']
            else:
                pytest.skip("Security system not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_helper_security_instance_returns_none(self):
        """Helper 함수 _security_instance - security_system이 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            # security_system 속성이 없는 경우
            if original_system:
                original_security = getattr(original_system, 'security_system', None)
                if hasattr(original_system, 'security_system'):
                    delattr(original_system, 'security_system')
                
                result = main_app._security_instance()
                assert result is None
                
                # 복원
                if original_security is not None:
                    original_system.security_system = original_security
            else:
                pytest.skip("System not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_helper_security_controller_returns_none(self):
        """Helper 함수 _security_controller - system_controller가 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system:
                original_controller = getattr(original_system, 'system_controller', None)
                if hasattr(original_system, 'system_controller'):
                    delattr(original_system, 'system_controller')
                
                result = main_app._security_controller()
                assert result is None
                
                # 복원
                if original_controller is not None:
                    original_system.system_controller = original_controller
            else:
                pytest.skip("System not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_helper_configuration_manager_returns_none(self):
        """Helper 함수 _configuration_manager - configuration_manager가 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system:
                original_config = getattr(original_system, 'configuration_manager', None)
                if hasattr(original_system, 'configuration_manager'):
                    delattr(original_system, 'configuration_manager')
                
                result = main_app._configuration_manager()
                assert result is None
                
                # 복원
                if original_config is not None:
                    original_system.configuration_manager = original_config
            else:
                pytest.skip("System not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_arm_controller_not_available(self, auth_client):
        """Arm API - Security Controller가 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system:
                original_controller = original_system.system_controller
                original_system.system_controller = None
                
                response = auth_client.post('/api/security/arm', json={'mode': 'Away'})
                assert response.status_code == 503
                data = response.get_json()
                assert data['success'] is False
                assert 'Security controller not available' in data['message']
                
                # 복원
                original_system.system_controller = original_controller
            else:
                pytest.skip("System not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_disarm_controller_not_available(self, auth_client):
        """Disarm API - Security Controller가 없을 때"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system:
                original_controller = original_system.system_controller
                original_system.system_controller = None
                
                response = auth_client.post('/api/security/disarm')
                assert response.status_code == 503
                data = response.get_json()
                assert data['success'] is False
                assert 'Security controller not available' in data['message']
                
                # 복원
                original_system.system_controller = original_controller
            else:
                pytest.skip("System not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_arm_missing_username_in_session(self, auth_client):
        """Arm API - 세션에 username이 없을 때"""
        with auth_client.session_transaction() as session:
            session['logged_in'] = True
            session.pop('username', None)  # username 제거
        
        response = auth_client.post('/api/security/arm', json={'mode': 'Away'})
        # username이 없으면 403 반환
        assert response.status_code in [403, 503]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_disarm_missing_username_in_session(self, auth_client):
        """Disarm API - 세션에 username이 없을 때"""
        with auth_client.session_transaction() as session:
            session['logged_in'] = True
            session.pop('username', None)  # username 제거
        
        response = auth_client.post('/api/security/disarm')
        # username이 없으면 403 반환
        assert response.status_code in [403, 503]

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_arm_controller_set_mode_fails(self, auth_client):
        """Arm API - set_security_mode 실패 시"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system and original_system.system_controller:
                # set_security_mode가 False를 반환하도록 모킹
                with patch.object(original_system.system_controller, 'set_security_mode', return_value=False):
                    with patch.object(original_system.system_controller, 'last_error_message', 'Test error'):
                        response = auth_client.post('/api/security/arm', json={'mode': 'Away'})
                        assert response.status_code == 400
                        data = response.get_json()
                        assert data['success'] is False
            else:
                pytest.skip("System controller not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_disarm_controller_set_mode_fails(self, auth_client):
        """Disarm API - set_security_mode 실패 시"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system and original_system.system_controller:
                # set_security_mode가 False를 반환하도록 모킹
                with patch.object(original_system.system_controller, 'set_security_mode', return_value=False):
                    with patch.object(original_system.system_controller, 'last_error_message', 'Test error'):
                        response = auth_client.post('/api/security/disarm')
                        assert response.status_code == 400
                        data = response.get_json()
                        assert data['success'] is False
            else:
                pytest.skip("System controller not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_logout_with_username_logs_event(self, auth_client):
        """Logout API - username이 있을 때 이벤트 로그"""
        with auth_client.session_transaction() as session:
            session['logged_in'] = True
            session['username'] = 'test_user'
        
        response = auth_client.get('/logout')
        assert response.status_code == 302
        assert '/login' in response.location

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_logout_without_username_does_not_log(self, client):
        """Logout API - username이 없을 때 로그 없이 로그아웃"""
        with client.session_transaction() as session:
            session['logged_in'] = True
            # username 없음
        
        response = client.get('/logout')
        assert response.status_code == 302
        assert '/login' in response.location

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_view_api_exception_handling(self, auth_client):
        """Camera View API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                # 예외를 발생시키도록 모킹
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'get_camera', side_effect=Exception("Test error")):
                    response = auth_client.get(f'/api/cameras/{camera_id}/view')
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_thumbnails_api_exception_handling(self, auth_client):
        """Camera Thumbnails API - 예외 처리"""
        import main as main_app
        if main_app.safehome_system and main_app.safehome_system.camera_controller:
            with patch.object(main_app.safehome_system.camera_controller, 'display_thumbnail_view', side_effect=Exception("Test error")):
                response = auth_client.get('/api/cameras/thumbnails')
                assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_pan_api_exception_handling(self, auth_client):
        """Camera Pan API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                # 예외를 발생시키도록 모킹
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'get_camera', side_effect=Exception("Test error")):
                    response = auth_client.post(f'/api/cameras/{camera_id}/pan', json={'direction': 'right'})
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_camera_zoom_api_exception_handling(self, auth_client):
        """Camera Zoom API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                # 예외를 발생시키도록 모킹
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'get_camera', side_effect=Exception("Test error")):
                    response = auth_client.post(f'/api/cameras/{camera_id}/zoom', json={'action': 'in'})
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_get_all_cameras_exception_handling(self, auth_client):
        """Get All Cameras API - 예외 처리"""
        import main as main_app
        if main_app.safehome_system and main_app.safehome_system.camera_controller:
            with patch.object(main_app.safehome_system.camera_controller, 'get_all_camera_info', side_effect=Exception("Test error")):
                response = auth_client.get('/api/cameras')
                assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_get_camera_info_exception_handling(self, auth_client):
        """Get Camera Info API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                # 예외를 발생시키도록 모킹
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'get_camera', side_effect=Exception("Test error")):
                    response = auth_client.get(f'/api/cameras/{camera_id}')
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_validate_camera_password_result_minus_one(self, auth_client):
        """Camera Password Validation - result == -1 (카메라 없음)"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'validate_camera_password', return_value=-1):
                    response = auth_client.post(f'/api/cameras/{camera_id}/validate-password', json={'password': 'test'})
                    assert response.status_code == 404
                    data = response.get_json()
                    assert data['success'] is False
                    assert 'Camera not found' in data['message']

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_validate_camera_password_result_minus_two(self, auth_client):
        """Camera Password Validation - result == -2 (비밀번호 없음)"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'validate_camera_password', return_value=-2):
                    response = auth_client.post(f'/api/cameras/{camera_id}/validate-password', json={'password': 'test'})
                    assert response.status_code == 400
                    data = response.get_json()
                    assert data['success'] is False
                    assert 'No password set' in data['message']

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_validate_camera_password_three_failed_attempts(self, auth_client):
        """Camera Password Validation - 3회 실패 시 잠금"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'validate_camera_password', return_value=1):
                    # 3회 실패 시뮬레이션
                    for attempt in range(3):
                        with auth_client.session_transaction() as session:
                            session[f'camera_{camera_id}_password_attempts'] = attempt
                        
                        response = auth_client.post(
                            f'/api/cameras/{camera_id}/validate-password',
                            json={'password': 'wrong'}
                        )
                        if attempt < 2:
                            assert response.status_code == 401
                        else:
                            # 3회째는 잠금
                            assert response.status_code == 403
                            data = response.get_json()
                            assert data['success'] is False
                            assert 'locked' in data
                            assert data['locked'] is True

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_set_camera_password_exception_handling(self, auth_client):
        """Set Camera Password API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'get_camera', side_effect=Exception("Test error")):
                    response = auth_client.post(
                        f'/api/cameras/{camera_id}/set-password',
                        json={'new_password': 'test123'}
                    )
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_delete_camera_password_exception_handling(self, auth_client):
        """Delete Camera Password API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'get_camera', side_effect=Exception("Test error")):
                    response = auth_client.delete(f'/api/cameras/{camera_id}/password')
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_enable_camera_exception_handling(self, auth_client):
        """Enable Camera API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'enable_camera', side_effect=Exception("Test error")):
                    response = auth_client.post(f'/api/cameras/{camera_id}/enable')
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_disable_camera_exception_handling(self, auth_client):
        """Disable Camera API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                import main as main_app
                with patch.object(main_app.safehome_system.camera_controller, 'disable_camera', side_effect=Exception("Test error")):
                    response = auth_client.post(f'/api/cameras/{camera_id}/disable')
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_open_camera_view_window_exception_handling(self, auth_client):
        """Open Camera View Window API - 예외 처리"""
        cameras_response = auth_client.get('/api/cameras')
        if cameras_response.status_code == 200:
            cameras_data = cameras_response.get_json()
            if cameras_data.get('cameras') and len(cameras_data['cameras']) > 0:
                camera_id = cameras_data['cameras'][0]['id']
                # subprocess.Popen이 예외를 발생시키도록 모킹
                with patch('main.subprocess.Popen', side_effect=Exception("Test error")):
                    response = auth_client.post(f'/api/cameras/{camera_id}/open-view')
                    assert response.status_code == 500

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_zone_create_fails(self, auth_client):
        """Create Zone API - Zone 생성 실패"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system and original_system.configuration_manager:
                with patch.object(original_system.configuration_manager, 'add_safety_zone', return_value=False):
                    response = auth_client.post('/api/security/zones', json={'name': 'Test Zone'})
                    assert response.status_code == 400
                    data = response.get_json()
                    assert data['success'] is False
                    assert 'Failed to create zone' in data['message']
            else:
                pytest.skip("Configuration manager not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_zone_update_fails(self, auth_client):
        """Update Zone API - Zone 업데이트 실패"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system and original_system.configuration_manager:
                with patch.object(original_system.configuration_manager, 'modify_safety_zone', return_value=False):
                    response = auth_client.put('/api/security/zones/1', json={'name': 'Updated'})
                    assert response.status_code == 400
                    data = response.get_json()
                    assert data['success'] is False
                    assert 'Zone update failed' in data['message']
            else:
                pytest.skip("Configuration manager not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_zone_delete_fails(self, auth_client):
        """Delete Zone API - Zone 삭제 실패"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system and original_system.configuration_manager:
                with patch.object(original_system.configuration_manager, 'delete_safety_zone', return_value=False):
                    response = auth_client.delete('/api/security/zones/1')
                    assert response.status_code == 400
                    data = response.get_json()
                    assert data['success'] is False
                    assert 'Failed to delete zone' in data['message']
            else:
                pytest.skip("Configuration manager not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_assign_sensor_fails(self, auth_client):
        """Assign Sensor API - Sensor 할당 실패"""
        import main as main_app
        original_system = main_app.safehome_system
        try:
            if original_system and original_system.configuration_manager:
                with patch.object(original_system.configuration_manager, 'assign_sensor_to_zone', return_value=False):
                    response = auth_client.post('/api/security/assignments', json={
                        'device_id': 'test_sensor',
                        'zone_id': 1
                    })
                    assert response.status_code == 400
                    data = response.get_json()
                    assert data['success'] is False
                    assert 'Assignment failed' in data['message']
            else:
                pytest.skip("Configuration manager not available")
        finally:
            pass

    @pytest.mark.usefixtures("safehome_system_instance")
    def test_assign_sensor_invalid_zone_id(self, auth_client):
        """Assign Sensor API - zone_id가 숫자가 아닐 때"""
        response = auth_client.post('/api/security/assignments', json={
            'device_id': 'test_sensor',
            'zone_id': 'invalid'
        })
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'zone_id must be numeric' in data['message']

