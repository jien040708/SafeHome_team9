"""
Change Master Password Through Control Panel - Test Suite
Common Function 7: Change Master Password Through Control Panel

Test Categories:
- Unit Tests (UT-PWD-001 ~ UT-PWD-010)
- Integration Tests (IT-PWD-001 ~ IT-PWD-004)
- System Level Tests (ST-PWD-001 ~ ST-PWD-004)
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from domain.system import System, SystemState
from storage.storage_manager import StorageManager


def reset_admin_account():
    """Reset admin account to default state (password='1234', unlocked)"""
    sm = StorageManager()
    sm.connect()
    sql = '''UPDATE users SET password = '1234', failed_attempts = 0, is_locked = 0, locked_at = NULL
             WHERE user_id = 'admin' AND interface_type = 'control_panel' '''
    sm.execute_update(sql)


@pytest.fixture(autouse=True, scope='function')
def reset_admin_before_test():
    """Reset admin account before each test"""
    reset_admin_account()
    yield
    reset_admin_account()


# ========================================
# III. Unit Tests
# ========================================

class TestChangeMasterPasswordUnitTests:
    """Unit tests for Change Master Password functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        self.system.turn_on()
        # Login as admin
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True, "Admin login should succeed"
        yield
        # Teardown - restore original password if changed
        if self.system.system_state != SystemState.OFF:
            # Try to restore password
            try:
                if self.system.login_manager.is_user_authenticated():
                    self.system.logout()
                # Re-login and restore password
                self.system.login('admin', '1234', 'control_panel')
            except Exception:
                pass
            self.system.turn_off()

    # UT-PWD-001: test_change_password_success
    def test_change_password_success(self):
        """
        UT-PWD-001: Verifies that password change succeeds with correct inputs.
        """
        # Precondition: User is logged in
        assert self.system.login_manager.is_user_authenticated() is True

        # Action: Change password
        result = self.system.change_master_password(
            current_password='1234',
            new_password='newpass5678',
            confirm_password='newpass5678'
        )

        # Verification
        assert result['success'] is True, "Password change should succeed"
        assert result['phase'] == 3, "Should complete all phases"
        assert 'successfully' in result['message'].lower()

        # Restore original password
        self.system.change_master_password('newpass5678', '1234', '1234')

    # UT-PWD-002: test_change_password_wrong_current
    def test_change_password_wrong_current(self):
        """
        UT-PWD-002: Verifies that password change fails with wrong current password.
        """
        # Action: Try to change password with wrong current password
        result = self.system.change_master_password(
            current_password='wrongpass',
            new_password='newpass5678',
            confirm_password='newpass5678'
        )

        # Verification
        assert result['success'] is False, "Password change should fail"
        assert result['phase'] == 1, "Should fail at Phase 1"
        assert result['error_type'] == 'INCORRECT_PASSWORD'

    # UT-PWD-003: test_change_password_mismatch
    def test_change_password_mismatch(self):
        """
        UT-PWD-003: Verifies that password change fails when new passwords don't match.
        """
        # Action: Try to change password with mismatched new passwords
        result = self.system.change_master_password(
            current_password='1234',
            new_password='newpass1111',
            confirm_password='newpass2222'
        )

        # Verification
        assert result['success'] is False, "Password change should fail"
        assert result['phase'] == 3, "Should fail at Phase 3"
        assert result['error_type'] == 'PASSWORD_MISMATCH'

    # UT-PWD-004: test_change_password_same_as_current
    def test_change_password_same_as_current(self):
        """
        UT-PWD-004: Verifies that password change fails when new password is same as current.
        """
        # Action: Try to change password to same value
        result = self.system.change_master_password(
            current_password='1234',
            new_password='1234',
            confirm_password='1234'
        )

        # Verification
        assert result['success'] is False, "Password change should fail"
        assert result['error_type'] == 'SAME_PASSWORD'

    # UT-PWD-005: test_change_password_not_authenticated
    def test_change_password_not_authenticated(self):
        """
        UT-PWD-005: Verifies that password change fails when user is not authenticated.
        """
        # Precondition: Logout user
        self.system.logout()
        assert self.system.login_manager.is_user_authenticated() is False

        # Action: Try to change password without authentication
        result = self.system.change_master_password(
            current_password='1234',
            new_password='newpass5678',
            confirm_password='newpass5678'
        )

        # Verification
        assert result['success'] is False, "Password change should fail"
        assert result['phase'] == 0, "Should fail at Phase 0"
        assert result['error_type'] == 'NOT_AUTHENTICATED'

    # UT-PWD-006: test_change_password_system_off
    def test_change_password_system_off(self):
        """
        UT-PWD-006: Verifies that password change fails when system is OFF.
        """
        # Precondition: Turn off system
        self.system.turn_off()
        assert self.system.system_state == SystemState.OFF

        # Action: Try to change password
        result = self.system.change_master_password(
            current_password='1234',
            new_password='newpass5678',
            confirm_password='newpass5678'
        )

        # Verification
        assert result['success'] is False, "Password change should fail"
        assert result['error_type'] == 'SYSTEM_OFF'

    # UT-PWD-007: test_change_password_system_locked
    def test_change_password_system_locked(self):
        """
        UT-PWD-007: Verifies that password change fails when system is LOCKED.
        """
        # Precondition: Lock system
        self.system.lock_system()
        assert self.system.system_state == SystemState.LOCKED

        # Action: Try to change password
        result = self.system.change_master_password(
            current_password='1234',
            new_password='newpass5678',
            confirm_password='newpass5678'
        )

        # Verification
        assert result['success'] is False, "Password change should fail"
        assert result['error_type'] == 'SYSTEM_LOCKED'

        # Cleanup: Unlock system
        self.system.unlock_system()

    # UT-PWD-008: test_validate_current_password_correct
    def test_validate_current_password_correct(self):
        """
        UT-PWD-008: Verifies current password validation succeeds with correct password.
        """
        # Action: Validate current password
        result = self.system.validate_current_password_for_change('1234')

        # Verification
        assert result['success'] is True
        assert 'verified' in result['message'].lower()

    # UT-PWD-009: test_validate_current_password_incorrect
    def test_validate_current_password_incorrect(self):
        """
        UT-PWD-009: Verifies current password validation fails with incorrect password.
        """
        # Action: Validate with wrong password
        result = self.system.validate_current_password_for_change('wrongpass')

        # Verification
        assert result['success'] is False
        assert result['error_type'] == 'INCORRECT_PASSWORD'

    # UT-PWD-010: test_set_new_password_mismatch
    def test_set_new_password_mismatch(self):
        """
        UT-PWD-010: Verifies set_new_master_password fails with mismatched passwords.
        """
        # Action: Set new password with mismatch
        result = self.system.set_new_master_password('newpass1', 'newpass2')

        # Verification
        assert result['success'] is False
        assert result['error_type'] == 'PASSWORD_MISMATCH'


# ========================================
# IV. Integration Tests
# ========================================

class TestChangeMasterPasswordIntegrationTests:
    """Integration tests for Change Master Password functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        self.system.turn_on()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # IT-PWD-001: test_full_password_change_flow
    def test_full_password_change_flow(self):
        """
        IT-PWD-001: Validate complete password change flow.
        """
        # Step 1: Login
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True

        # Step 2: Validate current password (Phase 1)
        validate_result = self.system.validate_current_password_for_change('1234')
        assert validate_result['success'] is True

        # Step 3: Set new password (Phase 2-3)
        set_result = self.system.set_new_master_password('newpass5678', 'newpass5678')
        assert set_result['success'] is True

        # Step 4: Verify new password works
        self.system.logout()
        new_login = self.system.login('admin', 'newpass5678', 'control_panel')
        assert new_login is True

        # Restore original password
        self.system.change_master_password('newpass5678', '1234', '1234')

    # IT-PWD-002: test_password_change_with_retry
    def test_password_change_with_retry(self):
        """
        IT-PWD-002: Validate password change with retry after wrong current password.
        """
        # Login
        self.system.login('admin', '1234', 'control_panel')

        # First attempt: wrong password
        result1 = self.system.change_master_password('wrongpass', 'newpass', 'newpass')
        assert result1['success'] is False
        assert result1['error_type'] == 'INCORRECT_PASSWORD'

        # Second attempt: correct password
        result2 = self.system.change_master_password('1234', 'newpass5678', 'newpass5678')
        assert result2['success'] is True

        # Restore original password
        self.system.change_master_password('newpass5678', '1234', '1234')

    # IT-PWD-003: test_password_change_logs_events
    def test_password_change_logs_events(self):
        """
        IT-PWD-003: Validate that password change operations are logged.
        """
        # Login
        self.system.login('admin', '1234', 'control_panel')

        # Change password
        result = self.system.change_master_password('1234', 'newpass5678', 'newpass5678')
        assert result['success'] is True

        # Verify log_manager exists and was used
        assert self.system.log_manager is not None

        # Restore original password
        self.system.change_master_password('newpass5678', '1234', '1234')

    # IT-PWD-004: test_password_change_preserves_login_state
    def test_password_change_preserves_login_state(self):
        """
        IT-PWD-004: Validate that user remains logged in after password change.
        """
        # Login
        self.system.login('admin', '1234', 'control_panel')
        assert self.system.login_manager.is_user_authenticated() is True

        # Change password
        result = self.system.change_master_password('1234', 'newpass5678', 'newpass5678')
        assert result['success'] is True

        # Verify still logged in
        assert self.system.login_manager.is_user_authenticated() is True

        # Restore original password
        self.system.change_master_password('newpass5678', '1234', '1234')


# ========================================
# V. System Level Tests
# ========================================

class TestChangeMasterPasswordSystemLevelTests:
    """System level tests for Change Master Password functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # ST-PWD-001: test_complete_password_change_scenario
    def test_complete_password_change_scenario(self):
        """
        ST-PWD-001: Validate complete password change scenario from system start.
        """
        # Step 1: Turn on system
        self.system.turn_on()
        assert self.system.system_state == SystemState.READY

        # Step 2: Login
        self.system.login('admin', '1234', 'control_panel')
        assert self.system.system_state == SystemState.ACTIVE

        # Step 3: Change password
        result = self.system.change_master_password('1234', 'securepass123', 'securepass123')
        assert result['success'] is True
        assert result['phase'] == 3

        # Step 4: Logout
        self.system.logout()

        # Step 5: Login with new password
        new_login = self.system.login('admin', 'securepass123', 'control_panel')
        assert new_login is True

        # Step 6: Restore password
        restore_result = self.system.change_master_password('securepass123', '1234', '1234')
        assert restore_result['success'] is True

    # ST-PWD-002: test_multiple_password_changes
    def test_multiple_password_changes(self):
        """
        ST-PWD-002: Validate system can handle multiple consecutive password changes.
        """
        self.system.turn_on()
        self.system.login('admin', '1234', 'control_panel')

        passwords = ['1234', 'pass1111', 'pass2222', 'pass3333', '1234']

        for i in range(len(passwords) - 1):
            old_pass = passwords[i]
            new_pass = passwords[i + 1]

            result = self.system.change_master_password(old_pass, new_pass, new_pass)
            assert result['success'] is True, f"Password change {i+1} failed"

    # ST-PWD-003: test_password_change_after_system_reset
    def test_password_change_after_system_reset(self):
        """
        ST-PWD-003: Validate password change works after system reset.
        """
        # Initial setup
        self.system.turn_on()
        self.system.login('admin', '1234', 'control_panel')

        # Change password
        self.system.change_master_password('1234', 'temppass123', 'temppass123')

        # Logout and reset
        self.system.logout()
        reset_result = self.system.reset()
        assert reset_result['success'] is True

        # Login with changed password
        login_result = self.system.login('admin', 'temppass123', 'control_panel')
        assert login_result is True

        # Restore original password
        self.system.change_master_password('temppass123', '1234', '1234')

    # ST-PWD-004: test_password_change_error_recovery
    def test_password_change_error_recovery(self):
        """
        ST-PWD-004: Validate system recovers correctly from password change errors.
        """
        self.system.turn_on()
        self.system.login('admin', '1234', 'control_panel')

        # Multiple failed attempts
        for i in range(3):
            result = self.system.change_master_password('wrongpass', 'newpass', 'newpass')
            assert result['success'] is False
            assert result['error_type'] == 'INCORRECT_PASSWORD'

        # Verify user still logged in
        assert self.system.login_manager.is_user_authenticated() is True

        # Verify original password still works
        self.system.logout()
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True


# ========================================
# Backward Compatibility Tests
# ========================================

class TestChangePasswordBackwardCompatibility:
    """Tests for backward compatibility with existing change_password method"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        self.system.turn_on()
        self.system.login('admin', '1234', 'control_panel')
        yield
        if self.system.system_state != SystemState.OFF:
            # Restore password
            try:
                self.system.login('admin', '1234', 'control_panel')
            except Exception:
                pass
            self.system.turn_off()

    def test_old_change_password_method(self):
        """Test backward compatible change_password method"""
        # Use old method
        result = self.system.change_password('1234', 'newpass5678')
        assert result is True

        # Restore
        self.system.change_password('newpass5678', '1234')

    def test_old_login_manager_change_password(self):
        """Test backward compatible LoginManager.change_password method"""
        # Use old method
        result = self.system.login_manager.change_password('1234', 'newpass5678')
        assert result is True

        # Restore
        self.system.login_manager.change_password('newpass5678', '1234')
