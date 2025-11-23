# Turn the System Off - Test Documentation

## Common Function 5: Turn the System Off

---

## III. Unit Tests

### 1. System Management

#### A. System class

##### 1. turn_off() method (System shutdown)

###### a. test_turn_off_from_ready_state (UT-SYS-OFF-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that calling turn_off() when system is READY results in successful shutdown and system state becomes OFF.

**Input Specifications**

System is in READY state (after turn_on() was called)

**Expected Result**

- turn_off() returns True
- system_state becomes SystemState.OFF

**Actual Result (Pass/Fail/Exception)**

Pass: turn_off() returns True
Pass: system_state is SystemState.OFF

**Comment (including references)**

A part of Sequence Diagram on Turn the System Off, page 51 of SDS

---

###### b. test_turn_off_when_already_off (UT-SYS-OFF-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that calling turn_off() when system is already OFF returns False and does not cause errors.

**Input Specifications**

System is already in OFF state

**Expected Result**

- turn_off() returns False
- system_state remains OFF
- No exception is raised

**Actual Result (Pass/Fail/Exception)**

Pass: turn_off() returns False
Pass: system_state remains OFF
Pass: No exception raised

**Comment (including references)**

Error handling in Turn the System Off flow - preventing double shutdown

---

###### c. test_turn_off_saves_configuration (UT-SYS-OFF-003)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that configuration is saved before shutdown.

**Input Specifications**

System is in READY state with ConfigurationManager initialized

**Expected Result**

- Configuration is saved before shutdown
- turn_off() returns True

**Actual Result (Pass/Fail/Exception)**

Pass: Configuration saved successfully
Pass: turn_off() returns True

**Comment (including references)**

Phase 1 (Save Configuration) in Turn the System Off sequence diagram

---

###### d. test_turn_off_deactivates_sensors (UT-SYS-OFF-004)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that all sensors are deactivated during shutdown.

**Input Specifications**

System is running with multiple sensors registered

**Expected Result**

- All sensors are deactivated
- turn_off() returns True

**Actual Result (Pass/Fail/Exception)**

Pass: All sensors deactivated
Pass: turn_off() returns True

**Comment (including references)**

Phase 2 (Deactivate Sensors) in Turn the System Off sequence diagram

---

###### e. test_turn_off_disables_cameras (UT-SYS-OFF-005)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that all cameras are disabled during shutdown.

**Input Specifications**

System is running with CameraController and cameras added

**Expected Result**

- All cameras are disabled via CameraController.disable_all_camera()
- turn_off() returns True

**Actual Result (Pass/Fail/Exception)**

Pass: All cameras disabled
Pass: turn_off() returns True

**Comment (including references)**

Phase 3 (Disable All Cameras) in Turn the System Off sequence diagram

---

###### f. test_turn_off_deactivates_siren (UT-SYS-OFF-006)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that siren is deactivated during shutdown.

**Input Specifications**

System is running with siren in active state

**Expected Result**

- Siren is deactivated (is_active = False)
- turn_off() returns True

**Actual Result (Pass/Fail/Exception)**

Pass: Siren deactivated
Pass: siren.is_active is False

**Comment (including references)**

Phase 4 (Deactivate Alarm/Siren) in Turn the System Off sequence diagram

---

###### g. test_turn_off_logs_out_user (UT-SYS-OFF-007)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that logged-in user is logged out during shutdown.

**Input Specifications**

System is running with a user logged in

**Expected Result**

- User is logged out
- turn_off() returns True
- System state becomes OFF

**Actual Result (Pass/Fail/Exception)**

Pass: User logged out
Pass: turn_off() returns True
Pass: System state is OFF

**Comment (including references)**

Phase 5 (Logout User) in Turn the System Off sequence diagram

---

###### h. test_turn_off_logs_shutdown_event (UT-SYS-OFF-008)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that SYSTEM_SHUTDOWN event is logged.

**Input Specifications**

System is in READY state with LogManager initialized

**Expected Result**

- SYSTEM_SHUTDOWN event is logged
- turn_off() completes successfully

**Actual Result (Pass/Fail/Exception)**

Pass: SYSTEM_SHUTDOWN event logged
Pass: turn_off() returns True

**Comment (including references)**

Phase 6 (Log SYSTEM_SHUTDOWN Event) in Turn the System Off sequence diagram

---

###### i. test_turn_off_disconnects_database (UT-SYS-OFF-009)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that database connection is closed during shutdown.

**Input Specifications**

System is running with StorageManager connected

**Expected Result**

- Database connection is closed via StorageManager.disconnect()
- turn_off() returns True

**Actual Result (Pass/Fail/Exception)**

Pass: Database disconnected
Pass: turn_off() returns True

**Comment (including references)**

Phase 7 (Disconnect Database) in Turn the System Off sequence diagram

---

###### j. test_turn_off_state_transition (UT-SYS-OFF-010)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies the state transitions: READY -> SHUTDOWN -> OFF

**Input Specifications**

System is in READY state

**Expected Result**

- Initial state is READY
- Final state is OFF after successful turn_off

**Actual Result (Pass/Fail/Exception)**

Pass: Initial state is SystemState.READY
Pass: Final state is SystemState.OFF

**Comment (including references)**

System lifecycle states defined in SDS

---

## IV. Integration Tests

### A. Turn the System Off

#### 1. test_turn_off_component_cleanup (IT-SYS-OFF-001)

| Field | Value |
|-------|-------|
| Class | System, StorageManager, ConfigurationManager, LoginManager |
| Function | Turn off the system |
| Author | |
| Date | |

**Test Case Description**

Validate that all components are properly cleaned up and can communicate during shutdown sequence.

**Input Specifications**

System is in READY state with all components initialized

**Detailed Steps**

1. Initialize System and turn on
2. Verify all components exist
3. Call turn_off()
4. Verify shutdown completes successfully
5. Verify system state is OFF

**Expected Result**

- All components are properly cleaned up
- Shutdown sequence completes without errors
- System state becomes OFF

**Actual Result (Pass/Fail/Exception)**

Pass: All components cleaned up
Pass: turn_off() returns True
Pass: System state is OFF

**Comment (including references)**

Component cleanup order in Turn the System Off sequence diagram

---

#### 2. test_turn_off_after_login (IT-SYS-OFF-002)

| Field | Value |
|-------|-------|
| Class | System, LoginManager |
| Function | Turn off after login flow |
| Author | |
| Date | |

**Test Case Description**

Validate that system can be turned off after user login.

**Input Specifications**

- System is turned on
- User is logged in

**Detailed Steps**

1. Turn on the system
2. Login with admin credentials
3. Verify system state is ACTIVE
4. Call turn_off()
5. Verify system state is OFF

**Expected Result**

- System turns off successfully
- User is logged out during shutdown
- System state becomes OFF

**Actual Result (Pass/Fail/Exception)**

Pass: turn_off() returns True
Pass: User logged out
Pass: System state is OFF

**Comment (including references)**

Integration between Turn the System Off and Login functionality

---

#### 3. test_turn_off_security_system_integration (IT-SYS-OFF-003)

| Field | Value |
|-------|-------|
| Class | System, SecuritySystem, Siren |
| Function | SecuritySystem integration |
| Author | |
| Date | |

**Test Case Description**

Validate that SecuritySystem alarm is deactivated during shutdown.

**Input Specifications**

System is in READY state with SecuritySystem initialized

**Expected Result**

- SecuritySystem alarm is deactivated
- Siren is silenced
- turn_off() returns True

**Actual Result (Pass/Fail/Exception)**

Pass: SecuritySystem alarm deactivated
Pass: turn_off() returns True

**Comment (including references)**

Security system deactivation during turn_off sequence

---

## V. System Level Tests

### A. Turn the System Off

#### 1. test_complete_turn_off_flow (ST-SYS-OFF-001)

| Field | Value |
|-------|-------|
| Class | System (all components) |
| Function | Complete system turn off flow |
| Author | |
| Date | |

**Test Case Description**

Validate the complete system turn off flow including all component cleanup and state transitions.

**Input Specifications**

Fresh system instance

**Detailed Steps**

1. Create new System instance (state: OFF)
2. Call turn_on()
3. Verify state becomes READY
4. Verify all components initialized
5. Login with admin credentials
6. Call turn_off()
7. Verify state becomes OFF

**Expected Result**

- System transitions from READY to SHUTDOWN to OFF
- All components properly cleaned up
- User logged out
- Shutdown event logged

**Actual Result (Pass/Fail/Exception)**

Pass: System transitions from READY to OFF
Pass: All components cleaned up
Pass: Admin login and logout successful
Pass: turn_off() returns True

**Comment (including references)**

Complete Turn the System Off sequence diagram in SDS

---

#### 2. test_turn_off_data_persistence (ST-SYS-OFF-002)

| Field | Value |
|-------|-------|
| Class | System, StorageManager, ConfigurationManager |
| Function | Turn off with data persistence |
| Author | |
| Date | |

**Test Case Description**

Validate that data is persisted correctly during shutdown and can be loaded on next turn_on.

**Input Specifications**

- First turn on and modify settings
- Turn off (should save settings)
- Second turn on should load existing data

**Detailed Steps**

1. First turn on - verify settings accessible
2. Turn off system (should save configuration)
3. Second turn on
4. Verify settings are accessible and persisted
5. Turn off system

**Expected Result**

- System saves configuration during shutdown
- Data persists across turn_on/turn_off cycles
- No errors during second turn on

**Actual Result (Pass/Fail/Exception)**

Pass: First turn_off() saves configuration
Pass: Second turn_on() loads settings successfully
Pass: Settings accessible after restart

**Comment (including references)**

Database persistence across system lifecycle

---

#### 3. test_turn_on_turn_off_cycle (ST-SYS-OFF-003)

| Field | Value |
|-------|-------|
| Class | System |
| Function | Multiple turn on/off cycles |
| Author | |
| Date | |

**Test Case Description**

Validate that system can be turned on and off multiple times without issues.

**Input Specifications**

Fresh system instance

**Detailed Steps**

1. Loop 3 times:
   - Turn on system
   - Verify state is READY
   - Verify LoginManager exists
   - Turn off system
   - Verify state is OFF

**Expected Result**

- Each turn_on succeeds
- Each turn_off succeeds
- No resource leaks
- State transitions correctly in each cycle

**Actual Result (Pass/Fail/Exception)**

Pass: All 3 turn_on cycles succeed
Pass: All 3 turn_off cycles succeed
Pass: State correctly transitions in each cycle

**Comment (including references)**

System lifecycle robustness testing

---

## Test Summary

| Category | Test Count | Passed | Failed |
|----------|------------|--------|--------|
| Unit Tests | 10 | 10 | 0 |
| Integration Tests | 3 | 3 | 0 |
| System Level Tests | 3 | 3 | 0 |
| **Total** | **16** | **16** | **0** |

---

## Test Execution

### Running Tests

```bash
# Run all Turn System Off tests
python tests/common_tests/test_turn_system_off.py

# Run with pytest (if installed)
pytest tests/common_tests/test_turn_system_off.py -v
```

### Test File Location

```
tests/common_tests/test_turn_system_off.py
```

---

## Shutdown Sequence

The turn_off() method follows this sequence:

1. **Save Configuration** - Persist current system settings
2. **Deactivate Sensors** - Disable all registered sensors
3. **Disable All Cameras** - Turn off all cameras via CameraController
4. **Deactivate Alarm/Siren** - Silence any active alarms
5. **Logout User** - Log out currently authenticated user
6. **Log SYSTEM_SHUTDOWN Event** - Record shutdown in system logs
7. **Disconnect Database** - Close database connection

---

## References

- SDS Document: Sequence Diagram on Turn the System Off (Page 51)
- System Lifecycle States (SystemState enum)
- Component Shutdown Order:
  1. ConfigurationManager (save settings)
  2. Sensors (deactivate)
  3. CameraController (disable all cameras)
  4. Siren/SecuritySystem (deactivate alarm)
  5. LoginManager (logout user)
  6. LogManager (log shutdown event)
  7. StorageManager (disconnect database)
