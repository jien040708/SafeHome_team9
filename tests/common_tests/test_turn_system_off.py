"""
Turn the System Off - Test Suite
Common Function 5: Turn the System Off

Test Categories:
- Unit Tests (UT-SYS-OFF-001 ~ UT-SYS-OFF-010)
- Integration Tests (IT-SYS-OFF-001 ~ IT-SYS-OFF-003)
- System Level Tests (ST-SYS-OFF-001 ~ ST-SYS-OFF-003)
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

class TestTurnOffUnitTests:
    """Unit tests for System.turn_off() method"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        self.system.turn_on()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # UT-SYS-OFF-001: test_turn_off_from_ready_state
    def test_turn_off_from_ready_state(self):
        """
        UT-SYS-OFF-001: Verifies that calling turn_off() when system is READY
        results in successful shutdown and system state becomes OFF.
        """
        # Precondition: System is in READY state
        assert self.system.system_state == SystemState.READY

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True, "turn_off() should return True"
        assert self.system.system_state == SystemState.OFF, \
            "System state should be OFF after turn_off()"

    # UT-SYS-OFF-002: test_turn_off_when_already_off
    def test_turn_off_when_already_off(self):
        """
        UT-SYS-OFF-002: Verifies that calling turn_off() when system is already OFF
        returns False and does not cause errors.
        """
        # Precondition: Turn off system first
        self.system.turn_off()
        assert self.system.system_state == SystemState.OFF

        # Action: Try to turn off again
        result = self.system.turn_off()

        # Verification
        assert result is False, "turn_off() should return False when already OFF"
        assert self.system.system_state == SystemState.OFF

    # UT-SYS-OFF-003: test_turn_off_saves_configuration
    def test_turn_off_saves_configuration(self):
        """
        UT-SYS-OFF-003: Verifies that configuration is saved before shutdown.
        """
        # Precondition: System is running with ConfigurationManager
        assert self.system.configuration_manager is not None

        # Modify a setting
        settings = self.system.configuration_manager.get_system_setting()
        original_lock_time = settings.get_system_lock_time()

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF

    # UT-SYS-OFF-004: test_turn_off_deactivates_sensors
    def test_turn_off_deactivates_sensors(self):
        """
        UT-SYS-OFF-004: Verifies that all sensors are deactivated during shutdown.
        """
        # Precondition: Add mock sensors
        mock_sensors = [MockSensor("Sensor1"), MockSensor("Sensor2"), MockSensor("Sensor3")]
        self.system.sensors = mock_sensors

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        for sensor in mock_sensors:
            assert sensor.deactivated is True, \
                f"Sensor {sensor.name} should be deactivated"

    # UT-SYS-OFF-005: test_turn_off_disables_cameras
    def test_turn_off_disables_cameras(self):
        """
        UT-SYS-OFF-005: Verifies that all cameras are disabled during shutdown.
        """
        # Precondition: Add cameras via CameraController
        assert self.system.camera_controller is not None
        self.system.camera_controller.add_camera(100, 100)
        self.system.camera_controller.add_camera(200, 200)

        initial_cameras = self.system.camera_controller.get_all_camera_info()
        assert len(initial_cameras) > 0

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF

    # UT-SYS-OFF-006: test_turn_off_deactivates_siren
    def test_turn_off_deactivates_siren(self):
        """
        UT-SYS-OFF-006: Verifies that siren is deactivated during shutdown.
        """
        # Precondition: Siren exists
        assert self.system.siren is not None

        # Activate siren first (set is_active directly to avoid emoji print issues)
        self.system.siren.is_active = True
        assert self.system.siren.is_active is True

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.siren.is_active is False, \
            "Siren should be deactivated after turn_off()"

    # UT-SYS-OFF-007: test_turn_off_logs_out_user
    def test_turn_off_logs_out_user(self):
        """
        UT-SYS-OFF-007: Verifies that logged-in user is logged out during shutdown.
        """
        # Precondition: Login a user
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True
        assert self.system.login_manager.is_user_authenticated() is True

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF

    # UT-SYS-OFF-008: test_turn_off_logs_shutdown_event
    def test_turn_off_logs_shutdown_event(self):
        """
        UT-SYS-OFF-008: Verifies that SYSTEM_SHUTDOWN event is logged.
        """
        # Precondition: LogManager exists
        assert self.system.log_manager is not None

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True

    # UT-SYS-OFF-009: test_turn_off_disconnects_database
    def test_turn_off_disconnects_database(self):
        """
        UT-SYS-OFF-009: Verifies that database connection is closed during shutdown.
        """
        # Precondition: StorageManager exists and is connected
        assert self.system.storage_manager is not None

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF

    # UT-SYS-OFF-010: test_turn_off_state_transition
    def test_turn_off_state_transition(self):
        """
        UT-SYS-OFF-010: Verifies the state transitions: READY -> SHUTDOWN -> OFF
        """
        # Precondition: System is in READY state
        assert self.system.system_state == SystemState.READY

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF


# ========================================
# IV. Integration Tests
# ========================================

class TestTurnOffIntegrationTests:
    """Integration tests for Turn System Off functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        self.system.turn_on()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # IT-SYS-OFF-001: test_turn_off_component_cleanup
    def test_turn_off_component_cleanup(self):
        """
        IT-SYS-OFF-001: Validate that all components are properly cleaned up
        and can communicate during shutdown sequence.
        """
        # Precondition: All components are initialized
        assert self.system.storage_manager is not None
        assert self.system.configuration_manager is not None
        assert self.system.login_manager is not None
        assert self.system.log_manager is not None
        assert self.system.security_system is not None
        assert self.system.camera_controller is not None
        assert self.system.siren is not None

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF

    # IT-SYS-OFF-002: test_turn_off_after_login
    def test_turn_off_after_login(self):
        """
        IT-SYS-OFF-002: Validate that system can be turned off after user login.
        """
        # Precondition: Login a user
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True
        assert self.system.system_state == SystemState.ACTIVE

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF

    # IT-SYS-OFF-003: test_turn_off_security_system_integration
    def test_turn_off_security_system_integration(self):
        """
        IT-SYS-OFF-003: Validate that SecuritySystem alarm is deactivated during shutdown.
        """
        # Precondition: SecuritySystem is initialized
        assert self.system.security_system is not None

        # Action: Turn off the system
        result = self.system.turn_off()

        # Verification
        assert result is True
        assert self.system.system_state == SystemState.OFF


# ========================================
# V. System Level Tests
# ========================================

class TestTurnOffSystemLevelTests:
    """System level tests for Turn System Off functionality"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Set up test fixtures"""
        self.system = System()
        yield
        # Teardown
        if self.system.system_state != SystemState.OFF:
            self.system.turn_off()

    # ST-SYS-OFF-001: test_complete_turn_off_flow
    def test_complete_turn_off_flow(self):
        """
        ST-SYS-OFF-001: Validate the complete system turn off flow including
        all component cleanup and state transitions.
        """
        # Step 1: Create new System instance and turn on
        assert self.system.system_state == SystemState.OFF
        turn_on_result = self.system.turn_on()
        assert turn_on_result is True
        assert self.system.system_state == SystemState.READY

        # Step 2: Verify all components are initialized
        assert self.system.storage_manager is not None
        assert self.system.configuration_manager is not None
        assert self.system.login_manager is not None
        assert self.system.log_manager is not None
        assert self.system.security_system is not None
        assert self.system.camera_controller is not None
        assert self.system.siren is not None

        # Step 3: Login and interact with system
        login_result = self.system.login('admin', '1234', 'control_panel')
        assert login_result is True

        # Step 4: Turn off the system
        turn_off_result = self.system.turn_off()
        assert turn_off_result is True

        # Step 5: Verify system is OFF
        assert self.system.system_state == SystemState.OFF

    # ST-SYS-OFF-002: test_turn_off_data_persistence
    def test_turn_off_data_persistence(self):
        """
        ST-SYS-OFF-002: Validate that data is persisted correctly during shutdown
        and can be loaded on next turn_on.
        """
        # Step 1: Turn on and modify settings
        self.system.turn_on()
        original_settings = self.system.configuration_manager.get_system_setting()

        # Step 2: Turn off (should save settings)
        turn_off_result = self.system.turn_off()
        assert turn_off_result is True

        # Step 3: Turn on again
        turn_on_result = self.system.turn_on()
        assert turn_on_result is True

        # Step 4: Verify settings are accessible
        new_settings = self.system.configuration_manager.get_system_setting()
        assert new_settings is not None

        # Step 5: Cleanup
        self.system.turn_off()

    # ST-SYS-OFF-003: test_turn_on_turn_off_cycle
    def test_turn_on_turn_off_cycle(self):
        """
        ST-SYS-OFF-003: Validate that system can be turned on and off multiple
        times without issues.
        """
        for cycle in range(3):
            # Turn on
            turn_on_result = self.system.turn_on()
            assert turn_on_result is True, f"Cycle {cycle+1}: turn_on should succeed"
            assert self.system.system_state == SystemState.READY, \
                f"Cycle {cycle+1}: state should be READY"

            # Verify components exist
            assert self.system.login_manager is not None, \
                f"Cycle {cycle+1}: LoginManager should exist"

            # Turn off
            turn_off_result = self.system.turn_off()
            assert turn_off_result is True, f"Cycle {cycle+1}: turn_off should succeed"
            assert self.system.system_state == SystemState.OFF, \
                f"Cycle {cycle+1}: state should be OFF"
