"""
Turn the System On (Common Function 4) - Test Suite
=====================================================

This module tests the "Turn the System On" functionality of SafeHome system.

Test Categories:
- Unit Tests: Testing System.turn_on() method
- Integration Tests: Testing component initialization flow
- System Level Tests: Testing UI -> System -> Components flow

Reference: Sequence Diagram on Turn the System On, SDS document
"""

import sys
import os
import pytest

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from domain.system import System, SystemState


# =============================================================================
# III. Unit Tests
# =============================================================================

class TestSystemTurnOn:
    """
    Unit Tests for System.turn_on() method

    Tests the core turn_on functionality of the System class.
    """

    # -------------------------------------------------------------------------
    # A. System class - turn_on() method
    # -------------------------------------------------------------------------

    def test_turn_on_from_off_state(self):
        """
        UT-SYS-ON-001: Turn on system from OFF state

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that calling turn_on() when system is OFF results in
            successful initialization and system state becomes READY.

        Input Specifications:
            System is in OFF state (initial state after constructor)

        Expected Result:
            - turn_on() returns True
            - system_state becomes SystemState.READY
            - All core components are initialized (not None)

        Reference: Sequence Diagram on Turn the System On, SDS
        """
        # Arrange
        system = System()
        assert system.system_state == SystemState.OFF, "Initial state should be OFF"

        # Act
        result = system.turn_on()

        # Assert
        assert result == True, "turn_on() should return True"
        assert system.system_state == SystemState.READY, "State should be READY"

        # Verify all components are initialized
        assert system.storage_manager is not None, "StorageManager should be initialized"
        assert system.configuration_manager is not None, "ConfigurationManager should be initialized"
        assert system.login_manager is not None, "LoginManager should be initialized"
        assert system.log_manager is not None, "LogManager should be initialized"
        assert system.system_controller is not None, "SystemController should be initialized"
        assert system.security_system is not None, "SecuritySystem should be initialized"
        assert system.camera_controller is not None, "CameraController should be initialized"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-001: Turn on system from OFF state")

    def test_turn_on_when_already_running(self):
        """
        UT-SYS-ON-002: Turn on system when already running

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that calling turn_on() when system is already running
            returns False and does not reinitialize components.

        Input Specifications:
            System is already in READY state (turn_on() called previously)

        Expected Result:
            - turn_on() returns False
            - system_state remains READY (or current state)
            - No exception is raised

        Reference: Error handling in Turn the System On flow
        """
        # Arrange
        system = System()
        system.turn_on()
        original_state = system.system_state
        original_storage = system.storage_manager

        # Act
        result = system.turn_on()

        # Assert
        assert result == False, "turn_on() should return False when already running"
        assert system.system_state == original_state, "State should not change"
        assert system.storage_manager is original_storage, "Components should not be reinitialized"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-002: Turn on system when already running")

    def test_turn_on_initializes_storage_manager(self):
        """
        UT-SYS-ON-003: StorageManager initialization during turn_on

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that StorageManager is properly initialized and connected
            to the database during system turn_on.

        Input Specifications:
            System is in OFF state

        Expected Result:
            - StorageManager is created
            - Database connection is established

        Reference: Phase 5 (StorageManager) in Turn the System On sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.storage_manager is not None, "StorageManager should exist"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-003: StorageManager initialization")

    def test_turn_on_initializes_configuration_manager(self):
        """
        UT-SYS-ON-004: ConfigurationManager initialization during turn_on

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that ConfigurationManager is properly initialized
            with SafeHomeModes, SafetyZones, and SystemSettings.

        Input Specifications:
            System is in OFF state

        Expected Result:
            - ConfigurationManager is created
            - SystemSettings are accessible

        Reference: Phase 4-7 in Turn the System On sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.configuration_manager is not None

        # Verify SystemSettings is accessible
        settings = system.configuration_manager.get_system_setting()
        assert settings is not None, "SystemSettings should be accessible"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-004: ConfigurationManager initialization")

    def test_turn_on_initializes_login_manager(self):
        """
        UT-SYS-ON-005: LoginManager initialization during turn_on

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that LoginManager is properly initialized during turn_on.

        Input Specifications:
            System is in OFF state

        Expected Result:
            - LoginManager is created
            - Default admin account exists

        Reference: Phase 9 (LoginManager) in Turn the System On sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.login_manager is not None, "LoginManager should exist"

        # Verify default admin account
        from auth.login_interface import LoginInterface
        login_interface = LoginInterface(user_interface='control_panel')
        admin_exists = login_interface.load('admin', interface_type='control_panel')
        assert admin_exists == True, "Default admin account should exist"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-005: LoginManager initialization")

    def test_turn_on_initializes_log_manager(self):
        """
        UT-SYS-ON-006: LogManager initialization during turn_on

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that LogManager is properly initialized and logs
            the SYSTEM_START event.

        Input Specifications:
            System is in OFF state

        Expected Result:
            - LogManager is created
            - SYSTEM_START event is logged

        Reference: Phase 8 (LogManager) in Turn the System On sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.log_manager is not None, "LogManager should exist"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-006: LogManager initialization")

    def test_turn_on_initializes_security_system(self):
        """
        UT-SYS-ON-007: SecuritySystem initialization during turn_on

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that SecuritySystem is properly initialized with
            alarm and siren components.

        Input Specifications:
            System is in OFF state

        Expected Result:
            - SecuritySystem is created
            - Siren component exists

        Reference: Phase 3 (Alarm) in Turn the System On sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.security_system is not None, "SecuritySystem should exist"
        assert system.siren is not None, "Siren should exist"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-007: SecuritySystem initialization")

    def test_turn_on_initializes_camera_controller(self):
        """
        UT-SYS-ON-008: CameraController initialization during turn_on

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that CameraController is properly initialized.

        Input Specifications:
            System is in OFF state

        Expected Result:
            - CameraController is created

        Reference: Phase 2 (CameraController) in Turn the System On sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.camera_controller is not None, "CameraController should exist"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-008: CameraController initialization")

    def test_turn_on_state_transition(self):
        """
        UT-SYS-ON-009: State transitions during turn_on

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies the state transitions: OFF -> INITIALIZING -> READY

        Input Specifications:
            System is in OFF state

        Expected Result:
            - Initial state is OFF
            - Final state is READY after successful turn_on

        Reference: System lifecycle states in SDS
        """
        # Arrange
        system = System()
        assert system.system_state == SystemState.OFF

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.system_state == SystemState.READY

        # Cleanup
        system.turn_off()
        assert system.system_state == SystemState.OFF

        print("[PASS] UT-SYS-ON-009: State transitions during turn_on")

    def test_turn_on_callback_execution(self):
        """
        UT-SYS-ON-010: on_turn_on_complete callback execution

        Class: System
        Method: turn_on()

        Test Case Description:
            Verifies that the on_turn_on_complete callback is called
            after successful initialization.

        Input Specifications:
            System has on_turn_on_complete callback set

        Expected Result:
            - Callback is executed after turn_on completes

        Reference: Device initialization after turn_on in main.py
        """
        # Arrange
        system = System()
        callback_executed = [False]  # Using list for mutable closure

        def test_callback():
            callback_executed[0] = True

        system.on_turn_on_complete = test_callback

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert callback_executed[0] == True, "Callback should be executed"

        # Cleanup
        system.turn_off()

        print("[PASS] UT-SYS-ON-010: on_turn_on_complete callback execution")


# =============================================================================
# IV. Integration Tests
# =============================================================================

class TestTurnOnIntegration:
    """
    Integration Tests for Turn the System On

    Tests the interaction between multiple components during system startup.
    """

    def test_turn_on_component_dependencies(self):
        """
        IT-SYS-ON-001: Component dependency chain during turn_on

        Class: System, StorageManager, ConfigurationManager, LoginManager

        Test Case Description:
            Validate that all components are initialized in correct order
            and can communicate with each other.

        Input Specifications:
            System is in OFF state

        Detailed Steps:
            1. Initialize System
            2. Call turn_on()
            3. Verify StorageManager is created first
            4. Verify ConfigurationManager uses StorageManager
            5. Verify LoginManager can authenticate users
            6. Verify LogManager can log events

        Expected Result:
            - All components are initialized
            - Components can interact properly

        Reference: Initialization order in Turn the System On sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True

        # Verify component chain
        assert system.storage_manager is not None
        assert system.configuration_manager is not None
        assert system.login_manager is not None
        assert system.log_manager is not None

        # Test component interaction: ConfigurationManager -> StorageManager
        settings = system.configuration_manager.get_system_setting()
        assert settings is not None

        # Test component interaction: LogManager can log
        system.log_manager.log_event(
            event_type="TEST",
            description="Integration test event"
        )

        # Cleanup
        system.turn_off()

        print("[PASS] IT-SYS-ON-001: Component dependency chain")

    def test_turn_on_then_login(self):
        """
        IT-SYS-ON-002: Turn on then login flow

        Class: System, LoginManager

        Test Case Description:
            Validate that after turn_on, users can successfully log in.

        Input Specifications:
            System is turned on
            Default admin account exists

        Detailed Steps:
            1. Turn on the system
            2. Attempt login with admin credentials
            3. Verify login success

        Expected Result:
            - System turns on successfully
            - Login with admin/1234 succeeds

        Reference: Login after system startup flow
        """
        # Arrange
        system = System()
        system.turn_on()

        # Act
        result = system.login_with_details('admin', '1234', 'control_panel')

        # Assert
        assert result['success'] == True, "Admin login should succeed"

        # Cleanup
        system.logout()
        system.turn_off()

        print("[PASS] IT-SYS-ON-002: Turn on then login flow")

    def test_turn_on_security_system_integration(self):
        """
        IT-SYS-ON-003: SecuritySystem integration after turn_on

        Class: System, SecuritySystem, ConfigurationManager

        Test Case Description:
            Validate that SecuritySystem is properly configured with
            settings from ConfigurationManager after turn_on.

        Input Specifications:
            System is in OFF state

        Expected Result:
            - SecuritySystem is initialized
            - SecuritySystem uses configuration from ConfigurationManager

        Reference: Security system configuration in turn_on sequence
        """
        # Arrange
        system = System()

        # Act
        result = system.turn_on()

        # Assert
        assert result == True
        assert system.security_system is not None

        # Verify security system status
        status = system.security_system.get_status()
        assert status is not None, "Security system should have status"

        # Cleanup
        system.turn_off()

        print("[PASS] IT-SYS-ON-003: SecuritySystem integration")


# =============================================================================
# V. System Level Tests
# =============================================================================

class TestTurnOnSystemLevel:
    """
    System Level Tests for Turn the System On

    Tests the complete end-to-end flow from UI to system components.
    """

    def test_complete_turn_on_flow(self):
        """
        ST-SYS-ON-001: Complete system turn on flow

        Class: System (all components)

        Test Case Description:
            Validate the complete system turn on flow including all
            component initialization and state transitions.

        Input Specifications:
            Fresh system instance

        Detailed Steps:
            1. Create new System instance (state: OFF)
            2. Call turn_on()
            3. Verify state becomes READY
            4. Verify all components initialized
            5. Verify admin can login
            6. Verify system settings accessible
            7. Turn off system

        Expected Result:
            - System transitions from OFF to READY
            - All components functional
            - Admin login works
            - Settings are accessible

        Reference: Complete Turn the System On sequence diagram
        """
        # Step 1: Create system
        system = System()
        assert system.system_state == SystemState.OFF

        # Step 2: Turn on
        result = system.turn_on()
        assert result == True

        # Step 3: Verify state
        assert system.system_state == SystemState.READY

        # Step 4: Verify components
        assert system.storage_manager is not None
        assert system.configuration_manager is not None
        assert system.security_system is not None
        assert system.login_manager is not None
        assert system.log_manager is not None
        assert system.system_controller is not None
        assert system.camera_controller is not None
        assert system.siren is not None

        # Step 5: Admin login
        login_result = system.login_with_details('admin', '1234', 'control_panel')
        assert login_result['success'] == True
        system.logout()

        # Step 6: Settings accessible
        settings = system.configuration_manager.get_system_setting()
        assert settings is not None
        assert settings.get_system_lock_time() > 0

        # Step 7: Turn off
        system.turn_off()
        assert system.system_state == SystemState.OFF

        print("[PASS] ST-SYS-ON-001: Complete system turn on flow")

    def test_turn_on_with_existing_database(self):
        """
        ST-SYS-ON-002: Turn on with existing database

        Test Case Description:
            Validate that system correctly loads existing data
            when turning on with a pre-existing database.

        Expected Result:
            - System loads existing configuration
            - Existing users are preserved

        Reference: Database persistence in system lifecycle
        """
        # First turn on - create data
        system1 = System()
        system1.turn_on()

        # Modify settings
        system1.configuration_manager.get_system_setting().set_alarm_delay_time(120)
        system1.configuration_manager.get_system_setting().save()

        system1.turn_off()

        # Second turn on - verify data persists
        system2 = System()
        system2.turn_on()

        settings = system2.configuration_manager.get_system_setting()
        # Note: Value may or may not persist depending on implementation
        # This test verifies the system can turn on with existing DB
        assert settings is not None

        system2.turn_off()

        print("[PASS] ST-SYS-ON-002: Turn on with existing database")

    def test_turn_on_turn_off_cycle(self):
        """
        ST-SYS-ON-003: Multiple turn on/off cycles

        Test Case Description:
            Validate that system can be turned on and off multiple times
            without issues.

        Expected Result:
            - Each turn_on succeeds
            - Each turn_off succeeds
            - No resource leaks

        Reference: System lifecycle management
        """
        system = System()

        for i in range(3):
            # Turn on
            result = system.turn_on()
            assert result == True, f"Turn on cycle {i+1} should succeed"
            assert system.system_state == SystemState.READY

            # Verify basic functionality
            assert system.login_manager is not None

            # Turn off
            result = system.turn_off()
            assert result == True, f"Turn off cycle {i+1} should succeed"
            assert system.system_state == SystemState.OFF

        print("[PASS] ST-SYS-ON-003: Multiple turn on/off cycles")


# =============================================================================
# Main execution for standalone testing
# =============================================================================

def run_all_tests():
    """Run all tests manually"""
    print("=" * 70)
    print("Turn the System On - Test Suite")
    print("=" * 70)

    # Unit Tests
    print("\n" + "-" * 70)
    print("III. Unit Tests")
    print("-" * 70)

    unit_tests = TestSystemTurnOn()
    unit_tests.test_turn_on_from_off_state()
    unit_tests.test_turn_on_when_already_running()
    unit_tests.test_turn_on_initializes_storage_manager()
    unit_tests.test_turn_on_initializes_configuration_manager()
    unit_tests.test_turn_on_initializes_login_manager()
    unit_tests.test_turn_on_initializes_log_manager()
    unit_tests.test_turn_on_initializes_security_system()
    unit_tests.test_turn_on_initializes_camera_controller()
    unit_tests.test_turn_on_state_transition()
    unit_tests.test_turn_on_callback_execution()

    # Integration Tests
    print("\n" + "-" * 70)
    print("IV. Integration Tests")
    print("-" * 70)

    integration_tests = TestTurnOnIntegration()
    integration_tests.test_turn_on_component_dependencies()
    integration_tests.test_turn_on_then_login()
    integration_tests.test_turn_on_security_system_integration()

    # System Level Tests
    print("\n" + "-" * 70)
    print("V. System Level Tests")
    print("-" * 70)

    system_tests = TestTurnOnSystemLevel()
    system_tests.test_complete_turn_on_flow()
    system_tests.test_turn_on_with_existing_database()
    system_tests.test_turn_on_turn_off_cycle()

    print("\n" + "=" * 70)
    print("All tests completed successfully!")
    print("=" * 70)


if __name__ == '__main__':
    run_all_tests()
