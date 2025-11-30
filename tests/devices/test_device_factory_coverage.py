"""
devices/device_factory.py Coverage 향상 테스트
7개의 missing lines를 커버하기 위한 추가 테스트
"""
import pytest
from unittest.mock import Mock
from devices.device_factory import (
    DeviceFactory,
    DeviceFactoryError,
    RegisteredDevice,
    register_builtin_devices,
    create_default_device_factory
)
from interfaces.sensor_interface import ISensor


class MockSensor(ISensor):
    """테스트용 Mock Sensor"""
    def __init__(self, device_id):
        self._id = device_id
    
    def get_id(self):
        return self._id
    
    def get_type(self):
        return "Mock"
    
    def get_status(self):
        return "Normal"


class TestDeviceFactoryCoverage:
    """DeviceFactory 커버리지 향상 테스트"""
    
    def test_register_with_override(self):
        """override=True로 등록"""
        factory = DeviceFactory()
        
        builder1 = lambda id: MockSensor(id)
        builder2 = lambda id: MockSensor(id)
        
        factory.register("test_type", builder1)
        # override=True로 재등록
        factory.register("test_type", builder2, override=True)
        
        sensor = factory.create("test_type", "sensor1")
        assert sensor.get_id() == "sensor1"
    
    def test_unregister_existing(self):
        """등록된 타입 제거"""
        factory = DeviceFactory()
        builder = lambda id: MockSensor(id)
        
        factory.register("test_type", builder)
        factory.unregister("test_type")
        
        # 제거 후 생성 시도하면 에러
        with pytest.raises(DeviceFactoryError):
            factory.create("test_type", "sensor1")
    
    def test_unregister_nonexistent(self):
        """존재하지 않는 타입 제거 (에러 없음)"""
        factory = DeviceFactory()
        
        # 에러 없이 실행되어야 함
        factory.unregister("nonexistent_type")
    
    def test_create_with_invalid_builder_return(self):
        """Builder가 ISensor를 반환하지 않을 때"""
        factory = DeviceFactory()
        
        def invalid_builder(device_id):
            return "not a sensor"
        
        factory.register("invalid_type", invalid_builder)
        
        with pytest.raises(DeviceFactoryError) as exc_info:
            factory.create("invalid_type", "sensor1")
        
        assert "must return an ISensor instance" in str(exc_info.value)
    
    def test_create_raises_keyerror_wrapped(self):
        """등록되지 않은 타입 생성 시 KeyError를 DeviceFactoryError로 래핑"""
        factory = DeviceFactory()
        
        with pytest.raises(DeviceFactoryError) as exc_info:
            factory.create("nonexistent_type", "sensor1")
        
        assert "No device registered" in str(exc_info.value)
    
    def test_normalize_type_empty_string(self):
        """빈 문자열 타입 정규화"""
        factory = DeviceFactory()
        
        with pytest.raises(ValueError) as exc_info:
            factory._normalize_type("")
        
        assert "non-empty" in str(exc_info.value)
    
    def test_normalize_type_whitespace(self):
        """공백만 있는 타입 정규화"""
        factory = DeviceFactory()
        
        with pytest.raises(ValueError) as exc_info:
            factory._normalize_type("   ")
        
        assert "non-empty" in str(exc_info.value)
    
    def test_normalize_type_strips_whitespace(self):
        """타입 문자열 공백 제거"""
        factory = DeviceFactory()
        
        normalized = factory._normalize_type("  test_type  ")
        assert normalized == "test_type"
    
    def test_normalize_type_non_string(self):
        """문자열이 아닌 타입"""
        factory = DeviceFactory()
        
        with pytest.raises(ValueError) as exc_info:
            factory._normalize_type(123)
        
        assert "must be a string" in str(exc_info.value)
    
    def test_build_many(self):
        """build_many 테스트"""
        factory = DeviceFactory()
        
        builder = lambda id: MockSensor(id)
        factory.register("test_type", builder)
        
        records = [
            ("sensor1", "test_type"),
            ("sensor2", "test_type"),
            ("sensor3", "test_type"),
        ]
        
        sensors = factory.build_many(records)
        
        assert len(sensors) == 3
        assert sensors[0].get_id() == "sensor1"
        assert sensors[1].get_id() == "sensor2"
        assert sensors[2].get_id() == "sensor3"
    
    def test_registered_devices(self):
        """등록된 디바이스 목록 반환"""
        factory = DeviceFactory()
        
        builder1 = lambda id: MockSensor(id)
        builder2 = lambda id: MockSensor(id)
        
        factory.register("type1", builder1)
        factory.register("type2", builder2)
        
        registered = factory.registered_devices()
        
        assert len(registered) == 2
        assert all(isinstance(r, RegisteredDevice) for r in registered)
        assert {r.device_type for r in registered} == {"type1", "type2"}
    
    def test_register_with_non_callable(self):
        """callable이 아닌 builder 등록 시도"""
        factory = DeviceFactory()
        
        with pytest.raises(ValueError) as exc_info:
            factory.register("test_type", "not callable")
        
        assert "must be callable" in str(exc_info.value)


class TestRegisterBuiltinDevices:
    """register_builtin_devices 함수 테스트"""
    
    def test_register_builtin_devices(self):
        """내장 디바이스 등록"""
        factory = DeviceFactory()
        
        result = register_builtin_devices(factory)
        
        # 같은 인스턴스 반환
        assert result is factory
        
        # 내장 디바이스들이 등록되었는지 확인
        from utils.constants import SENSOR_WIN_DOOR, SENSOR_MOTION, SENSOR_CAMERA
        
        sensor1 = factory.create(SENSOR_WIN_DOOR, "door1")
        sensor2 = factory.create(SENSOR_MOTION, "motion1")
        sensor3 = factory.create(SENSOR_CAMERA, "camera1")
        
        assert sensor1.get_id() == "door1"
        assert sensor2.get_id() == "motion1"
        assert sensor3.get_id() == "camera1"


class TestCreateDefaultDeviceFactory:
    """create_default_device_factory 함수 테스트"""
    
    def test_create_default_device_factory(self):
        """기본 디바이스 팩토리 생성"""
        factory = create_default_device_factory()
        
        assert isinstance(factory, DeviceFactory)
        
        # 내장 디바이스들이 등록되어 있는지 확인
        from utils.constants import SENSOR_WIN_DOOR, SENSOR_MOTION, SENSOR_CAMERA
        
        sensor1 = factory.create(SENSOR_WIN_DOOR, "door1")
        assert sensor1.get_id() == "door1"

