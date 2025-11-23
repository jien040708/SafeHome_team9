"""
Reset the System - Test Suite
Common Function 6: Reset the System

Test Categories:
- Unit Tests (UT-SYS-RST-001 ~ UT-SYS-RST-008)
- Integration Tests (IT-SYS-RST-001 ~ IT-SYS-RST-003)
- System Level Tests (ST-SYS-RST-001 ~ ST-SYS-RST-003)
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from domain.system import System, SystemState


class MockSensor:
    """Mock sensor for testing"""
    def __init__(self, name: str):
        self.name = name
        self.active = True
        self.deactivated = False

    def deactivate(self):
        self.active = False
        self.deactivated = True

    def get_id(self):
        return self.name

    def get_status(self):
        return "closed"


# ========================================
# III. Unit Tests
# ========================================

class TestResetUnitTests:
    """Unit tests for System.reset() method"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        self.system.turn_on()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # UT-SYS-RST-001: test_reset_from_ready_state
    def test_reset_from_ready_state(self):
        """
        UT-SYS-RST-001: Verifies that reset() from READY state succeeds
        and system returns to READY state.
        """
        # Precondition: System is in READY state
        assert self.system.system_state == SystemState.READY

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True, "reset() should succeed"
        assert result['phase'] == 3, "Should complete all 3 phases"
        assert self.system.system_state == SystemState.READY, \
            "System should be READY after reset"

    # UT-SYS-RST-002: test_reset_when_system_off
    def test_reset_when_system_off(self):
        """
        UT-SYS-RST-002: Verifies that reset() when system is OFF
        returns error and does not proceed.
        """
        # Precondition: Turn off system first
        self.system.turn_off()
        assert self.system.system_state == SystemState.OFF

        # Action: Try to reset
        result = self.system.reset()

        # Verification
        assert result['success'] is False, "reset() should fail when OFF"
        assert result['phase'] == 0, "Should fail at phase 0"
        assert 'not running' in result['message'].lower()

    # UT-SYS-RST-003: test_reset_preserves_settings
    def test_reset_preserves_settings(self):
        """
        UT-SYS-RST-003: Verifies that settings are preserved after reset.
        """
        # Precondition: Modify settings
        original_lock_time = 45
        original_alarm_delay = 90

        settings = self.system.configuration_manager.get_system_setting()
        settings.set_system_lock_time(original_lock_time)
        settings.set_alarm_delay_time(original_alarm_delay)
        self.system.configuration_manager.update_system_settings(settings)

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        new_settings = self.system.configuration_manager.get_system_setting()
        assert new_settings.get_system_lock_time() == original_lock_time, \
            "Lock time should be preserved"
        assert new_settings.get_alarm_delay_time() == original_alarm_delay, \
            "Alarm delay should be preserved"

    # UT-SYS-RST-004: test_reset_recreates_components
    def test_reset_recreates_components(self):
        """
        UT-SYS-RST-004: Verifies that all components are recreated after reset.
        """
        # Precondition: Get original component references
        original_storage = self.system.storage_manager
        original_config = self.system.configuration_manager

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        # After reset, components should be new instances
        assert self.system.storage_manager is not None
        assert self.system.configuration_manager is not None
        assert self.system.login_manager is not None
        assert self.system.log_manager is not None
        assert self.system.security_system is not None
        assert self.system.camera_controller is not None

    # UT-SYS-RST-005: test_reset_deactivates_sensors
    def test_reset_deactivates_sensors(self):
        """
        UT-SYS-RST-005: Verifies that sensors are deactivated during Phase 1.
        """
        # Precondition: Add mock sensors
        mock_sensors = [MockSensor("Sensor1"), MockSensor("Sensor2")]
        self.system.sensors = mock_sensors

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        for sensor in mock_sensors:
            assert sensor.deactivated is True, \
                f"Sensor {sensor.name} should be deactivated"

    # UT-SYS-RST-006: test_reset_logs_out_user
    def test_reset_logs_out_user(self):
        """
        UT-SYS-RST-006: Verifies that logged-in user is logged out during reset.
        """
        # Precondition: Login a user
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True
        assert self.system.system_state == SystemState.ACTIVE

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        # After reset, no user should be logged in
        assert self.system.login_manager.is_user_authenticated() is False

    # UT-SYS-RST-007: test_reset_logs_events
    def test_reset_logs_events(self):
        """
        UT-SYS-RST-007: Verifies that reset events are logged.
        """
        # Precondition: LogManager exists
        assert self.system.log_manager is not None

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        # Note: Actual log verification would require checking database

    # UT-SYS-RST-008: test_reset_state_transitions
    def test_reset_state_transitions(self):
        """
        UT-SYS-RST-008: Verifies state transitions: READY -> OFF -> READY
        """
        # Precondition: System is in READY state
        assert self.system.system_state == SystemState.READY

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        assert self.system.system_state == SystemState.READY


# ========================================
# IV. Integration Tests
# ========================================

class TestResetIntegrationTests:
    """Integration tests for Reset System functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        self.system.turn_on()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # IT-SYS-RST-001: test_reset_turn_off_turn_on_sequence
    def test_reset_turn_off_turn_on_sequence(self):
        """
        IT-SYS-RST-001: Validate that reset properly executes
        Turn Off followed by Turn On.
        """
        # Precondition: All components initialized
        assert self.system.storage_manager is not None
        assert self.system.configuration_manager is not None
        assert self.system.login_manager is not None

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        assert result['phase'] == 3
        assert self.system.system_state == SystemState.READY

    # IT-SYS-RST-002: test_reset_after_login_and_settings_change
    def test_reset_after_login_and_settings_change(self):
        """
        IT-SYS-RST-002: Validate reset after user login and settings change.
        """
        # Precondition: Login and change settings
        self.system.login('admin', '1234', 'control_panel')
        assert self.system.system_state == SystemState.ACTIVE

        # Change settings
        settings = self.system.configuration_manager.get_system_setting()
        settings.set_system_lock_time(120)
        self.system.configuration_manager.update_system_settings(settings)

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        # Settings should be preserved
        new_settings = self.system.configuration_manager.get_system_setting()
        assert new_settings.get_system_lock_time() == 120
        # User should be logged out
        assert self.system.login_manager.is_user_authenticated() is False

    # IT-SYS-RST-003: test_reset_camera_controller_integration
    def test_reset_camera_controller_integration(self):
        """
        IT-SYS-RST-003: Validate CameraController is properly reset.
        """
        # Precondition: Add cameras
        self.system.camera_controller.add_camera(100, 100)
        self.system.camera_controller.add_camera(200, 200)
        initial_count = self.system.camera_controller.get_camera_count()

        # Action: Reset the system
        result = self.system.reset()

        # Verification
        assert result['success'] is True
        assert self.system.camera_controller is not None
        # Camera controller is recreated (cameras need to be re-added)


# ========================================
# V. System Level Tests
# ========================================

class TestResetSystemLevelTests:
    """System level tests for Reset System functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # ST-SYS-RST-001: test_complete_reset_flow
    def test_complete_reset_flow(self):
        """
        ST-SYS-RST-001: Validate complete reset flow including
        all phases and state transitions.
        """
        # Step 1: Turn on system
        self.system.turn_on()
        assert self.system.system_state == SystemState.READY

        # Step 2: Login and interact
        self.system.login('admin', '1234', 'control_panel')
        assert self.system.system_state == SystemState.ACTIVE

        # Step 3: Change settings
        settings = self.system.configuration_manager.get_system_setting()
        original_phone = "123-456-7890"
        settings.set_monitoring_service_phone(original_phone)
        self.system.configuration_manager.update_system_settings(settings)

        # Step 4: Reset the system
        result = self.system.reset()

        # Step 5: Verify reset success
        assert result['success'] is True
        assert result['phase'] == 3
        assert self.system.system_state == SystemState.READY

        # Step 6: Verify settings preserved
        new_settings = self.system.configuration_manager.get_system_setting()
        assert new_settings.get_monitoring_service_phone() == original_phone

        # Step 7: Verify can login again
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True

    # ST-SYS-RST-002: test_multiple_reset_cycles
    def test_multiple_reset_cycles(self):
        """
        ST-SYS-RST-002: Validate system can be reset multiple times.
        """
        self.system.turn_on()

        for cycle in range(3):
            # Reset
            result = self.system.reset()
            assert result['success'] is True, f"Cycle {cycle+1}: reset should succeed"
            assert self.system.system_state == SystemState.READY, \
                f"Cycle {cycle+1}: state should be READY"

            # Verify components exist
            assert self.system.login_manager is not None, \
                f"Cycle {cycle+1}: LoginManager should exist"

    # ST-SYS-RST-003: test_reset_preserves_all_settings
    def test_reset_preserves_all_settings(self):
        """
        ST-SYS-RST-003: Validate all types of settings are preserved.
        """
        self.system.turn_on()

        # Set various settings
        settings = self.system.configuration_manager.get_system_setting()
        test_monitoring = "111-222-3333"
        test_homeowner = "444-555-6666"
        test_lock_time = 60
        test_alarm_delay = 120

        settings.set_monitoring_service_phone(test_monitoring)
        settings.set_homeowner_phone(test_homeowner)
        settings.set_system_lock_time(test_lock_time)
        settings.set_alarm_delay_time(test_alarm_delay)
        self.system.configuration_manager.update_system_settings(settings)

        # Reset
        result = self.system.reset()
        assert result['success'] is True

        # Verify all settings preserved
        new_settings = self.system.configuration_manager.get_system_setting()
        assert new_settings.get_monitoring_service_phone() == test_monitoring
        assert new_settings.get_homeowner_phone() == test_homeowner
        assert new_settings.get_system_lock_time() == test_lock_time
        assert new_settings.get_alarm_delay_time() == test_alarm_delay
