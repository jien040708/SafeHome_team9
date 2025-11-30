"""
devices/device_base.py Coverage 테스트
"""
import pytest
from devices.device_base import DeviceBase


class TestDeviceBase:
    """DeviceBase 클래스 테스트"""
    
    def test_device_base_init(self):
        """DeviceBase 초기화"""
        device = DeviceBase("device1", "Window/Door Sensor")
        
        assert device.device_id == "device1"
        assert device.device_type == "Window/Door Sensor"
        assert isinstance(device.observers, list)
        assert len(device.observers) == 0
    
    def test_add_observer(self):
        """Observer 추가"""
        device = DeviceBase("device1", "Motion Detector")
        observer = Mock()
        
        device.add_observer(observer)
        
        assert len(device.observers) == 1
        assert observer in device.observers
    
    def test_notify_observers(self):
        """Observer 알림"""
        device = DeviceBase("device1", "Camera")
        observer1 = Mock()
        observer2 = Mock()
        
        device.add_observer(observer1)
        device.add_observer(observer2)
        
        device.notify_observers("Triggered")
        
        observer1.update_sensor_status.assert_called_once_with("device1", "Camera", "Triggered")
        observer2.update_sensor_status.assert_called_once_with("device1", "Camera", "Triggered")
    
    def test_get_id(self):
        """get_id 메서드"""
        device = DeviceBase("device1", "Window/Door Sensor")
        
        assert device.get_id() == "device1"
    
    def test_get_type(self):
        """get_type 메서드"""
        device = DeviceBase("device1", "Motion Detector")
        
        assert device.get_type() == "Motion Detector"
    
    def test_get_status(self):
        """get_status 메서드 (기본값)"""
        device = DeviceBase("device1", "Camera")
        
        assert device.get_status() == "Unknown"
    
    def test_multiple_observers(self):
        """여러 Observer 추가"""
        device = DeviceBase("device1", "Window/Door Sensor")
        observers = [Mock() for _ in range(3)]
        
        for obs in observers:
            device.add_observer(obs)
        
        assert len(device.observers) == 3
        
        device.notify_observers("Open")
        
        for obs in observers:
            obs.update_sensor_status.assert_called_once()


# Mock import 추가
from unittest.mock import Mock

