"""
storage/storage_manager.py Coverage 향상 테스트
31개의 missing lines를 커버하기 위한 추가 테스트
"""
import pytest
import sqlite3
from unittest.mock import Mock, patch, MagicMock
from storage.storage_manager import StorageManager
from utils.constants import DB_FILE


class TestStorageManagerConnection:
    """StorageManager 연결 테스트"""
    
    def test_connect_when_already_connected(self):
        """이미 연결되어 있을 때"""
        manager = StorageManager()
        manager.connect()
        
        # 두 번째 연결 시도
        result = manager.connect()
        
        assert result is True
    
    def test_disconnect_when_not_connected(self):
        """연결되지 않았을 때 disconnect"""
        manager = StorageManager()
        manager.connection = None
        
        # 예외 없이 실행되어야 함
        manager.disconnect()
    
    @patch('sqlite3.connect')
    def test_connect_with_error(self, mock_connect):
        """연결 중 오류 발생 시"""
        mock_connect.side_effect = sqlite3.Error("Connection error")
        
        manager = StorageManager()
        result = manager.connect()
        
        assert result is False


class TestStorageManagerQuery:
    """StorageManager 쿼리 실행 테스트"""
    
    @pytest.fixture
    def manager(self):
        """StorageManager 인스턴스 생성"""
        return StorageManager()
    
    def test_execute_query_without_connection(self, manager):
        """연결 없이 쿼리 실행 시 자동 연결"""
        manager.connection = None
        
        with patch.object(manager, 'connect', return_value=True):
            with patch.object(manager.connection, 'cursor') as mock_cursor:
                mock_cursor.return_value.execute.return_value = None
                mock_cursor.return_value.fetchall.return_value = []
                
                result = manager.execute_query("SELECT * FROM users")
                
                # connect가 호출되었는지 확인
                manager.connect.assert_called_once()
    
    def test_execute_update_without_connection(self, manager):
        """연결 없이 update 실행 시 자동 연결"""
        manager.connection = None
        
        with patch.object(manager, 'connect', return_value=True):
            with patch.object(manager.connection, 'cursor') as mock_cursor:
                mock_cursor.return_value.execute.return_value = None
                
                result = manager.execute_update("UPDATE users SET password = ?", ("newpass",))
                
                # connect가 호출되었는지 확인
                manager.connect.assert_called_once()
    
    def test_execute_query_with_error(self, manager):
        """쿼리 실행 중 오류 발생 시"""
        with patch.object(manager, 'connection') as mock_conn:
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.execute.side_effect = sqlite3.Error("Query error")
            
            result = manager.execute_query("SELECT * FROM users")
            
            assert result is None
    
    def test_execute_update_with_error(self, manager):
        """Update 실행 중 오류 발생 시"""
        with patch.object(manager, 'connection') as mock_conn:
            mock_cursor = Mock()
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.execute.side_effect = sqlite3.Error("Update error")
            
            result = manager.execute_update("UPDATE users SET password = ?", ("newpass",))
            
            assert result is False


class TestStorageManagerSchema:
    """StorageManager 스키마 초기화 테스트"""
    
    @pytest.fixture
    def manager(self):
        """StorageManager 인스턴스 생성"""
        manager = StorageManager()
        manager.connection = sqlite3.connect(":memory:")
        return manager
    
    def test_schema_initialization(self, manager):
        """스키마 초기화 테스트"""
        manager._initialize_schema()
        
        # users 테이블이 생성되었는지 확인
        cursor = manager.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        
        assert result is not None
    
    def test_default_settings_creation(self, manager):
        """기본 설정 데이터 생성"""
        manager._initialize_schema()
        
        cursor = manager.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM system_settings")
        count = cursor.fetchone()[0]
        
        assert count > 0
    
    def test_default_users_creation(self, manager):
        """기본 사용자 데이터 생성"""
        manager._initialize_schema()
        
        cursor = manager.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        
        assert count > 0


class TestStorageManagerExecuteMany:
    """StorageManager execute_many 테스트"""
    
    @pytest.fixture
    def manager(self):
        """StorageManager 인스턴스 생성"""
        manager = StorageManager()
        manager.connection = sqlite3.connect(":memory:")
        manager._initialize_schema()
        return manager
    
    def test_execute_many_success(self, manager):
        """execute_many 성공"""
        users = [
            ('user1', 'control_panel', 'pass1', None, 1, 0, 0, None, None),
            ('user2', 'control_panel', 'pass2', None, 1, 0, 0, None, None),
        ]
        
        sql = """
            INSERT INTO users
            (user_id, interface_type, password, second_password, access_level,
             failed_attempts, is_locked, locked_at, last_login_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        result = manager.execute_many(sql, users)
        
        assert result is True
        
        # 데이터가 삽입되었는지 확인
        cursor = manager.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id IN ('user1', 'user2')")
        count = cursor.fetchone()[0]
        
        assert count == 2
    
    def test_execute_many_with_error(self, manager):
        """execute_many 중 오류 발생"""
        users = [
            ('user1', 'control_panel', 'pass1', None, 1, 0, 0, None, None),
        ]
        
        # 잘못된 SQL
        sql = "INSERT INTO nonexistent_table VALUES (?, ?, ?)"
        
        result = manager.execute_many(sql, users)
        
        assert result is False
    
    def test_execute_many_without_connection(self, manager):
        """연결 없이 execute_many 실행 시 자동 연결"""
        manager.connection = None
        
        with patch.object(manager, 'connect', return_value=True):
            with patch.object(manager.connection, 'cursor') as mock_cursor:
                mock_cursor.return_value.executemany.return_value = None
                
                result = manager.execute_many("INSERT INTO users VALUES (?, ?)", [('user1', 'pass1')])
                
                # connect가 호출되었는지 확인
                manager.connect.assert_called_once()


class TestStorageManagerGetUser:
    """StorageManager 사용자 조회 테스트"""
    
    @pytest.fixture
    def manager(self):
        """StorageManager 인스턴스 생성"""
        manager = StorageManager()
        manager.connection = sqlite3.connect(":memory:")
        manager._initialize_schema()
        return manager
    
    def test_get_user_by_username_existing(self, manager):
        """존재하는 사용자 조회"""
        result = manager.get_user_by_username('admin', 'control_panel')
        
        assert result is not None
        assert result['user_id'] == 'admin'
    
    def test_get_user_by_username_nonexistent(self, manager):
        """존재하지 않는 사용자 조회"""
        result = manager.get_user_by_username('nonexistent', 'control_panel')
        
        assert result is None


class TestStorageManagerSingleton:
    """StorageManager 싱글톤 패턴 테스트"""
    
    def test_singleton_instance(self):
        """싱글톤 인스턴스 확인"""
        manager1 = StorageManager()
        manager2 = StorageManager()
        
        assert manager1 is manager2

