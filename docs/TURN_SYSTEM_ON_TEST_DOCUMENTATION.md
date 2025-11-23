# Turn the System On - Test Documentation

## Common Function 4: Turn the System On

---

## III. Unit Tests

### 1. System Management

#### A. System class

##### 1. turn_on() method (System initialization)

###### a. test_turn_on_from_off_state (UT-SYS-ON-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that calling turn_on() when system is OFF results in successful initialization and system state becomes READY.

**Input Specifications**

System is in OFF state (initial state after constructor)

**Expected Result**

- turn_on() returns True
- system_state becomes SystemState.READY
- All core components are initialized (not None)

**Actual Result (Pass/Fail/Exception)**

Pass: turn_on() returns True
Pass: system_state is SystemState.READY
Pass: All components (StorageManager, ConfigurationManager, LoginManager, LogManager, SystemController, SecuritySystem, CameraController) are not None

**Comment (including references)**

A part of Sequence Diagram on Turn the System On, page 50 of SDS

---

###### b. test_turn_on_when_already_running (UT-SYS-ON-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that calling turn_on() when system is already running returns False and does not reinitialize components.

**Input Specifications**

System is already in READY state (turn_on() called previously)

**Expected Result**

- turn_on() returns False
- system_state remains READY (or current state)
- No exception is raised

**Actual Result (Pass/Fail/Exception)**

Pass: turn_on() returns False
Pass: system_state remains READY
Pass: Components are not reinitialized

**Comment (including references)**

Error handling in Turn the System On flow - preventing double initialization

---

###### c. test_turn_on_initializes_storage_manager (UT-SYS-ON-003)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that StorageManager is properly initialized and connected to the database during system turn_on.

**Input Specifications**

System is in OFF state

**Expected Result**

- StorageManager is created
- Database connection is established

**Actual Result (Pass/Fail/Exception)**

Pass: StorageManager is not None after turn_on()

**Comment (including references)**

Phase 5 (StorageManager creation) in Turn the System On sequence diagram

---

###### d. test_turn_on_initializes_configuration_manager (UT-SYS-ON-004)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that ConfigurationManager is properly initialized with SafeHomeModes, SafetyZones, and SystemSettings.

**Input Specifications**

System is in OFF state

**Expected Result**

- ConfigurationManager is created
- SystemSettings are accessible

**Actual Result (Pass/Fail/Exception)**

Pass: ConfigurationManager is not None
Pass: get_system_setting() returns valid settings object

**Comment (including references)**

Phase 4-7 (ConfigurationManager, SafeHomeModes, SafetyZones, SystemSettings) in sequence diagram

---

###### e. test_turn_on_initializes_login_manager (UT-SYS-ON-005)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that LoginManager is properly initialized and default admin account is created.

**Input Specifications**

System is in OFF state

**Expected Result**

- LoginManager is created
- Default admin account exists

**Actual Result (Pass/Fail/Exception)**

Pass: LoginManager is not None
Pass: Default admin account exists in database

**Comment (including references)**

Phase 9 (LoginManager creation) in Turn the System On sequence diagram

---

###### f. test_turn_on_initializes_log_manager (UT-SYS-ON-006)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that LogManager is properly initialized and SYSTEM_START event is logged.

**Input Specifications**

System is in OFF state

**Expected Result**

- LogManager is created
- SYSTEM_START event is logged

**Actual Result (Pass/Fail/Exception)**

Pass: LogManager is not None
Pass: SYSTEM_START event logged

**Comment (including references)**

Phase 8 (LogManager creation) in Turn the System On sequence diagram

---

###### g. test_turn_on_initializes_security_system (UT-SYS-ON-007)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that SecuritySystem is properly initialized with alarm and siren components.

**Input Specifications**

System is in OFF state

**Expected Result**

- SecuritySystem is created
- Siren component exists

**Actual Result (Pass/Fail/Exception)**

Pass: SecuritySystem is not None
Pass: Siren is not None

**Comment (including references)**

Phase 3 (Alarm creation) in Turn the System On sequence diagram

---

###### h. test_turn_on_initializes_camera_controller (UT-SYS-ON-008)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that CameraController is properly initialized.

**Input Specifications**

System is in OFF state

**Expected Result**

- CameraController is created

**Actual Result (Pass/Fail/Exception)**

Pass: CameraController is not None

**Comment (including references)**

Phase 2 (CameraController creation) in Turn the System On sequence diagram

---

###### i. test_turn_on_state_transition (UT-SYS-ON-009)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies the state transitions: OFF -> INITIALIZING -> READY

**Input Specifications**

System is in OFF state

**Expected Result**

- Initial state is OFF
- Final state is READY after successful turn_on

**Actual Result (Pass/Fail/Exception)**

Pass: Initial state is SystemState.OFF
Pass: Final state is SystemState.READY

**Comment (including references)**

System lifecycle states defined in SDS

---

###### j. test_turn_on_callback_execution (UT-SYS-ON-010)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that the on_turn_on_complete callback is called after successful initialization.

**Input Specifications**

System has on_turn_on_complete callback set

**Expected Result**

- Callback is executed after turn_on completes

**Actual Result (Pass/Fail/Exception)**

Pass: Callback function is executed

**Comment (including references)**

Device initialization callback mechanism in main.py

---

## IV. Integration Tests

### A. Turn the System On

#### 1. test_turn_on_component_dependencies (IT-SYS-ON-001)

| Field | Value |
|-------|-------|
| Class | System, StorageManager, ConfigurationManager, LoginManager |
| Function | Turn on the system |
| Author | |
| Date | |

**Test Case Description**

Validate that all components are initialized in correct order and can communicate with each other.

**Input Specifications**

System is in OFF state

**Detailed Steps**

1. Initialize System
2. Call turn_on()
3. Verify StorageManager is created first
4. Verify ConfigurationManager uses StorageManager
5. Verify LoginManager can authenticate users
6. Verify LogManager can log events

**Expected Result**

- All components are initialized
- Components can interact properly
- ConfigurationManager can retrieve settings
- LogManager can save log events

**Actual Result (Pass/Fail/Exception)**

Pass: All components initialized
Pass: get_system_setting() returns valid settings
Pass: log_event() successfully saves test event

**Comment (including references)**

Initialization order and component dependency chain in Turn the System On sequence diagram

---

#### 2. test_turn_on_then_login (IT-SYS-ON-002)

| Field | Value |
|-------|-------|
| Class | System, LoginManager |
| Function | Turn on then login flow |
| Author | |
| Date | |

**Test Case Description**

Validate that after turn_on, users can successfully log in.

**Input Specifications**

- System is turned on
- Default admin account exists

**Detailed Steps**

1. Turn on the system
2. Attempt login with admin credentials
3. Verify login success

**Expected Result**

- System turns on successfully
- Login with admin/1234 succeeds

**Actual Result (Pass/Fail/Exception)**

Pass: turn_on() returns True
Pass: login_with_details('admin', '1234', 'control_panel') returns success

**Comment (including references)**

Integration between Turn the System On and Login functionality

---

#### 3. test_turn_on_security_system_integration (IT-SYS-ON-003)

| Field | Value |
|-------|-------|
| Class | System, SecuritySystem, ConfigurationManager |
| Function | SecuritySystem integration |
| Author | |
| Date | |

**Test Case Description**

Validate that SecuritySystem is properly configured with settings from ConfigurationManager after turn_on.

**Input Specifications**

System is in OFF state

**Expected Result**

- SecuritySystem is initialized
- SecuritySystem uses configuration from ConfigurationManager
- get_status() returns valid status

**Actual Result (Pass/Fail/Exception)**

Pass: SecuritySystem is not None
Pass: get_status() returns valid status object

**Comment (including references)**

Security system configuration during turn_on sequence

---

## V. System Level Tests

### A. Turn the System On

#### 1. test_complete_turn_on_flow (ST-SYS-ON-001)

| Field | Value |
|-------|-------|
| Class | System (all components) |
| Function | Complete system turn on flow |
| Author | |
| Date | |

**Test Case Description**

Validate the complete system turn on flow including all component initialization and state transitions.

**Input Specifications**

Fresh system instance

**Detailed Steps**

1. Create new System instance (state: OFF)
2. Call turn_on()
3. Verify state becomes READY
4. Verify all components initialized
5. Verify admin can login
6. Verify system settings accessible
7. Turn off system

**Expected Result**

- System transitions from OFF to READY
- All components functional
- Admin login works
- Settings are accessible
- System can be turned off

**Actual Result (Pass/Fail/Exception)**

Pass: System transitions from OFF to READY
Pass: All 8 components initialized (StorageManager, ConfigurationManager, SecuritySystem, LoginManager, LogManager, SystemController, CameraController, Siren)
Pass: Admin login succeeds
Pass: Settings accessible with valid lock_time > 0
Pass: turn_off() returns True and state becomes OFF

**Comment (including references)**

Complete Turn the System On sequence diagram in SDS

---

#### 2. test_turn_on_with_existing_database (ST-SYS-ON-002)

| Field | Value |
|-------|-------|
| Class | System, StorageManager |
| Function | Turn on with existing data |
| Author | |
| Date | |

**Test Case Description**

Validate that system correctly loads existing data when turning on with a pre-existing database.

**Input Specifications**

- First turn on creates and modifies data
- Second turn on should load existing data

**Detailed Steps**

1. First turn on - create and modify settings
2. Turn off system
3. Second turn on
4. Verify system loads correctly

**Expected Result**

- System loads existing configuration
- No errors during second turn on

**Actual Result (Pass/Fail/Exception)**

Pass: Second turn_on() returns True
Pass: Settings are accessible after second turn on

**Comment (including references)**

Database persistence across system lifecycle

---

#### 3. test_turn_on_turn_off_cycle (ST-SYS-ON-003)

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
# Run all Turn System On tests
python tests/common_tests/test_turn_system_on.py

# Run with pytest (if installed)
pytest tests/common_tests/test_turn_system_on.py -v
```

### Test File Location

```
tests/common_tests/test_turn_system_on.py
```

---

## References

- SDS Document: Sequence Diagram on Turn the System On (Page 50)
- System Lifecycle States (SystemState enum)
- Component Initialization Order:
  1. StorageManager
  2. ConfigurationManager (with SafeHomeModes, StorageManager, SafetyZones, SystemSettings)
  3. Siren & SecuritySystem
  4. LoginManager
  5. LogManager
  6. SystemController
  7. CameraController
