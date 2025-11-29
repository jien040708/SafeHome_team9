# domain/system_states.py
from abc import ABC, abstractmethod
from utils.constants import (
    MODE_DISARMED, MODE_AWAY, MODE_STAY,
    SENSOR_WIN_DOOR, SENSOR_MOTION, SENSOR_CAMERA,
    STATE_OPEN, STATE_DETECTED
)

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
        # Disarmed 상태에서는 센서 신호를 무시하고 로그만 남김
        print(f"[Logic] System Disarmed. Ignoring sensor: {device_id} ({status})")

class AwayState(SecurityState):
    def get_name(self):
        return MODE_AWAY

    def handle_sensor(self, controller, device_id, device_type, status):
        # Away 상태: 모든 센서(문열림, 동작, 카메라 스냅샷)에 대해 알람 시퀀스 시작
        
        # [수정] 카메라의 'Picture Taken' 상태도 알람 조건에 포함
        triggers = [STATE_OPEN, STATE_DETECTED, "Picture Taken"] 
        
        if status in triggers:
            print(f"[Logic/Away] Intrusion detected on {device_id}! Initiating ALARM sequence.")
            # [수정] 즉시 알람 대신, 지연 시간을 가진 시퀀스를 시작하도록 호출 변경
            controller.initiate_alarm_sequence() 

class StayState(SecurityState):
    def get_name(self):
        return MODE_STAY

    def handle_sensor(self, controller, device_id, device_type, status):
        # Stay 상태: 문열림(Perimeter)만 감지, 내부 동작 무시
        
        if device_type == SENSOR_WIN_DOOR and status == STATE_OPEN:
            print(f"[Logic/Stay] Perimeter breached at {device_id}! Initiating ALARM sequence.")
            # [수정] 즉시 알람 대신, 지연 시간을 가진 시퀀스를 시작하도록 호출 변경
            controller.initiate_alarm_sequence()
            
        elif device_type == SENSOR_MOTION and status == STATE_DETECTED:
            print(f"[Logic/Stay] Motion at {device_id} ignored (User inside).")

        # 카메라 이벤트는 Stay 상태에서는 무시하도록 명확히 함
        elif device_type == SENSOR_CAMERA:
            print(f"[Logic/Stay] Camera activity at {device_id} ignored.")