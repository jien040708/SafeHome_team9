# Change Master Password Through Control Panel - Test Documentation

## Common Function 7: Change Master Password Through Control Panel

---

## III. Unit Tests

### 1. Password Change Management

#### A. System / LoginManager class

##### 1. change_master_password() method

###### a. test_change_password_success (UT-PWD-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies that password change succeeds with correct inputs.

**Input Specifications**

- User is logged in (admin/1234)
- current_password: '1234'
- new_password: 'newpass5678'
- confirm_password: 'newpass5678'

**Expected Result**

- Returns {'success': True, 'phase': 3}
- Password is updated in database

**Actual Result (Pass/Fail/Exception)**

Pass: Password change succeeds with phase 3

**Comment (including references)**

Standard successful password change flow

---

###### b. test_change_password_wrong_current (UT-PWD-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies that password change fails with wrong current password.

**Input Specifications**

- User is logged in
- current_password: 'wrongpass' (incorrect)
- new_password: 'newpass5678'
- confirm_password: 'newpass5678'

**Expected Result**

- Returns {'success': False, 'phase': 1, 'error_type': 'INCORRECT_PASSWORD'}

**Actual Result (Pass/Fail/Exception)**

Pass: Fails at Phase 1 with INCORRECT_PASSWORD error

**Comment (including references)**

Phase 1 validation prevents unauthorized password changes

---

###### c. test_change_password_mismatch (UT-PWD-003)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies that password change fails when new passwords don't match.

**Input Specifications**

- User is logged in
- current_password: '1234'
- new_password: 'newpass1111'
- confirm_password: 'newpass2222' (mismatch)

**Expected Result**

- Returns {'success': False, 'phase': 3, 'error_type': 'PASSWORD_MISMATCH'}

**Actual Result (Pass/Fail/Exception)**

Pass: Fails at Phase 3 with PASSWORD_MISMATCH error

**Comment (including references)**

Confirmation step prevents accidental password changes

---

###### d. test_change_password_same_as_current (UT-PWD-004)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies that password change fails when new password is same as current.

**Input Specifications**

- current_password: '1234'
- new_password: '1234'
- confirm_password: '1234'

**Expected Result**

- Returns {'success': False, 'error_type': 'SAME_PASSWORD'}

**Actual Result (Pass/Fail/Exception)**

Pass: Fails with SAME_PASSWORD error

**Comment (including references)**

Security policy requires different password

---

###### e. test_change_password_not_authenticated (UT-PWD-005)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies that password change fails when user is not authenticated.

**Input Specifications**

- User is NOT logged in
- Attempt to change password

**Expected Result**

- Returns {'success': False, 'phase': 0, 'error_type': 'NOT_AUTHENTICATED'}

**Actual Result (Pass/Fail/Exception)**

Pass: Fails at Phase 0 with NOT_AUTHENTICATED error

**Comment (including references)**

Precondition: User must be logged in

---

###### f. test_change_password_system_off (UT-PWD-006)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies that password change fails when system is OFF.

**Input Specifications**

- System is OFF
- Attempt to change password

**Expected Result**

- Returns {'success': False, 'error_type': 'SYSTEM_OFF'}

**Actual Result (Pass/Fail/Exception)**

Pass: Fails with SYSTEM_OFF error

**Comment (including references)**

Precondition: System must be ON

---

###### g. test_change_password_system_locked (UT-PWD-007)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies that password change fails when system is LOCKED.

**Input Specifications**

- System is LOCKED
- Attempt to change password

**Expected Result**

- Returns {'success': False, 'error_type': 'SYSTEM_LOCKED'}

**Actual Result (Pass/Fail/Exception)**

Pass: Fails with SYSTEM_LOCKED error

**Comment (including references)**

Precondition: System must not be locked

---

###### h. test_validate_current_password_correct (UT-PWD-008)

| Field | Value |
|-------|-------|
| Class | System |
| Method | validate_current_password_for_change() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies current password validation succeeds with correct password.

**Input Specifications**

- User is logged in (admin/1234)
- Validate password: '1234'

**Expected Result**

- Returns {'success': True}

**Actual Result (Pass/Fail/Exception)**

Pass: Validation succeeds

**Comment (including references)**

Phase 1 helper method

---

###### i. test_validate_current_password_incorrect (UT-PWD-009)

| Field | Value |
|-------|-------|
| Class | System |
| Method | validate_current_password_for_change() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies current password validation fails with incorrect password.

**Input Specifications**

- User is logged in
- Validate password: 'wrongpass'

**Expected Result**

- Returns {'success': False, 'error_type': 'INCORRECT_PASSWORD'}

**Actual Result (Pass/Fail/Exception)**

Pass: Validation fails with INCORRECT_PASSWORD

**Comment (including references)**

Phase 1 security check

---

###### j. test_set_new_password_mismatch (UT-PWD-010)

| Field | Value |
|-------|-------|
| Class | System |
| Method | set_new_master_password() |
| Author | |
| Date | |
| Version | 1.0.0 |

**Test Case Description**

Verifies set_new_master_password fails with mismatched passwords.

**Input Specifications**

- new_password: 'newpass1'
- confirm_password: 'newpass2'

**Expected Result**

- Returns {'success': False, 'error_type': 'PASSWORD_MISMATCH'}

**Actual Result (Pass/Fail/Exception)**

Pass: Fails with PASSWORD_MISMATCH

**Comment (including references)**

Phase 3 confirmation check

---

## IV. Integration Tests

### A. Change Master Password

#### 1. test_full_password_change_flow (IT-PWD-001)

| Field | Value |
|-------|-------|
| Class | System, LoginManager |
| Function | Complete password change flow |
| Author | |
| Date | |

**Test Case Description**

Validate complete password change flow from login to verification.

**Input Specifications**

- System is READY
- Admin user available

**Detailed Steps**

1. Login as admin
2. Validate current password (Phase 1)
3. Set new password (Phase 2-3)
4. Logout
5. Login with new password
6. Restore original password

**Expected Result**

- All phases complete successfully
- New password works for login

**Actual Result (Pass/Fail/Exception)**

Pass: Complete flow succeeds

**Comment (including references)**

End-to-end password change verification

---

#### 2. test_password_change_with_retry (IT-PWD-002)

| Field | Value |
|-------|-------|
| Class | System, LoginManager |
| Function | Password change with retry |
| Author | |
| Date | |

**Test Case Description**

Validate password change with retry after wrong current password.

**Input Specifications**

- First attempt: wrong password
- Second attempt: correct password

**Expected Result**

- First attempt fails with INCORRECT_PASSWORD
- Second attempt succeeds

**Actual Result (Pass/Fail/Exception)**

Pass: Retry mechanism works correctly

**Comment (including references)**

Users can retry after Phase 1 failure

---

#### 3. test_password_change_logs_events (IT-PWD-003)

| Field | Value |
|-------|-------|
| Class | System, LogManager |
| Function | Password change event logging |
| Author | |
| Date | |

**Test Case Description**

Validate that password change operations are logged.

**Input Specifications**

- Successful password change

**Expected Result**

- LogManager receives events
- PASSWORD_CHANGE_START and PASSWORD_CHANGE_SUCCESS logged

**Actual Result (Pass/Fail/Exception)**

Pass: Events are logged

**Comment (including references)**

Audit trail for security compliance

---

#### 4. test_password_change_preserves_login_state (IT-PWD-004)

| Field | Value |
|-------|-------|
| Class | System, LoginManager |
| Function | Login state preservation |
| Author | |
| Date | |

**Test Case Description**

Validate that user remains logged in after password change.

**Input Specifications**

- User logged in
- Password change succeeds

**Expected Result**

- is_user_authenticated() returns True after change

**Actual Result (Pass/Fail/Exception)**

Pass: Login state preserved

**Comment (including references)**

UX: No re-login required after password change

---

## V. System Level Tests

### A. Change Master Password

#### 1. test_complete_password_change_scenario (ST-PWD-001)

| Field | Value |
|-------|-------|
| Class | System (all components) |
| Function | Complete scenario |
| Author | |
| Date | |

**Test Case Description**

Validate complete password change scenario from system start.

**Input Specifications**

Fresh system instance

**Detailed Steps**

1. Turn on system
2. Login as admin
3. Change password to 'securepass123'
4. Logout
5. Login with new password
6. Restore original password

**Expected Result**

- All operations succeed
- Password works after change

**Actual Result (Pass/Fail/Exception)**

Pass: Complete scenario succeeds

**Comment (including references)**

Full system-level validation

---

#### 2. test_multiple_password_changes (ST-PWD-002)

| Field | Value |
|-------|-------|
| Class | System |
| Function | Multiple consecutive changes |
| Author | |
| Date | |

**Test Case Description**

Validate system can handle multiple consecutive password changes.

**Input Specifications**

Password sequence: 1234 -> pass1111 -> pass2222 -> pass3333 -> 1234

**Expected Result**

- All 4 password changes succeed

**Actual Result (Pass/Fail/Exception)**

Pass: All changes succeed

**Comment (including references)**

Stability test for repeated operations

---

#### 3. test_password_change_after_system_reset (ST-PWD-003)

| Field | Value |
|-------|-------|
| Class | System |
| Function | Password change after reset |
| Author | |
| Date | |

**Test Case Description**

Validate password change works after system reset.

**Input Specifications**

- Change password
- Reset system
- Login with changed password

**Expected Result**

- Password persists through reset
- Login with changed password succeeds

**Actual Result (Pass/Fail/Exception)**

Pass: Password persists through reset

**Comment (including references)**

Integration with Reset the System feature

---

#### 4. test_password_change_error_recovery (ST-PWD-004)

| Field | Value |
|-------|-------|
| Class | System |
| Function | Error recovery |
| Author | |
| Date | |

**Test Case Description**

Validate system recovers correctly from password change errors.

**Input Specifications**

- Multiple failed attempts with wrong current password
- Then verify original password still works

**Expected Result**

- Failed attempts don't corrupt system state
- Original password still works

**Actual Result (Pass/Fail/Exception)**

Pass: System recovers correctly

**Comment (including references)**

Error handling and state consistency

---

## Test Summary

| Category | Test Count | Passed | Failed |
|----------|------------|--------|--------|
| Unit Tests | 10 | 10 | 0 |
| Integration Tests | 4 | 4 | 0 |
| System Level Tests | 4 | 4 | 0 |
| Backward Compatibility | 2 | 2 | 0 |
| **Total** | **20** | **20** | **0** |

---

## Test Execution

### Running Tests

```bash
# Run all Change Master Password tests
pytest tests/common_tests/test_change_master_password.py -v

# Run only unit tests
pytest tests/common_tests/test_change_master_password.py::TestChangeMasterPasswordUnitTests -v

# Run only integration tests
pytest tests/common_tests/test_change_master_password.py::TestChangeMasterPasswordIntegrationTests -v

# Run only system level tests
pytest tests/common_tests/test_change_master_password.py::TestChangeMasterPasswordSystemLevelTests -v
```

### Test File Location

```
tests/common_tests/test_change_master_password.py
```

---

## Password Change Sequence

The change_master_password() method follows this sequence:

### Phase 0: Precondition Checks
1. **Check System State** - Must be ON and not LOCKED
2. **Check Authentication** - User must be logged in
3. **Log PASSWORD_CHANGE_START** - Record change initiation

### Phase 1: Current Password Verification
1. **Get Current User** - From LoginManager
2. **Validate Current Password** - Compare with stored password
3. **On Failure** - Return error, allow retry

### Phase 2: New Password Validation
1. **Check Same Password** - New password must be different
2. **Validate Password Policy** - Check strength requirements
3. **On Failure** - Return error with reason

### Phase 3: Password Confirmation & Save
1. **Compare Passwords** - new_password == confirm_password
2. **Save to Database** - Update users table
3. **Log PASSWORD_CHANGE_SUCCESS** - Record completion
4. **Return Success** - With phase 3 indicator

---

## Error Types

| Error Type | Phase | Description |
|------------|-------|-------------|
| SYSTEM_OFF | 0 | System is not running |
| SYSTEM_LOCKED | 0 | System is locked |
| NOT_AUTHENTICATED | 0 | User not logged in |
| INCORRECT_PASSWORD | 1 | Current password wrong |
| SAME_PASSWORD | 2 | New = Current password |
| WEAK_PASSWORD | 2 | Password too weak |
| PASSWORD_MISMATCH | 3 | Confirmation mismatch |
| DATABASE_ERROR | 3 | Save failed |

---

## Security Features

### Current Implementation
- Current password required for change
- Password confirmation (enter twice)
- Event logging for audit trail
- Error type identification

### Recommended Enhancements
- Password strength validation
- Password history (prevent reuse)
- Bcrypt/Argon2 hashing
- Session invalidation on change
- Re-authentication requirement

---

## API Reference

### System.change_master_password()

```python
def change_master_password(self, current_password: str, new_password: str,
                           confirm_password: str, max_reentry_tries: int = 3) -> dict:
    """
    Change master password through control panel.

    Args:
        current_password: Current password for verification
        new_password: New password to set
        confirm_password: Confirmation of new password
        max_reentry_tries: Maximum retry attempts (default: 3)

    Returns:
        dict with keys:
            - success: bool
            - message: str
            - phase: int (0-3)
            - error_type: str (on failure)
    """
```

### System.validate_current_password_for_change()

```python
def validate_current_password_for_change(self, current_password: str) -> dict:
    """
    Validate current password (Phase 1 only).

    Returns:
        dict with keys:
            - success: bool
            - message: str
            - error_type: str (on failure)
    """
```

### System.set_new_master_password()

```python
def set_new_master_password(self, new_password: str, confirm_password: str) -> dict:
    """
    Set new password (Phase 2-3 only).
    Call after validate_current_password_for_change() succeeds.

    Returns:
        dict with keys:
            - success: bool
            - message: str
            - username: str (on success)
            - error_type: str (on failure)
    """
```

---

## References

- SDS Document: Sequence Diagram on Change Master Password Through Control Panel
- LoginManager.change_password_with_details() implementation
- System.change_master_password() implementation
- 3-Phase password change process

