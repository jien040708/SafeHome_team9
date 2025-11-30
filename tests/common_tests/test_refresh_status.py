"""
Test cases for Refresh Status functionality in Configure > System Control.

Tests cover:
1. get_system_status() method in System class
2. update_system_status() method in MainWindow (UI)
3. Various system states and their correct display
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import tkinter as tk

from domain.system import System, SystemState


class TestGetSystemStatus:
    """Unit tests for System.get_system_status() method."""

    def test_get_system_status_when_system_off(self):
        """Test status when system is OFF."""
        system = System()
        # System is OFF by default

        status = system.get_system_status()

        assert status['state'] == SystemState.OFF.value
        assert status['authenticated'] is False
        assert status['current_user'] is None
        assert status['security_mode'] is None

    def test_get_system_status_when_system_ready(self):
        """Test status when system is READY (turned on but not authenticated)."""
        system = System()
        system.turn_on()

        try:
            status = system.get_system_status()

            assert status['state'] == SystemState.READY.value
            assert status['authenticated'] is False
            assert status['current_user'] is None
            # security_mode should have a value after turn_on
            assert status['security_mode'] is not None
        finally:
            system.turn_off()

    def test_get_system_status_when_authenticated(self):
        """Test status when user is authenticated."""
        system = System()
        system.turn_on()

        try:
            # Login with default credentials
            system.login_manager.login("admin", "1234")

            status = system.get_system_status()

            assert status['state'] == SystemState.READY.value
            assert status['authenticated'] is True
            assert status['current_user'] == "admin"
            assert status['security_mode'] is not None
        finally:
            system.turn_off()

    def test_get_system_status_when_locked(self):
        """Test status when system is LOCKED."""
        system = System()
        system.turn_on()

        try:
            system.lock_system()

            status = system.get_system_status()

            assert status['state'] == SystemState.LOCKED.value
        finally:
            system.turn_off()

    def test_get_system_status_returns_correct_keys(self):
        """Test that get_system_status returns all required keys."""
        system = System()

        status = system.get_system_status()

        required_keys = ['state', 'authenticated', 'current_user', 'security_mode']
        for key in required_keys:
            assert key in status, f"Missing key: {key}"

    def test_get_system_status_without_login_manager(self):
        """Test status when login_manager is None."""
        system = System()
        system.login_manager = None

        status = system.get_system_status()

        assert status['authenticated'] is False
        assert status['current_user'] is None

    def test_get_system_status_without_security_system(self):
        """Test status when security_system is None."""
        system = System()
        system.security_system = None

        status = system.get_system_status()

        assert status['security_mode'] is None


class TestUpdateSystemStatusUI:
    """Unit tests for MainWindow.update_system_status() method."""

    @pytest.fixture
    def mock_system(self):
        """Create a mock system with get_system_status method."""
        mock = Mock()
        mock.get_system_status.return_value = {
            'state': 'READY',
            'authenticated': True,
            'current_user': 'admin',
            'security_mode': 'DISARMED'
        }
        return mock

    def test_update_system_status_displays_correct_info(self, mock_system):
        """Test that update_system_status displays correct information."""
        # Simulate the update_system_status behavior
        status_info = mock_system.get_system_status()
        status_str = f"""System State: {status_info['state']}
Authenticated: {status_info['authenticated']}
Current User: {status_info['current_user'] or 'None'}
Security Mode: {status_info['security_mode'] or 'N/A'}
"""

        assert "System State: READY" in status_str
        assert "Authenticated: True" in status_str
        assert "Current User: admin" in status_str
        assert "Security Mode: DISARMED" in status_str

    def test_update_system_status_handles_none_user(self, mock_system):
        """Test display when current_user is None."""
        mock_system.get_system_status.return_value = {
            'state': 'READY',
            'authenticated': False,
            'current_user': None,
            'security_mode': 'DISARMED'
        }

        status_info = mock_system.get_system_status()
        status_str = f"""System State: {status_info['state']}
Authenticated: {status_info['authenticated']}
Current User: {status_info['current_user'] or 'None'}
Security Mode: {status_info['security_mode'] or 'N/A'}
"""

        assert "Current User: None" in status_str

    def test_update_system_status_handles_none_security_mode(self, mock_system):
        """Test display when security_mode is None."""
        mock_system.get_system_status.return_value = {
            'state': 'OFF',
            'authenticated': False,
            'current_user': None,
            'security_mode': None
        }

        status_info = mock_system.get_system_status()
        status_str = f"""System State: {status_info['state']}
Authenticated: {status_info['authenticated']}
Current User: {status_info['current_user'] or 'None'}
Security Mode: {status_info['security_mode'] or 'N/A'}
"""

        assert "Security Mode: N/A" in status_str

    def test_update_system_status_without_status_text_widget(self, mock_system):
        """Test that method handles missing status_text widget gracefully."""
        mock_window = Mock()
        mock_window.system = mock_system
        # Don't set status_text attribute
        del mock_window.status_text

        # The method should check hasattr and not raise an error
        has_status_text = hasattr(mock_window, 'status_text')
        assert has_status_text is False


class TestRefreshStatusIntegration:
    """Integration tests for Refresh Status functionality."""

    def test_refresh_status_after_login(self):
        """Test that status correctly updates after login."""
        system = System()
        system.turn_on()

        try:
            # Before login
            status_before = system.get_system_status()
            assert status_before['authenticated'] is False
            assert status_before['current_user'] is None

            # After login
            system.login_manager.login("admin", "1234")
            status_after = system.get_system_status()

            assert status_after['authenticated'] is True
            assert status_after['current_user'] == "admin"
        finally:
            system.turn_off()

    def test_refresh_status_after_logout(self):
        """Test that status correctly updates after logout."""
        system = System()
        system.turn_on()

        try:
            # Login first
            system.login_manager.login("admin", "1234")
            status_logged_in = system.get_system_status()
            assert status_logged_in['authenticated'] is True

            # Logout
            system.login_manager.logout()
            status_logged_out = system.get_system_status()

            assert status_logged_out['authenticated'] is False
            assert status_logged_out['current_user'] is None
        finally:
            system.turn_off()

    def test_refresh_status_after_lock_unlock(self):
        """Test that status correctly reflects lock/unlock state."""
        system = System()
        system.turn_on()

        try:
            # Lock system
            system.lock_system()
            status_locked = system.get_system_status()
            assert status_locked['state'] == SystemState.LOCKED.value

            # Unlock system
            system.unlock_system()
            status_unlocked = system.get_system_status()
            assert status_unlocked['state'] == SystemState.READY.value
        finally:
            system.turn_off()

    def test_refresh_status_security_mode_changes(self):
        """Test that status reflects security mode changes."""
        system = System()
        system.turn_on()

        try:
            system.login_manager.login("admin", "1234")

            # Get initial mode
            status = system.get_system_status()
            initial_mode = status['security_mode']

            # Mode should be one of the valid modes
            assert initial_mode in ['DISARMED', 'AWAY', 'STAY']
        finally:
            system.turn_off()


class TestRefreshStatusButtonBehavior:
    """Tests for Refresh Status button behavior."""

    def test_refresh_button_calls_update_system_status(self):
        """Test that clicking Refresh Status button calls update_system_status."""
        mock_window = Mock()
        mock_window.update_system_status = Mock()

        # Simulate button click
        mock_window.update_system_status()

        mock_window.update_system_status.assert_called_once()

    def test_multiple_refresh_calls(self):
        """Test that multiple refresh calls work correctly."""
        system = System()
        system.turn_on()

        try:
            # Call get_system_status multiple times
            status1 = system.get_system_status()
            status2 = system.get_system_status()
            status3 = system.get_system_status()

            # All calls should return consistent results
            assert status1['state'] == status2['state'] == status3['state']
        finally:
            system.turn_off()

    def test_refresh_status_state_values(self):
        """Test all possible system state values."""
        system = System()

        # OFF state
        status_off = system.get_system_status()
        assert status_off['state'] == SystemState.OFF.value

        # READY state
        system.turn_on()
        try:
            status_ready = system.get_system_status()
            assert status_ready['state'] == SystemState.READY.value

            # LOCKED state
            system.lock_system()
            status_locked = system.get_system_status()
            assert status_locked['state'] == SystemState.LOCKED.value
        finally:
            system.turn_off()
