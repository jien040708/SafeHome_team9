# domain/system_states.py
from abc import ABC, abstractmethod
from utils.constants import *

class SecurityState(ABC):
    @abstractmethod
    def handle_sensor(self, controller, device_id, device_type, status):
        pass

    @abstractmethod
    def get_name(self):
        pass

class DisarmedState(SecurityState):
    def get_name(self):
        return MODE_DISARMED

    def handle_sensor(self, controller, device_id, device_type, status):
        # Disarmed 상태에서는 센서가 울려도 무시하거나 로그만 남김
        print(f"[Logic] System Disarmed. Ignoring sensor: {device_id}")

class AwayState(SecurityState):
    def get_name(self):
        return MODE_AWAY

    def handle_sensor(self, controller, device_id, device_type, status):
        # Away 상태: 모든 센서(문열림, 동작)에 대해 알람 울림
        if status == STATE_OPEN or status == STATE_DETECTED:
            print(f"[Logic/Away] Intrusion detected on {device_id}! Triggering Alarm.")
            controller.trigger_alarm()

class StayState(SecurityState):
    def get_name(self):
        return MODE_STAY

    def handle_sensor(self, controller, device_id, device_type, status):
        # Stay 상태: 문열림만 감지, 내부 동작 감지는 무시
        if device_type == SENSOR_WIN_DOOR and status == STATE_OPEN:
            print(f"[Logic/Stay] Perimeter breached at {device_id}! Triggering Alarm.")
            controller.trigger_alarm()
        elif device_type == SENSOR_MOTION and status == STATE_DETECTED:
            print(f"[Logic/Stay] Motion at {device_id} ignored (User inside).")