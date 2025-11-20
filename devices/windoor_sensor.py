from devices.device_base import DeviceBase
from utils.constants import SENSOR_WIN_DOOR, STATE_CLOSED, STATE_OPEN

class WindowDoorSensor(DeviceBase):
    def __init__(self, device_id):
        super().__init__(device_id, SENSOR_WIN_DOOR)
        self.status = STATE_CLOSED

    def get_status(self):
        return self.status

    def set_open(self):
        self.status = STATE_OPEN
        self.notify_observers(self.status)

    def set_closed(self):
        self.status = STATE_CLOSED
        self.notify_observers(self.status)