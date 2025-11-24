# IV. Integration Tests

## A. Control Panel Login Process

### 1. test_control_panel_login_with_presenter_and_system (IT-CP-Login-001)

| Field | Value |
|-------|-------|
| Class | ControlPanelLoginPresenter, System, LoginManager, StorageManager |
| Function | Log onto the system via Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that ControlPanelLoginPresenter successfully coordinates with System and LoginManager to authenticate a user when valid credentials are provided.

**Input Specifications**
- Database has predefined username and password: "admin" and "1234"
- User ID: "admin"
- Password: "1234"

**Detailed Step**
1. Initialize System and call turn_on() to initialize all components including LoginManager and StorageManager.
2. Create ControlPanelLoginPresenter with reference to the System instance.
3. Call presenter.attempt_login() with "admin" as user_id and "1234" as password.
4. Presenter delegates to System.login_with_details() which internally calls LoginManager.login_with_details().
5. LoginManager validates credentials against StorageManager data.
6. System returns success response with navigation information.
7. Presenter transforms response into LoginOutcome dataclass.

**Expected Result**
- LoginOutcome.success equals True
- LoginOutcome.navigate_to equals "MainMenu"
- System.login_tries equals 0 after successful authentication
- User session is established in System

**Actual Result (Pass/Fail/Exception)**
- Pass: LoginOutcome.success equals True
- Pass: LoginOutcome.navigate_to equals "MainMenu"
- Pass: System.login_tries equals 0

**Comment (including references)**
Integration between Presenter layer and System/LoginManager layer. Validates the MVP pattern implementation introduced in Phase 2.

---

### 2. test_control_panel_login_lockout_integration (IT-CP-Login-002)

| Field | Value |
|-------|-------|
| Class | ControlPanelLoginPresenter, System, LoginManager |
| Function | Account lockout after failed attempts |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that the integration between ControlPanelLoginPresenter and LoginManager correctly handles account lockout after maximum failed attempts.

**Input Specifications**
- Database has predefined username: "admin" with password: "1234"
- Incorrect password attempts: 5 times with "wrongpw"
- system_lock_time: 30 seconds

**Detailed Step**
1. Initialize System with turn_on().
2. Create ControlPanelLoginPresenter with System reference.
3. Attempt login 5 times with incorrect password "wrongpw".
4. On each failed attempt, LoginManager increments tries counter.
5. After 5th failed attempt, LoginManager locks the account.
6. 6th attempt returns locked status with remaining_time.
7. Presenter formats the lock message with time remaining.

**Expected Result**
- After 5 failed attempts, account is locked
- LoginOutcome.success equals False
- LoginOutcome.status_color equals "red"
- LoginOutcome.alert_level equals "error"
- LoginOutcome.alert_title equals "Account Locked"
- remaining_time is included in status_text

**Actual Result (Pass/Fail/Exception)**
- Pass: Account locked after 5 attempts
- Pass: LoginOutcome contains lock information
- Pass: Time remaining is formatted correctly

**Comment (including references)**
Tests the complete lockout flow from UI through business logic. Implements time-based unlock feature.

---

## B. Control Panel Settings Configuration

### 1. test_settings_save_integration (IT-CP-Settings-001)

| Field | Value |
|-------|-------|
| Class | ControlPanelSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Save system settings via Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that ControlPanelSettingsPresenter correctly saves settings through the System layer and persists them to the database.

**Input Specifications**
- monitoring_phone: "911"
- homeowner_phone: "010-1234-5678"
- lock_time: "45"
- alarm_delay: "90"

**Detailed Step**
1. Initialize System with turn_on().
2. Create ControlPanelSettingsPresenter with System reference.
3. Call presenter.save_settings() with the input values.
4. Presenter validates inputs (non-numeric check, negative check).
5. Presenter converts string time values to integers.
6. Presenter calls System.configure_system_setting().
7. System delegates to SettingsService which updates ConfigurationManager.
8. ConfigurationManager persists changes via StorageManager.

**Expected Result**
- SettingsOutcome.success equals True
- SettingsOutcome.alert_level equals "info"
- ConfigurationManager.lock_time equals 45
- ConfigurationManager.alarm_delay equals 90
- Database contains updated values

**Actual Result (Pass/Fail/Exception)**
- Pass: SettingsOutcome.success equals True
- Pass: Settings persisted correctly
- Pass: Values retrievable after save

**Comment (including references)**
Tests complete settings flow from UI validation through persistence layer.

---

## C. Control Panel Password Change

### 1. test_password_change_full_flow_integration (IT-CP-PWD-001)

| Field | Value |
|-------|-------|
| Class | ControlPanelChangePasswordPresenter, System, LoginManager, StorageManager |
| Function | Change master password via Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete password change flow from ControlPanelChangePasswordPresenter through System to database persistence.

**Input Specifications**
- User is logged in as "admin"
- current_password: "1234"
- new_password: "newpass5678"
- confirm_password: "newpass5678"

**Detailed Step**
1. Initialize System and login with admin/1234.
2. Create ControlPanelChangePasswordPresenter with System reference.
3. Call presenter.change_password() with current, new, and confirm passwords.
4. Presenter validates: passwords match, minimum length met.
5. Presenter calls System.change_master_password().
6. System executes 3-phase password change:
   - Phase 1: Verify current password
   - Phase 2: Validate new password rules
   - Phase 3: Confirm and save
7. StorageManager updates password in database.

**Expected Result**
- ChangePasswordOutcome.success equals True
- ChangePasswordOutcome.message equals "Password changed successfully!"
- New password works for subsequent login
- Old password no longer works

**Actual Result (Pass/Fail/Exception)**
- Pass: Password change succeeds
- Pass: New password authenticates correctly
- Pass: Old password rejected

**Comment (including references)**
Validates complete 3-phase password change flow. Test file: test_change_master_password.py

---

## D. Web Login Process (2FA)

### 1. test_web_login_two_factor_integration (IT-Web-Login-001)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter, System, LoginManager, StorageManager |
| Function | Two-factor authentication via Web interface |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete 2-factor authentication flow for web login, including first password and second password/PIN validation.

**Input Specifications**
- username: "admin"
- first_password: "password123"
- second_password: "pin1234"

**Detailed Step**
1. Initialize System with turn_on().
2. Create WebLoginPresenter with System reference.
3. Call presenter.validate_first_password() with username and first_password.
4. Presenter calls LoginManager.validate_first_password() with interface='web_browser'.
5. LoginManager validates first credential against StorageManager.
6. On success, call presenter.validate_second_password() with username and second_password.
7. LoginManager validates second credential (PIN).
8. On success, user session is established and redirect URL is returned.

**Expected Result**
- First password validation: WebLoginOutcome.success equals True
- Second password validation: WebLoginOutcome.success equals True
- WebLoginOutcome.redirect_url equals "/dashboard"
- User session established in System

**Actual Result (Pass/Fail/Exception)**
- Pass: First password validated successfully
- Pass: Second password validated successfully
- Pass: Redirect to dashboard

**Comment (including references)**
Tests complete 2FA flow for web interface. Implements separate tracking for each authentication factor.

---

### 2. test_web_login_lockout_across_factors (IT-Web-Login-002)

| Field | Value |
|-------|-------|
| Class | WebLoginPresenter, System, LoginManager |
| Function | Account lockout during 2FA |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that account lockout works correctly across both authentication factors in 2FA.

**Input Specifications**
- username: "admin"
- Incorrect first_password attempts: 5 times
- system_lock_time: 30 seconds

**Detailed Step**
1. Initialize System with turn_on().
2. Create WebLoginPresenter.
3. Attempt first password validation 5 times with wrong password.
4. Verify account gets locked after 5 failed attempts.
5. Verify that even correct credentials are rejected while locked.
6. Verify remaining_time is returned in response.

**Expected Result**
- Account locked after 5 failed first password attempts
- WebLoginOutcome.locked equals True
- WebLoginOutcome.remaining_time shows seconds until unlock
- Correct credentials rejected while locked

**Actual Result (Pass/Fail/Exception)**
- Pass: Account locked correctly
- Pass: Remaining time calculated
- Pass: Locked state enforced

**Comment (including references)**
Tests lockout behavior specific to web 2FA authentication.

---

## E. Web Settings Configuration

### 1. test_web_settings_update_integration (IT-Web-Settings-001)

| Field | Value |
|-------|-------|
| Class | WebSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Update system settings via Web interface |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that WebSettingsPresenter correctly validates and saves settings through the System layer.

**Input Specifications**
- monitoring_service_phone: "111-222-3333"
- homeowner_phone: "444-555-6666"
- system_lock_time: 30
- alarm_delay_time: 60

**Detailed Step**
1. Initialize System with turn_on().
2. Create WebSettingsPresenter with System reference.
3. Call presenter.update_settings() with all parameters.
4. Presenter validates:
   - Phone number formats
   - Lock time > 0
   - Alarm delay >= 0
   - Type checking for numeric fields
5. Presenter calls System.configure_system_setting().
6. Settings are persisted to database.

**Expected Result**
- WebSettingsOutcome.success equals True
- WebSettingsOutcome.message equals "Settings updated successfully"
- All values persisted correctly
- No validation errors

**Actual Result (Pass/Fail/Exception)**
- Pass: Settings saved successfully
- Pass: Values retrievable via get_settings()

**Comment (including references)**
Tests web-specific validation rules including phone format validation.

---

## F. System Power Management

### 1. test_system_power_cycle_integration (IT-SYS-Power-001)

| Field | Value |
|-------|-------|
| Class | System, StorageManager, ConfigurationManager, LoginManager, SecuritySystem, CameraController |
| Function | Complete power cycle (On -> Off -> On) |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that System correctly initializes and shuts down all components during power cycle.

**Input Specifications**
- System starts in OFF state
- Modified settings: lock_time=45, alarm_delay=90

**Detailed Step**
1. Create System instance (starts in OFF state).
2. Call turn_on() - Phase 1: Initialize all components.
3. Verify all managers and controllers are initialized.
4. Modify settings: lock_time=45, alarm_delay=90.
5. Call turn_off() - Execute shutdown sequence:
   - Save configuration
   - Deactivate sensors
   - Disable cameras
   - Deactivate siren
   - Logout user
   - Log SYSTEM_SHUTDOWN
   - Disconnect database
6. Call turn_on() again.
7. Verify settings are preserved.

**Expected Result**
- First turn_on(): Returns True, state becomes READY
- turn_off(): Returns True, state becomes OFF
- Second turn_on(): Returns True, state becomes READY
- Settings preserved: lock_time=45, alarm_delay=90

**Actual Result (Pass/Fail/Exception)**
- Pass: Power cycle completes successfully
- Pass: All components initialized/shutdown correctly
- Pass: Settings preserved across cycle

**Comment (including references)**
Tests complete initialization and shutdown sequences as specified in SDS pages 50-51.

---

### 2. test_system_reset_integration (IT-SYS-Reset-001)

| Field | Value |
|-------|-------|
| Class | System, ControlPanelResetPresenter, all managers |
| Function | System reset via Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that system reset correctly executes turn_off followed by turn_on and preserves settings.

**Input Specifications**
- System is running (READY state)
- User is logged in
- Custom settings configured

**Detailed Step**
1. Initialize System and turn_on().
2. Login as admin.
3. Configure custom settings.
4. Create ControlPanelResetPresenter.
5. Call presenter.perform_reset().
6. Presenter calls System.reset().
7. System executes turn_off() then turn_on().
8. Verify system returns to READY state.
9. Verify settings are preserved.
10. Verify user is logged out (must re-authenticate).

**Expected Result**
- ResetOutcome.success equals True
- ResetOutcome.phase equals 3
- System state equals READY
- Settings preserved
- User session cleared (logged out)

**Actual Result (Pass/Fail/Exception)**
- Pass: Reset completes successfully
- Pass: Settings preserved
- Pass: User logged out

**Comment (including references)**
Tests reset as combination of turn_off and turn_on sequences.

---

## G. LoginManager Backend Integration

### 1. test_login_manager_auto_unlock_integration (IT-LM-001)

| Field | Value |
|-------|-------|
| Class | LoginManager, StorageManager, ConfigurationManager |
| Function | Automatic account unlock after time elapsed |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that LoginManager automatically unlocks an account when the configured lock duration has elapsed.

**Input Specifications**
- Account locked at timestamp T
- system_lock_time: 30 seconds
- Current time: T + 31 seconds

**Detailed Step**
1. Initialize LoginManager with StorageManager and ConfigurationManager.
2. Simulate 5 failed login attempts to lock account.
3. Record lock timestamp.
4. Advance time by 31 seconds (mock time).
5. Attempt login with correct credentials.
6. LoginManager checks _check_and_unlock_if_time_passed().
7. Account is automatically unlocked.
8. Login proceeds and succeeds.

**Expected Result**
- Account automatically unlocked after 30 seconds
- Console message: "Account 'admin' automatically unlocked after 30 seconds"
- Login succeeds with correct credentials

**Actual Result (Pass/Fail/Exception)**
- Pass: Auto-unlock triggered
- Pass: Login succeeds after unlock

**Comment (including references)**
Tests time-based automatic unlock feature implementation.

---

---

# V. System Level Tests

## A. Log onto the System through Control Panel

### 1. test_control_panel_login_success_flow (ST-CP-Login-001)

| Field | Value |
|-------|-------|
| Class | ControlPanel, ControlPanelLoginPresenter, System, LoginManager, StorageManager |
| Function | Log onto the system through Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete login flow from Control Panel UI through all system layers to successful authentication.

**Input Specifications**
- ControlPanel receives user_id "admin" and password "1234"
- StorageManager contains admin credentials ("admin", "1234")

**Detailed Step**
1. Seed StorageManager with admin user and password "1234".
2. Initialize System with turn_on().
3. Initialize ControlPanel connected to System.
4. Simulate user entering "admin" as user_id.
5. Simulate user entering "1234" as password.
6. Simulate pressing Login button.
7. ControlPanel creates ControlPanelLoginPresenter.
8. Presenter.attempt_login() is called.
9. System.login_with_details() processes authentication.
10. LoginManager validates against StorageManager.
11. Success response flows back through layers.
12. ControlPanel displays success and navigates to MainMenu.

**Expected Result**
- System.login_with_details() returns success
- ControlPanel displays "Login successful"
- ControlPanel navigates to MainMenu screen
- User session is established
- Login attempts counter reset to 0

**Actual Result (Pass/Fail/Exception)**
- Pass: Login succeeds through all layers
- Pass: UI displays success message
- Pass: Navigation to MainMenu

**Comment (including references)**
End-to-end test of Control Panel login. Validates complete MVP pattern flow.

---

### 2. test_control_panel_login_lockout_and_unlock_flow (ST-CP-Login-002)

| Field | Value |
|-------|-------|
| Class | ControlPanel, ControlPanelLoginPresenter, System, LoginManager |
| Function | Account lockout and time-based unlock via Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete lockout flow including time-based automatic unlock through Control Panel.

**Input Specifications**
- 5 failed login attempts with wrong password
- system_lock_time: 30 seconds
- Wait 31 seconds, then try with correct password

**Detailed Step**
1. Initialize full system stack.
2. Attempt login 5 times with wrong password "wrongpw".
3. Verify ControlPanel displays remaining attempts on each failure.
4. After 5th attempt, verify account locked message displayed.
5. Verify ControlPanel shows "Account locked. Try again in X seconds".
6. Wait for lock_time to elapse (30 seconds).
7. Attempt login with correct password "1234".
8. Verify account auto-unlocks and login succeeds.
9. Verify ControlPanel navigates to MainMenu.

**Expected Result**
- Failed attempts show remaining count
- Account locked after 5 attempts
- Lock message shows remaining time
- Auto-unlock after 30 seconds
- Successful login after unlock

**Actual Result (Pass/Fail/Exception)**
- Pass: Lockout enforced
- Pass: Time-based unlock works
- Pass: Successful login after unlock

**Comment (including references)**
Tests complete lockout lifecycle including automatic unlock feature.

---

## B. Configure System Settings through Control Panel

### 1. test_control_panel_settings_save_flow (ST-CP-Settings-001)

| Field | Value |
|-------|-------|
| Class | ControlPanel, ControlPanelSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Configure system settings through Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete settings configuration flow from Control Panel UI through persistence.

**Input Specifications**
- User is logged in
- monitoring_phone: "911"
- homeowner_phone: "010-1234-5678"
- lock_time: "45"
- alarm_delay: "90"

**Detailed Step**
1. Initialize System and login as admin.
2. Navigate to Settings screen in ControlPanel.
3. Enter monitoring_phone: "911".
4. Enter homeowner_phone: "010-1234-5678".
5. Enter lock_time: "45".
6. Enter alarm_delay: "90".
7. Press Save button.
8. ControlPanel creates ControlPanelSettingsPresenter.
9. Presenter validates all inputs.
10. Presenter converts strings to appropriate types.
11. System.configure_system_setting() is called.
12. ConfigurationManager updates values.
13. StorageManager persists to database.
14. ControlPanel displays success message.

**Expected Result**
- Validation passes for all inputs
- Settings saved successfully
- ControlPanel displays "System settings saved successfully!"
- Values persist in database
- Values retrievable after system restart

**Actual Result (Pass/Fail/Exception)**
- Pass: All validations pass
- Pass: Settings persisted
- Pass: Success message displayed

**Comment (including references)**
End-to-end settings configuration test.

---

### 2. test_control_panel_settings_validation_errors (ST-CP-Settings-002)

| Field | Value |
|-------|-------|
| Class | ControlPanel, ControlPanelSettingsPresenter, System |
| Function | Settings validation error handling |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that invalid settings inputs are properly rejected with appropriate error messages.

**Input Specifications**
- lock_time: "abc" (non-numeric)
- alarm_delay: "-5" (negative)

**Detailed Step**
1. Initialize System and login as admin.
2. Navigate to Settings screen.
3. Enter invalid lock_time: "abc".
4. Enter invalid alarm_delay: "-5".
5. Press Save button.
6. Presenter validates inputs.
7. Validation fails with multiple errors.
8. ControlPanel displays error messages.
9. Settings are NOT saved.

**Expected Result**
- Validation fails
- Error message: "Invalid input. Please enter valid numbers for time fields."
- Settings not modified
- User remains on Settings screen

**Actual Result (Pass/Fail/Exception)**
- Pass: Validation rejects invalid inputs
- Pass: Error messages displayed
- Pass: No changes persisted

**Comment (including references)**
Tests presenter-level validation preventing invalid data.

---

## C. Change Password through Control Panel

### 1. test_control_panel_password_change_success (ST-CP-PWD-001)

| Field | Value |
|-------|-------|
| Class | ControlPanel, ControlPanelChangePasswordPresenter, System, LoginManager, StorageManager |
| Function | Change master password through Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete password change flow from Control Panel through all phases.

**Input Specifications**
- User logged in as admin with password "1234"
- current_password: "1234"
- new_password: "newpass5678"
- confirm_password: "newpass5678"

**Detailed Step**
1. Initialize System and login with admin/1234.
2. Navigate to Change Password screen.
3. Enter current password: "1234".
4. Enter new password: "newpass5678".
5. Enter confirm password: "newpass5678".
6. Press Change Password button.
7. Presenter validates passwords match and length.
8. System.change_master_password() executes 3 phases:
   - Phase 1: Verify current password
   - Phase 2: Validate new password rules
   - Phase 3: Confirm and save
9. Password updated in database.
10. ControlPanel displays success message.
11. Logout and login with new password succeeds.

**Expected Result**
- All 3 phases complete successfully
- ControlPanel displays "Password changed successfully!"
- Old password no longer works
- New password authenticates correctly

**Actual Result (Pass/Fail/Exception)**
- Pass: Password change completes
- Pass: New password works
- Pass: Old password rejected

**Comment (including references)**
Tests complete 3-phase password change flow through UI.

---

### 2. test_control_panel_password_change_mismatch (ST-CP-PWD-002)

| Field | Value |
|-------|-------|
| Class | ControlPanel, ControlPanelChangePasswordPresenter, System |
| Function | Password change with mismatched confirmation |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that password change fails when new password and confirmation don't match.

**Input Specifications**
- current_password: "1234"
- new_password: "newpass1111"
- confirm_password: "newpass2222" (mismatch)

**Detailed Step**
1. Initialize System and login.
2. Navigate to Change Password screen.
3. Enter current password: "1234".
4. Enter new password: "newpass1111".
5. Enter confirm password: "newpass2222".
6. Press Change Password button.
7. Presenter validates passwords do not match.
8. Error returned before calling System.
9. ControlPanel displays error message.
10. Password remains unchanged.

**Expected Result**
- Validation fails at presenter level
- Error message: "New passwords do not match!"
- System.change_master_password() is NOT called
- Original password still works

**Actual Result (Pass/Fail/Exception)**
- Pass: Mismatch detected
- Pass: Error displayed
- Pass: Password unchanged

**Comment (including references)**
Tests early validation at presenter layer preventing unnecessary system calls.

---

## D. Log onto the System through Web Browser (2FA)

### 1. test_web_login_two_factor_success (ST-Web-Login-001)

| Field | Value |
|-------|-------|
| Class | WebBrowser, WebLoginPresenter, System, LoginManager, StorageManager |
| Function | Two-factor authentication through Web Browser |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete 2-factor authentication flow through the web interface.

**Input Specifications**
- username: "admin"
- first_password: "password123"
- second_password: "pin1234"

**Detailed Step**
1. Initialize System with turn_on().
2. Open WebBrowser and navigate to login page.
3. Enter username: "admin".
4. Enter first password: "password123".
5. Click "Next" or "Continue".
6. WebLoginPresenter.validate_first_password() called.
7. First password validated successfully.
8. Web page transitions to second password input.
9. Enter second password/PIN: "pin1234".
10. Click "Login".
11. WebLoginPresenter.validate_second_password() called.
12. Second password validated successfully.
13. User redirected to dashboard.
14. Session established.

**Expected Result**
- First password validation succeeds
- UI transitions to second factor input
- Second password validation succeeds
- Redirect to "/dashboard"
- User session active

**Actual Result (Pass/Fail/Exception)**
- Pass: Both factors validated
- Pass: Redirect successful
- Pass: Session established

**Comment (including references)**
End-to-end test of 2FA web login flow.

---

### 2. test_web_login_system_off_rejected (ST-Web-Login-002)

| Field | Value |
|-------|-------|
| Class | WebBrowser, WebLoginPresenter, System |
| Function | Web login rejected when system is OFF |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that web login is rejected when the system is in OFF state.

**Input Specifications**
- System is OFF (not initialized)
- Valid credentials provided

**Detailed Step**
1. Create System instance but do NOT call turn_on().
2. Open WebBrowser and navigate to login page.
3. Enter valid username and password.
4. Click login.
5. WebLoginPresenter checks system state.
6. System state is OFF.
7. Login rejected with appropriate message.
8. User remains on login page.

**Expected Result**
- WebLoginOutcome.success equals False
- WebLoginOutcome.system_off equals True
- Error message: "System is currently off"
- No redirect occurs

**Actual Result (Pass/Fail/Exception)**
- Pass: Login rejected
- Pass: System off message displayed
- Pass: User stays on login page

**Comment (including references)**
Precondition validation: System must be ON for login.

---

## E. Configure System Settings through Web Browser

### 1. test_web_settings_full_update_flow (ST-Web-Settings-001)

| Field | Value |
|-------|-------|
| Class | WebBrowser, WebSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Full settings update through Web Browser |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate the complete settings configuration flow through the web interface.

**Input Specifications**
- User is logged in via web
- monitoring_service_phone: "111-222-3333"
- homeowner_phone: "444-555-6666"
- system_lock_time: 30
- alarm_delay_time: 60

**Detailed Step**
1. Initialize System and complete web 2FA login.
2. Navigate to Settings page in web interface.
3. Enter monitoring_service_phone: "111-222-3333".
4. Enter homeowner_phone: "444-555-6666".
5. Enter system_lock_time: 30.
6. Enter alarm_delay_time: 60.
7. Click "Save Settings".
8. WebSettingsPresenter.update_settings() called.
9. Presenter validates all fields.
10. System.configure_system_setting() called.
11. Settings persisted to database.
12. Success message displayed.
13. Verify settings via get_settings().

**Expected Result**
- All validations pass
- WebSettingsOutcome.success equals True
- Success message: "Settings updated successfully"
- Values persisted and retrievable

**Actual Result (Pass/Fail/Exception)**
- Pass: Settings saved
- Pass: Success displayed
- Pass: Values persist

**Comment (including references)**
End-to-end web settings configuration test.

---

### 2. test_web_settings_multiple_validation_errors (ST-Web-Settings-002)

| Field | Value |
|-------|-------|
| Class | WebBrowser, WebSettingsPresenter, System |
| Function | Multiple validation errors in web settings |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate that multiple validation errors are collected and displayed together.

**Input Specifications**
- monitoring_service_phone: "invalid"
- homeowner_phone: "bad"
- system_lock_time: 0
- alarm_delay_time: -5

**Detailed Step**
1. Initialize System and login via web.
2. Navigate to Settings page.
3. Enter all invalid values.
4. Click "Save Settings".
5. WebSettingsPresenter validates all fields.
6. Multiple validation errors collected:
   - Invalid monitoring phone format
   - Invalid homeowner phone format
   - Lock time must be > 0
   - Alarm delay must be >= 0
7. All errors returned in response.
8. Web page displays all errors.
9. Settings NOT saved.

**Expected Result**
- WebSettingsOutcome.success equals False
- WebSettingsOutcome.errors contains 4+ errors
- All errors displayed to user
- No changes persisted

**Actual Result (Pass/Fail/Exception)**
- Pass: All errors collected
- Pass: Comprehensive error display
- Pass: No persistence

**Comment (including references)**
Tests comprehensive validation feedback for better user experience.

---

## F. System Power On/Off through Control Panel

### 1. test_system_turn_on_full_initialization (ST-SYS-ON-001)

| Field | Value |
|-------|-------|
| Class | ControlPanel, System, StorageManager, ConfigurationManager, LoginManager, SecuritySystem, CameraController, Siren |
| Function | System turn on through Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate complete system initialization when turning on through Control Panel.

**Input Specifications**
- System is in OFF state
- ControlPanel power button pressed

**Detailed Step**
1. System starts in OFF state.
2. User presses Power On button on ControlPanel.
3. ControlPanel calls System.turn_on().
4. System initialization sequence:
   - Initialize StorageManager (connect to database)
   - Initialize ConfigurationManager (load settings)
   - Initialize LoginManager (setup authentication)
   - Initialize LogManager (setup logging)
   - Initialize SystemController
   - Initialize SecuritySystem (sensors)
   - Initialize CameraController
   - Initialize Siren
   - Initialize AuthService
   - Initialize SettingsService
5. System state changes to READY.
6. ControlPanel displays "System Ready".
7. All components operational.

**Expected Result**
- System.turn_on() returns True
- System.system_state equals READY
- All components initialized (not None)
- ControlPanel shows ready status

**Actual Result (Pass/Fail/Exception)**
- Pass: Initialization complete
- Pass: All components ready
- Pass: UI updated

**Comment (including references)**
Complete system initialization as per SDS page 50.

---

### 2. test_system_turn_off_full_shutdown (ST-SYS-OFF-001)

| Field | Value |
|-------|-------|
| Class | ControlPanel, System, all managers and controllers |
| Function | System turn off through Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate complete system shutdown sequence when turning off through Control Panel.

**Input Specifications**
- System is in READY state
- User is logged in
- Sensors and cameras are active

**Detailed Step**
1. System is running with user logged in.
2. Some sensors and cameras are active.
3. User presses Power Off button on ControlPanel.
4. ControlPanel calls System.turn_off().
5. System shutdown sequence:
   - Phase 1: Save configuration to database
   - Phase 2: Deactivate all sensors
   - Phase 3: Disable all cameras
   - Phase 4: Deactivate siren
   - Phase 5: Logout current user
   - Phase 6: Log SYSTEM_SHUTDOWN event
   - Phase 7: Disconnect database
6. System state changes to OFF.
7. ControlPanel displays "System Off".

**Expected Result**
- System.turn_off() returns True
- System.system_state equals OFF
- All sensors deactivated
- All cameras disabled
- Siren off
- User logged out
- Configuration saved

**Actual Result (Pass/Fail/Exception)**
- Pass: Shutdown complete
- Pass: All components deactivated
- Pass: Data persisted

**Comment (including references)**
Complete shutdown sequence as per SDS page 51.

---

### 3. test_system_reset_through_control_panel (ST-SYS-Reset-001)

| Field | Value |
|-------|-------|
| Class | ControlPanel, ControlPanelResetPresenter, System, all components |
| Function | System reset through Control Panel |
| Author | Minseok Jo |
| Date | 2025-11-25 |

**Test Case Description**

Validate complete system reset flow through Control Panel.

**Input Specifications**
- System is running
- User is logged in
- Custom settings: lock_time=45, alarm_delay=90

**Detailed Step**
1. System running with custom settings configured.
2. User logged in as admin.
3. User selects Reset option in ControlPanel menu.
4. ControlPanel shows confirmation dialog.
5. User confirms reset.
6. ControlPanel creates ControlPanelResetPresenter.
7. Presenter calls System.reset().
8. System.reset() executes:
   - turn_off() (saves settings)
   - turn_on() (reloads settings)
9. System returns to READY state.
10. User is logged out (session cleared).
11. Settings are preserved.
12. ControlPanel shows login screen.

**Expected Result**
- Reset completes with phase 3
- System in READY state
- Settings preserved (lock_time=45, alarm_delay=90)
- User logged out
- ControlPanel on login screen

**Actual Result (Pass/Fail/Exception)**
- Pass: Reset successful
- Pass: Settings preserved
- Pass: User logged out

**Comment (including references)**
Reset combines turn_off and turn_on sequences with data preservation.

---

## Summary

### Integration Tests

| Test ID | Category | Description |
|---------|----------|-------------|
| IT-CP-Login-001 | Control Panel Login | Presenter + System + LoginManager integration |
| IT-CP-Login-002 | Control Panel Login | Account lockout integration |
| IT-CP-Settings-001 | Control Panel Settings | Settings save through all layers |
| IT-CP-PWD-001 | Control Panel Password | Password change full flow |
| IT-Web-Login-001 | Web Login | Two-factor authentication integration |
| IT-Web-Login-002 | Web Login | Lockout across authentication factors |
| IT-Web-Settings-001 | Web Settings | Settings update integration |
| IT-SYS-Power-001 | System Power | Complete power cycle integration |
| IT-SYS-Reset-001 | System Reset | Reset integration with settings preservation |
| IT-LM-001 | LoginManager | Auto-unlock integration |

**Total Integration Tests: 10**

### System Level Tests

| Test ID | Category | Description |
|---------|----------|-------------|
| ST-CP-Login-001 | Control Panel Login | Complete login success flow |
| ST-CP-Login-002 | Control Panel Login | Lockout and time-based unlock |
| ST-CP-Settings-001 | Control Panel Settings | Full settings configuration |
| ST-CP-Settings-002 | Control Panel Settings | Validation error handling |
| ST-CP-PWD-001 | Control Panel Password | Password change success |
| ST-CP-PWD-002 | Control Panel Password | Password mismatch handling |
| ST-Web-Login-001 | Web Login | 2FA success flow |
| ST-Web-Login-002 | Web Login | System OFF rejection |
| ST-Web-Settings-001 | Web Settings | Full settings update |
| ST-Web-Settings-002 | Web Settings | Multiple validation errors |
| ST-SYS-ON-001 | System Power | Full initialization |
| ST-SYS-OFF-001 | System Power | Full shutdown |
| ST-SYS-Reset-001 | System Power | Reset through Control Panel |

**Total System Level Tests: 13**

---

## References

### Test Files
- `tests/integration/test_control_panel_login.py`
- `tests/integration/test_control_panel_settings.py`
- `tests/integration/test_control_panel_password.py`
- `tests/integration/test_web_login.py`
- `tests/integration/test_web_settings.py`
- `tests/integration/test_system_power.py`
- `tests/system/test_control_panel_flows.py`
- `tests/system/test_web_flows.py`
- `tests/system/test_system_power_flows.py`

### Source Files
- `domain/system.py`
- `auth/login_manager.py`
- `domain/services/login_presenter.py`
- `domain/services/change_password_presenter.py`
- `domain/services/settings_presenter.py`
- `domain/services/web_login_presenter.py`
- `domain/services/web_settings_presenter.py`

### Documentation
- SDS (Software Design Specification) pages 47, 50-51
- UNIT_TEST_DOCUMENTATION_UPDATED.md
