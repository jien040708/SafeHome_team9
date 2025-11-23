import threading
import tkinter as tk
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from domain.system import System
from ui.main_window import SafeHomeApp
from devices.windoor_sensor import WindowDoorSensor
from devices.motion_detector import MotionDetector
from devices.camera import Camera
from utils.constants import *

app = Flask(__name__, static_folder='virtual_device_v3', static_url_path='/static')
app.secret_key = os.urandom(24)  # 세션 암호화 키
safehome_system = None

@app.route('/')
def home():
    """메인 페이지 - 로그인 상태에 따라 리다이렉트"""
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))


@app.route('/login')
def login_page():
    """로그인 페이지"""
    return render_template('login.html')


@app.route('/api/login/first', methods=['POST'])
def validate_first_password():
    """First Password 검증 API"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # 디버깅: 입력된 username 확인
        print(f"[DEBUG] Login attempt - Username: '{username}', Interface: 'web_browser'")

        if not username or not password:
            return jsonify({
                'success': False,
                'message': 'Username and password are required'
            }), 400

        # LoginManager를 통한 검증
        if safehome_system and safehome_system.login_manager:
            result = safehome_system.login_manager.validate_first_password(
                username,
                password,
                'web_browser'
            )

            if result['success']:
                # 세션에 임시 저장 (First password 검증 완료)
                session['temp_username'] = username
                session['first_validated'] = True

                # 이벤트 로그
                if safehome_system.log_manager:
                    safehome_system.log_manager.log_event(
                        'INFO',
                        f'First password validation successful for user: {username}',
                        username
                    )

                return jsonify({
                    'success': True,
                    'message': 'First password correct'
                }), 200
            else:
                # 실패 로그
                if safehome_system.log_manager:
                    safehome_system.log_manager.log_event(
                        'WARNING',
                        f'First password validation failed for user: {username}',
                        username
                    )
                # 디버깅: 응답 내용 출력
                print(f"[DEBUG] First password validation result: {result}")
                print(f"[DEBUG] Response locked status: {result.get('locked', False)}")
                print(f"[DEBUG] Response message: {result.get('message', 'N/A')}")
                return jsonify(result), 401
        else:
            return jsonify({
                'success': False,
                'message': 'System not available'
            }), 503

    except Exception as e:
        print(f"[Flask] First password validation error: {e}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500


@app.route('/api/login/second', methods=['POST'])
def validate_second_password():
    """Second Password 검증 API"""
    try:
        data = request.get_json()
        second_password = data.get('second_password')

        # First password가 검증되지 않았으면 오류
        if not session.get('first_validated'):
            return jsonify({
                'success': False,
                'message': 'First password not validated'
            }), 403

        username = session.get('temp_username')

        if not second_password:
            return jsonify({
                'success': False,
                'message': 'Second password is required'
            }), 400

        # LoginManager를 통한 검증
        if safehome_system and safehome_system.login_manager:
            result = safehome_system.login_manager.validate_second_password(
                username,
                second_password,
                'web_browser'
            )

            if result['success']:
                # 로그인 성공 - 세션 설정
                session['logged_in'] = True
                session['username'] = username
                session.pop('temp_username', None)
                session.pop('first_validated', None)

                # 이벤트 로그
                if safehome_system.log_manager:
                    safehome_system.log_manager.log_event(
                        'INFO',
                        f'Web login successful for user: {username}',
                        username
                    )

                return jsonify({
                    'success': True,
                    'message': 'Login successful',
                    'redirect': url_for('dashboard')
                }), 200
            else:
                # 실패 로그
                if safehome_system.log_manager:
                    safehome_system.log_manager.log_event(
                        'WARNING',
                        f'Second password validation failed for user: {username}',
                        username
                    )
                # 디버깅: 응답 내용 출력
                print(f"[DEBUG] Second password validation result: {result}")
                print(f"[DEBUG] Response locked status: {result.get('locked', False)}")
                print(f"[DEBUG] Response message: {result.get('message', 'N/A')}")
                return jsonify(result), 401
        else:
            return jsonify({
                'success': False,
                'message': 'System not available'
            }), 503

    except Exception as e:
        print(f"[Flask] Second password validation error: {e}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500


@app.route('/dashboard')
def dashboard():
    """메인 대시보드 (로그인 필요)"""
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    username = session.get('username')

    # 시스템 상태 정보
    status_info = {}
    if safehome_system:
        status_info = safehome_system.get_system_status()

    return render_template('dashboard.html', username=username, status=status_info)


@app.route('/logout')
def logout():
    """로그아웃"""
    username = session.get('username')
    if username and safehome_system and safehome_system.log_manager:
        safehome_system.log_manager.log_event('INFO', 'Web user logged out', username)

    session.clear()
    return redirect(url_for('login_page'))


@app.route('/configure')
def configure_page():
    """시스템 설정 페이지 (로그인 필요)"""
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    username = session.get('username')
    return render_template('configure_system.html', username=username)


@app.route('/surveillance')
def surveillance_page():
    """Surveillance 페이지 (로그인 필요)"""
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))

    username = session.get('username')
    return render_template('surveillance.html', username=username)


@app.route('/api/settings', methods=['GET'])
def get_settings():
    """현재 시스템 설정 조회 API"""
    if not session.get('logged_in'):
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401

    try:
        if safehome_system and safehome_system.configuration_manager:
            settings = safehome_system.configuration_manager.get_system_setting()
            return jsonify({
                'success': True,
                'settings': {
                    'monitoring_service_phone': settings.get_monitoring_service_phone(),
                    'homeowner_phone': settings.get_homeowner_phone(),
                    'system_lock_time': settings.get_system_lock_time(),
                    'alarm_delay_time': settings.get_alarm_delay_time()
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': 'System not available'
            }), 503
    except Exception as e:
        print(f"[Flask] Get settings error: {e}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500


@app.route('/api/settings', methods=['PUT'])
def update_settings():
    """시스템 설정 업데이트 API"""
    if not session.get('logged_in'):
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401

    try:
        data = request.get_json()
        monitoring_phone = data.get('monitoring_service_phone')
        homeowner_phone = data.get('homeowner_phone')
        lock_time = data.get('system_lock_time')
        alarm_delay = data.get('alarm_delay_time')

        # 입력 검증
        errors = []

        # 전화번호 형식 검증 (XXX-XXX-XXXX)
        import re
        phone_pattern = r'^\d{3}-\d{3}-\d{4}$'
        flexible_phone_pattern = r'^[\d\-+() ]+$'

        if monitoring_phone:
            if not (re.match(phone_pattern, monitoring_phone) or
                    (re.match(flexible_phone_pattern, monitoring_phone) and len(monitoring_phone) >= 3)):
                errors.append('Invalid monitoring service phone format (recommended: XXX-XXX-XXXX)')

        if homeowner_phone:
            if not (re.match(phone_pattern, homeowner_phone) or
                    (re.match(flexible_phone_pattern, homeowner_phone) and len(homeowner_phone) >= 3)):
                errors.append('Invalid homeowner phone format (recommended: XXX-XXX-XXXX)')

        # 시간 값 검증
        if lock_time is not None:
            try:
                lock_time = int(lock_time)
                if lock_time <= 0:
                    errors.append('System lock time must be greater than 0')
            except (ValueError, TypeError):
                errors.append('System lock time must be a valid number')

        if alarm_delay is not None:
            try:
                alarm_delay = int(alarm_delay)
                if alarm_delay < 0:
                    errors.append('Alarm delay time must be non-negative')
            except (ValueError, TypeError):
                errors.append('Alarm delay time must be a valid number')

        # 검증 실패 시
        if errors:
            return jsonify({
                'success': False,
                'message': 'Validation failed',
                'errors': errors
            }), 400

        # 설정 업데이트
        if safehome_system and safehome_system.configuration_manager:
            settings = safehome_system.configuration_manager.get_system_setting()

            if monitoring_phone:
                settings.set_monitoring_service_phone(monitoring_phone)
            if homeowner_phone:
                settings.set_homeowner_phone(homeowner_phone)
            if lock_time is not None:
                settings.set_system_lock_time(lock_time)
            if alarm_delay is not None:
                settings.set_alarm_delay_time(alarm_delay)

            # 데이터베이스에 저장
            success = settings.save()

            if success:
                # 로그 기록
                username = session.get('username')
                if safehome_system.log_manager:
                    safehome_system.log_manager.log_event(
                        'INFO',
                        'System settings updated via web interface',
                        username
                    )

                return jsonify({
                    'success': True,
                    'message': 'Settings updated successfully',
                    'settings': {
                        'monitoring_service_phone': settings.get_monitoring_service_phone(),
                        'homeowner_phone': settings.get_homeowner_phone(),
                        'system_lock_time': settings.get_system_lock_time(),
                        'alarm_delay_time': settings.get_alarm_delay_time()
                    }
                }), 200
            else:
                return jsonify({
                    'success': False,
                    'message': 'Failed to save settings'
                }), 500
        else:
            return jsonify({
                'success': False,
                'message': 'System not available'
            }), 503

    except Exception as e:
        print(f"[Flask] Update settings error: {e}")
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500

@app.route('/arm')
def arm():
    if safehome_system and safehome_system.login_manager.is_user_authenticated():
        safehome_system.system_controller.set_security_mode(MODE_AWAY)
        return "Armed Away! <a href='/'>Back</a>"
    return "Please login first on Control Panel. <a href='/'>Back</a>"

@app.route('/disarm')
def disarm():
    if safehome_system and safehome_system.system_controller:
        safehome_system.system_controller.set_security_mode(MODE_DISARMED)
        return "Disarmed. <a href='/'>Back</a>"
    return "Error <a href='/'>Back</a>"

@app.route('/status')
def status():
    if safehome_system:
        status_info = safehome_system.get_system_status()
        return f"""
        <h2>System Status</h2>
        <ul>
            <li>State: {status_info['state']}</li>
            <li>Authenticated: {status_info['authenticated']}</li>
            <li>Current User: {status_info['current_user']}</li>
            <li>Security Mode: {status_info['security_mode']}</li>
        </ul>
        <a href='/'>Back</a>
        """
    return "System offline <a href='/'>Back</a>"

# ========================================
# Surveillance API Endpoints
# ========================================

@app.route('/pick-a-camera')
def pick_a_camera_page():
    """Pick a Camera 페이지 (로그인 필요)"""
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    username = session.get('username')
    return render_template('pick_a_camera.html', username=username)

@app.route('/all-cameras')
def all_cameras_page():
    """All Cameras 페이지 (로그인 필요)"""
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    username = session.get('username')
    return render_template('all_cameras.html', username=username)

@app.route('/camera-view/<int:camera_id>')
def camera_view_page(camera_id):
    """Camera View 페이지 (로그인 필요)"""
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    username = session.get('username')
    return render_template('camera_view.html', username=username, camera_id=camera_id)

@app.route('/api/cameras', methods=['GET'])
def get_all_cameras():
    """모든 카메라 정보 조회"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        if safehome_system and safehome_system.camera_controller:
            cameras_info = safehome_system.camera_controller.get_all_camera_info()
            cameras = []
            for info in cameras_info:
                camera_id = info[0]
                camera = safehome_system.camera_controller.get_camera(camera_id)
                cameras.append({
                    'id': camera_id,
                    'x': info[1],
                    'y': info[2],
                    'enabled': bool(info[3]),
                    'has_password': camera.has_password() if camera else False
                })
            return jsonify({'success': True, 'cameras': cameras}), 200
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Get cameras error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>', methods=['GET'])
def get_camera_info(camera_id):
    """특정 카메라 정보 조회"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        if safehome_system and safehome_system.camera_controller:
            camera = safehome_system.camera_controller.get_camera(camera_id)
            if not camera:
                return jsonify({'success': False, 'message': 'Camera not found'}), 404
            
            info = safehome_system.camera_controller._camera_info.get(camera_id, {})
            has_password = camera_id in safehome_system.camera_controller._camera_passwords
            
            return jsonify({
                'success': True,
                'camera': {
                    'id': camera_id,
                    'x': info.get('x', 0),
                    'y': info.get('y', 0),
                    'enabled': info.get('enabled', False),
                    'has_password': has_password
                }
            }), 200
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Get camera info error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/validate-password', methods=['POST'])
def validate_camera_password(camera_id):
    """카메라 비밀번호 검증"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not safehome_system or not safehome_system.camera_controller:
            return jsonify({'success': False, 'message': 'System not available'}), 503
        
        # 세션에 실패 횟수 저장
        key = f'camera_{camera_id}_password_attempts'
        attempts = session.get(key, 0)
        
        result = safehome_system.camera_controller.validate_camera_password(camera_id, password)
        
        if result == 0:  # 성공
            session[key] = 0
            return jsonify({'success': True, 'message': 'Password validated'}), 200
        elif result == 1:  # 실패
            attempts += 1
            session[key] = attempts
            
            if attempts >= 3:
                # 시스템 잠금 (설정 시간 동안)
                lock_time = 30  # 기본값, 실제로는 설정에서 가져와야 함
                if safehome_system.configuration_manager:
                    lock_time = safehome_system.configuration_manager.get_system_setting().get_system_lock_time()
                
                return jsonify({
                    'success': False,
                    'message': f'Too many failed attempts. System locked for {lock_time} seconds.',
                    'locked': True,
                    'lock_time': lock_time
                }), 403
            else:
                return jsonify({
                    'success': False,
                    'message': 'Incorrect password',
                    'attempts': attempts,
                    'remaining': 3 - attempts
                }), 401
        elif result == -1:
            return jsonify({'success': False, 'message': 'Camera not found'}), 404
        else:  # -2: 비밀번호 없음
            return jsonify({'success': False, 'message': 'No password set'}), 400
    except Exception as e:
        print(f"[Flask] Validate password error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/set-password', methods=['POST'])
def set_camera_password(camera_id):
    """카메라 비밀번호 설정"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        old_password = data.get('old_password', '')
        new_password = data.get('new_password', '')
        confirm_password = data.get('confirm_password', '')
        
        if not safehome_system or not safehome_system.camera_controller:
            return jsonify({'success': False, 'message': 'System not available'}), 503
        
        # 새 비밀번호 확인
        if new_password != confirm_password:
            return jsonify({'success': False, 'message': 'Passwords do not match'}), 400
        
        # 기존 비밀번호 검증 (있는 경우)
        has_password = camera_id in safehome_system.camera_controller._camera_passwords
        if has_password:
            if not old_password:
                return jsonify({'success': False, 'message': 'Old password required'}), 400
            
            result = safehome_system.camera_controller.validate_camera_password(camera_id, old_password)
            if result != 0:
                return jsonify({'success': False, 'message': 'Incorrect old password'}), 401
        
        # 비밀번호 설정
        safehome_system.camera_controller.set_camera_password(camera_id, new_password)
        
        return jsonify({'success': True, 'message': 'Password set successfully'}), 200
    except Exception as e:
        print(f"[Flask] Set password error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/password', methods=['DELETE'])
def delete_camera_password(camera_id):
    """카메라 비밀번호 삭제"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        if not safehome_system or not safehome_system.camera_controller:
            return jsonify({'success': False, 'message': 'System not available'}), 503
        
        # 비밀번호 검증
        result = safehome_system.camera_controller.validate_camera_password(camera_id, password)
        if result != 0:
            return jsonify({'success': False, 'message': 'Incorrect password'}), 401
        
        # 비밀번호 삭제
        result = safehome_system.camera_controller._delete_camera_password(camera_id)
        if result == 0:
            return jsonify({'success': True, 'message': 'Password deleted successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to delete password'}), 400
    except Exception as e:
        print(f"[Flask] Delete password error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/enable', methods=['POST'])
def enable_camera(camera_id):
    """카메라 활성화"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        if safehome_system and safehome_system.camera_controller:
            success = safehome_system.camera_controller.enable_camera(camera_id)
            if success:
                return jsonify({'success': True, 'message': 'Camera enabled'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to enable camera'}), 400
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Enable camera error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/disable', methods=['POST'])
def disable_camera(camera_id):
    """카메라 비활성화"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        if safehome_system and safehome_system.camera_controller:
            success = safehome_system.camera_controller.disable_camera(camera_id)
            if success:
                return jsonify({'success': True, 'message': 'Camera disabled'}), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to disable camera'}), 400
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Disable camera error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/view', methods=['GET'])
def get_camera_view(camera_id):
    """카메라 뷰 이미지 (초당 1프레임)"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        if safehome_system and safehome_system.camera_controller:
            camera = safehome_system.camera_controller.get_camera(camera_id)
            if not camera:
                return jsonify({'success': False, 'message': 'Camera not found'}), 404
            
            # 실제 구현 시 카메라에서 이미지를 가져와야 함
            # 여기서는 base64 인코딩된 이미지 반환
            from io import BytesIO
            import base64
            
            img = safehome_system.camera_controller.display_single_view(camera_id)
            if img:
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                return jsonify({
                    'success': True,
                    'image': f'data:image/png;base64,{img_str}'
                }), 200
            else:
                return jsonify({'success': False, 'message': 'Failed to get camera view'}), 500
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Get camera view error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/thumbnails', methods=['GET'])
def get_camera_thumbnails():
    """모든 카메라 썸네일"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        if safehome_system and safehome_system.camera_controller:
            from io import BytesIO
            import base64
            
            img = safehome_system.camera_controller.display_thumbnail_view()
            if img:
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                img_str = base64.b64encode(buffer.getvalue()).decode()
                return jsonify({
                    'success': True,
                    'image': f'data:image/png;base64,{img_str}'
                }), 200
            else:
                return jsonify({'success': False, 'message': 'No cameras available'}), 404
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Get thumbnails error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/pan', methods=['POST'])
def pan_camera(camera_id):
    """카메라 팬 제어"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        direction = data.get('direction', '')  # 'left' or 'right'
        
        if safehome_system and safehome_system.camera_controller:
            camera = safehome_system.camera_controller.get_camera(camera_id)
            if not camera:
                return jsonify({'success': False, 'message': 'Camera not found'}), 404
            
            # SafeHomeCamera를 사용해야 하는데, 현재는 Camera 객체를 사용 중
            # 임시로 성공 반환
            return jsonify({'success': True, 'message': f'Camera {camera_id} panned {direction}'}), 200
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Pan camera error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/zoom', methods=['POST'])
def zoom_camera(camera_id):
    """카메라 줌 제어"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        data = request.get_json()
        action = data.get('action', '')  # 'in' or 'out'
        
        if safehome_system and safehome_system.camera_controller:
            camera = safehome_system.camera_controller.get_camera(camera_id)
            if not camera:
                return jsonify({'success': False, 'message': 'Camera not found'}), 404
            
            # SafeHomeCamera를 사용해야 하는데, 현재는 Camera 객체를 사용 중
            # 임시로 성공 반환
            return jsonify({'success': True, 'message': f'Camera {camera_id} zoomed {action}'}), 200
        else:
            return jsonify({'success': False, 'message': 'System not available'}), 503
    except Exception as e:
        print(f"[Flask] Zoom camera error: {e}")
        return jsonify({'success': False, 'message': 'Server error'}), 500

@app.route('/api/cameras/<int:camera_id>/open-view', methods=['POST'])
def open_camera_view_window(camera_id):
    """카메라 뷰 Tkinter GUI 창 열기"""
    if not session.get('logged_in'):
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    try:
        import subprocess
        import sys
        import os
        
        # virtual_device_v3/example/example_camera.py 경로
        base_dir = os.path.dirname(os.path.abspath(__file__))
        camera_script = os.path.join(base_dir, 'virtual_device_v3', 'example', 'example_camera.py')
        
        # 카메라 ID를 환경변수로 전달
        env = os.environ.copy()
        env['CAMERA_ID'] = str(camera_id)
        
        # 작업 디렉토리를 virtual_device_v3로 설정 (camera 이미지 파일을 찾기 위해)
        work_dir = os.path.join(base_dir, 'virtual_device_v3')
        
        # Python 프로세스로 example_camera.py 실행
        if sys.platform == 'win32':
            # Windows
            subprocess.Popen(
                [sys.executable, camera_script],
                cwd=work_dir,
                env=env,
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac
            subprocess.Popen(
                [sys.executable, camera_script],
                cwd=work_dir,
                env=env
            )
        
        return jsonify({
            'success': True,
            'message': f'Camera {camera_id} view window opened'
        }), 200
        
    except Exception as e:
        print(f"[Flask] Open camera view error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'Failed to open camera view: {str(e)}'
        }), 500

def run_web():
    app.run(port=5000, debug=False, use_reloader=False)

def main():
    global safehome_system
    root = tk.Tk()

    # System Init (Common Function 4: Turn the system on)
    safehome_system = System()
    if not safehome_system.turn_on():
        print("Failed to start SafeHome system. Exiting...")
        return

    # Devices Init
    sensors = [
        WindowDoorSensor("Front Door"),
        MotionDetector("Living Room"),
        Camera("Garden Cam")
    ]

    # Connect Devices to SystemController
    if safehome_system.system_controller:
        for s in sensors:
            s.add_observer(safehome_system.system_controller)
            if isinstance(s, Camera):
                safehome_system.system_controller.add_camera(s)

    # Initialize cameras in CameraController (3 cameras)
    # Positions based on black dots in floorplan.png (607x373)
    if safehome_system.camera_controller:
        # Camera 1 at position (350, 20) - top center
        safehome_system.camera_controller.add_camera(350, 20)
        # Camera 2 at position (330, 208) - middle center
        safehome_system.camera_controller.add_camera(330, 208)
        # Camera 3 at position (332, 262) - bottom center
        safehome_system.camera_controller.add_camera(332, 262)
        print("[Main] Initialized 3 cameras in CameraController at floorplan black dot positions")

    # UI Init
    ui_app = SafeHomeApp(root, safehome_system, sensors)
    safehome_system.set_ui(ui_app)

    # Web Server Start
    t = threading.Thread(target=run_web, daemon=True)
    t.start()

    print("=" * 50)
    print("SafeHome System Started Successfully!")
    print("Control Panel: Running on Tkinter window")
    print("Web Interface: http://localhost:5000")
    print("=" * 50)

    try:
        root.mainloop()
    finally:
        # System Shutdown (Common Function 5: Turn the system off)
        print("\nShutting down SafeHome system...")
        safehome_system.turn_off()

if __name__ == "__main__":
    main()