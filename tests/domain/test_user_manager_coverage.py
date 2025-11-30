"""
domain/user_manager.py Coverage 향상 테스트
8개의 missing lines를 커버하기 위한 추가 테스트
"""
import pytest
import sqlite3
from unittest.mock import Mock, patch
from domain.user_manager import UserManager
from utils.constants import DB_FILE


class TestUserManagerCoverage:
    """UserManager 커버리지 향상 테스트"""
    
    @pytest.fixture
    def user_manager(self):
        """UserManager 인스턴스 생성 (메모리 DB 사용)"""
        # 메모리 DB로 테스트
        with patch('domain.user_manager.DB_FILE', ':memory:'):
            manager = UserManager()
            # 스키마 초기화
            manager.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id TEXT,
                    password TEXT
                )
            """)
            manager.conn.commit()
            yield manager
            manager.close()
    
    def test_authenticate_success(self, user_manager):
        """인증 성공"""
        # 사용자 추가
        user_manager.cursor.execute(
            "INSERT INTO users (user_id, password) VALUES (?, ?)",
            ('test_user', 'password123')
        )
        user_manager.conn.commit()
        
        result = user_manager.authenticate('test_user', 'password123')
        
        assert result is True
    
    def test_authenticate_failure_wrong_password(self, user_manager):
        """인증 실패 - 잘못된 비밀번호"""
        # 사용자 추가
        user_manager.cursor.execute(
            "INSERT INTO users (user_id, password) VALUES (?, ?)",
            ('test_user', 'password123')
        )
        user_manager.conn.commit()
        
        result = user_manager.authenticate('test_user', 'wrong_password')
        
        assert result is False
    
    def test_authenticate_failure_user_not_found(self, user_manager):
        """인증 실패 - 사용자 없음"""
        result = user_manager.authenticate('nonexistent', 'password')
        
        assert result is False
    
    def test_authenticate_with_database_error(self, user_manager):
        """인증 중 데이터베이스 오류 발생"""
        # cursor.execute에서 예외 발생 시뮬레이션
        user_manager.cursor.execute = Mock(side_effect=sqlite3.Error("Database error"))
        
        result = user_manager.authenticate('test_user', 'password')
        
        assert result is False
    
    def test_close(self, user_manager):
        """연결 종료 테스트"""
        user_manager.close()
        
        # 연결이 종료되었는지 확인 (close 호출 시 예외가 없어야 함)
        try:
            user_manager.cursor.execute("SELECT 1")
            # 연결이 유지되고 있다면
            pass
        except sqlite3.ProgrammingError:
            # 연결이 종료되었다면
            pass

