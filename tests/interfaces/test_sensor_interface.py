"""
interfaces/sensor_interface.py Coverage 테스트
"""
import pytest
from interfaces.sensor_interface import ISensor


class TestSensor(ISensor):
    """ISensor 구현 테스트 클래스"""
    
    def __init__(self, sensor_id, sensor_type, status):
        self._id = sensor_id
        self._type = sensor_type
        self._status = status
    
    def get_id(self):
        return self._id
    
    def get_type(self):
        return self._type
    
    def get_status(self):
        return self._status


class TestISensorInterface:
    """ISensor 인터페이스 테스트"""
    
    def test_isensor_implementation(self):
        """ISensor 구현 테스트"""
        sensor = TestSensor("sensor1", "door", "closed")
        
        assert sensor.get_id() == "sensor1"
        assert sensor.get_type() == "door"
        assert sensor.get_status() == "closed"
    
    def test_isensor_abstract_methods(self):
        """ISensor 추상 메서드 확인"""
        # ISensor는 추상 클래스이므로 직접 인스턴스화 불가
        # 구현 클래스를 통해 테스트
        sensor = TestSensor("sensor2", "motion", "active")
        
        # 모든 추상 메서드가 구현되어야 함
        assert hasattr(sensor, 'get_id')
        assert hasattr(sensor, 'get_type')
        assert hasattr(sensor, 'get_status')
        
        # 메서드가 호출 가능한지 확인
        assert callable(sensor.get_id)
        assert callable(sensor.get_type)
        assert callable(sensor.get_status)

