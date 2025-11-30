from devices.device_base import DeviceBase
from utils.constants import SENSOR_MOTION, STATE_DETECTED, STATE_CLEAR

class MotionDetector(DeviceBase):
    def __init__(self, device_id):
        super().__init__(device_id, SENSOR_MOTION)
        self.status = STATE_CLEAR

    def get_status(self):
        return self.status

    def detect_motion(self):
        self.status = STATE_DETECTED
        self.notify_observers(self.status)

    def clear_motion(self):
        """모션 감지 상태 클리어"""
        self.status = STATE_CLEAR
        self.notify_observers(self.status)