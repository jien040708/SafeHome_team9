# III. Unit Tests

## 1. External Communication Management

### A. Control Panel Management

#### 1. ControlPanelLoginPresenter (Control Panel Login)

##### A. attempt_login() (handling login from Control Panel)

###### a. test_missing_credentials_triggers_warning (UT-LP-001)

| Field | Value |
|-------|-------|
| Class | ControlPanelLoginPresenter |
| Method | attempt_login() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that attempting login without providing both user ID and password triggers an appropriate warning message.

**Input Specifications**
- User ID: "" (empty string)
- Password: "pw" (any value)

**Expected Result**
```python
LoginOutcome(
    success=False,
    alert_level="warning",
    alert_title="Input Required",
    alert_message="Please enter both User ID and Password"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure outcome with warning level
- Pass: Alert message requests both credentials
- Pass: No system call is made

**Comment**

Input validation at the presenter layer prevents unnecessary system calls. Part of the Presenter pattern implementation introduced in Phase 2.

---

###### b. test_success_navigates_to_main_menu (UT-LP-002)

| Field | Value |
|-------|-------|
| Class | ControlPanelLoginPresenter |
| Method | attempt_login() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that successful login results in navigation to the MainMenu screen.

**Input Specifications**
- User ID: "user"
- Password: "pw"
- System returns: `{"success": True}`

**Expected Result**
```python
LoginOutcome(
    success=True,
    navigate_to="MainMenu"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success outcome
- Pass: navigate_to field is set to "MainMenu"

**Comment**

Presenter encapsulates navigation logic, separating UI flow from business logic.

---

###### c. test_locked_with_remaining_time_sets_status (UT-LP-003)

| Field | Value |
|-------|-------|
| Class | ControlPanelLoginPresenter |
| Method | attempt_login() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that when an account is locked with remaining time, the presenter formats an appropriate user-friendly message with time remaining.

**Input Specifications**
- System returns: `{"locked": True, "remaining_time": 90, "message": "Locked due to attempts"}`

**Expected Result**
```python
LoginOutcome(
    success=False,
    status_text="Account locked. Try again in 1 minutes 30 seconds",
    status_color="red",
    alert_level="error",
    alert_title="Account Locked"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Remaining time is formatted as minutes and seconds
- Pass: Status color is red
- Pass: Alert level is error

**Comment**

Presenter handles time formatting for user-friendly display. Implements time-based unlock feedback.

---

###### d. test_general_failure_with_attempts_shows_message (UT-LP-004)

| Field | Value |
|-------|-------|
| Class | ControlPanelLoginPresenter |
| Method | attempt_login() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that failed login attempts display remaining attempts to the user.

**Input Specifications**
- System returns: `{"success": False, "tries": 2, "remaining": 1}`

**Expected Result**
```python
LoginOutcome(
    success=False,
    status_text="Login failed. Remaining attempts: 1",
    status_color="red",
    alert_level="error",
    alert_title="Login Failed",
    alert_message="Incorrect password.\n\nFailed attempts: 2\nRemaining attempts: 1"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Status text shows remaining attempts
- Pass: Alert message includes both failed and remaining counts

**Comment**

User feedback for failed login attempts helps prevent account lockout through awareness.

---

#### 2. ControlPanelSettingsPresenter (Control Panel Settings Configuration)

##### A. save_settings() (handling settings save from Control Panel)

###### a. test_rejects_non_numeric_values (UT-SP-001)

| Field | Value |
|-------|-------|
| Class | ControlPanelSettingsPresenter |
| Method | save_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that the presenter rejects non-numeric values for time fields.

**Input Specifications**
- monitoring_phone: "911"
- homeowner_phone: "010"
- lock_time: "abc" (invalid)
- alarm_delay: "5"

**Expected Result**
```python
SettingsOutcome(
    success=False,
    alert_level="error",
    message="Invalid input. Please enter valid numbers for time fields."
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns error outcome
- Pass: Message indicates invalid input

**Comment**

Input validation at presenter layer prevents invalid data from reaching business logic.

---

###### b. test_rejects_negative_values (UT-SP-002)

| Field | Value |
|-------|-------|
| Class | ControlPanelSettingsPresenter |
| Method | save_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that the presenter rejects negative values for timing fields.

**Input Specifications**
- monitoring_phone: "911"
- homeowner_phone: "010"
- lock_time: "-1" (negative)
- alarm_delay: "0"

**Expected Result**
```python
SettingsOutcome(
    success=False,
    alert_level="error",
    message="Timing values cannot be negative."
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns error outcome for negative values
- Pass: Appropriate validation message

**Comment**

Business rule: Timing values must be non-negative.

---

###### c. test_successful_save_invokes_system (UT-SP-003)

| Field | Value |
|-------|-------|
| Class | ControlPanelSettingsPresenter |
| Method | save_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that valid settings are successfully passed to the system layer.

**Input Specifications**
- monitoring_phone: "911"
- homeowner_phone: "010"
- lock_time: "30"
- alarm_delay: "60"

**Expected Result**
```python
SettingsOutcome(
    success=True,
    alert_level="info",
    message="System settings saved successfully!"
)
```

System receives:
```python
{
    'monitoring_phone': '911',
    'homeowner_phone': '010',
    'lock_time': 30,
    'alarm_delay': 60
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success outcome
- Pass: System method called with correct parameters
- Pass: Integer conversion performed correctly

**Comment**

Presenter handles type conversion from string to integer for time fields.

---

#### 3. ControlPanelChangePasswordPresenter (Control Panel Password Management)

##### A. change_password() (handling password change from Control Panel)

###### a. test_mismatched_passwords_return_error (UT-CPP-001)

| Field | Value |
|-------|-------|
| Class | ControlPanelChangePasswordPresenter |
| Method | change_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that presenter-level validation catches mismatched passwords before calling system.

**Input Specifications**
- current_password: "old"
- new_password: "new-1"
- confirm_password: "new-2" (mismatch)

**Expected Result**
```python
ChangePasswordOutcome(
    success=False,
    message="New passwords do not match!",
    alert_level="error"
)
```
- System method is NOT called

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns error outcome
- Pass: No system call made

**Comment**

Early validation at presenter layer prevents unnecessary system calls. Test file: test_change_password_presenter.py:21

---

###### b. test_short_password_rejected (UT-CPP-002)

| Field | Value |
|-------|-------|
| Class | ControlPanelChangePasswordPresenter |
| Method | change_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that presenter validates minimum password length.

**Input Specifications**
- min_length: 4 (default)
- new_password: "123" (only 3 characters)
- confirm_password: "123"

**Expected Result**
```python
ChangePasswordOutcome(
    success=False,
    message="Password must be at least 4 characters long.",
    alert_level="error"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns error for short password
- Pass: No system call made

**Comment**

Password policy enforcement at presenter layer. Test file: test_change_password_presenter.py:28

---

###### c. test_successful_change_returns_info (UT-CPP-003)

| Field | Value |
|-------|-------|
| Class | ControlPanelChangePasswordPresenter |
| Method | change_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that successful password change through presenter returns appropriate outcome.

**Input Specifications**
- current_password: "old"
- new_password: "1234"
- confirm_password: "1234"
- System returns: True

**Expected Result**
```python
ChangePasswordOutcome(
    success=True,
    message="Password changed successfully!",
    alert_level="info"
)
```
- System called with: ("old", "1234")

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success outcome with info level
- Pass: System method called correctly

**Comment**

Presenter translates boolean system response into structured outcome. Test file: test_change_password_presenter.py:35

---

#### 4. ControlPanelResetPresenter (Control Panel System Reset)

##### A. perform_reset() (handling system reset from Control Panel)

###### a. test_perform_reset_success (UT-RP-001)

| Field | Value |
|-------|-------|
| Class | ControlPanelResetPresenter |
| Method | perform_reset() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that the presenter correctly handles successful system reset.

**Input Specifications**
- System reset returns: `{"success": True, "message": "Reset complete", "phase": 3}`

**Expected Result**
```python
ResetOutcome(
    success=True,
    alert_level="info",
    alert_title="Success",
    alert_message="Reset complete",
    phase=3
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success outcome
- Pass: Alert level is info
- Pass: Phase information preserved

**Comment**

Presenter translates system response into UI-appropriate format.

---

### B. Web Interface Management

#### 1. WebLoginPresenter (Web Browser Login - 2FA)

##### A. validate_first_password() (handling first password validation from Web)

###### a. test_first_password_missing_username (UT-WL-001)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that attempting to validate first password without username triggers validation error.

**Input Specifications**
- username: "" (empty string)
- password: "password123"

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    message="Username and password are required"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure outcome
- Pass: Appropriate error message

**Comment**

Input validation at the presenter layer prevents unnecessary system calls. Web interface uses 2-factor authentication (first password + second password/PIN).

---

###### b. test_first_password_missing_password (UT-WL-002)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that attempting to validate first password without password triggers validation error.

**Input Specifications**
- username: "admin"
- password: "" (empty string)

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    message="Username and password are required"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure outcome
- Pass: Appropriate error message

**Comment**

Prevents submission of incomplete credentials.

---

###### c. test_first_password_success (UT-WL-003)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that successful first password validation returns success.

**Input Specifications**
- username: "admin"
- password: "password123"
- System returns: `{"success": True}`

**Expected Result**
```python
WebLoginOutcome(
    success=True,
    message="First password correct"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success outcome
- Pass: User proceeds to second password input

**Comment**

First step of 2-factor authentication for web interface.

---

###### d. test_first_password_locked_with_remaining_time (UT-WL-004)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that locked account with remaining time returns appropriate information.

**Input Specifications**
- username: "admin"
- password: "wrong"
- Account locked with remaining_time: 30 seconds

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    locked=True,
    remaining_time=30,
    tries=5,
    message="Account locked due to too many attempts"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns locked status
- Pass: Includes remaining time information

**Comment**

Time-based account locking for security.

---

###### e. test_first_password_system_off (UT-WL-005)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that first password validation fails when system is OFF.

**Input Specifications**
- System state: OFF
- Valid credentials provided

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    system_off=True,
    message="System is currently off"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure with system_off flag
- Pass: Appropriate error message

**Comment**

Precondition: System must be ON for login.

---

###### f. test_first_password_system_locked (UT-WL-006)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that first password validation fails when system is LOCKED.

**Input Specifications**
- System state: LOCKED
- Valid credentials provided

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    system_locked=True,
    message="System is locked by administrator"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure with system_locked flag

**Comment**

System-level lock prevents all logins.

---

###### g. test_first_password_failed_with_attempts (UT-WL-007)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that failed first password validation includes attempt information.

**Input Specifications**
- username: "admin"
- password: "wrong"
- tries: 2, remaining: 3

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    message="Incorrect first password",
    tries=2,
    remaining=3
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure with attempt counts

**Comment**

User feedback helps prevent account lockout.

---

###### h. test_first_password_system_not_available (UT-WL-008)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies proper error handling when system is not available.

**Input Specifications**
- system: None

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    message="System not available"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns appropriate error

**Comment**

Graceful degradation when system unavailable.

---

##### B. validate_second_password() (handling second password/PIN validation from Web)

###### a. test_second_password_missing (UT-WL2-001)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_second_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that empty second password triggers validation error.

**Input Specifications**
- username: "admin"
- second_password: "" (empty string)

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    message="Second password is required"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure outcome

**Comment**

Second factor of 2FA must be provided.

---

###### b. test_second_password_success (UT-WL2-002)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_second_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that successful second password validation completes login.

**Input Specifications**
- username: "admin"
- second_password: "pin1234"
- System returns: `{"success": True}`

**Expected Result**
```python
WebLoginOutcome(
    success=True,
    message="Login successful",
    redirect_url="/dashboard"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success with redirect URL

**Comment**

Completes 2-factor authentication and redirects to dashboard.

---

###### c. test_second_password_locked_with_remaining_time (UT-WL2-003)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_second_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies handling of locked account during second password validation.

**Input Specifications**
- Account locked with remaining_time: 45 seconds

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    locked=True,
    remaining_time=45,
    tries=5
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns locked status with remaining time

**Comment**

Account can be locked at either authentication stage.

---

###### d. test_second_password_system_off (UT-WL2-004)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_second_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that second password validation fails when system is OFF.

**Input Specifications**
- System state: OFF

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    system_off=True
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure with system_off flag

**Comment**

System state checked at each authentication stage.

---

###### e. test_second_password_system_locked (UT-WL2-005)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_second_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that second password validation fails when system is LOCKED.

**Input Specifications**
- System state: LOCKED

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    system_locked=True
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure with system_locked flag

**Comment**

System-level lock enforced at all authentication stages.

---

###### f. test_second_password_failed_with_attempts (UT-WL2-006)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_second_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies failed second password validation includes attempt information.

**Input Specifications**
- second_password: "wrong"
- tries: 1, remaining: 4

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    message="Incorrect second password",
    tries=1,
    remaining=4
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure with attempt counts

**Comment**

Separate attempt tracking for each authentication factor.

---

###### g. test_second_password_system_not_available (UT-WL2-007)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_second_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies error handling when system unavailable during second password validation.

**Input Specifications**
- system: None

**Expected Result**
```python
WebLoginOutcome(
    success=False,
    message="System not available"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns appropriate error

**Comment**

Consistent error handling across both authentication stages.

---

###### h. test_calls_login_manager_with_correct_interface (UT-WL2-008)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter |
| Method | validate_first_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that presenter calls LoginManager with 'web_browser' interface.

**Input Specifications**
- username: "admin"
- password: "password123"

**Expected Result**
- LoginManager.validate_first_password called with interface='web_browser'

**Actual Result (Pass/Fail/Exception)**
- Pass: Correct interface parameter passed

**Comment**

Ensures proper logging and tracking of web-based logins. Test file: test_web_login_presenter.py:162

---

#### 2. WebSettingsPresenter (Web Browser Settings Configuration)

##### A. update_settings() (handling settings update from Web)

###### a. test_invalid_monitoring_phone_format (UT-WS-001)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that invalid monitoring phone format is rejected.

**Input Specifications**
- monitoring_service_phone: "invalid"
- homeowner_phone: "123-456-7890"

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    message="Validation failed",
    errors=["Invalid monitoring service phone format (recommended: XXX-XXX-XXXX)"]
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns validation error

**Comment**

Phone number format validation at presenter layer.

---

###### b. test_invalid_homeowner_phone_format (UT-WS-002)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that invalid homeowner phone format is rejected.

**Input Specifications**
- monitoring_service_phone: "123-456-7890"
- homeowner_phone: "abc"

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    message="Validation failed",
    errors=["Invalid homeowner phone format (recommended: XXX-XXX-XXXX)"]
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns validation error

**Comment**

Consistent phone validation for both fields.

---

###### c. test_valid_phone_formats_accepted (UT-WS-003)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that valid phone formats are accepted (standard and flexible).

**Input Specifications**
- Standard format: "111-222-3333"
- Flexible format: "(123) 456-7890", "+1-234-567-8900"

**Expected Result**
- Both formats accepted successfully

**Actual Result (Pass/Fail/Exception)**
- Pass: Standard XXX-XXX-XXXX format accepted
- Pass: Flexible format with at least 3 chars accepted

**Comment**

Flexible validation supports international formats while maintaining basic validation.

---

###### d. test_zero_lock_time_rejected (UT-WS-004)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that zero lock time is rejected.

**Input Specifications**
- system_lock_time: 0

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    errors=["System lock time must be greater than 0"]
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns validation error

**Comment**

Business rule: Lock time must be positive.

---

###### e. test_negative_lock_time_rejected (UT-WS-005)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that negative lock time is rejected.

**Input Specifications**
- system_lock_time: -5

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    errors=["System lock time must be greater than 0"]
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns validation error

**Comment**

Prevents invalid negative values.

---

###### f. test_negative_alarm_delay_rejected (UT-WS-006)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that negative alarm delay is rejected.

**Input Specifications**
- alarm_delay_time: -10

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    errors=["Alarm delay time must be non-negative"]
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns validation error

**Comment**

Alarm delay can be 0 (immediate) but not negative.

---

###### g. test_invalid_lock_time_type (UT-WS-007)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that invalid lock time type is rejected.

**Input Specifications**
- system_lock_time: "abc"

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    errors=["System lock time must be a valid number"]
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns type validation error

**Comment**

Type checking prevents non-numeric values.

---

###### h. test_invalid_alarm_delay_type (UT-WS-008)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that invalid alarm delay type is rejected.

**Input Specifications**
- alarm_delay_time: "xyz"

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    errors=["Alarm delay time must be a valid number"]
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns type validation error

**Comment**

Consistent type validation for time fields.

---

###### i. test_multiple_validation_errors (UT-WS-009)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that multiple validation errors are collected.

**Input Specifications**
- monitoring_service_phone: "invalid"
- homeowner_phone: "bad"
- system_lock_time: 0
- alarm_delay_time: -5

**Expected Result**
- At least 4 validation errors returned

**Actual Result (Pass/Fail/Exception)**
- Pass: All validation errors collected

**Comment**

Comprehensive validation feedback improves user experience.

---

###### j. test_successful_settings_update (UT-WS-010)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies successful settings update with valid inputs.

**Input Specifications**
- monitoring_service_phone: "111-222-3333"
- homeowner_phone: "444-555-6666"
- system_lock_time: 30
- alarm_delay_time: 60

**Expected Result**
```python
WebSettingsOutcome(
    success=True,
    message="Settings updated successfully"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success outcome
- Pass: Settings persisted to database

**Comment**

Complete update flow with all parameters.

---

###### k. test_partial_update_only_phones (UT-WS-011)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies partial update of only phone numbers.

**Input Specifications**
- monitoring_service_phone: "123-456-7890"
- homeowner_phone: "098-765-4321"
- (time values not provided)

**Expected Result**
- Update succeeds with only phones modified

**Actual Result (Pass/Fail/Exception)**
- Pass: Partial update succeeds
- Pass: Only phone fields updated

**Comment**

Supports selective field updates.

---

###### l. test_partial_update_only_times (UT-WS-012)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies partial update of only time values.

**Input Specifications**
- system_lock_time: 45
- alarm_delay_time: 90
- (phone numbers not provided)

**Expected Result**
- Update succeeds with only times modified

**Actual Result (Pass/Fail/Exception)**
- Pass: Partial update succeeds
- Pass: Only time fields updated

**Comment**

Flexible update mechanism for different field combinations.

---

###### m. test_update_converts_string_times_to_int (UT-WS-013)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that string time values are converted to integers.

**Input Specifications**
- system_lock_time: "30" (string)
- alarm_delay_time: "60" (string)

**Expected Result**
- Values converted to integers: 30, 60

**Actual Result (Pass/Fail/Exception)**
- Pass: String to int conversion successful
- Pass: Values stored as integers

**Comment**

Type coercion handles web form data (strings).

---

###### n. test_save_failure_returns_error (UT-WS-014)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies handling of database save failure.

**Input Specifications**
- Valid inputs provided
- Database save fails

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    message="Failed to save settings"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns failure outcome

**Comment**

Graceful error handling for persistence failures.

---

###### o. test_system_not_available (UT-WS-015)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies error handling when system is not available.

**Input Specifications**
- system: None

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    message="System not available"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns appropriate error

**Comment**

System availability check prevents null reference errors.

---

###### p. test_get_settings_system_not_available (UT-WS-016)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | get_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies get_settings error handling when system unavailable.

**Input Specifications**
- system: None

**Expected Result**
```python
WebSettingsOutcome(
    success=False,
    message="System not available"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns appropriate error

**Comment**

Consistent error handling across all operations.

---

###### q. test_get_settings_success (UT-WS-017)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | get_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies successful retrieval of current settings.

**Input Specifications**
- System and ConfigurationManager available

**Expected Result**
```python
WebSettingsOutcome(
    success=True,
    message="Settings retrieved successfully"
)
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success outcome

**Comment**

Retrieval operation for GET requests.

---

###### r. test_empty_update_succeeds (UT-WS-018)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that update with no parameters succeeds.

**Input Specifications**
- No parameters provided

**Expected Result**
- Operation succeeds (no-op)

**Actual Result (Pass/Fail/Exception)**
- Pass: Empty update succeeds

**Comment**

Handles edge case of empty update request.

---

###### s. test_zero_alarm_delay_accepted (UT-WS-019)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter |
| Method | update_settings() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that zero alarm delay is accepted (immediate alarm).

**Input Specifications**
- alarm_delay_time: 0

**Expected Result**
- Update succeeds

**Actual Result (Pass/Fail/Exception)**
- Pass: Zero alarm delay accepted

**Comment**

Zero is valid for alarm delay (immediate activation), unlike lock time which must be positive.

---

## 2. Surveillance

### A. Camera Management

#### 1. X

##### A. X

###### a. X

---

## 3. Security

### A. Sensor Management

#### 1. X

##### A. X

###### a. X

---

### B. Alarm Processing

#### 1. X

##### A. X

###### a. X

---

## 4. Configuration and Data Management

### A. Log Management

#### 1. X

##### A. X

###### a. X

---

### B. LoginManager (Backend Authentication Logic)

#### 1. LoginManager class

##### A. login_with_details() (detailed login response)

###### a. test_login_with_details_success (UT-LM-001)

| Field | Value |
|-------|-------|
| Class | LoginManager |
| Method | login_with_details() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that successful login returns detailed information including username and access level.

**Input Specifications**
- Username: "admin"
- Password: "1234"
- Interface: "control_panel"
- Account is not locked
- Credentials are correct

**Expected Result**
```python
{
    'success': True,
    'message': 'Login successful',
    'username': 'admin',
    'access_level': 1
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns success with detailed information
- Pass: Username and access level included in response

**Comment**

Enhanced login method provides additional information for UI display and logging. Replaces boolean-only return value.

---

###### b. test_locked_account_with_auto_unlock (UT-LM-002)

| Field | Value |
|-------|-------|
| Class | LoginManager |
| Method | login_with_details() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that the system automatically unlocks an account when the configured lock duration has elapsed.

**Input Specifications**
- User account locked at timestamp T
- system_lock_time = 30 seconds (default)
- Current time = T + 31 seconds
- User attempts login

**Expected Result**
- Account is automatically unlocked
- Login proceeds with credential validation
- If credentials correct, login succeeds

**Actual Result (Pass/Fail/Exception)**
- Pass: Account automatically unlocked after duration
- Pass: Console message: "Account 'admin' automatically unlocked after 30 seconds"
- Pass: Successful login after auto-unlock

**Comment**

Implements time-based automatic unlock feature. Uses _check_and_unlock_if_time_passed() internal method.

---

###### c. test_locked_account_returns_remaining_time (UT-LM-003)

| Field | Value |
|-------|-------|
| Class | LoginManager |
| Method | login_with_details() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that attempting to login with a locked account returns the remaining lock time.

**Input Specifications**
- User account locked at timestamp T
- system_lock_time = 30 seconds
- Current time = T + 10 seconds
- Remaining time = 20 seconds

**Expected Result**
```python
{
    'success': False,
    'message': 'Account is locked. Please try again in 20 seconds.',
    'locked': True,
    'tries': 5,
    'remaining_time': 20
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns locked status with remaining time
- Pass: Remaining time calculated correctly (30 - 10 = 20)

**Comment**

Provides user feedback on when they can attempt login again.

---

### C. System Integration (Login & Configuration)

#### 1. System class - Login Integration

##### A. login_with_details() (system-level login)

###### a. test_login_system_off (UT-SYS-Login-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | login_with_details() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that login attempt fails when system is OFF.

**Input Specifications**
- System state: SystemState.OFF
- Valid credentials provided

**Expected Result**
```python
{
    'success': False,
    'message': 'System is off. Please turn on the system first.',
    'system_off': True
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Login fails with system_off flag
- Pass: Appropriate error message returned

**Comment**

Precondition check: System must be ON for login.

---

###### b. test_login_system_locked (UT-SYS-Login-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | login_with_details() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that login attempt fails when system is LOCKED.

**Input Specifications**
- System state: SystemState.LOCKED
- Valid credentials provided

**Expected Result**
```python
{
    'success': False,
    'message': 'System is locked. Please contact administrator.',
    'system_locked': True
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Login fails with system_locked flag
- Pass: Appropriate error message returned

**Comment**

System-level lock prevents all logins regardless of user credentials.

---

#### 2. System class - Configuration Integration

##### A. configure_system_setting() (system-level configuration)

###### a. test_configure_system_setting (UT-SYS-Config-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | configure_system_setting() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that system settings can be configured through the System class.

**Input Specifications**
- System is ON
- monitoring_phone: "111-222-3333"
- homeowner_phone: "444-555-6666"
- lock_time: 45
- alarm_delay: 90

**Expected Result**
- Method returns True
- Settings are persisted to database
- SettingsService is invoked correctly

**Actual Result (Pass/Fail/Exception)**
- Pass: Returns True
- Pass: Settings saved successfully
- Pass: Database contains updated values

**Comment**

Uses SettingsService internally for separation of concerns.

---

### D. Password Management

#### 1. System class - Password Change

##### A. change_master_password() (system-level password change)

###### a. test_change_password_success (UT-PWD-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that password change succeeds with correct inputs through all 3 phases.

**Input Specifications**
- User is logged in (admin/1234)
- current_password: '1234'
- new_password: 'newpass5678'
- confirm_password: 'newpass5678'

**Expected Result**
```python
{
    'success': True,
    'message': 'Password changed successfully',
    'phase': 3
}
```
- Password is updated in database
- User remains logged in

**Actual Result (Pass/Fail/Exception)**
- Pass: Password change succeeds with phase 3
- Pass: New password works for subsequent login

**Comment**

Complete 3-phase password change flow. Test file: test_change_master_password.py:68

---

###### b. test_change_password_wrong_current (UT-PWD-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that password change fails with wrong current password at Phase 1.

**Input Specifications**
- User is logged in
- current_password: 'wrongpass' (incorrect)
- new_password: 'newpass5678'
- confirm_password: 'newpass5678'

**Expected Result**
```python
{
    'success': False,
    'phase': 1,
    'error_type': 'INCORRECT_PASSWORD',
    'message': 'Current password is incorrect'
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Fails at Phase 1 with INCORRECT_PASSWORD error
- Pass: Password remains unchanged

**Comment**

Phase 1 validation prevents unauthorized password changes. Test file: test_change_master_password.py:91

---

###### c. test_change_password_mismatch (UT-PWD-003)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that password change fails when new passwords don't match at Phase 3.

**Input Specifications**
- User is logged in
- current_password: '1234'
- new_password: 'newpass1111'
- confirm_password: 'newpass2222' (mismatch)

**Expected Result**
```python
{
    'success': False,
    'phase': 3,
    'error_type': 'PASSWORD_MISMATCH',
    'message': 'New passwords do not match'
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Fails at Phase 3 with PASSWORD_MISMATCH error
- Pass: Password remains unchanged

**Comment**

Phase 3 confirmation prevents accidental password changes. Test file: test_change_master_password.py:108

---

###### d. test_change_password_same_as_current (UT-PWD-004)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that password change fails when new password is same as current.

**Input Specifications**
- current_password: '1234'
- new_password: '1234'
- confirm_password: '1234'

**Expected Result**
```python
{
    'success': False,
    'error_type': 'SAME_PASSWORD',
    'message': 'New password must be different from current password'
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Fails with SAME_PASSWORD error
- Pass: Password remains unchanged

**Comment**

Security policy requires different password. Test file: test_change_master_password.py:125

---

###### e. test_change_password_not_authenticated (UT-PWD-005)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that password change fails when user is not authenticated.

**Input Specifications**
- User is NOT logged in
- Attempt to change password

**Expected Result**
```python
{
    'success': False,
    'phase': 0,
    'error_type': 'NOT_AUTHENTICATED',
    'message': 'Authentication required to change password'
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Fails at Phase 0 with NOT_AUTHENTICATED error

**Comment**

Precondition: User must be logged in. Test file: test_change_master_password.py:141

---

###### f. test_change_password_system_off (UT-PWD-006)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that password change fails when system is OFF.

**Input Specifications**
- System is OFF
- Attempt to change password

**Expected Result**
```python
{
    'success': False,
    'error_type': 'SYSTEM_OFF',
    'message': 'System is off. Please turn on the system first.'
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Fails with SYSTEM_OFF error

**Comment**

Precondition: System must be ON. Test file: test_change_master_password.py:162

---

###### g. test_change_password_system_locked (UT-PWD-007)

| Field | Value |
|-------|-------|
| Class | System |
| Method | change_master_password() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.0 |

**Test Case Description**

Verifies that password change fails when system is LOCKED.

**Input Specifications**
- System is LOCKED
- Attempt to change password

**Expected Result**
```python
{
    'success': False,
    'error_type': 'SYSTEM_LOCKED',
    'message': 'System is locked. Please contact administrator.'
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: Fails with SYSTEM_LOCKED error

**Comment**

Precondition: System must not be locked. Test file: test_change_master_password.py:182

---

### E. System Power Management

#### 1. System class - Power On

##### A. turn_on() (system power on)

###### a. test_turn_on_from_off_state (UT-SYS-ON-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that calling turn_on() when system is OFF results in successful initialization and system state becomes READY.

**Input Specifications**
- System is in OFF state (initial state after constructor)

**Expected Result**
- turn_on() returns True
- system_state becomes SystemState.READY
- All core components are initialized (not None):
  - StorageManager
  - ConfigurationManager
  - LoginManager
  - LogManager
  - SystemController
  - SecuritySystem
  - CameraController
  - Siren

**Actual Result (Pass/Fail/Exception)**
- Pass: turn_on() returns True
- Pass: system_state is SystemState.READY
- Pass: All components initialized

**Comment**

Complete system initialization sequence as specified in SDS page 50. Includes initialization of AuthService and SettingsService (new in Phase 2).

---

###### b. test_turn_on_when_already_running (UT-SYS-ON-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_on() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that calling turn_on() when system is already running returns False and does not reinitialize components.

**Input Specifications**
- System is already in READY state (turn_on() called previously)

**Expected Result**
- turn_on() returns False
- system_state remains READY
- No exception is raised
- Console message: "System is already Ready"

**Actual Result (Pass/Fail/Exception)**
- Pass: turn_on() returns False
- Pass: system_state remains READY
- Pass: Components are not reinitialized

**Comment**

Error handling prevents double initialization.

---

#### 2. System class - Power Off

##### A. turn_off() (system power off)

###### a. test_turn_off_from_ready_state (UT-SYS-OFF-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that calling turn_off() when system is READY results in successful shutdown following the complete sequence.

**Input Specifications**
- System is in READY state (after turn_on() was called)

**Expected Result**
- turn_off() returns True
- system_state becomes SystemState.OFF
- Shutdown sequence executed:
  1. Configuration saved
  2. Sensors deactivated
  3. Cameras disabled
  4. Siren deactivated
  5. User logged out
  6. SYSTEM_SHUTDOWN event logged
  7. Database disconnected

**Actual Result (Pass/Fail/Exception)**
- Pass: turn_off() returns True
- Pass: system_state is SystemState.OFF
- Pass: All shutdown steps completed

**Comment**

Complete shutdown sequence as specified in SDS page 51. Test file: test_system_power_flow.py:115

---

###### b. test_turn_off_when_already_off (UT-SYS-OFF-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that calling turn_off() when system is already OFF returns False and does not cause errors.

**Input Specifications**
- System is already in OFF state

**Expected Result**
- turn_off() returns False
- system_state remains OFF
- No exception is raised
- Console message: "System is already off"

**Actual Result (Pass/Fail/Exception)**
- Pass: turn_off() returns False
- Pass: system_state remains OFF
- Pass: No exception raised

**Comment**

Prevents redundant shutdown operations. Test file: test_system_power_flow.py:133

---

###### c. test_turn_off_deactivates_sensors (UT-SYS-OFF-003)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that all sensors are deactivated during shutdown (Phase 2 of turn_off sequence).

**Input Specifications**
- System is running with multiple sensors registered

**Expected Result**
- All sensors are deactivated
- turn_off() returns True
- Console message: "N sensors deactivated"

**Actual Result (Pass/Fail/Exception)**
- Pass: All sensors deactivated
- Pass: Each sensor's deactivate() method called

**Comment**

Phase 2 of Turn the System Off sequence. Test file: test_system_power_flow.py:115

---

###### d. test_turn_off_disables_cameras (UT-SYS-OFF-004)

| Field | Value |
|-------|-------|
| Class | System |
| Method | turn_off() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that all cameras are disabled during shutdown (Phase 3 of turn_off sequence).

**Input Specifications**
- System is running with CameraController and cameras added

**Expected Result**
- CameraController.disable_all_camera() is called
- All cameras in SystemController are deactivated
- turn_off() returns True

**Actual Result (Pass/Fail/Exception)**
- Pass: Camera controller disabled flag is True
- Pass: All camera objects deactivated

**Comment**

Phase 3 of Turn the System Off sequence. Test file: test_system_power_flow.py:115

---

#### 3. System class - System Reset

##### A. reset() (system reset)

###### a. test_reset_from_ready_state (UT-SYS-RST-001)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that calling reset() from READY state succeeds and system returns to READY state.

**Input Specifications**
- System is in READY state (after turn_on() was called)

**Expected Result**
```python
{
    'success': True,
    'message': 'System reset successfully',
    'phase': 3
}
```
- system_state becomes SystemState.READY

**Actual Result (Pass/Fail/Exception)**
- Pass: reset() returns success with phase 3
- Pass: system_state is SystemState.READY
- Pass: Reset = Turn Off + Turn On

**Comment**

Reset executes turn_off() followed by turn_on(). Enhanced return format includes phase information.

---

###### b. test_reset_when_system_off (UT-SYS-RST-002)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that calling reset() when system is OFF returns error and does not proceed.

**Input Specifications**
- System is in OFF state

**Expected Result**
```python
{
    'success': False,
    'message': 'Cannot reset: System is not running',
    'phase': 0
}
```

**Actual Result (Pass/Fail/Exception)**
- Pass: reset() returns False with phase 0
- Pass: Error message indicates system not running

**Comment**

Precondition: System must be ON to perform reset.

---

###### c. test_reset_preserves_settings (UT-SYS-RST-003)

| Field | Value |
|-------|-------|
| Class | System |
| Method | reset() |
| Author | Minseok Jo |
| Date | 2025-11-25 |
| Version | 2.0.1 |

**Test Case Description**

Verifies that settings are preserved after reset.

**Input Specifications**
- System is in READY state
- Settings modified:
  - lock_time = 45
  - alarm_delay = 90

**Expected Result**
- reset() succeeds
- Modified settings are preserved after reset
- lock_time remains 45
- alarm_delay remains 90

**Actual Result (Pass/Fail/Exception)**
- Pass: reset() returns success
- Pass: Settings values preserved

**Comment**

Settings are saved during Turn Off (Phase 1) and loaded during Turn On (Phase 2).

---

## 5. Branch Coverage

### A. File Level

(To be completed with coverage data)

---

### B. Class Level

(To be completed with coverage data)

---

### C. Method Level

(To be completed with coverage data)

---

## Summary

### Test Coverage by Category

1. **External Communication Management - Control Panel**: 12 tests
   - Login (Presenter): 4 tests
   - Settings (Presenter): 3 tests
   - Password Change (Presenter): 3 tests
   - Reset (Presenter): 1 test
   - System Integration: 1 test

2. **Configuration and Data Management**: 20 tests
   - LoginManager: 3 tests
   - System Integration (Login): 2 tests
   - System Integration (Config): 1 test
   - Password Management: 7 tests
   - Power Management: 10 tests

**Total Unit Tests Documented: 32 tests**

### Design Patterns

**Presenter Pattern** (Phase 2):
- **Presentation Logic** (Presenters): Input validation, formatting, UI flow
- **Business Logic** (System, Services): Authentication, authorization, state management
- **Data Access** (Managers): Database operations, persistence

### Benefits

1. **Testability**: Each layer can be tested independently
2. **Maintainability**: Clear separation of concerns
3. **Flexibility**: UI can change without affecting business logic
4. **Type Safety**: Structured outcomes with dataclasses

---

## References

### Test Files
- `tests/domain/test_login_presenter.py`
- `tests/domain/test_settings_presenter.py`
- `tests/domain/test_change_password_presenter.py`
- `tests/domain/test_power_presenter.py`
- `tests/domain/test_reset_presenter.py`
- `tests/domain/test_system_power_flow.py`
- `tests/common_tests/test_change_master_password.py`

### Source Files
- `domain/system.py`
- `auth/login_manager.py`
- `domain/services/login_presenter.py`
- `domain/services/change_password_presenter.py`
- `domain/services/settings_presenter.py`
- `domain/services/power_presenter.py`
- `domain/services/reset_presenter.py`

### Documentation
- SDS (Software Design Specification)
- WEB_LOGIN_README.md
- CHANGE_MASTER_PASSWORD_TEST_DOCUMENTATION.md
