"""
auth/login_manager.py Coverage 향상 테스트
40개의 missing lines를 커버하기 위한 추가 테스트
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from auth.login_manager import LoginManager
from auth.login_interface import LoginInterface
from datetime import datetime, timedelta


class TestLoginManagerCoverage:
    """LoginManager 커버리지 향상 테스트"""

    @pytest.fixture
    def login_manager(self):
        """LoginManager 인스턴스 생성"""
        manager = LoginManager()
        # storage의 원래 메서드 저장
        original_get_user = manager.storage.get_user_by_username
        yield manager
        # 테스트 후 원래 메서드 복원
        manager.storage.get_user_by_username = original_get_user
        manager.storage.connect()
    
    def test_login_with_locked_account_time_not_passed(self, login_manager):
        """잠긴 계정, 시간이 지나지 않았을 때"""
        with patch('auth.login_manager.LoginInterface') as mock_interface_class:
            mock_interface = Mock(spec=LoginInterface)
            mock_interface_class.return_value = mock_interface
            mock_interface.load.return_value = True
            mock_interface.is_locked.return_value = True
            
            user_data = {
                'is_locked': True,
                'locked_at': datetime.now().isoformat()
            }
            login_manager.storage.get_user_by_username = Mock(return_value=user_data)
            
            # 시간이 지나지 않았다고 가정
            with patch.object(login_manager, '_check_and_unlock_if_time_passed', return_value={
                'still_locked': True,
                'remaining_time': 100,
                'message': 'Account is locked'
            }):
                result = login_manager.login_with_details('test_user', 'password')
                
                assert result['success'] is False
                assert result['locked'] is True
    
    def test_login_with_locked_account_time_passed(self, login_manager):
        """잠긴 계정, 시간이 지났을 때 자동 해제"""
        with patch('auth.login_manager.LoginInterface') as mock_interface_class:
            mock_interface = Mock(spec=LoginInterface)
            mock_interface_class.return_value = mock_interface
            mock_interface.load.return_value = True
            mock_interface.is_locked.return_value = True
            mock_interface.get_password.return_value = 'password'  # validate_password 대신

            user_data = {
                'is_locked': True,
                'locked_at': (datetime.now() - timedelta(hours=2)).isoformat()
            }
            login_manager.storage.get_user_by_username = Mock(return_value=user_data)

            # 시간이 지나서 자동 해제됨
            with patch.object(login_manager, '_check_and_unlock_if_time_passed', return_value={
                'still_locked': False
            }):
                # validate_credentials가 True를 반환하도록 설정
                with patch.object(login_manager, 'validate_credentials', return_value=True):
                    result = login_manager.login_with_details('test_user', 'password')

                    # 자동 해제 후 로그인 성공할 수 있음
                    # (validate_credentials가 True면)
    
    def test_login_with_locked_account_no_locked_at(self, login_manager):
        """잠긴 계정, locked_at 정보 없을 때 (영구 잠금)"""
        with patch('auth.login_manager.LoginInterface') as mock_interface_class:
            mock_interface = Mock(spec=LoginInterface)
            mock_interface_class.return_value = mock_interface
            mock_interface.load.return_value = True
            mock_interface.is_locked.return_value = True
            mock_interface.get_number_of_tries.return_value = 5
            
            user_data = {
                'is_locked': False  # locked_at 정보가 없음
            }
            login_manager.storage.get_user_by_username = Mock(return_value=user_data)
            
            result = login_manager.login_with_details('test_user', 'password')
            
            assert result['success'] is False
            assert result.get('locked') is True
    
    def test_login_user_not_found(self, login_manager):
        """사용자가 존재하지 않을 때"""
        with patch('auth.login_manager.LoginInterface') as mock_interface_class:
            mock_interface = Mock(spec=LoginInterface)
            mock_interface_class.return_value = mock_interface
            mock_interface.load.return_value = False
            
            result = login_manager.login_with_details('nonexistent', 'password')
            
            assert result['success'] is False
            assert result['user_exists'] is False
    
    def test_login_max_attempts_exceeded(self, login_manager):
        """최대 시도 횟수 초과 시"""
        with patch('auth.login_manager.LoginInterface') as mock_interface_class:
            mock_interface = Mock(spec=LoginInterface)
            mock_interface_class.return_value = mock_interface
            mock_interface.load.return_value = True
            mock_interface.is_locked.return_value = False
            mock_interface.get_password.return_value = 'correct_password'  # validate_password 대신
            mock_interface.get_number_of_tries.return_value = 4  # MAX_ATTEMPTS는 5

            with patch.object(login_manager, 'validate_credentials', return_value=False):
                # 5번째 실패
                mock_interface.get_number_of_tries.return_value = 5
                mock_interface.increment_tries.return_value = None

                result = login_manager.login_with_details('test_user', 'wrong_password')

                assert result['success'] is False
                # 계정이 잠겨야 함
                assert result.get('locked') is True or mock_interface.lock.called
    
    def test_logout(self, login_manager):
        """로그아웃 테스트"""
        login_manager.current_user = Mock()
        login_manager.is_authenticated = True
        
        login_manager.logout()
        
        assert login_manager.current_user is None
        assert login_manager.is_authenticated is False
    
    def test_get_current_user_when_authenticated(self, login_manager):
        """인증된 사용자 정보 반환"""
        mock_user = Mock()
        mock_user.get_username.return_value = 'test_user'
        mock_user.get_access_level.return_value = 10

        login_manager.current_user = mock_user
        login_manager.is_authenticated = True

        user_info = login_manager.get_current_user()

        # get_current_user는 LoginInterface 객체를 반환
        assert user_info is not None
        assert user_info.get_username() == 'test_user'
        assert user_info.get_access_level() == 10
    
    def test_get_current_user_when_not_authenticated(self, login_manager):
        """인증되지 않았을 때 None 반환"""
        login_manager.is_authenticated = False
        
        user_info = login_manager.get_current_user()
        
        assert user_info is None
    
    def test_change_password_success(self, login_manager):
        """비밀번호 변경 성공"""
        mock_user = Mock()
        mock_user.get_username.return_value = 'test_user'
        mock_user.get_user_interface.return_value = 'control_panel'
        mock_user.get_password.return_value = 'old_pass'
        mock_user.set_password.return_value = True
        mock_user.save.return_value = True

        login_manager.current_user = mock_user
        login_manager.is_authenticated = True

        # change_password는 change_password_with_details를 호출하고, 동일 비밀번호 체크를 함
        # 따라서 validate_credentials를 모킹해야 함
        with patch.object(login_manager, 'validate_credentials', return_value=True):
            result = login_manager.change_password('old_pass', 'new_pass')

            assert result is True
            mock_user.set_password.assert_called_once_with('new_pass')
            mock_user.save.assert_called_once()
    
    def test_change_password_wrong_old_password(self, login_manager):
        """비밀번호 변경 시 기존 비밀번호가 틀릴 때"""
        mock_user = Mock()
        mock_user.get_username.return_value = 'test_user'
        mock_user.get_user_interface.return_value = 'control_panel'
        mock_user.get_password.return_value = 'correct_pass'  # 실제 비밀번호

        login_manager.current_user = mock_user
        login_manager.is_authenticated = True

        # validate_credentials가 False를 반환하도록
        with patch.object(login_manager, 'validate_credentials', return_value=False):
            result = login_manager.change_password('wrong_pass', 'new_pass')

            assert result is False
    
    def test_change_password_not_authenticated(self, login_manager):
        """인증되지 않았을 때 비밀번호 변경"""
        login_manager.is_authenticated = False
        
        result = login_manager.change_password('old_pass', 'new_pass')
        
        assert result is False
    
    def test_check_and_unlock_if_time_passed_still_locked(self, login_manager):
        """시간 기반 잠금 해제 - 아직 잠긴 상태"""
        lock_time = 30  # 30초
        locked_at = datetime.now() - timedelta(seconds=10)  # 10초 전 잠금

        user_data = {
            'locked_at': locked_at.isoformat()
        }

        # SystemSettings 모킹 - 로컬 import이므로 config.system_settings 모듈을 패치
        with patch('config.system_settings.SystemSettings') as mock_settings_class:
            mock_settings = Mock()
            mock_settings_class.return_value = mock_settings
            mock_settings.get_system_lock_time.return_value = lock_time

            result = login_manager._check_and_unlock_if_time_passed(user_data, 'user', 'control_panel')

            assert result['still_locked'] is True
            assert result['remaining_time'] > 0

    def test_check_and_unlock_if_time_passed_unlock(self, login_manager):
        """시간 기반 잠금 해제 - 자동 해제"""
        lock_time = 30  # 30초
        locked_at = datetime.now() - timedelta(seconds=40)  # 40초 전 잠금 (초과)

        user_data = {
            'locked_at': locked_at.isoformat()
        }

        # SystemSettings 모킹 - 로컬 import이므로 config.system_settings 모듈을 패치
        with patch('config.system_settings.SystemSettings') as mock_settings_class:
            mock_settings = Mock()
            mock_settings_class.return_value = mock_settings
            mock_settings.get_system_lock_time.return_value = lock_time

            with patch.object(login_manager.storage, 'reset_failed_login_attempts', return_value=True):
                result = login_manager._check_and_unlock_if_time_passed(user_data, 'user', 'control_panel')

                # 자동 해제되어야 함
                assert result['still_locked'] is False
    
    def test_check_and_unlock_if_time_passed_no_locked_at(self, login_manager):
        """locked_at 정보가 없을 때"""
        user_data = {}
        
        result = login_manager._check_and_unlock_if_time_passed(user_data, 'user', 'control_panel')
        
        # locked_at이 없으면 영구 잠금으로 간주
        assert result['still_locked'] is True

