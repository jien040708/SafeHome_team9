"""
domain/device_manager.py Coverage 향상 테스트
11개의 missing lines를 커버하기 위한 추가 테스트
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from domain.device_manager import DeviceManager


def create_mock_row(data: dict):
    """sqlite3.Row를 모방하는 Mock 객체 생성"""
    mock_row = MagicMock()
    mock_row.__getitem__ = lambda self, key: data[key]
    mock_row.__contains__ = lambda self, key: key in data
    for key, value in data.items():
        setattr(mock_row, key, value)
    return mock_row


class TestDeviceManagerCoverage:
    """DeviceManager 커버리지 향상 테스트"""
    
    @pytest.fixture
    def device_manager(self):
        """DeviceManager 인스턴스 생성 (초기화 방지)"""
        with patch.object(DeviceManager, '_initialize_tables'):
            manager = DeviceManager()
            return manager
    
    def test_add_device_success(self, device_manager):
        """디바이스 추가 성공"""
        with patch.object(device_manager.storage, 'execute_update', return_value=1):
            result = device_manager.add_device("device1", "Window/Door Sensor")
            
            assert result is True
    
    def test_add_device_failure(self, device_manager):
        """디바이스 추가 실패"""
        with patch.object(device_manager.storage, 'execute_update', return_value=0):
            result = device_manager.add_device("device1", "Window/Door Sensor")
            
            assert result is False
    
    def test_load_all_devices_empty(self, device_manager):
        """모든 디바이스 로드 - 빈 결과"""
        with patch.object(device_manager.storage, 'execute_query', return_value=None):
            devices = device_manager.load_all_devices()
            
            assert isinstance(devices, list)
            assert len(devices) == 0
    
    def test_load_all_devices_with_data(self, device_manager):
        """모든 디바이스 로드 - 데이터 있음"""
        mock_rows = [
            create_mock_row({'device_id': 'device1', 'device_type': 'Window/Door Sensor'}),
            create_mock_row({'device_id': 'device2', 'device_type': 'Motion Detector'}),
        ]
        
        with patch.object(device_manager.storage, 'execute_query', return_value=mock_rows):
            devices = device_manager.load_all_devices()
            
            assert len(devices) == 2
    
    def test_ensure_default_devices_no_existing(self, device_manager):
        """기본 디바이스 보장 - 기존 디바이스 없음"""
        mock_row = create_mock_row({'cnt': 0})
        
        def query_side_effect(sql, params=()):
            if 'count(*) as cnt' in sql.lower():
                return [mock_row]
            return []
        
        with patch.object(device_manager.storage, 'execute_query', side_effect=query_side_effect):
            with patch.object(device_manager, 'add_device', return_value=True) as mock_add:
                device_manager.ensure_default_devices()
                
                # 기본 디바이스들이 추가되었는지 확인
                assert mock_add.called
    
    def test_ensure_default_devices_existing(self, device_manager):
        """기본 디바이스 보장 - 기존 디바이스 있음"""
        mock_row = create_mock_row({'cnt': 1})
        
        def query_side_effect(sql, params=()):
            if 'count(*) as cnt' in sql.lower():
                return [mock_row]
            return []
        
        with patch.object(device_manager.storage, 'execute_query', side_effect=query_side_effect):
            result = device_manager.ensure_default_devices()
            
            # 기존 디바이스가 있으면 False 반환
            assert result is False
    
    def test_delete_device_success(self, device_manager):
        """디바이스 삭제 성공"""
        with patch.object(device_manager.storage, 'execute_update', return_value=1):
            with patch.object(device_manager, 'remove_device_zone_assignment', return_value=True):
                result = device_manager.remove_device("device1")
                
                assert result is True
    
    def test_delete_device_failure(self, device_manager):
        """디바이스 삭제 실패"""
        with patch.object(device_manager.storage, 'execute_update', return_value=0):
            result = device_manager.remove_device("device1")
            
            assert result is False
    
    def test_get_device_by_id_found(self, device_manager):
        """디바이스 ID로 조회 - 찾음"""
        mock_row = create_mock_row({'device_id': 'device1', 'device_type': 'Window/Door Sensor'})
        
        with patch.object(device_manager.storage, 'execute_query', return_value=[mock_row]):
            device = device_manager.get_device_by_id("device1")
            
            assert device is not None
            assert device['device_id'] == 'device1'
    
    def test_get_device_by_id_not_found(self, device_manager):
        """디바이스 ID로 조회 - 없음"""
        with patch.object(device_manager.storage, 'execute_query', return_value=[]):
            device = device_manager.get_device_by_id("nonexistent")
            
            assert device is None

