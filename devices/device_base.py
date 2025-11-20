from interfaces.sensor_interface import ISensor

class DeviceBase(ISensor):
    def __init__(self, device_id, device_type):
        self.device_id = device_id
        self.device_type = device_type
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, status):
        for observer in self.observers:
            observer.update_sensor_status(self.device_id, self.device_type, status)

    def get_id(self):
        return self.device_id

    def get_type(self):
        return self.device_type
    
    def get_status(self):
        return "Unknown"