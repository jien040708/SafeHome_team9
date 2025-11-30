"""
config/configuration_manager.py Coverage 향상 테스트
34개의 missing lines를 커버하기 위한 추가 테스트
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from config.configuration_manager import ConfigurationManager, SafeHomeMode, SafetyZone
from config.system_settings import SystemSettings
from security.security_system import SecuritySystem, SecurityMode
from tests.utils import create_mock_row
from domain.device_manager import DeviceManager


class TestSafeHomeMode:
    """SafeHomeMode 클래스 테스트"""
    
    def test_safehome_mode_init(self):
        """SafeHomeMode 초기화"""
        mode = SafeHomeMode(1, "Away", "All sensors active")
        
        assert mode.mode_id == 1
        assert mode.mode_name == "Away"
        assert mode.description == "All sensors active"
    
    def test_safehome_mode_repr(self):
        """SafeHomeMode __repr__"""
        mode = SafeHomeMode(1, "Away", "All sensors active")
        
        repr_str = repr(mode)
        assert "SafeHomeMode" in repr_str
        assert "id=1" in repr_str
        assert "name=Away" in repr_str


class TestSafetyZone:
    """SafetyZone 클래스 테스트"""
    
    def test_safety_zone_init(self):
        """SafetyZone 초기화"""
        zone = SafetyZone(1, "Zone1", False)
        
        assert zone.zone_id == 1
        assert zone.zone_name == "Zone1"
        assert zone.is_armed is False
    
    def test_safety_zone_arm(self):
        """SafetyZone arm"""
        zone = SafetyZone(1, "Zone1", False)
        zone.arm()
        
        assert zone.is_armed is True
    
    def test_safety_zone_disarm(self):
        """SafetyZone disarm"""
        zone = SafetyZone(1, "Zone1", True)
        zone.disarm()
        
        assert zone.is_armed is False
    
    def test_safety_zone_repr_armed(self):
        """SafetyZone __repr__ (armed)"""
        zone = SafetyZone(1, "Zone1", True)
        
        repr_str = repr(zone)
        assert "SafetyZone" in repr_str
        assert "Armed" in repr_str
    
    def test_safety_zone_repr_disarmed(self):
        """SafetyZone __repr__ (disarmed)"""
        zone = SafetyZone(1, "Zone1", False)
        
        repr_str = repr(zone)
        assert "SafetyZone" in repr_str
        assert "Disarmed" in repr_str


class TestConfigurationManagerCoverage:
    """ConfigurationManager 커버리지 향상 테스트"""
    
    @pytest.fixture
    def config_manager(self):
        """ConfigurationManager 인스턴스 생성 (DeviceManager 초기화 방지)"""
        # DeviceManager 초기화 시 _initialize_tables가 호출되는데, 
        # 이때 DB 쿼리가 실행되므로 Mock으로 방지
        with patch.object(DeviceManager, '_initialize_tables'):
            manager = ConfigurationManager()
            return manager
    
    def test_initialize_configuration(self, config_manager):
        """설정 초기화"""
        with patch.object(config_manager, '_load_safehome_modes'), \
             patch.object(config_manager, '_load_safety_zones'):
            result = config_manager.initialize_configuration()
            
            assert result is True
    
    def test_refresh_safety_zones(self, config_manager):
        """Safety Zone 새로고침"""
        with patch.object(config_manager, '_load_safety_zones'):
            zones = config_manager.refresh_safety_zones()
            
            assert isinstance(zones, list)
    
    def test_load_safehome_modes_empty(self, config_manager):
        """SafeHome 모드 로드 - 빈 결과"""
        config_manager.storage.execute_query = Mock(return_value=None)
        
        config_manager._load_safehome_modes()
        
        assert len(config_manager.safehome_modes) == 0
    
    def test_load_safehome_modes_with_data(self, config_manager):
        """SafeHome 모드 로드 - 데이터 있음"""
        mock_rows = [
            create_mock_row({'mode_id': 1, 'mode_name': 'Disarmed', 'description': 'System disarmed'}),
            create_mock_row({'mode_id': 2, 'mode_name': 'Away', 'description': 'All sensors active'}),
        ]
        config_manager.storage.execute_query = Mock(return_value=mock_rows)
        
        config_manager._load_safehome_modes()
        
        assert len(config_manager.safehome_modes) == 2
        assert config_manager.safehome_modes[0].mode_name == 'Disarmed'
    
    def test_load_safety_zones_empty(self, config_manager):
        """Safety Zone 로드 - 빈 결과"""
        config_manager.storage.execute_query = Mock(return_value=None)
        
        config_manager._load_safety_zones()
        
        assert len(config_manager.safety_zones) == 0
    
    def test_load_safety_zones_with_data(self, config_manager):
        """Safety Zone 로드 - 데이터 있음"""
        mock_rows = [
            create_mock_row({'zone_id': 1, 'zone_name': 'Zone1', 'is_armed': 0}),
            create_mock_row({'zone_id': 2, 'zone_name': 'Zone2', 'is_armed': 1}),
        ]
        config_manager.storage.execute_query = Mock(return_value=mock_rows)
        
        config_manager._load_safety_zones()
        
        assert len(config_manager.safety_zones) == 2
        assert config_manager.safety_zones[0].zone_name == 'Zone1'
        assert config_manager.safety_zones[0].is_armed is False
        assert config_manager.safety_zones[1].is_armed is True
    
    def test_get_system_setting(self, config_manager):
        """시스템 설정 반환"""
        settings = config_manager.get_system_setting()
        
        assert settings is not None
    
    def test_get_safety_zone_by_id_found(self, config_manager):
        """Zone ID로 Zone 조회 - 찾음"""
        zone = SafetyZone(1, "Zone1", False)
        config_manager.safety_zones = [zone]
        
        result = config_manager.get_safety_zone_by_id(1)
        
        assert result is not None
        assert result.zone_id == 1
    
    def test_get_safety_zone_by_id_not_found(self, config_manager):
        """Zone ID로 Zone 조회 - 없음"""
        config_manager.safety_zones = []
        
        result = config_manager.get_safety_zone_by_id(999)
        
        assert result is None
    
    def test_get_all_zones(self, config_manager):
        """모든 Zone 반환"""
        zone1 = SafetyZone(1, "Zone1", False)
        zone2 = SafetyZone(2, "Zone2", True)
        config_manager.safety_zones = [zone1, zone2]
        
        zones = config_manager.get_all_zones()
        
        assert len(zones) == 2
    
    def test_configure_security_system(self, config_manager):
        """SecuritySystem 설정"""
        security_system = Mock(spec=SecuritySystem)
        
        # Zone과 센서 설정
        zone = SafetyZone(1, "Zone1", False)
        config_manager.safety_zones = [zone]
        
        config_manager.configure_security_system(security_system)
        
        # SecuritySystem이 설정되었는지 확인
        assert config_manager._security_system_ref is not None
    
    def test_create_zone(self, config_manager):
        """Zone 생성 (add_safety_zone)"""
        config_manager.storage.execute_update = Mock(return_value=1)
        config_manager.storage.get_last_insert_id = Mock(return_value=1)
        config_manager.reconfigure_security_system = Mock()
        
        result = config_manager.add_safety_zone("NewZone")
        
        assert result is True
    
    def test_create_zone_failure(self, config_manager):
        """Zone 생성 실패"""
        config_manager.storage.execute_update = Mock(return_value=0)
        
        result = config_manager.add_safety_zone("NewZone")
        
        assert result is False
    
    def test_update_zone(self, config_manager):
        """Zone 업데이트 (modify_safety_zone)"""
        zone = SafetyZone(1, "Zone1", False)
        config_manager.safety_zones = [zone]
        config_manager.storage.execute_update = Mock(return_value=1)
        
        result = config_manager.modify_safety_zone(1, zone_name="UpdatedZone")
        
        assert result is True
        assert zone.zone_name == "UpdatedZone"
    
    def test_update_zone_not_found(self, config_manager):
        """Zone 업데이트 - Zone 없음"""
        config_manager.safety_zones = []
        
        result = config_manager.modify_safety_zone(999, zone_name="UpdatedZone")
        
        assert result is False
    
    def test_delete_zone(self, config_manager):
        """Zone 삭제 (delete_safety_zone)"""
        zone = SafetyZone(1, "Zone1", False)
        config_manager.safety_zones = [zone]
        config_manager.storage.execute_update = Mock(return_value=1)
        config_manager.reconfigure_security_system = Mock()
        
        result = config_manager.delete_safety_zone(1)
        
        assert result is True
    
    def test_delete_zone_not_found(self, config_manager):
        """Zone 삭제 - Zone 없음"""
        config_manager.safety_zones = []
        
        result = config_manager.delete_safety_zone(999)
        
        assert result is False
    
    def test_assign_sensor_to_zone(self, config_manager):
        """센서를 Zone에 할당"""
        zone = SafetyZone(1, "Zone1", False)
        config_manager.safety_zones = [zone]
        config_manager.device_manager.assign_device_to_zone = Mock(return_value=True)
        config_manager.reconfigure_security_system = Mock()
        
        result = config_manager.assign_sensor_to_zone("sensor1", 1)
        
        assert result is True
    
    def test_assign_sensor_to_zone_failure(self, config_manager):
        """센서 할당 실패 - Zone 없음"""
        config_manager.safety_zones = []
        
        result = config_manager.assign_sensor_to_zone("sensor1", 999)
        
        assert result is False
    
    def test_unassign_sensor_from_zone(self, config_manager):
        """센서 할당 해제 (remove_sensor_assignment)"""
        config_manager.device_manager.remove_device_zone_assignment = Mock(return_value=True)
        config_manager.reconfigure_security_system = Mock()
        
        result = config_manager.remove_sensor_assignment("sensor1")
        
        assert result is True
    
    def test_unassign_sensor_from_zone_failure(self, config_manager):
        """센서 할당 해제 실패"""
        config_manager.device_manager.remove_device_zone_assignment = Mock(return_value=False)
        
        result = config_manager.remove_sensor_assignment("sensor1")
        
        assert result is False

