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

app = Flask(__name__)
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
    safehome_system.sensors = sensors

    # Connect Devices to SystemController
    if safehome_system.system_controller:
        for s in sensors:
            s.add_observer(safehome_system.system_controller)
            if isinstance(s, Camera):
                safehome_system.system_controller.add_camera(s)

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
