from devices.windoor_sensor import WindowDoorSensor
from devices.motion_detector import MotionDetector
from devices.camera import Camera
from utils.constants import *

class DeviceFactory:
    @staticmethod
    def create_device(device_id, device_type):
        if device_type == SENSOR_WIN_DOOR:
            return WindowDoorSensor(device_id)
        elif device_type == SENSOR_MOTION:
            return MotionDetector(device_id)
        elif device_type == SENSOR_CAMERA:
            return Camera(device_id)
        else:
            # 알 수 없는 타입이면 기본값으로 WindowSensor 반환하거나 에러 처리
            print(f"[Factory] Unknown type '{device_type}', defaulting to WindowSensor.")
            return WindowDoorSensor(device_id)