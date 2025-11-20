from domain.user_manager import UserManager
from domain.system_states import DisarmedState, AwayState, StayState
from devices.siren import Siren
from utils.constants import *

class SystemController:
    def __init__(self, ui_app=None):
        self.ui_app = ui_app
        self.user_manager = UserManager()
        self.current_state = DisarmedState()
        self.siren = Siren("MainSiren")
        self.authenticated_user = None
        self.cameras = [] # 카메라 리스트 별도 관리

    def set_ui(self, ui_app):
        self.ui_app = ui_app

    def add_camera(self, camera):
        self.cameras.append(camera)

    def login(self, user_id, password):
        if self.user_manager.authenticate(user_id, password):
            self.authenticated_user = user_id
            print(f"[Controller] User '{user_id}' logged in.")
            return True
        return False

    def set_security_mode(self, mode_str):
        if not self.authenticated_user:
            print("[Error] Login required.")
            return False

        if mode_str == MODE_DISARMED:
            self.current_state = DisarmedState()
            self.siren.deactivate()
        elif mode_str == MODE_AWAY:
            self.current_state = AwayState()
        elif mode_str == MODE_STAY:
            self.current_state = StayState()
        
        print(f"[Controller] State changed to: {self.current_state.get_name()}")
        
        if self.ui_app:
            self.ui_app.update_status_label(self.current_state.get_name())
        return True

    def update_sensor_status(self, device_id, device_type, status):
        """Observer Pattern: 센서 신호 수신"""
        self.current_state.handle_sensor(self, device_id, device_type, status)
        if self.ui_app:
            self.ui_app.add_log(f"Sensor {device_id} -> {status}")

    def trigger_alarm(self):
        self.siren.activate()
        if self.ui_app:
            self.ui_app.show_alert("!!! SECURITY BREACH DETECTED !!!")

    def trigger_camera(self, trigger_source):
        """침입 발생 시 모든 카메라 촬영"""
        for cam in self.cameras:
            cam.take_picture()