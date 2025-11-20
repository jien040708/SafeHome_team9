from devices.device_base import DeviceBase
from utils.constants import SENSOR_CAMERA, STATE_RECORDING, STATE_IDLE

class Camera(DeviceBase):
    def __init__(self, device_id):
        super().__init__(device_id, SENSOR_CAMERA)
        self.status = STATE_IDLE

    def get_status(self):
        return self.status

    def take_picture(self):
        print(f"📸 [Camera] {self.device_id} CAPTURED IMAGE!")
        self.notify_observers("Picture Taken")

    def start_recording(self):
        self.status = STATE_RECORDING
        print(f"🎥 [Camera] {self.device_id} Started Recording")
        self.notify_observers(self.status)