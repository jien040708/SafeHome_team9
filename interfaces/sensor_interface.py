# interfaces/sensor_interface.py
from abc import ABC, abstractmethod

class ISensor(ABC):
    @abstractmethod
    def get_id(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def get_status(self):
        pass