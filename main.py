import threading
import tkinter as tk
import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

from devices.camera import Camera
from devices.motion_detector import MotionDetector
from devices.windoor_sensor import WindowDoorSensor
from domain.system import System
from ui.main_window import SafeHomeApp
from devices.device_factory import create_default_device_factory, DeviceFactoryError
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
                        username,
                        interface_type='web_browser',
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
                        username,
                        interface_type='web_browser',
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
                        username,
                        interface_type='web_browser',
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
                        username,
                        interface_type='web_browser',
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
        safehome_system.log_manager.log_event('INFO', 'Web user logged out', username, interface_type='web_browser')

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
                        username,
                        interface_type='web_browser',
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


def _require_api_login():
    if not session.get('logged_in'):
        return jsonify({
            'success': False,
            'message': 'Authentication required'
        }), 401
    return None


def _security_instance():
    if safehome_system and getattr(safehome_system, "security_system", None):
        return safehome_system.security_system
    return None


def _security_controller():
    if safehome_system and getattr(safehome_system, "system_controller", None):
        return safehome_system.system_controller
    return None


def _configuration_manager():
    if safehome_system and getattr(safehome_system, "configuration_manager", None):
        return safehome_system.configuration_manager
    return None


def _build_security_status_payload():
    """Helper that returns (payload, error_response)."""
    security_system = _security_instance()
    if not security_system:
        return None, (jsonify({
            'success': False,
            'message': 'Security system not available'
        }), 503)

    status = security_system.get_status()
    if not status:
        return None, (jsonify({
            'success': False,
            'message': 'Security status unavailable'
        }), 500)

    payload = {
        'mode': status.mode.name,
        'alarm_state': status.alarm_state.name,
        'armed_zones': sorted(list(status.armed_zones)) if status.armed_zones else [],
        'entry_delay_deadline': status.entry_delay_deadline.isoformat() if status.entry_delay_deadline else None,
        'monitoring_call_scheduled': status.monitoring_call_scheduled,
    }
    return payload, None


@app.route('/api/security/status', methods=['GET'])
def api_security_status():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    status_payload, error = _build_security_status_payload()
    if error:
        return error
    return jsonify({'success': True, 'status': status_payload}), 200


@app.route('/api/security/intrusions', methods=['GET'])
def api_security_intrusions():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    security_system = _security_instance()
    if not security_system:
        return jsonify({
            'success': False,
            'message': 'Security system not available'
        }), 503

    limit = request.args.get('limit', default=50, type=int)
    if limit is None or limit <= 0:
        limit = 50
    limit = min(limit, 200)

    records = security_system.get_intrusion_logs()
    payload = []
    for record in records[-limit:]:
        payload.append({
            'timestamp': record.timestamp.isoformat(),
            'sensor_id': record.sensor_id,
            'zone_id': record.zone_id,
            'sensor_type': record.sensor_type.name if record.sensor_type else None,
            'mode': record.mode.name,
            'action': record.action,
            'status': record.status.name if record.status else None,
            'details': record.details,
        })

    return jsonify({'success': True, 'intrusions': payload}), 200


@app.route('/api/security/arm', methods=['POST'])
def api_security_arm():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    controller = _security_controller()
    if not controller:
        return jsonify({
            'success': False,
            'message': 'Security controller not available'
        }), 503

    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'User session missing'}), 403

    controller.authenticated_user = username

    data = request.get_json(silent=True) or {}
    requested_mode = data.get('mode', MODE_AWAY)
    allowed_modes = {MODE_AWAY, MODE_STAY}
    if requested_mode not in allowed_modes:
        return jsonify({
            'success': False,
            'message': f'Unsupported arm mode: {requested_mode}'
        }), 400

    if not controller.set_security_mode(requested_mode):
        message = controller.last_error_message or 'Unable to arm system'
        return jsonify({'success': False, 'message': message}), 400

    status_payload, error = _build_security_status_payload()
    if error:
        return error

    return jsonify({
        'success': True,
        'message': f'System armed in {requested_mode} mode',
        'status': status_payload
    }), 200


@app.route('/api/security/disarm', methods=['POST'])
def api_security_disarm():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    controller = _security_controller()
    if not controller:
        return jsonify({
            'success': False,
            'message': 'Security controller not available'
        }), 503

    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'User session missing'}), 403

    controller.authenticated_user = username

    if not controller.set_security_mode(MODE_DISARMED):
        message = controller.last_error_message or 'Unable to disarm system'
        return jsonify({'success': False, 'message': message}), 400

    status_payload, error = _build_security_status_payload()
    if error:
        return error

    return jsonify({
        'success': True,
        'message': 'System disarmed',
        'status': status_payload
    }), 200


@app.route('/api/security/panic', methods=['POST'])
def api_security_panic():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    security_system = _security_instance()
    if not security_system:
        return jsonify({
            'success': False,
            'message': 'Security system not available'
        }), 503

    security_system.trigger_panic()

    if safehome_system and getattr(safehome_system, 'log_manager', None):
        safehome_system.log_manager.log_event(
            event_type='PANIC_TRIGGERED',
            description='Panic alarm triggered via web dashboard',
            user_id=session.get('username'),
            interface_type='web_browser',
        )

    status_payload, error = _build_security_status_payload()
    if error:
        return error

    return jsonify({
        'success': True,
        'message': 'Panic alarm triggered',
        'status': status_payload
    }), 200


def _serialize_zones(config):
    zones = config.refresh_safety_zones()
    assignments = config.list_sensor_assignments()
    counts = {}
    for zone_id in assignments.values():
        counts[zone_id] = counts.get(zone_id, 0) + 1

    payload = []
    for zone in zones:
        payload.append({
            'zone_id': zone.zone_id,
            'zone_name': zone.zone_name,
            'is_armed': zone.is_armed,
            'sensor_count': counts.get(zone.zone_id, 0),
        })
    return payload


def _serialize_sensors(config):
    devices = config.device_manager.load_all_devices()
    assignments = config.list_sensor_assignments()
    zone_map = config.get_zone_name_map()

    payload = []
    for device_id, device_type in devices:
        zone_id = assignments.get(device_id)
        payload.append({
            'device_id': device_id,
            'device_type': device_type,
            'zone_id': zone_id,
            'zone_name': zone_map.get(str(zone_id), str(zone_id)) if zone_id is not None else None,
        })
    return payload


@app.route('/api/security/zones', methods=['GET'])
def api_security_zones():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    config = _configuration_manager()
    if not config:
        return jsonify({'success': False, 'message': 'Configuration manager unavailable'}), 503

    return jsonify({'success': True, 'zones': _serialize_zones(config)}), 200


@app.route('/api/security/zones', methods=['POST'])
def api_security_create_zone():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    config = _configuration_manager()
    if not config:
        return jsonify({'success': False, 'message': 'Configuration manager unavailable'}), 503

    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'success': False, 'message': 'Zone name is required'}), 400

    if not config.add_safety_zone(name):
        return jsonify({'success': False, 'message': 'Failed to create zone'}), 400

    return jsonify({'success': True, 'zones': _serialize_zones(config)}), 201


@app.route('/api/security/zones/<int:zone_id>', methods=['PUT'])
def api_security_update_zone(zone_id: int):
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    config = _configuration_manager()
    if not config:
        return jsonify({'success': False, 'message': 'Configuration manager unavailable'}), 503

    data = request.get_json(silent=True) or {}
    name = data.get('name')
    if not name:
        return jsonify({'success': False, 'message': 'Zone name is required'}), 400

    if not config.modify_safety_zone(zone_id, zone_name=name.strip()):
        return jsonify({'success': False, 'message': 'Zone update failed'}), 400

    return jsonify({'success': True, 'zones': _serialize_zones(config)}), 200


@app.route('/api/security/zones/<int:zone_id>', methods=['DELETE'])
def api_security_delete_zone(zone_id: int):
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    config = _configuration_manager()
    if not config:
        return jsonify({'success': False, 'message': 'Configuration manager unavailable'}), 503

    if not config.delete_safety_zone(zone_id):
        return jsonify({'success': False, 'message': 'Failed to delete zone'}), 400

    return jsonify({'success': True, 'zones': _serialize_zones(config)}), 200


@app.route('/api/security/sensors', methods=['GET'])
def api_security_sensors():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    config = _configuration_manager()
    if not config:
        return jsonify({'success': False, 'message': 'Configuration manager unavailable'}), 503

    return jsonify({
        'success': True,
        'sensors': _serialize_sensors(config),
        'zones': _serialize_zones(config)
    }), 200


@app.route('/api/security/assignments', methods=['POST'])
def api_security_assign_sensor():
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    config = _configuration_manager()
    if not config:
        return jsonify({'success': False, 'message': 'Configuration manager unavailable'}), 503

    data = request.get_json(silent=True) or {}
    device_id = data.get('device_id')
    zone_id = data.get('zone_id')

    if not device_id or zone_id is None:
        return jsonify({'success': False, 'message': 'device_id and zone_id are required'}), 400

    try:
        zone_id = int(zone_id)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'zone_id must be numeric'}), 400

    if not config.assign_sensor_to_zone(device_id, zone_id):
        return jsonify({'success': False, 'message': 'Assignment failed'}), 400

    return jsonify({'success': True, 'sensors': _serialize_sensors(config)}), 200


@app.route('/api/security/assignments/<device_id>', methods=['DELETE'])
def api_security_unassign_sensor(device_id: str):
    auth_error = _require_api_login()
    if auth_error:
        return auth_error

    config = _configuration_manager()
    if not config:
        return jsonify({'success': False, 'message': 'Configuration manager unavailable'}), 503

    if not config.remove_sensor_assignment(device_id):
        return jsonify({'success': False, 'message': 'No assignment to remove'}), 400

    return jsonify({'success': True, 'sensors': _serialize_sensors(config)}), 200

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
            
            # SafeHomeCamera 객체에서 직접 정보 가져오기
            location = camera.get_location()
            
            return jsonify({
                'success': True,
                'camera': {
                    'id': camera_id,
                    'x': location[0] if len(location) > 0 else 0,
                    'y': location[1] if len(location) > 1 else 0,
                    'enabled': camera.is_enabled(),
                    'has_password': camera.has_password()
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
        camera = safehome_system.camera_controller.get_camera(camera_id)
        if not camera:
            return jsonify({'success': False, 'message': 'Camera not found'}), 404
        
        has_password = camera.has_password()
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


def _load_system_sensors(system: System):
    """Instantiate sensor objects from the persisted catalog (with fallback defaults)."""
    factory = create_default_device_factory()
    config = getattr(system, "configuration_manager", None)
    device_records = []

    if config and getattr(config, "device_manager", None):
        try:
            device_records = config.device_manager.load_all_devices()
        except Exception as exc:  # pragma: no cover - defensive
            print(f"[Main] Failed to load devices from database: {exc}")

    sensors = []
    for device_id, device_type in device_records:
        try:
            sensors.append(factory.create(device_type, device_id))
        except DeviceFactoryError as exc:
            print(f"[Main] Skipping device '{device_id}': {exc}")

    if sensors:
        return sensors

    fallback_reason = (
        "System configuration unavailable" if not config else "No registered devices available"
    )
    print(f"[Main] {fallback_reason}; using fallback defaults.")
    fallback_records = [
        ("Front Door", SENSOR_WIN_DOOR),
        ("Living Room", SENSOR_MOTION),
        ("Garden Cam", SENSOR_CAMERA),
    ]

    for device_id, device_type in fallback_records:
        try:
            sensors.append(factory.create(device_type, device_id))
        except DeviceFactoryError as exc:  # pragma: no cover - defensive
            print(f"[Main] Failed to create fallback device '{device_id}': {exc}")

    return sensors


def initialize_devices_after_turn_on(system: System, ui_sensors):
    """Refresh device objects once the system is fully initialized."""
    loaded_sensors = _load_system_sensors(system)
    if loaded_sensors:
        ui_sensors.clear()
        ui_sensors.extend(loaded_sensors)
    system.sensors = ui_sensors

    if system.system_controller:
        for sensor in ui_sensors:
            sensor.add_observer(system.system_controller)
            if sensor.get_type() == SENSOR_CAMERA and hasattr(sensor, "take_picture"):
                system.system_controller.add_camera(sensor)
        print("[Main] Connected sensors to SystemController")

    if system.camera_controller:
        system.camera_controller.add_camera(350, 20)
        system.camera_controller.add_camera(330, 208)
        system.camera_controller.add_camera(332, 262)
        print("[Main] Initialized 3 cameras in CameraController at floorplan black dot positions")


def main():
    global safehome_system
    root = tk.Tk()

    safehome_system = System()

    ui_sensors = [
        WindowDoorSensor("Front Door"),
        MotionDetector("Living Room"),
        Camera("Garden Cam"),
    ]

    ui_app = SafeHomeApp(root, safehome_system, ui_sensors)

    safehome_system.set_ui(ui_app)
    safehome_system.on_turn_on_complete = lambda: initialize_devices_after_turn_on(
        safehome_system, ui_sensors
    )

    t = threading.Thread(target=run_web, daemon=True)
    t.start()

    print("=" * 50)
    print("SafeHome Control Panel Started")
    print("System Status: OFF (Press 'Turn On' to start)")
    print("Web Interface: http://localhost:5000")
    print("=" * 50)

    try:
        root.mainloop()
    finally:
        if safehome_system.system_state.value != "Off":
            print("\nShutting down SafeHome system...")
            safehome_system.turn_off()



if __name__ == "__main__":
    main()
