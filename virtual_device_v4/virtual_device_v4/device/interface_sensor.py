from abc import ABC, abstractmethod


class InterfaceSensor(ABC):

    @abstractmethod
    def get_id(self):
        raise NotImplementedError

    @abstractmethod
    def read(self):
        raise NotImplementedError

    @abstractmethod
    def arm(self):
        raise NotImplementedError

    @abstractmethod
    def disarm(self):
        raise NotImplementedError

    @abstractmethod
    def test_armed_state(self):
        raise NotImplementedError
