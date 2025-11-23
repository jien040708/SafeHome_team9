# Reset the System - Test Documentation

## Common Function 6: Reset the System

---

## III. Unit Tests

### 1. System Management

#### A. System class

##### 1. reset() method (System restart)

###### a. test_reset_from_ready_state (UT-SYS-RST-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that calling reset() from READY state succeeds and system returns to READY state.

**Input Specifications**

System is in READY state (after turn_on() was called)

**Expected Result**

- reset() returns {'success': True, 'phase': 3}
- system_state becomes SystemState.READY

**Actual Result (Pass/Fail/Exception)**

Pass: reset() returns success with phase 3
Pass: system_state is SystemState.READY

**Comment (including references)**

Reset = Turn Off + Turn On, system should be ready after successful reset

---

###### b. test_reset_when_system_off (UT-SYS-RST-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that calling reset() when system is OFF returns error and does not proceed.

**Input Specifications**

System is in OFF state

**Expected Result**

- reset() returns {'success': False, 'phase': 0}
- Message indicates system is not running

**Actual Result (Pass/Fail/Exception)**

Pass: reset() returns False with phase 0
Pass: Error message contains 'not running'

**Comment (including references)**

Precondition: System must be ON to perform reset

---

###### c. test_reset_preserves_settings (UT-SYS-RST-003)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that settings are preserved after reset.

**Input Specifications**

- System is in READY state
- Settings modified (lock_time=45, alarm_delay=90)

**Expected Result**

- reset() succeeds
- Modified settings are preserved after reset

**Actual Result (Pass/Fail/Exception)**

Pass: reset() returns success
Pass: lock_time remains 45
Pass: alarm_delay remains 90

**Comment (including references)**

Settings are saved during Turn Off (Phase 1) and loaded during Turn On (Phase 2)

---

###### d. test_reset_recreates_components (UT-SYS-RST-004)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that all components are recreated after reset.

**Input Specifications**

System is in READY state with all components initialized

**Expected Result**

- All components (StorageManager, ConfigurationManager, LoginManager, LogManager, SecuritySystem, CameraController) exist after reset

**Actual Result (Pass/Fail/Exception)**

Pass: All components are not None after reset

**Comment (including references)**

Components are destroyed during Turn Off and recreated during Turn On

---

###### e. test_reset_deactivates_sensors (UT-SYS-RST-005)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that sensors are deactivated during Phase 1 of reset.

**Input Specifications**

System has sensors registered

**Expected Result**

- All sensors are deactivated during Phase 1 (Turn Off)

**Actual Result (Pass/Fail/Exception)**

Pass: All mock sensors show deactivated=True

**Comment (including references)**

Phase 1 executes turn_off() which deactivates all sensors

---

###### f. test_reset_logs_out_user (UT-SYS-RST-006)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that logged-in user is logged out during reset.

**Input Specifications**

- System is in ACTIVE state
- User is logged in

**Expected Result**

- User is logged out after reset
- No user authenticated after reset completes

**Actual Result (Pass/Fail/Exception)**

Pass: User logged out during Phase 1
Pass: is_user_authenticated() returns False

**Comment (including references)**

Phase 1 (Turn Off) includes logout operation

---

###### g. test_reset_logs_events (UT-SYS-RST-007)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies that reset events (SYSTEM_RESET_START, SYSTEM_RESET_COMPLETE) are logged.

**Input Specifications**

System is in READY state with LogManager initialized

**Expected Result**

- SYSTEM_RESET_START event logged before Phase 1
- SYSTEM_RESET_COMPLETE event logged after Phase 3

**Actual Result (Pass/Fail/Exception)**

Pass: reset() completes successfully
Pass: Events are logged (verified by method completion)

**Comment (including references)**

Logging provides audit trail for system reset operations

---

###### h. test_reset_state_transitions (UT-SYS-RST-008)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | |
| Date | |
| Version | 1.0.1 |

**Test Case Description**

Verifies state transitions: READY -> (OFF during reset) -> READY

**Input Specifications**

System is in READY state

**Expected Result**

- Initial state is READY
- Final state is READY after successful reset

**Actual Result (Pass/Fail/Exception)**

Pass: Initial state is READY
Pass: Final state is READY

**Comment (including references)**

Reset transitions through OFF state internally then returns to READY

---

## IV. Integration Tests

### A. Reset the System

#### 1. test_reset_turn_off_turn_on_sequence (IT-SYS-RST-001)

| Field | Value |
|-------|-------|
| Class | System |
| Function | Reset the system |
| Author | |
| Date | |

**Test Case Description**

Validate that reset properly executes Turn Off followed by Turn On.

**Input Specifications**

System is in READY state with all components initialized

**Detailed Steps**

1. Initialize System and turn on
2. Verify all components exist
3. Call reset()
4. Verify reset completes with phase 3
5. Verify system state is READY

**Expected Result**

- reset() executes Phase 1 (Turn Off) then Phase 2 (Turn On)
- All components properly destroyed and recreated
- System state is READY

**Actual Result (Pass/Fail/Exception)**

Pass: reset() returns success with phase 3
Pass: System state is READY after reset

**Comment (including references)**

Reset = Turn Off + Turn On sequence

---

#### 2. test_reset_after_login_and_settings_change (IT-SYS-RST-002)

| Field | Value |
|-------|-------|
| Class | System, LoginManager, ConfigurationManager |
| Function | Reset after user activity |
| Author | |
| Date | |

**Test Case Description**

Validate reset after user login and settings change.

**Input Specifications**

- System in ACTIVE state (user logged in)
- Settings modified (lock_time=120)

**Detailed Steps**

1. Turn on system
2. Login as admin
3. Change system_lock_time to 120
4. Call reset()
5. Verify settings preserved
6. Verify user logged out

**Expected Result**

- Reset succeeds
- Settings (lock_time=120) preserved
- User is logged out

**Actual Result (Pass/Fail/Exception)**

Pass: reset() succeeds
Pass: lock_time is 120 after reset
Pass: is_user_authenticated() is False

**Comment (including references)**

Demonstrates settings persistence across reset

---

#### 3. test_reset_camera_controller_integration (IT-SYS-RST-003)

| Field | Value |
|-------|-------|
| Class | System, CameraController |
| Function | CameraController reset |
| Author | |
| Date | |

**Test Case Description**

Validate CameraController is properly reset.

**Input Specifications**

System has cameras added via CameraController

**Expected Result**

- CameraController is recreated after reset
- System is functional

**Actual Result (Pass/Fail/Exception)**

Pass: CameraController is not None after reset
Pass: System state is READY

**Comment (including references)**

CameraController is recreated during Phase 2 (Turn On)

---

## V. System Level Tests

### A. Reset the System

#### 1. test_complete_reset_flow (ST-SYS-RST-001)

| Field | Value |
|-------|-------|
| Class | System (all components) |
| Function | Complete reset flow |
| Author | |
| Date | |

**Test Case Description**

Validate complete reset flow including all phases and state transitions.

**Input Specifications**

Fresh system instance

**Detailed Steps**

1. Turn on system
2. Login as admin
3. Change monitoring phone number
4. Call reset()
5. Verify reset success (phase 3)
6. Verify settings preserved
7. Verify can login again

**Expected Result**

- System transitions through all 3 phases
- Settings (phone number) preserved
- System is functional (can login again)

**Actual Result (Pass/Fail/Exception)**

Pass: reset() returns success with phase 3
Pass: monitoring_phone preserved
Pass: Admin can login after reset

**Comment (including references)**

Complete Reset the System sequence diagram flow

---

#### 2. test_multiple_reset_cycles (ST-SYS-RST-002)

| Field | Value |
|-------|-------|
| Class | System |
| Function | Multiple reset cycles |
| Author | |
| Date | |

**Test Case Description**

Validate system can be reset multiple times without issues.

**Input Specifications**

System turned on

**Detailed Steps**

1. Loop 3 times:
   - Call reset()
   - Verify success
   - Verify state is READY
   - Verify components exist

**Expected Result**

- Each reset succeeds
- State is READY after each reset
- No resource leaks

**Actual Result (Pass/Fail/Exception)**

Pass: All 3 reset cycles succeed
Pass: State is READY after each cycle
Pass: Components exist after each cycle

**Comment (including references)**

System stability testing for repeated reset operations

---

#### 3. test_reset_preserves_all_settings (ST-SYS-RST-003)

| Field | Value |
|-------|-------|
| Class | System, ConfigurationManager, SystemSettings |
| Function | All settings preserved |
| Author | |
| Date | |

**Test Case Description**

Validate all types of settings are preserved after reset.

**Input Specifications**

- monitoring_phone: "111-222-3333"
- homeowner_phone: "444-555-6666"
- lock_time: 60
- alarm_delay: 120

**Expected Result**

All settings are preserved after reset

**Actual Result (Pass/Fail/Exception)**

Pass: monitoring_phone is "111-222-3333"
Pass: homeowner_phone is "444-555-6666"
Pass: lock_time is 60
Pass: alarm_delay is 120

**Comment (including references)**

Comprehensive settings preservation verification

---

## Test Summary

| Category | Test Count | Passed | Failed |
|----------|------------|--------|--------|
| Unit Tests | 8 | 8 | 0 |
| Integration Tests | 3 | 3 | 0 |
| System Level Tests | 3 | 3 | 0 |
| **Total** | **14** | **14** | **0** |

---

## Test Execution

### Running Tests

```bash
# Run all Reset System tests
pytest tests/common_tests/test_reset_system.py -v

# Run only unit tests
pytest tests/common_tests/test_reset_system.py::TestResetUnitTests -v

# Run only integration tests
pytest tests/common_tests/test_reset_system.py::TestResetIntegrationTests -v
```

### Test File Location

```
tests/common_tests/test_reset_system.py
```

---

## Reset Sequence

The reset() method follows this sequence:

### Phase 1: Turn Off the System
1. **Log SYSTEM_RESET_START** - Record reset initiation
2. **Save Configuration** - Persist current settings to database
3. **Deactivate Sensors** - Disable all sensors
4. **Disable All Cameras** - Turn off all cameras
5. **Deactivate Alarm/Siren** - Silence any active alarms
6. **Logout User** - Log out current user
7. **Log SYSTEM_SHUTDOWN** - Record shutdown
8. **Disconnect Database** - Close DB connection
9. **System State = OFF**

### Phase 2: Turn On the System
1. **Connect Database** - Open DB connection
2. **Create StorageManager**
3. **Create ConfigurationManager** - Load saved settings
4. **Create Siren & SecuritySystem**
5. **Create LoginManager**
6. **Create LogManager**
7. **Create SystemController**
8. **Create CameraController**
9. **Log SYSTEM_START**
10. **System State = READY**

### Phase 3: Reset Complete
1. **Log SYSTEM_RESET_COMPLETE**
2. **Return success result**

---

## Key Differences: Reset vs Turn On vs Turn Off

| Aspect | Turn On | Turn Off | Reset |
|--------|---------|----------|-------|
| **Purpose** | Start system | Stop system | Restart system |
| **Precondition** | OFF state | ON state | ON state |
| **Settings** | Load from DB | Save to DB | Save then Load |
| **Components** | Create | Destroy | Destroy & Create |
| **Final State** | READY | OFF | READY |

---

## References

- SDS Document: Sequence Diagram on Reset the System
- System Lifecycle States (SystemState enum)
- Reset = Turn Off + Turn On
- Settings are preserved through database persistence
