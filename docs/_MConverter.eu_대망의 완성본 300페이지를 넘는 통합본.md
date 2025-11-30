I.  **Overview**

<!-- -->

1.  **Introduction**

> This document contains detailed implementation and testing information
> for Team 3\'s SafeHome Security System project, fulfilling the
> requirements outlined in the Software Requirements Specification (SRS)
> and the Software Design Specification (SDS). We implemented the core
> logic and security domain using Python, and structured the user
> interface and system simulation environment as follows:
>
> • Web Interface: Implemented using a Flask backend for logic and plain
> \> HTML for the user interface presentation.
>
> • Virtual Devices: Established simulated devices (Virtual Devices) \>
> based on the documentation provided by the TA (Teaching Assistant) \>
> to emulate sensor and control panel functionalities.
>
> We performed comprehensive quality assurance by utilizing Pytest for
> all test levels, including Unit, Integration, and System-Level
> testing, supplemented by Coverage analysis to ensure structural test
> completeness. This report provides full traceability from the design
> models to the code implementation, detailing the test procedures,
> environments, and final results.

2.  **Goal**

> The primary goals of this implementation and testing phase were to:
>
> • Software Engineering Principles: Exercise core software engineering
> \> principles in the implementation phase, maintaining traceability \>
> from the SRS (Requirements) and SDS (Design).
>
> • Testing Proficiency: Demonstrate proficiency in performing software
> \> testing at various levels: Unit Tests, Integration Tests, and \>
> System-Level Tests.
>
> • Program Documentation: Learn how to properly document the software
> \> implementation, including the use of comments in code, generating
> \> user manuals (if required), and producing this structured testing
> \> report.
>
> • Quality Assurance: Achieve a high level of code coverage, \>
> specifically focusing on branch coverage, to certify the quality \>
> and robustness of the implemented system logic.

# II. Class Diagram {#ii.-class-diagram .unnumbered}

## Class Diagram of Login Module

![](media/image1.png){width="6.267716535433071in"
height="4.680555555555555in"}

## 2. Configure Feature Class Diagram {#configure-feature-class-diagram .unnumbered}

![](media/image2.png){width="6.267716535433071in"
height="3.7222222222222223in"}

## 3. System On/Off/Reset Feature Class Diagram {#system-onoffreset-feature-class-diagram .unnumbered}

![](media/image3.png){width="6.267716535433071in"
height="2.888888888888889in"}

## 4. Password Change Feature Class Diagram {#password-change-feature-class-diagram .unnumbered}

![](media/image4.png){width="6.267716535433071in" height="4.125in"}

# **III. Unit Tests** {#iii.-unit-tests .unnumbered}

## **1. External Communication Management** {#external-communication-management .unnumbered}

### **A. Control Panel Management** {#a.-control-panel-management .unnumbered}

#### **1. ControlPanelLoginPresenter (Control Panel Login)** {#controlpanelloginpresenter-control-panel-login .unnumbered}

##### **A. attempt_login() (handling login from Control Panel)** {#a.-attempt_login-handling-login-from-control-panel .unnumbered}

###### **a. test_missing_credentials_triggers_warning (UT-LP-001)** {#a.-test_missing_credentials_triggers_warning-ut-lp-001 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | ControlPanelLoginPresenter |
| Method  | attempt_login()            |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that attempting login without providing both user ID and
password triggers an appropriate warning message.

**Input Specifications**

• User ID: \"\" (empty string)

• Password: \"pw\" (any value)

**Expected Result**

LoginOutcome(  
success=False,  
alert_level=\"warning\",  
alert_title=\"Input Required\",  
alert_message=\"Please enter both User ID and Password\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure outcome with warning level

• Pass: Alert message requests both credentials

• Pass: No system call is made

**Comment**

Input validation at the presenter layer prevents unnecessary system
calls. Part of the Presenter pattern implementation introduced in Phase
2.

###### **b. test_success_navigates_to_main_menu (UT-LP-002)** {#b.-test_success_navigates_to_main_menu-ut-lp-002 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | ControlPanelLoginPresenter |
| Method  | attempt_login()            |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that successful login results in navigation to the MainMenu
screen.

**Input Specifications**

• User ID: \"user\"

• Password: \"pw\"

• System returns: \`{\"success\": True}\`

**Expected Result**

LoginOutcome(  
success=True,  
navigate_to=\"MainMenu\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success outcome

• Pass: navigate_to field is set to \"MainMenu\"

**Comment**

Presenter encapsulates navigation logic, separating UI flow from
business logic.

###### **c. test_locked_with_remaining_time_sets_status (UT-LP-003)** {#c.-test_locked_with_remaining_time_sets_status-ut-lp-003 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | ControlPanelLoginPresenter |
| Method  | attempt_login()            |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that when an account is locked with remaining time, the
presenter formats an appropriate user-friendly message with time
remaining.

**Input Specifications**

• System returns: \`{\"locked\": True, \"remaining_time\": 90,
\"message\": \"Locked due to attempts\"}\`

**Expected Result**

LoginOutcome(  
success=False,  
status_text=\"Account locked. Try again in 1 minutes 30 seconds\",  
status_color=\"red\",  
alert_level=\"error\",  
alert_title=\"Account Locked\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Remaining time is formatted as minutes and seconds

• Pass: Status color is red

• Pass: Alert level is error

**Comment**

Presenter handles time formatting for user-friendly display. Implements
time-based unlock feedback.

###### **d. test_general_failure_with_attempts_shows_message (UT-LP-004)** {#d.-test_general_failure_with_attempts_shows_message-ut-lp-004 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | ControlPanelLoginPresenter |
| Method  | attempt_login()            |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that failed login attempts display remaining attempts to the
user.

**Input Specifications**

• System returns: \`{\"success\": False, \"tries\": 2, \"remaining\":
1}\`

**Expected Result**

LoginOutcome(  
success=False,  
status_text=\"Login failed. Remaining attempts: 1\",  
status_color=\"red\",  
alert_level=\"error\",  
alert_title=\"Login Failed\",  
alert_message=\"Incorrect password.\n\nFailed attempts: 2\nRemaining
attempts: 1\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Status text shows remaining attempts

• Pass: Alert message includes both failed and remaining counts

**Comment**

User feedback for failed login attempts helps prevent account lockout
through awareness.

#### **2. ControlPanelSettingsPresenter (Control Panel Settings Configuration)** {#controlpanelsettingspresenter-control-panel-settings-configuration .unnumbered}

##### **A. save_settings() (handling settings save from Control Panel)** {#a.-save_settings-handling-settings-save-from-control-panel .unnumbered}

###### **a. test_rejects_non_numeric_values (UT-SP-001)** {#a.-test_rejects_non_numeric_values-ut-sp-001 .unnumbered}

|         |                               |
|---------|-------------------------------|
| Field   | Value                         |
| Class   | ControlPanelSettingsPresenter |
| Method  | save_settings()               |
| Author  | Minseok Jo                    |
| Date    | 2025-11-25                    |
| Version | 2.0.0                         |

**Test Case Description**

Verifies that the presenter rejects non-numeric values for time fields.

**Input Specifications**

• monitoring_phone: \"911\"

• homeowner_phone: \"010\"

• lock_time: \"abc\" (invalid)

• alarm_delay: \"5\"

**Expected Result**

SettingsOutcome(  
success=False,  
alert_level=\"error\",  
message=\"Invalid input. Please enter valid numbers for time fields.\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns error outcome

• Pass: Message indicates invalid input

**Comment**

Input validation at presenter layer prevents invalid data from reaching
business logic.

###### **b. test_rejects_negative_values (UT-SP-002)** {#b.-test_rejects_negative_values-ut-sp-002 .unnumbered}

|         |                               |
|---------|-------------------------------|
| Field   | Value                         |
| Class   | ControlPanelSettingsPresenter |
| Method  | save_settings()               |
| Author  | Minseok Jo                    |
| Date    | 2025-11-25                    |
| Version | 2.0.0                         |

**Test Case Description**

Verifies that the presenter rejects negative values for timing fields.

**Input Specifications**

• monitoring_phone: \"911\"

• homeowner_phone: \"010\"

• lock_time: \"-1\" (negative)

• alarm_delay: \"0\"

**Expected Result**

SettingsOutcome(  
success=False,  
alert_level=\"error\",  
message=\"Timing values cannot be negative.\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns error outcome for negative values

• Pass: Appropriate validation message

**Comment**

Business rule: Timing values must be non-negative.

###### **c. test_successful_save_invokes_system (UT-SP-003)** {#c.-test_successful_save_invokes_system-ut-sp-003 .unnumbered}

|         |                               |
|---------|-------------------------------|
| Field   | Value                         |
| Class   | ControlPanelSettingsPresenter |
| Method  | save_settings()               |
| Author  | Minseok Jo                    |
| Date    | 2025-11-25                    |
| Version | 2.0.0                         |

**Test Case Description**

Verifies that valid settings are successfully passed to the system
layer.

**Input Specifications**

• monitoring_phone: \"911\"

• homeowner_phone: \"010\"

• lock_time: \"30\"

• alarm_delay: \"60\"

**Expected Result**

SettingsOutcome(  
success=True,  
alert_level=\"info\",  
message=\"System settings saved successfully!\"  
)

System receives:

{  
\'monitoring_phone\': \'911\',  
\'homeowner_phone\': \'010\',  
\'lock_time\': 30,  
\'alarm_delay\': 60  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success outcome

• Pass: System method called with correct parameters

• Pass: Integer conversion performed correctly

**Comment**

Presenter handles type conversion from string to integer for time
fields.

#### **3. ControlPanelChangePasswordPresenter (Control Panel Password Management)** {#controlpanelchangepasswordpresenter-control-panel-password-management .unnumbered}

##### **A. change_password() (handling password change from Control Panel)** {#a.-change_password-handling-password-change-from-control-panel .unnumbered}

###### **a. test_mismatched_passwords_return_error (UT-CPP-001)** {#a.-test_mismatched_passwords_return_error-ut-cpp-001 .unnumbered}

|         |                                     |
|---------|-------------------------------------|
| Field   | Value                               |
| Class   | ControlPanelChangePasswordPresenter |
| Method  | change_password()                   |
| Author  | Minseok Jo                          |
| Date    | 2025-11-25                          |
| Version | 2.0.0                               |

**Test Case Description**

Verifies that presenter-level validation catches mismatched passwords
before calling system.

**Input Specifications**

• current_password: \"old\"

• new_password: \"new-1\"

• confirm_password: \"new-2\" (mismatch)

**Expected Result**

ChangePasswordOutcome(  
success=False,  
message=\"New passwords do not match!\",  
alert_level=\"error\"  
)

• System method is NOT called

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns error outcome

• Pass: No system call made

**Comment**

Early validation at presenter layer prevents unnecessary system calls.
Test file: test_change_password_presenter.py:21

###### **b. test_short_password_rejected (UT-CPP-002)** {#b.-test_short_password_rejected-ut-cpp-002 .unnumbered}

|         |                                     |
|---------|-------------------------------------|
| Field   | Value                               |
| Class   | ControlPanelChangePasswordPresenter |
| Method  | change_password()                   |
| Author  | Minseok Jo                          |
| Date    | 2025-11-25                          |
| Version | 2.0.0                               |

**Test Case Description**

Verifies that presenter validates minimum password length.

**Input Specifications**

• min_length: 4 (default)

• new_password: \"123\" (only 3 characters)

• confirm_password: \"123\"

**Expected Result**

ChangePasswordOutcome(  
success=False,  
message=\"Password must be at least 4 characters long.\",  
alert_level=\"error\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns error for short password

• Pass: No system call made

**Comment**

Password policy enforcement at presenter layer. Test file:
test_change_password_presenter.py:28

###### **c. test_successful_change_returns_info (UT-CPP-003)** {#c.-test_successful_change_returns_info-ut-cpp-003 .unnumbered}

|         |                                     |
|---------|-------------------------------------|
| Field   | Value                               |
| Class   | ControlPanelChangePasswordPresenter |
| Method  | change_password()                   |
| Author  | Minseok Jo                          |
| Date    | 2025-11-25                          |
| Version | 2.0.0                               |

**Test Case Description**

Verifies that successful password change through presenter returns
appropriate outcome.

**Input Specifications**

• current_password: \"old\"

• new_password: \"1234\"

• confirm_password: \"1234\"

• System returns: True

**Expected Result**

ChangePasswordOutcome(  
success=True,  
message=\"Password changed successfully!\",  
alert_level=\"info\"  
)

• System called with: (\"old\", \"1234\")

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success outcome with info level

• Pass: System method called correctly

**Comment**

Presenter translates boolean system response into structured outcome.
Test file: test_change_password_presenter.py:35

#### **4. ControlPanelResetPresenter (Control Panel System Reset)** {#controlpanelresetpresenter-control-panel-system-reset .unnumbered}

##### **A. perform_reset() (handling system reset from Control Panel)** {#a.-perform_reset-handling-system-reset-from-control-panel .unnumbered}

###### **a. test_perform_reset_success (UT-RP-001)** {#a.-test_perform_reset_success-ut-rp-001 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | ControlPanelResetPresenter |
| Method  | perform_reset()            |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that the presenter correctly handles successful system reset.

**Input Specifications**

• System reset returns: \`{\"success\": True, \"message\": \"Reset
complete\", \"phase\": 3}\`

**Expected Result**

ResetOutcome(  
success=True,  
alert_level=\"info\",  
alert_title=\"Success\",  
alert_message=\"Reset complete\",  
phase=3  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success outcome

• Pass: Alert level is info

• Pass: Phase information preserved

**Comment**

Presenter translates system response into UI-appropriate format.

### **B. Web Interface Management** {#b.-web-interface-management .unnumbered}

#### **1. WebLoginPresenter (Web Browser Login - 2FA)** {#webloginpresenter-web-browser-login---2fa .unnumbered}

##### **A. validate_first_password() (handling first password validation from Web)** {#a.-validate_first_password-handling-first-password-validation-from-web .unnumbered}

###### **a. test_first_password_missing_username (UT-WL-001)** {#a.-test_first_password_missing_username-ut-wl-001 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that attempting to validate first password without username
triggers validation error.

**Input Specifications**

• username: \"\" (empty string)

• password: \"password123\"

**Expected Result**

WebLoginOutcome(  
success=False,  
message=\"Username and password are required\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure outcome

• Pass: Appropriate error message

**Comment**

Input validation at the presenter layer prevents unnecessary system
calls. Web interface uses 2-factor authentication (first password +
second password/PIN).

###### **b. test_first_password_missing_password (UT-WL-002)** {#b.-test_first_password_missing_password-ut-wl-002 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that attempting to validate first password without password
triggers validation error.

**Input Specifications**

• username: \"admin\"

• password: \"\" (empty string)

**Expected Result**

WebLoginOutcome(  
success=False,  
message=\"Username and password are required\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure outcome

• Pass: Appropriate error message

**Comment**

Prevents submission of incomplete credentials.

###### **c. test_first_password_success (UT-WL-003)** {#c.-test_first_password_success-ut-wl-003 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that successful first password validation returns success.

**Input Specifications**

• username: \"admin\"

• password: \"password123\"

• System returns: \`{\"success\": True}\`

**Expected Result**

WebLoginOutcome(  
success=True,  
message=\"First password correct\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success outcome

• Pass: User proceeds to second password input

**Comment**

First step of 2-factor authentication for web interface.

###### **d. test_first_password_locked_with_remaining_time (UT-WL-004)** {#d.-test_first_password_locked_with_remaining_time-ut-wl-004 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that locked account with remaining time returns appropriate
information.

**Input Specifications**

• username: \"admin\"

• password: \"wrong\"

• Account locked with remaining_time: 30 seconds

**Expected Result**

WebLoginOutcome(  
success=False,  
locked=True,  
remaining_time=30,  
tries=5,  
message=\"Account locked due to too many attempts\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns locked status

• Pass: Includes remaining time information

**Comment**

Time-based account locking for security.

###### **e. test_first_password_system_off (UT-WL-005)** {#e.-test_first_password_system_off-ut-wl-005 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that first password validation fails when system is OFF.

**Input Specifications**

• System state: OFF

• Valid credentials provided

**Expected Result**

WebLoginOutcome(  
success=False,  
system_off=True,  
message=\"System is currently off\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure with system_off flag

• Pass: Appropriate error message

**Comment**

Precondition: System must be ON for login.

###### **f. test_first_password_system_locked (UT-WL-006)** {#f.-test_first_password_system_locked-ut-wl-006 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that first password validation fails when system is LOCKED.

**Input Specifications**

• System state: LOCKED

• Valid credentials provided

**Expected Result**

WebLoginOutcome(  
success=False,  
system_locked=True,  
message=\"System is locked by administrator\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure with system_locked flag

**Comment**

System-level lock prevents all logins.

###### **g. test_first_password_failed_with_attempts (UT-WL-007)** {#g.-test_first_password_failed_with_attempts-ut-wl-007 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that failed first password validation includes attempt
information.

**Input Specifications**

• username: \"admin\"

• password: \"wrong\"

• tries: 2, remaining: 3

**Expected Result**

WebLoginOutcome(  
success=False,  
message=\"Incorrect first password\",  
tries=2,  
remaining=3  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure with attempt counts

**Comment**

User feedback helps prevent account lockout.

###### **h. test_first_password_system_not_available (UT-WL-008)** {#h.-test_first_password_system_not_available-ut-wl-008 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies proper error handling when system is not available.

**Input Specifications**

• system: None

**Expected Result**

WebLoginOutcome(  
success=False,  
message=\"System not available\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns appropriate error

**Comment**

Graceful degradation when system unavailable.

##### **B. validate_second_password() (handling second password/PIN validation from Web)** {#b.-validate_second_password-handling-second-passwordpin-validation-from-web .unnumbered}

###### **a. test_second_password_missing (UT-WL2-001)** {#a.-test_second_password_missing-ut-wl2-001 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | WebLoginPresenter          |
| Method  | validate_second_password() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that empty second password triggers validation error.

**Input Specifications**

• username: \"admin\"

• second_password: \"\" (empty string)

**Expected Result**

WebLoginOutcome(  
success=False,  
message=\"Second password is required\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure outcome

**Comment**

Second factor of 2FA must be provided.

###### **b. test_second_password_success (UT-WL2-002)** {#b.-test_second_password_success-ut-wl2-002 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | WebLoginPresenter          |
| Method  | validate_second_password() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that successful second password validation completes login.

**Input Specifications**

• username: \"admin\"

• second_password: \"pin1234\"

• System returns: \`{\"success\": True}\`

**Expected Result**

WebLoginOutcome(  
success=True,  
message=\"Login successful\",  
redirect_url=\"/dashboard\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success with redirect URL

**Comment**

Completes 2-factor authentication and redirects to dashboard.

###### **c. test_second_password_locked_with_remaining_time (UT-WL2-003)** {#c.-test_second_password_locked_with_remaining_time-ut-wl2-003 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | WebLoginPresenter          |
| Method  | validate_second_password() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies handling of locked account during second password validation.

**Input Specifications**

• Account locked with remaining_time: 45 seconds

**Expected Result**

WebLoginOutcome(  
success=False,  
locked=True,  
remaining_time=45,  
tries=5  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns locked status with remaining time

**Comment**

Account can be locked at either authentication stage.

###### **d. test_second_password_system_off (UT-WL2-004)** {#d.-test_second_password_system_off-ut-wl2-004 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | WebLoginPresenter          |
| Method  | validate_second_password() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that second password validation fails when system is OFF.

**Input Specifications**

• System state: OFF

**Expected Result**

WebLoginOutcome(  
success=False,  
system_off=True  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure with system_off flag

**Comment**

System state checked at each authentication stage.

###### **e. test_second_password_system_locked (UT-WL2-005)** {#e.-test_second_password_system_locked-ut-wl2-005 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | WebLoginPresenter          |
| Method  | validate_second_password() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that second password validation fails when system is LOCKED.

**Input Specifications**

• System state: LOCKED

**Expected Result**

WebLoginOutcome(  
success=False,  
system_locked=True  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure with system_locked flag

**Comment**

System-level lock enforced at all authentication stages.

###### **f. test_second_password_failed_with_attempts (UT-WL2-006)** {#f.-test_second_password_failed_with_attempts-ut-wl2-006 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | WebLoginPresenter          |
| Method  | validate_second_password() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies failed second password validation includes attempt information.

**Input Specifications**

• second_password: \"wrong\"

• tries: 1, remaining: 4

**Expected Result**

WebLoginOutcome(  
success=False,  
message=\"Incorrect second password\",  
tries=1,  
remaining=4  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure with attempt counts

**Comment**

Separate attempt tracking for each authentication factor.

###### **g. test_second_password_system_not_available (UT-WL2-007)** {#g.-test_second_password_system_not_available-ut-wl2-007 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | WebLoginPresenter          |
| Method  | validate_second_password() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies error handling when system unavailable during second password
validation.

**Input Specifications**

• system: None

**Expected Result**

WebLoginOutcome(  
success=False,  
message=\"System not available\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns appropriate error

**Comment**

Consistent error handling across both authentication stages.

###### **h. test_calls_login_manager_with_correct_interface (UT-WL2-008)** {#h.-test_calls_login_manager_with_correct_interface-ut-wl2-008 .unnumbered}

|         |                           |
|---------|---------------------------|
| Field   | Value                     |
| Class   | WebLoginPresenter         |
| Method  | validate_first_password() |
| Author  | Minseok Jo                |
| Date    | 2025-11-25                |
| Version | 2.0.0                     |

**Test Case Description**

Verifies that presenter calls LoginManager with \'web_browser\'
interface.

**Input Specifications**

• username: \"admin\"

• password: \"password123\"

**Expected Result**

• LoginManager.validate_first_password called with
interface=\'web_browser\'

**Actual Result (Pass/Fail/Exception)**

• Pass: Correct interface parameter passed

**Comment**

Ensures proper logging and tracking of web-based logins. Test file:
test_web_login_presenter.py:162

#### **2. WebSettingsPresenter (Web Browser Settings Configuration)** {#websettingspresenter-web-browser-settings-configuration .unnumbered}

##### **A. update_settings() (handling settings update from Web)** {#a.-update_settings-handling-settings-update-from-web .unnumbered}

###### **a. test_invalid_monitoring_phone_format (UT-WS-001)** {#a.-test_invalid_monitoring_phone_format-ut-ws-001 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that invalid monitoring phone format is rejected.

**Input Specifications**

• monitoring_service_phone: \"invalid\"

• homeowner_phone: \"123-456-7890\"

**Expected Result**

WebSettingsOutcome(  
success=False,  
message=\"Validation failed\",  
errors=\[\"Invalid monitoring service phone format (recommended:
XXX-XXX-XXXX)\"\]  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns validation error

**Comment**

Phone number format validation at presenter layer.

###### **b. test_invalid_homeowner_phone_format (UT-WS-002)** {#b.-test_invalid_homeowner_phone_format-ut-ws-002 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that invalid homeowner phone format is rejected.

**Input Specifications**

• monitoring_service_phone: \"123-456-7890\"

• homeowner_phone: \"abc\"

**Expected Result**

WebSettingsOutcome(  
success=False,  
message=\"Validation failed\",  
errors=\[\"Invalid homeowner phone format (recommended:
XXX-XXX-XXXX)\"\]  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns validation error

**Comment**

Consistent phone validation for both fields.

###### **c. test_valid_phone_formats_accepted (UT-WS-003)** {#c.-test_valid_phone_formats_accepted-ut-ws-003 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that valid phone formats are accepted (standard and flexible).

**Input Specifications**

• Standard format: \"111-222-3333\"

• Flexible format: \"(123) 456-7890\", \"+1-234-567-8900\"

**Expected Result**

• Both formats accepted successfully

**Actual Result (Pass/Fail/Exception)**

• Pass: Standard XXX-XXX-XXXX format accepted

• Pass: Flexible format with at least 3 chars accepted

**Comment**

Flexible validation supports international formats while maintaining
basic validation.

###### **d. test_zero_lock_time_rejected (UT-WS-004)** {#d.-test_zero_lock_time_rejected-ut-ws-004 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that zero lock time is rejected.

**Input Specifications**

• system_lock_time: 0

**Expected Result**

WebSettingsOutcome(  
success=False,  
errors=\[\"System lock time must be greater than 0\"\]  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns validation error

**Comment**

Business rule: Lock time must be positive.

###### **e. test_negative_lock_time_rejected (UT-WS-005)** {#e.-test_negative_lock_time_rejected-ut-ws-005 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that negative lock time is rejected.

**Input Specifications**

• system_lock_time: -5

**Expected Result**

WebSettingsOutcome(  
success=False,  
errors=\[\"System lock time must be greater than 0\"\]  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns validation error

**Comment**

Prevents invalid negative values.

###### **f. test_negative_alarm_delay_rejected (UT-WS-006)** {#f.-test_negative_alarm_delay_rejected-ut-ws-006 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that negative alarm delay is rejected.

**Input Specifications**

• alarm_delay_time: -10

**Expected Result**

WebSettingsOutcome(  
success=False,  
errors=\[\"Alarm delay time must be non-negative\"\]  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns validation error

**Comment**

Alarm delay can be 0 (immediate) but not negative.

###### **g. test_invalid_lock_time_type (UT-WS-007)** {#g.-test_invalid_lock_time_type-ut-ws-007 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that invalid lock time type is rejected.

**Input Specifications**

• system_lock_time: \"abc\"

**Expected Result**

WebSettingsOutcome(  
success=False,  
errors=\[\"System lock time must be a valid number\"\]  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns type validation error

**Comment**

Type checking prevents non-numeric values.

###### **h. test_invalid_alarm_delay_type (UT-WS-008)** {#h.-test_invalid_alarm_delay_type-ut-ws-008 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that invalid alarm delay type is rejected.

**Input Specifications**

• alarm_delay_time: \"xyz\"

**Expected Result**

WebSettingsOutcome(  
success=False,  
errors=\[\"Alarm delay time must be a valid number\"\]  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns type validation error

**Comment**

Consistent type validation for time fields.

###### **i. test_multiple_validation_errors (UT-WS-009)** {#i.-test_multiple_validation_errors-ut-ws-009 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that multiple validation errors are collected.

**Input Specifications**

• monitoring_service_phone: \"invalid\"

• homeowner_phone: \"bad\"

• system_lock_time: 0

• alarm_delay_time: -5

**Expected Result**

• At least 4 validation errors returned

**Actual Result (Pass/Fail/Exception)**

• Pass: All validation errors collected

**Comment**

Comprehensive validation feedback improves user experience.

###### **j. test_successful_settings_update (UT-WS-010)** {#j.-test_successful_settings_update-ut-ws-010 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies successful settings update with valid inputs.

**Input Specifications**

• monitoring_service_phone: \"111-222-3333\"

• homeowner_phone: \"444-555-6666\"

• system_lock_time: 30

• alarm_delay_time: 60

**Expected Result**

WebSettingsOutcome(  
success=True,  
message=\"Settings updated successfully\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success outcome

• Pass: Settings persisted to database

**Comment**

Complete update flow with all parameters.

###### **k. test_partial_update_only_phones (UT-WS-011)** {#k.-test_partial_update_only_phones-ut-ws-011 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies partial update of only phone numbers.

**Input Specifications**

• monitoring_service_phone: \"123-456-7890\"

• homeowner_phone: \"098-765-4321\"

• (time values not provided)

**Expected Result**

• Update succeeds with only phones modified

**Actual Result (Pass/Fail/Exception)**

• Pass: Partial update succeeds

• Pass: Only phone fields updated

**Comment**

Supports selective field updates.

###### **l. test_partial_update_only_times (UT-WS-012)** {#l.-test_partial_update_only_times-ut-ws-012 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies partial update of only time values.

**Input Specifications**

• system_lock_time: 45

• alarm_delay_time: 90

• (phone numbers not provided)

**Expected Result**

• Update succeeds with only times modified

**Actual Result (Pass/Fail/Exception)**

• Pass: Partial update succeeds

• Pass: Only time fields updated

**Comment**

Flexible update mechanism for different field combinations.

###### **m. test_update_converts_string_times_to_int (UT-WS-013)** {#m.-test_update_converts_string_times_to_int-ut-ws-013 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that string time values are converted to integers.

**Input Specifications**

• system_lock_time: \"30\" (string)

• alarm_delay_time: \"60\" (string)

**Expected Result**

• Values converted to integers: 30, 60

**Actual Result (Pass/Fail/Exception)**

• Pass: String to int conversion successful

• Pass: Values stored as integers

**Comment**

Type coercion handles web form data (strings).

###### **n. test_save_failure_returns_error (UT-WS-014)** {#n.-test_save_failure_returns_error-ut-ws-014 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies handling of database save failure.

**Input Specifications**

• Valid inputs provided

• Database save fails

**Expected Result**

WebSettingsOutcome(  
success=False,  
message=\"Failed to save settings\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns failure outcome

**Comment**

Graceful error handling for persistence failures.

###### **o. test_system_not_available (UT-WS-015)** {#o.-test_system_not_available-ut-ws-015 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies error handling when system is not available.

**Input Specifications**

• system: None

**Expected Result**

WebSettingsOutcome(  
success=False,  
message=\"System not available\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns appropriate error

**Comment**

System availability check prevents null reference errors.

###### **p. test_get_settings_system_not_available (UT-WS-016)** {#p.-test_get_settings_system_not_available-ut-ws-016 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | get_settings()       |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies get_settings error handling when system unavailable.

**Input Specifications**

• system: None

**Expected Result**

WebSettingsOutcome(  
success=False,  
message=\"System not available\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns appropriate error

**Comment**

Consistent error handling across all operations.

###### **q. test_get_settings_success (UT-WS-017)** {#q.-test_get_settings_success-ut-ws-017 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | get_settings()       |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies successful retrieval of current settings.

**Input Specifications**

• System and ConfigurationManager available

**Expected Result**

WebSettingsOutcome(  
success=True,  
message=\"Settings retrieved successfully\"  
)

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success outcome

**Comment**

Retrieval operation for GET requests.

###### **r. test_empty_update_succeeds (UT-WS-018)** {#r.-test_empty_update_succeeds-ut-ws-018 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that update with no parameters succeeds.

**Input Specifications**

• No parameters provided

**Expected Result**

• Operation succeeds (no-op)

**Actual Result (Pass/Fail/Exception)**

• Pass: Empty update succeeds

**Comment**

Handles edge case of empty update request.

###### **s. test_zero_alarm_delay_accepted (UT-WS-019)** {#s.-test_zero_alarm_delay_accepted-ut-ws-019 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | WebSettingsPresenter |
| Method  | update_settings()    |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that zero alarm delay is accepted (immediate alarm).

**Input Specifications**

• alarm_delay_time: 0

**Expected Result**

• Update succeeds

**Actual Result (Pass/Fail/Exception)**

• Pass: Zero alarm delay accepted

**Comment**

Zero is valid for alarm delay (immediate activation), unlike lock time
which must be positive.

## **2. Surveillance** {#surveillance .unnumbered}

### A. Camera Management {#a.-camera-management .unnumbered}

#### 1. SafeHomeCamera {#safehomecamera .unnumbered}

##### A. get_location() {#a.-get_location .unnumbered}

###### a. test_get_location (UT-CAM-LOC-CPY) {#a.-test_get_location-ut-cam-loc-cpy .unnumbered}

|                |                |            |            |             |
|----------------|----------------|------------|------------|-------------|
| **Class**      | **Method**     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | get_location() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling get_location() returns a defensive copy of the
location list, ensuring the camera\'s internal state is protected from
external modifications.\"

Input Specifications

\"Initial location: \[100, 200\]. Action: Modify the returned list
value.\"

**Detailed Step**

1.  Call get_location() and store the list.

2.  Modify the list (e.g., change index 0 to 999).

3.  Call get_location() again to assert the internal value remains
    \[100, 200\].

Expected Result

\"The internal location must remain \[100, 200\], verifying that a copy
was returned.\"

Actual Result (Pass/Fail/Exception)

Pass: Internal state was preserved.

Comment (including references)

Verification of defensive programming based on the Object State
Protection Principle.

###### b. test_get_location_returns_copy (UT-CAM-LOC-CPY-ENF) {#b.-test_get_location_returns_copy-ut-cam-loc-cpy-enf .unnumbered}

|                |                |            |            |             |
|----------------|----------------|------------|------------|-------------|
| **Class**      | **Method**     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | get_location() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that appending elements to the returned list does not affect
the original list\'s length, reinforcing the defensive copy check.\"

Input Specifications

\"Initial location: \[100, 200\]. Action: Append 999 to the returned
list.\"

**Detailed Step**

1.  Call get_location() and append a new element to the returned list.

2.  Call get_location() again and assert the returned list\'s length is
    still 2.

Expected Result

The original list length must remain 2.

Actual Result (Pass/Fail/Exception)

Pass: Defensive copy prevented unauthorized length modification.

Comment (including references)

Coverage reinforcement for the defensive copy check.

###### c. test_initialization_with_location (UT-CAM-INIT-LOC) {#c.-test_initialization_with_location-ut-cam-init-loc .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | \_\_init\_\_(), get_location() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the object is initialized with a specific location,
get_location() correctly retrieves the set coordinates.\"

Input Specifications

\"Instantiate SafeHomeCamera with location=\[100, 200\].\"

**Detailed Step**

1.  Instantiate the object with the specified location.

2.  Call get_location() and assert the returned value.

Expected Result

\"get_location() must return exactly \[100, 200\].\"

Actual Result (Pass/Fail/Exception)

Pass: Initial location was correctly set and retrieved.

Comment (including references)

Validation of initial attribute setting.

###### d. test_initialization_without_location (UT-CAM-INIT-DEF) {#d.-test_initialization_without_location-ut-cam-init-def .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | \_\_init\_\_(), get_location() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the object is initialized without specifying a
location, get_location() correctly returns the default coordinates \[0,
0\].\"

Input Specifications

Instantiate SafeHomeCamera omitting the location parameter.

**Detailed Step**

1.  Instantiate the object without the location.

2.  Call get_location() and assert the returned value.

Expected Result

\"get_location() must return the default location \[0, 0\].\"

Actual Result (Pass/Fail/Exception)

\"Pass: Default location \[0, 0\] was correctly assigned.\"

Comment (including references)

Verification of default value handling.

##### B. set_location() {#b.-set_location .unnumbered}

###### a. test_set_location (UT-CAM-LOC-SET) {#a.-test_set_location-ut-cam-loc-set .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_location(), get_location() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling set_location() with valid coordinates (\[x, y\])
successfully updates the location, returns True, and the new value is
retrieved by get_location().\"

Input Specifications

\"Initial location: \[100, 200\]. Action: Call set_location(\[300,
400\]).\"

**Detailed Step**

1.  Call set_location(\[300, 400\]).

2.  Assert the return value is True.

3.  Call get_location() and assert the new value \[300, 400\].

Expected Result

\"set_location() must return True, and get_location() must return \[300,
400\].\"

Actual Result (Pass/Fail/Exception)

Pass: Location was successfully updated.

Comment (including references)

Validation of the camera coordinate setting functionality.

###### b. test_set_invalid_location (UT-CAM-LOC-INV-BAS) {#b.-test_set_invalid_location-ut-cam-loc-inv-bas .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_location(), get_location() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that an invalid location format (specifically, missing the
Y-coordinate) is rejected, returns False, and preserves the existing
location.\"

Input Specifications

\"Initial location: \[100, 200\]. Action: Call set_location(\[100\])
(invalid format).\"

**Detailed Step**

1.  Call set_location(\[100\]).

2.  Assert the return value is False.

3.  Call get_location() and assert the location remains \[100, 200\].

Expected Result

\"set_location() must return False, and get_location() must remain
\[100, 200\].\"

Actual Result (Pass/Fail/Exception)

\"Pass: Invalid input was correctly rejected, and state was preserved.\"

Comment (including references)

Validation of input validation and error handling logic.

###### c. test_set_location_invalid_lengths (UT-CAM-LOC-INV-COV) {#c.-test_set_location_invalid_lengths-ut-cam-loc-inv-cov .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_location(), get_location() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the input validation handles various incorrect list
lengths (e.g., 0, 1, or 3 elements), rejecting them and ensuring the
current location is unchanged.\"

Input Specifications

\"Initial location: \[100, 200\]. Action: Call set_location with \[\],
\[100\], and \[100, 200, 300\] sequentially.\"

**Detailed Step**

1.  Iterate through invalid inputs.

2.  For each, assert set_location returns False.

3.  Assert get_location() remains \[100, 200\] after each attempt.

Expected Result

\"set_location() must return False for all invalid inputs, and the
location must remain \[100, 200\].\"

Actual Result (Pass/Fail/Exception)

Pass: All invalid list lengths were correctly handled and rejected.

Comment (including references)

Coverage test ensuring validation handles various incorrect list
lengths.

##### C. get_id() {#c.-get_id .unnumbered}

###### a. test_get_id (UT-CAM-ID-GET) {#a.-test_get_id-ut-cam-id-get .unnumbered}

|                |            |            |            |             |
|----------------|------------|------------|------------|-------------|
| **Class**      | **Method** | **Author** | **Date**   | **Version** |
| SafeHomeCamera | get_id()   | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the camera\'s unique ID, assigned during initialization,
is correctly retrieved.\"

Input Specifications

Initial state: Camera ID is 1 (set by fixture/initialization).

**Detailed Step**

1.  Instantiate the camera object.

2.  Call get_id().

3.  Assert the returned ID matches the initialized value.

Expected Result

get_id() must return 1.

Actual Result (Pass/Fail/Exception)

Pass: ID was correctly retrieved.

Comment (including references)

Basic getter functionality check for the camera\'s static identifier.

###### b. test_initialization_with_location (UT-CAM-INIT-ID) {#b.-test_initialization_with_location-ut-cam-init-id .unnumbered}

|                |                          |            |            |             |
|----------------|--------------------------|------------|------------|-------------|
| **Class**      | **Method**               | **Author** | **Date**   | **Version** |
| SafeHomeCamera | \_\_init\_\_(), get_id() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that the camera ID (1) is correctly set and immediately
retrieved after object initialization.

Input Specifications

Instantiate SafeHomeCamera with camera_id=1.

**Detailed Step**

1.  Instantiate the object with the specified ID.

2.  Call get_id() and assert the returned value.

Expected Result

get_id() must return 1.

Actual Result (Pass/Fail/Exception)

Pass: ID was correctly set during initialization.

Comment (including references)

Fundamental initial state check for ID consistency.

##### D. set_id() {#d.-set_id .unnumbered}

###### a. test_set_id (UT-CAM-ID-SET-PASS) {#a.-test_set_id-ut-cam-id-set-pass .unnumbered}

|                |                    |            |            |             |
|----------------|--------------------|------------|------------|-------------|
| **Class**      | **Method**         | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_id(), get_id() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that calling set_id() with a valid positive integer
successfully updates the camera\'s ID and is correctly retrieved by
get_id().

Input Specifications

Initial ID: 1. Action: Call set_id(5).

**Detailed Step**

1.  Call set_id(5).

2.  Assert the return value is True.

3.  Call get_id() and assert the new ID is 5.

Expected Result

\"set_id() must return True, and get_id() must return 5.\"

Actual Result (Pass/Fail/Exception)

Pass: ID was successfully changed and retrieved.

Comment (including references)

Verification of successful ID mutation and retrieval.

###### b. test_set_invalid_id (UT-CAM-ID-SET-FAIL) {#b.-test_set_invalid_id-ut-cam-id-set-fail .unnumbered}

|                |                    |            |            |             |
|----------------|--------------------|------------|------------|-------------|
| **Class**      | **Method**         | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_id(), get_id() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling set_id() with non-positive integers (0 or
negative) is rejected, returns False, and preserves the original ID.\"

Input Specifications

Initial ID: 1. Action: Call set_id(0) and then set_id(-1).

**Detailed Step**

1.  Call set_id(0).

2.  Assert the return value is False.

3.  Call get_id() and assert the ID remains the initial value (1).

Expected Result

\"set_id() must return False for non-positive inputs, and get_id() must
return 1.\"

Actual Result (Pass/Fail/Exception)

\"Pass: Invalid ID attempts were rejected, and state was preserved.\"

Comment (including references)

Validation of ID input validation (ID must be a positive integer) and
state preservation.

###### c. test_set_id_boundary_values (UT-CAM-ID-BOUND) {#c.-test_set_id_boundary_values-ut-cam-id-bound .unnumbered}

|                |                    |            |            |             |
|----------------|--------------------|------------|------------|-------------|
| **Class**      | **Method**         | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_id(), get_id() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the ID setter correctly handles valid boundary values,
specifically the minimum positive integer (1) and a large valid ID
(99999).\"

Input Specifications

Initial state ID: 1. Action: Call set_id(1) and then set_id(99999).

**Detailed Step**

1.  Call set_id(1) and assert result is True.

2.  Call set_id(99999) and assert result is True.

3.  Verify get_id() reflects the final value 99999.

Expected Result

\"set_id() must return True for both valid boundary attempts, and the
final get_id() must return 99999.\"

Actual Result (Pass/Fail/Exception)

Pass: Valid ID boundaries were correctly accepted.

Comment (including references)

Comprehensive check of valid ID boundaries for the set_id method.

##### E. display_view() {#e.-display_view .unnumbered}

###### a. test_display_view (UT-CAM-VIEW-PASS) {#a.-test_display_view-ut-cam-view-pass .unnumbered}

|                |                |            |            |             |
|----------------|----------------|------------|------------|-------------|
| **Class**      | **Method**     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | display_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the camera is enabled, display_view() successfully
returns a non-null object, confirming the feed is accessible.\"

Input Specifications

Initial state: Camera is enabled (is_enabled() is True).

**Detailed Step**

1.  Ensure the camera is enabled.

2.  Call display_view().

3.  Assert the result is not None and is an instance of PIL.Image.Image.

Expected Result

Returns a valid PIL.Image.Image object.

Actual Result (Pass/Fail/Exception)

Pass: View object was successfully retrieved.

Comment (including references)

Core function test for accessing the camera feed.

###### b. test_display_view_disabled_camera (UT-CAM-VIEW-FAIL) {#b.-test_display_view_disabled_camera-ut-cam-view-fail .unnumbered}

|                |                           |            |            |             |
|----------------|---------------------------|------------|------------|-------------|
| **Class**      | **Method**                | **Author** | **Date**   | **Version** |
| SafeHomeCamera | display_view(), disable() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the camera is disabled, display_view() enforces the
security policy by returning None, blocking access to the feed.\"

Input Specifications

Action: camera.disable() is called to set the state to disabled.

**Detailed Step**

1.  Call camera.disable().

2.  Call display_view().

3.  Assert the result is None.

Expected Result

Returns None.

Actual Result (Pass/Fail/Exception)

Pass: Access to the view was correctly denied when disabled.

Comment (including references)

Security policy validation for access control in a disabled state.

###### c. test_display_view_exception_handling (UT-CAM-VIEW-EXC) {#c.-test_display_view_exception_handling-ut-cam-view-exc .unnumbered}

|                |                |            |            |             |
|----------------|----------------|------------|------------|-------------|
| **Class**      | **Method**     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | display_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the method\'s robustness by ensuring that if the underlying
device camera throws an exception during view retrieval, the method
handles it gracefully and returns None.\"

Input Specifications

\"Mocking: The underlying device camera\'s get_view() method is patched
to raise an Exception(\"\"Camera error\"\").\"

**Detailed Step**

1.  Patch get_view() to raise an exception.

2.  Call display_view() within the patched context.

3.  Assert the result is None.

Expected Result

\"Returns None, and the system does not crash or raise the exception.\"

Actual Result (Pass/Fail/Exception)

Pass: External component failure was handled gracefully.

Comment (including references)

Robustness check for failures in the virtual device layer.

##### F. zoom_in() {#f.-zoom_in .unnumbered}

###### a. test_zoom_in (UT-CAM-ZOOM-IN-PASS) {#a.-test_zoom_in-ut-cam-zoom-in-pass .unnumbered}

|                |                               |            |            |             |
|----------------|-------------------------------|------------|------------|-------------|
| **Class**      | **Method**                    | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_in(), get_zoom_setting() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the current zoom level is below the maximum,
calling zoom_in() returns True and increases the zoom level by exactly
1.\"

Input Specifications

Initial state: Zoom level is 1. Action: Call zoom_in() once.

**Detailed Step**

1.  Call zoom_in().

2.  Assert the return value is True.

3.  Call get_zoom_setting() and assert the new level is 2.

Expected Result

\"zoom_in() must return True, and the new zoom_setting must be 2.\"

Actual Result (Pass/Fail/Exception)

Pass: Zoom level was successfully incremented.

Comment (including references)

Core function test for camera zoom operation.

###### b. test_zoom_in_max (UT-CAM-ZOOM-IN-MAX) {#b.-test_zoom_in_max-ut-cam-zoom-in-max .unnumbered}

|                |                               |            |            |             |
|----------------|-------------------------------|------------|------------|-------------|
| **Class**      | **Method**                    | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_in(), get_zoom_setting() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the boundary condition: when the maximum zoom level (10) is
reached, subsequent calls to zoom_in() fail, return False, and the level
remains 10.\"

Input Specifications

\"Action: Repeatedly call zoom_in() until the level reaches 10, then
call it one more time.\"

**Detailed Step**

1.  Set zoom level to 10.

2.  Call zoom_in().

3.  Assert the return value is False.

4.  Assert get_zoom_setting() is still 10.

Expected Result

\"zoom_in() must return False , and the zoom level must remain 10.\"

Actual Result (Pass/Fail/Exception)

Pass: Zoom operation was correctly blocked at the maximum limit.

Comment (including references)

Boundary condition check for maximum zoom level.

###### c. test_zoom_in_disabled_camera (UT-CAM-ZOOM-IN-FAIL) {#c.-test_zoom_in_disabled_camera-ut-cam-zoom-in-fail .unnumbered}

|                |                                          |            |            |             |
|----------------|------------------------------------------|------------|------------|-------------|
| **Class**      | **Method**                               | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_in(), disable(), get_zoom_setting() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling zoom_in() on a disabled camera is rejected,
returns False, and preserves the original zoom level.\"

Input Specifications

Initial state: Zoom level 1. Action: camera.disable() is called.

**Detailed Step**

1.  Disable the camera.

2.  Record the initial zoom level.

3.  Call zoom_in() and assert the return value is False.

4.  Assert the zoom level has not changed.

Expected Result

\"zoom_in() must return False, and the zoom level must remain the
initial value.\"

Actual Result (Pass/Fail/Exception)

Pass: Control command was correctly blocked in the disabled state.

Comment (including references)

Security and state awareness check for control operations.

###### d. test_zoom_in_device_camera_integration (UT-CAM-ZOOM-IN-INT) {#d.-test_zoom_in_device_camera_integration-ut-cam-zoom-in-int .unnumbered}

|                |            |            |            |             |
|----------------|------------|------------|------------|-------------|
| **Class**      | **Method** | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_in()  | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling zoom_in() successfully executes the underlying
virtual device interaction logic and returns a boolean result,
confirming proper integration.\"

Input Specifications

Initial state: Camera is enabled and below max zoom.

**Detailed Step**

1.  Call zoom_in().

2.  Assert the return value is a boolean (True) and the internal logic
    path for device interaction is executed.

Expected Result

The method must execute the device interaction path and return True.

Actual Result (Pass/Fail/Exception)

Pass: Integration with the virtual device layer for zoom control was
confirmed.

Comment (including references)

Verifies the linkage between the domain model and the virtual device
simulator.

##### G. zoom_out() {#g.-zoom_out .unnumbered}

###### a. test_zoom_out (UT-CAM-ZOOM-OUT-PASS) {#a.-test_zoom_out-ut-cam-zoom-out-pass .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_out(), get_zoom_setting() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the current zoom level is above the minimum,
calling zoom_out() returns True and decreases the zoom level by exactly
1.\"

Input Specifications

Initial state: Zoom level is set to 2 (after one zoom_in call). Action:
Call zoom_out() once.

**Detailed Step**

1.  Ensure zoom level is \> 1.

2.  Call zoom_out().

3.  Assert the return value is True.

4.  Call get_zoom_setting() and assert the new level is 1.

Expected Result

\"zoom_out() must return True, and the new zoom_setting must be 1.\"

Actual Result (Pass/Fail/Exception)

Pass: Zoom level was successfully decremented.

Comment (including references)

Core function test for camera zoom operation.

###### b. test_zoom_out_min (UT-CAM-ZOOM-OUT-MIN) {#b.-test_zoom_out_min-ut-cam-zoom-out-min .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_out(), get_zoom_setting() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the boundary condition: when the minimum zoom level (1) is
reached, subsequent calls to zoom_out() fail, return False, and the
level remains unchanged.\"

Input Specifications

Initial state: Zoom level is 1. Action: Call zoom_out() once.

**Detailed Step**

1.  Ensure zoom level is 1.

2.  Call zoom_out().

3.  Assert the return value is False.

4.  Assert get_zoom_setting() is still 1.

Expected Result

\"zoom_out() must return False , and the zoom level must remain 1.\"

Actual Result (Pass/Fail/Exception)

Pass: Zoom operation was correctly blocked at the minimum limit.

Comment (including references)

Boundary condition check for minimum zoom level.

###### c. test_zoom_out_disabled_camera (UT-CAM-ZOOM-OUT-FAIL) {#c.-test_zoom_out_disabled_camera-ut-cam-zoom-out-fail .unnumbered}

|                |                                           |            |            |             |
|----------------|-------------------------------------------|------------|------------|-------------|
| **Class**      | **Method**                                | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_out(), disable(), get_zoom_setting() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling zoom_out() on a disabled camera is rejected,
returns False, and preserves the original zoom level.\"

Input Specifications

Initial state: Zoom level 2. Action: camera.disable() is called.

**Detailed Step**

1.  Disable the camera.

2.  Record the initial zoom level.

3.  Call zoom_out() and assert the return value is False.

4.  Assert the zoom level has not changed.

Expected Result

\"zoom_out() must return False, and the zoom level must remain the
initial value.\"

Actual Result (Pass/Fail/Exception)

Pass: Control command was correctly blocked in the disabled state.

Comment (including references)

Security and state awareness check for control operations.

###### d. test_zoom_out_device_camera_integration (UT-CAM-ZOOM-OUT-INT) {#d.-test_zoom_out_device_camera_integration-ut-cam-zoom-out-int .unnumbered}

|                |            |            |            |             |
|----------------|------------|------------|------------|-------------|
| **Class**      | **Method** | **Author** | **Date**   | **Version** |
| SafeHomeCamera | zoom_out() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling zoom_out() correctly executes the underlying
virtual device interaction logic and returns a boolean result,
confirming proper integration.\"

Input Specifications

\"Initial state: Camera is enabled and zoomed in (e.g., level 2).\"

**Detailed Step**

1.  Ensure zoom level \> 1.

2.  Call zoom_out().

3.  Assert the return value is a boolean (True) and the internal logic
    path for device interaction is executed.

Expected Result

The method must execute the device interaction path and return True.

Actual Result (Pass/Fail/Exception)

Pass: Integration with the virtual device layer for zoom control was
confirmed.

Comment (including references)

Verifies the linkage between the domain model and the virtual device
simulator.

##### H. pan_left() {#h.-pan_left .unnumbered}

###### a. test_pan_left (UT-CAM-PAN-LEFT-PASS) {#a.-test_pan_left-ut-cam-pan-left-pass .unnumbered}

|                |                             |            |            |             |
|----------------|-----------------------------|------------|------------|-------------|
| **Class**      | **Method**                  | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_left(), get_pan_angle() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the pan angle is above the minimum limit, calling
pan_left() returns True and decreases the angle by exactly 5.0
degrees.\"

Input Specifications

Initial state: Pan angle is 0.0 degrees. Action: Call pan_left() once.

**Detailed Step**

1.  Call pan_left().

2.  Assert the return value is True.

3.  Call get_pan_angle() and assert the new angle is -5.0 degrees.

Expected Result

\"pan_left() must return True, and the new pan_angle must be -5.0.\"

Actual Result (Pass/Fail/Exception)

Pass: Pan angle was successfully decremented.

Comment (including references)

Core function test for camera pan operation.

###### b. test_pan_left_limit (UT-CAM-PAN-LEFT-MIN) {#b.-test_pan_left_limit-ut-cam-pan-left-min .unnumbered}

|                |                             |            |            |             |
|----------------|-----------------------------|------------|------------|-------------|
| **Class**      | **Method**                  | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_left(), get_pan_angle() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the boundary condition: once the minimum pan angle (-180.0
degrees) is reached, subsequent calls to pan_left() preserve the limit
and the angle does not decrease further.\"

Input Specifications

\"Action: Repeatedly call pan_left() until the angle reaches -180.0
degrees, then call it one more time.\"

**Detailed Step**

1.  Set pan angle to -180.0 degrees.

2.  Call pan_left().

3.  Assert the return value is True.

4.  Assert get_pan_angle() is still -180.0.

Expected Result

\"pan_left() must return True, and the angle must remain -180.0
degrees.\"

Actual Result (Pass/Fail/Exception)

Pass: Pan operation was correctly blocked at the minimum limit.

Comment (including references)

Boundary condition check for minimum pan angle.

###### c. test_pan_left_disabled_camera (UT-CAM-PAN-LEFT-FAIL) {#c.-test_pan_left_disabled_camera-ut-cam-pan-left-fail .unnumbered}

|                |                                        |            |            |             |
|----------------|----------------------------------------|------------|------------|-------------|
| **Class**      | **Method**                             | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_left(), disable(), get_pan_angle() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling pan_left() on a disabled camera is rejected,
returns False, and preserves the original angle.\"

Input Specifications

Initial state: Angle 0.0. Action: camera.disable() is called.

**Detailed Step**

1.  Disable the camera.

2.  Record the initial angle.

3.  Call pan_left() and assert the return value is False.

4.  Assert the angle has not changed.

Expected Result

\"pan_left() must return False, and the angle must remain the initial
value.\"

Actual Result (Pass/Fail/Exception)

Pass: Control command was correctly blocked in the disabled state.

Comment (including references)

Security and state awareness check for control operations.

###### d. test_pan_left_device_camera_integration (UT-CAM-PAN-LEFT-INT) {#d.-test_pan_left_device_camera_integration-ut-cam-pan-left-int .unnumbered}

|                |            |            |            |             |
|----------------|------------|------------|------------|-------------|
| **Class**      | **Method** | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_left() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling pan_left() successfully executes the underlying
virtual device interaction logic and returns a boolean result,
confirming proper integration.\"

Input Specifications

Initial state: Camera is enabled and at 0.0 degrees.

**Detailed Step**

1.  Call pan_left().

2.  Assert the return value is a boolean (True) and the internal logic
    path for device interaction is executed.

Expected Result

The method must execute the device interaction path and return True.

Actual Result (Pass/Fail/Exception)

Pass: Integration with the virtual device layer for pan control was
confirmed.

Comment (including references)

Verifies the linkage between the domain model and the virtual device
simulator.

##### I. pan_right() {#i.-pan_right .unnumbered}

###### a. test_pan_right (UT-CAM-PAN-RIGHT-PASS) {#a.-test_pan_right-ut-cam-pan-right-pass .unnumbered}

|                |                              |            |            |             |
|----------------|------------------------------|------------|------------|-------------|
| **Class**      | **Method**                   | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_right(), get_pan_angle() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the pan angle is below the maximum limit, calling
pan_right() returns True and increases the angle by exactly 5.0
degrees.\"

Input Specifications

Initial state: Pan angle is 0.0 degrees. Action: Call pan_right() once.

**Detailed Step**

1.  Call pan_right().

2.  Assert the return value is True.

3.  Call get_pan_angle() and assert the new angle is 5.0 degrees.

Expected Result

\"pan_right() must return True, and the new pan_angle must be 5.0.\"

Actual Result (Pass/Fail/Exception)

Pass: Pan angle was successfully incremented.

Comment (including references)

Core function test for camera pan operation.

###### b. test_pan_right_limit (UT-CAM-PAN-RIGHT-MAX) {#b.-test_pan_right_limit-ut-cam-pan-right-max .unnumbered}

|                |                              |            |            |             |
|----------------|------------------------------|------------|------------|-------------|
| **Class**      | **Method**                   | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_right(), get_pan_angle() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the boundary condition: once the maximum pan angle (+180.0
degrees) is reached, subsequent calls to pan_right() preserve the limit
and the angle does not increase further.\"

Input Specifications

\"Action: Repeatedly call pan_right() until the angle reaches 180.0
degrees, then call it one more time.\"

**Detailed Step**

1.  Set pan angle to 180.0 degrees.

2.  Call pan_right().

3.  Assert the return value is True.

4.  Assert get_pan_angle() is still 180.0.

Expected Result

\"pan_right() must return True, and the angle must remain 180.0
degrees.\"

Actual Result (Pass/Fail/Exception)

Pass: Pan operation was correctly blocked at the maximum limit.

Comment (including references)

Boundary condition check for maximum pan angle.

###### c. test_pan_right_disabled_camera (UT-CAM-PAN-RIGHT-FAIL) {#c.-test_pan_right_disabled_camera-ut-cam-pan-right-fail .unnumbered}

|                |                                         |            |            |             |
|----------------|-----------------------------------------|------------|------------|-------------|
| **Class**      | **Method**                              | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_right(), disable(), get_pan_angle() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling pan_right() on a disabled camera is rejected,
returns False, and preserves the original angle.\"

Input Specifications

Initial state: Angle 0.0. Action: camera.disable() is called.

**Detailed Step**

1.  Disable the camera.

2.  Record the initial angle.

3.  Call pan_right() and assert the return value is False.

4.  Assert the angle has not changed.

Expected Result

\"pan_right() must return False, and the angle must remain the initial
value.\"

Actual Result (Pass/Fail/Exception)

Pass: Control command was correctly blocked in the disabled state.

Comment (including references)

Security and state awareness check for control operations.

###### d. test_pan_right_device_camera_integration (UT-CAM-PAN-RIGHT-INT) {#d.-test_pan_right_device_camera_integration-ut-cam-pan-right-int .unnumbered}

|                |             |            |            |             |
|----------------|-------------|------------|------------|-------------|
| **Class**      | **Method**  | **Author** | **Date**   | **Version** |
| SafeHomeCamera | pan_right() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling pan_right() successfully executes the underlying
virtual device interaction logic and returns a boolean result,
confirming proper integration.\"

Input Specifications

Initial state: Camera is enabled and at 0.0 degrees.

**Detailed Step**

1.  Call pan_right().

2.  Assert the return value is a boolean (True) and the internal logic
    path for device interaction is executed.

Expected Result

The method must execute the device interaction path and return True.

Actual Result (Pass/Fail/Exception)

Pass: Integration with the virtual device layer for pan control was
confirmed.

Comment (including references)

Verifies the linkage between the domain model and the virtual device
simulator.

##### J. get_password() {#j.-get_password .unnumbered}

###### a. test_get_password_not_set (UT-CAM-PW-GET-DEF) {#a.-test_get_password_not_set-ut-cam-pw-get-def .unnumbered}

|                |                |            |            |             |
|----------------|----------------|------------|------------|-------------|
| **Class**      | **Method**     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | get_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the camera password has not been initialized or
set, get_password() correctly returns an empty string (\"\"\"\").\"

Input Specifications

Initial state: No password set.

**Detailed Step**

1.  Instantiate the camera object (default state).

2.  Call get_password().

3.  Assert the returned value is \"\".

Expected Result

\"get_password() must return \"\".\"

Actual Result (Pass/Fail/Exception)

Pass: Empty string was correctly retrieved in the default state.

Comment (including references)

Basic getter functionality check for the default password state.

###### b. test_set_password (UT-CAM-PW-SET-GET) {#b.-test_set_password-ut-cam-pw-set-get .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_password(), get_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that after a successful password setting (set_password),
get_password() correctly returns the newly stored password.\"

Input Specifications

\"Action: Call set_password(\"\"mypassword123\"\").\"

**Detailed Step**

1.  Call set_password(\"mypassword123\").

2.  Assert the return value is True.

3.  Call get_password() and assert the value is \"mypassword123\".

Expected Result

\"get_password() must return \"\"mypassword123\"\".\"

Actual Result (Pass/Fail/Exception)

Pass: Password was successfully stored and retrieved.

Comment (including references)

Verification of password storage and retrieval functionality.

##### K. set_password() {#k.-set_password .unnumbered}

###### a. test_set_password (UT-CAM-PW-SET-PASS) {#a.-test_set_password-ut-cam-pw-set-pass .unnumbered}

|                |                                                |            |            |             |
|----------------|------------------------------------------------|------------|------------|-------------|
| **Class**      | **Method**                                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_password(), has_password(), get_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling set_password() with a valid password string
returns True, updates the password internally, and sets the
has_password() flag to True.\"

Input Specifications

\"Action: Call set_password(\"\"mypassword123\"\").\"

**Detailed Step**

1.  Call set_password(\"mypassword123\").

2.  Assert the return value is True.

3.  Assert has_password() is True and get_password() returns the set
    value.

Expected Result

\"set_password() must return True, and the new password must be
successfully stored.\"

Actual Result (Pass/Fail/Exception)

Pass: Password was successfully set and validated.

Comment (including references)

Core function test for password storage and retrieval.

###### b. test_set_empty_password (UT-CAM-PW-SET-EMPTY) {#b.-test_set_empty_password-ut-cam-pw-set-empty .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_password(), has_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that setting an empty string (\"\"\"\") is rejected by
set_password(), which returns False and ensures the has_password() state
remains False.\"

Input Specifications

\"Action: Call set_password(\"\"\"\").\"

**Detailed Step**

1.  Call set_password(\"\").

2.  Assert the return value is False.

3.  Assert has_password() is False and get_password() is \"\".

Expected Result

\"set_password() must return False , and no password should be set.\"

Actual Result (Pass/Fail/Exception)

Pass: Empty password setting was correctly rejected.

Comment (including references)

Input validation check for minimum password length/content.

###### c. test_set_password_special_characters (UT-CAM-PW-SET-SPEC) {#c.-test_set_password_special_characters-ut-cam-pw-set-spec .unnumbered}

|                |                |            |            |             |
|----------------|----------------|------------|------------|-------------|
| **Class**      | **Method**     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the system can successfully accept and store passwords
containing various special characters and non-standard characters,
confirming character set compatibility.\"

Input Specifications

\"Action: Call set_password with strings like \"\"!@#\$%\"\",
\"\"암호123\"\" .\"

**Detailed Step**

1.  Call set_password with a special character string.

2.  Assert the return value is True.

3.  Assert get_password() returns the exact string.

Expected Result

\"set_password() must return True, and the special character password
must be saved correctly.\"

Actual Result (Pass/Fail/Exception)

Pass: Special character passwords were successfully accepted.

Comment (including references)

Coverage test for character set compatibility in password fields.

###### d. test_set_password_long_password (UT-CAM-PW-SET-LONG) {#d.-test_set_password_long_password-ut-cam-pw-set-long .unnumbered}

|                |                |            |            |             |
|----------------|----------------|------------|------------|-------------|
| **Class**      | **Method**     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the system\'s robustness by ensuring it can successfully
accept and store a very long password (e.g., 1000 characters) without
truncation or failure.\"

Input Specifications

Action: Call set_password with a 1000-character long string.

**Detailed Step**

1.  Create a long string.

2.  Call set_password() with the long string.

3.  Assert the return value is True and get_password() returns the full,
    intact long string.

Expected Result

\"set_password() must return True, and the long password must be saved
correctly.\"

Actual Result (Pass/Fail/Exception)

Pass: Long password was successfully stored and retrieved.

Comment (including references)

Stress and robustness test for maximum password length constraints.

###### e. test_set_password_whitespace_only (UT-CAM-PW-SET-SPACE) {#e.-test_set_password_whitespace_only-ut-cam-pw-set-space .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | set_password(), get_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies how the system handles passwords consisting only of
whitespace characters, confirming the outcome (in this implementation,
it is accepted as a valid, non-empty string).\"

Input Specifications

\"Action: Call set_password(\"\" \"\") (three spaces).\"

**Detailed Step**

1.  Call set_password(\" \").

2.  Assert the return value is True.

3.  Assert get_password() returns the exact whitespace string.

Expected Result

\"set_password() must return True, and the password must be saved as
\"\" \"\".\"

Actual Result (Pass/Fail/Exception)

Pass: Whitespace-only string was accepted and stored as a valid
password.

Comment (including references)

Detailed input validation check for whitespace content.

##### L. is_enabled() {#l.-is_enabled .unnumbered}

###### a. test_is_enabled (UT-CAM-STAT-FULL) {#a.-test_is_enabled-ut-cam-stat-full .unnumbered}

|                |                                   |            |            |             |
|----------------|-----------------------------------|------------|------------|-------------|
| **Class**      | **Method**                        | **Author** | **Date**   | **Version** |
| SafeHomeCamera | is_enabled(), disable(), enable() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that is_enabled() accurately reflects the camera\'s status
through a full operational cycle: checking the initial state, switching
to disabled, and switching back to enabled.\"

Input Specifications

\"Initial state: Enabled. Actions: Call disable(), then call enable().\"

**Detailed Step**

1.  Assert initial state is True.

2.  Call disable() and assert state is False.

3.  Call enable() and assert state is True.

Expected Result

\"The sequence of is_enabled() returns must be True, then False, then
True.\"

Actual Result (Pass/Fail/Exception)

Pass: The camera state was correctly tracked throughout the cycle.

Comment (including references)

Core functionality test for state retrieval and status consistency.

###### b. test_enable (UT-CAM-STAT-EN) {#b.-test_enable-ut-cam-stat-en .unnumbered}

|                |                        |            |            |             |
|----------------|------------------------|------------|------------|-------------|
| **Class**      | **Method**             | **Author** | **Date**   | **Version** |
| SafeHomeCamera | enable(), is_enabled() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling enable() successfully transitions the camera to
the active state, as confirmed by is_enabled().\"

Input Specifications

Initial state: Camera is disabled (via disable() call). Action: Call
enable().

**Detailed Step**

1.  Set the initial state to disabled.

2.  Call enable().

3.  Assert is_enabled() returns True.

Expected Result

is_enabled() must return True after enable() is called.

Actual Result (Pass/Fail/Exception)

Pass: The camera successfully transitioned to the enabled state.

Comment (including references)

Verification of the enable setter\'s result.

###### c. test_disable (UT-CAM-STAT-DIS) {#c.-test_disable-ut-cam-stat-dis .unnumbered}

|                |                         |            |            |             |
|----------------|-------------------------|------------|------------|-------------|
| **Class**      | **Method**              | **Author** | **Date**   | **Version** |
| SafeHomeCamera | disable(), is_enabled() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling disable() successfully transitions the camera to
the inactive state, as confirmed by is_enabled().\"

Input Specifications

Initial state: Camera is enabled. Action: Call disable().

**Detailed Step**

1.  Assert initial state is True.

2.  Call disable().

3.  Assert is_enabled() returns False.

Expected Result

is_enabled() must return False after disable() is called.

Actual Result (Pass/Fail/Exception)

Pass: The camera successfully transitioned to the disabled state.

Comment (including references)

Verification of the disable setter\'s result.

###### d. test_enable_disable_toggle (UT-CAM-STAT-TOG) {#d.-test_enable_disable_toggle-ut-cam-stat-tog .unnumbered}

|                |                                   |            |            |             |
|----------------|-----------------------------------|------------|------------|-------------|
| **Class**      | **Method**                        | **Author** | **Date**   | **Version** |
| SafeHomeCamera | is_enabled(), enable(), disable() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the stability of the camera\'s enabled state by checking its
status after multiple consecutive, redundant calls to enable() and
disable().\"

Input Specifications

\"Actions: Multiple calls to disable() (3x), followed by multiple calls
to enable() (3x).\"

**Detailed Step**

1.  Call disable() multiple times. Assert state is False.

2.  Call enable() multiple times. Assert final state is True.

Expected Result

\"The state should correctly switch and persist based on the last
command, regardless of redundant calls.\"

Actual Result (Pass/Fail/Exception)

Pass: State toggling was stable across redundant commands.

Comment (including references)

Robustness check for state persistence across repeated setter calls.

##### M. enable() {#m.-enable .unnumbered}

###### a. test_enable (UT-CAM-EN-PASS) {#a.-test_enable-ut-cam-en-pass .unnumbered}

|                |                        |            |            |             |
|----------------|------------------------|------------|------------|-------------|
| **Class**      | **Method**             | **Author** | **Date**   | **Version** |
| SafeHomeCamera | enable(), is_enabled() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling enable() successfully transitions the camera
from the disabled state to the active state, as confirmed by
is_enabled().\"

Input Specifications

Initial state: Camera is first disabled. Action: Call enable().

**Detailed Step**

1.  Set the initial state to disabled.

2.  Call enable().

3.  Assert is_enabled() returns True.

Expected Result

is_enabled() must return True after enable() is called.

Actual Result (Pass/Fail/Exception)

Pass: The camera successfully transitioned to the enabled state.

Comment (including references)

Core function test for setting the camera to an active state.

###### b. test_enable_disable_toggle (UT-CAM-EN-TOG) {#b.-test_enable_disable_toggle-ut-cam-en-tog .unnumbered}

|                |                        |            |            |             |
|----------------|------------------------|------------|------------|-------------|
| **Class**      | **Method**             | **Author** | **Date**   | **Version** |
| SafeHomeCamera | enable(), is_enabled() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the stability of the enabled state by checking the status
after multiple consecutive, redundant calls to enable().\"

Input Specifications

Initial state: Camera is disabled. Action: Multiple (3x) consecutive
calls to enable().

**Detailed Step**

1.  Set the initial state to disabled.

2.  Call enable() multiple times.

3.  Assert is_enabled() returns True.

Expected Result

\"The state should consistently switch and persist as True, regardless
of redundant calls.\"

Actual Result (Pass/Fail/Exception)

\"Pass: State toggling was stable, and the enabled state persisted.\"

Comment (including references)

Robustness check for state persistence across repeated enable() calls.

##### N. disable() {#n.-disable .unnumbered}

###### a. test_disable (UT-CAM-DIS-PASS) {#a.-test_disable-ut-cam-dis-pass .unnumbered}

|                |                         |            |            |             |
|----------------|-------------------------|------------|------------|-------------|
| **Class**      | **Method**              | **Author** | **Date**   | **Version** |
| SafeHomeCamera | disable(), is_enabled() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling disable() successfully transitions the camera
from the active state to the inactive state, as confirmed by
is_enabled().\"

Input Specifications

Initial state: Camera is enabled. Action: Call disable().

**Detailed Step**

1.  Assert initial state is True.

2.  Call disable().

3.  Assert is_enabled() returns False.

Expected Result

is_enabled() must return False after disable() is called.

Actual Result (Pass/Fail/Exception)

Pass: The camera successfully transitioned to the disabled state.

Comment (including references)

Core function test for setting the camera to an inactive state.

###### b. test_display_view_disabled_camera (UT-CAM-DIS-CONSEQ) {#b.-test_display_view_disabled_camera-ut-cam-dis-conseq .unnumbered}

|                |                           |            |            |             |
|----------------|---------------------------|------------|------------|-------------|
| **Class**      | **Method**                | **Author** | **Date**   | **Version** |
| SafeHomeCamera | disable(), display_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the direct consequence of the disabled state: after calling
disable(), attempting to access the camera view (display_view()) is
correctly denied, returning None.\"

Input Specifications

Action: Call disable()., Consequence Check: Call display_view().

**Detailed Step**

1.  Call disable() to change the state.

2.  Call display_view().

3.  Assert the result is None.

Expected Result

\"display_view() must return None , confirming view access is blocked in
the disabled state.\"

Actual Result (Pass/Fail/Exception)

Pass: View access was correctly denied after disabling the camera.

Comment (including references)

Verification of the security consequence of the disabled state.

###### c. test_enable_disable_toggle (UT-CAM-DIS-TOG) {#c.-test_enable_disable_toggle-ut-cam-dis-tog .unnumbered}

|                |                         |            |            |             |
|----------------|-------------------------|------------|------------|-------------|
| **Class**      | **Method**              | **Author** | **Date**   | **Version** |
| SafeHomeCamera | disable(), is_enabled() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the stability of the disabled state by checking the status
after multiple consecutive, redundant calls to disable().\"

Input Specifications

Initial state: Camera is enabled. Action: Multiple (3x) consecutive
calls to disable().

**Detailed Step**

1.  Call disable() multiple times.

2.  Assert is_enabled() returns False.

Expected Result

\"The state should consistently switch and persist as False, regardless
of redundant calls.\"

Actual Result (Pass/Fail/Exception)

\"Pass: State toggling was stable, and the disabled state persisted.\"

Comment (including references)

Robustness check for state persistence across repeated disable() calls.

##### O. has_password() {#o.-has_password .unnumbered}

###### a. test_has_password (UT-CAM-PW-STAT-FULL) {#a.-test_has_password-ut-cam-pw-stat-full .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | has_password(), set_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that has_password() accurately reflects the camera\'s
password status: initially False, and switching to True after a valid
password is set.\"

Input Specifications

\"Initial state: No password set. Action: Call
set_password(\"\"password123\"\").\"

**Detailed Step**

1.  Assert initial state is False.

2.  Call set_password(\"password123\").

3.  Assert has_password() returns True.

Expected Result

\"The sequence of has_password() returns must be False, then True.\"

Actual Result (Pass/Fail/Exception)

Pass: Password status was correctly tracked through the lifecycle.

Comment (including references)

Core functionality test for password status retrieval.

###### b. test_set_empty_password (UT-CAM-PW-STAT-INV) {#b.-test_set_empty_password-ut-cam-pw-stat-inv .unnumbered}

|                |                                |            |            |             |
|----------------|--------------------------------|------------|------------|-------------|
| **Class**      | **Method**                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera | has_password(), set_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when an attempt to set an invalid password (empty
string) is rejected, has_password() correctly remains False, ensuring
the status is not corrupted by failed operations.\"

Input Specifications

\"Initial state: No password set. Action: Call set_password(\"\"\"\").\"

**Detailed Step**

1.  Assert initial state is False.

2.  Call set_password(\"\").

3.  Assert the return value is False.

4.  Assert has_password() remains False.

Expected Result

\"set_password() must return False, and has_password() must remain
False.\"

Actual Result (Pass/Fail/Exception)

Pass: Status was correctly preserved after the failed operation.

Comment (including references)

Validation check ensuring failed password setting attempts do not
corrupt the has_password flag.

##### P. save_info() {#p.-save_info .unnumbered}

###### a. test_save_info (UT-CAM-SAVE) {#a.-test_save_info-ut-cam-save .unnumbered}

|                |             |            |            |             |
|----------------|-------------|------------|------------|-------------|
| **Class**      | **Method**  | **Author** | **Date**   | **Version** |
| SafeHomeCamera | save_info() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the method is callable and returns True, confirming that
the logic for triggering the camera\'s information persistence (saving
its state) was successfully executed.\"

Input Specifications

None.

**Detailed Step**

1.  Call camera.save_info().

2.  Assert the return value is True.

Expected Result

save_info() must return True.

Actual Result (Pass/Fail/Exception)

Pass: The data persistence interface call succeeded.

Comment (including references)

Verification of the interface method responsible for triggering data
persistence (state saving) in the system.

#### 2. CameraController {#cameracontroller .unnumbered}

##### A. add_camera() {#a.-add_camera .unnumbered}

###### a. test_add_camera (UT-CC-ADD-SINGLE) {#a.-test_add_camera-ut-cc-add-single .unnumbered}

|                  |                  |            |            |             |
|------------------|------------------|------------|------------|-------------|
| **Class**        | **Method**       | **Author** | **Date**   | **Version** |
| CameraController | add_camera(x, y) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the successful addition of a single camera, ensuring the
correct ID (1) is assigned, the total count increments, and all internal
metadata (\_cameras, \_camera_info) is updated with the location and
enabled status.\"

Input Specifications

\"Initial state: 0 cameras. Action: Call add_camera(100, 200).\"

**Detailed Step**

1.  Call add_camera(100, 200).

2.  Assert the return value is True.

3.  Assert total count is 1 and the camera information is correctly
    registered with ID 1.

Expected Result

\"Returns True. \_total_camera_number is 1, and \_next_camera_id is 2.
Camera info (100, 200, True) is stored.\"

Actual Result (Pass/Fail/Exception)

Pass: Camera was successfully added and tracked.

Comment (including references)

Core function test for registering a new surveillance device.

###### b. test_add_multiple_cameras (UT-CC-ADD-MULTI) {#b.-test_add_multiple_cameras-ut-cc-add-multi .unnumbered}

|                  |                  |            |            |             |
|------------------|------------------|------------|------------|-------------|
| **Class**        | **Method**       | **Author** | **Date**   | **Version** |
| CameraController | add_camera(x, y) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that multiple sequential calls to add_camera() correctly handle
the ID sequencing and consistently update the total camera count and
internal tracking.

Input Specifications

Action: Call add_camera() three times with varying coordinates.

**Detailed Step**

1.  Call add_camera() three times.

2.  Assert that \_total_camera_number is 3.

3.  Assert that \_next_camera_id is 4.

4.  Verify coordinates for cameras 1, 2, and 3.

Expected Result

\"\_total_camera_number must be 3, and the next available ID must be 4.
All three cameras should be registered.\"

Actual Result (Pass/Fail/Exception)

\"Pass: Sequential camera additions were successful, and ID management
was correct.\"

Comment (including references)

Verification of internal ID management and state tracking robustness
under sequential operation.

##### B. delete_camera() {#b.-delete_camera .unnumbered}

###### a. test_delete_camera (UT-CC-DEL-PASS) {#a.-test_delete_camera-ut-cc-del-pass .unnumbered}

|                  |                   |            |            |             |
|------------------|-------------------|------------|------------|-------------|
| **Class**        | **Method**        | **Author** | **Date**   | **Version** |
| CameraController | delete_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the successful deletion of an existing camera, ensuring the
total count decreases, and the camera is removed from all internal
collections (\_cameras, \_camera_info).\"

Input Specifications

\"Initial state: Two cameras exist (IDs 1, 2). Action: Call
delete_camera(1).\"

**Detailed Step**

1.  Add two cameras.

2.  Call delete_camera(1).

3.  Assert the return value is True.

4.  Assert total count is 1 and ID 1 is no longer in the tracking lists.

Expected Result

\"Returns True. \_total_camera_number decreases by 1, and the camera ID
is removed from all internal dictionaries.\"

Actual Result (Pass/Fail/Exception)

Pass: Camera was successfully de-registered.

Comment (including references)

Core function test for camera de-registration and state update.

###### b. test_delete_nonexistent_camera (UT-CC-DEL-FAIL) {#b.-test_delete_nonexistent_camera-ut-cc-del-fail .unnumbered}

|                  |                   |            |            |             |
|------------------|-------------------|------------|------------|-------------|
| **Class**        | **Method**        | **Author** | **Date**   | **Version** |
| CameraController | delete_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling delete_camera() with a non-existent ID fails,
returns False, and ensures the controller\'s state remains unaltered.\"

Input Specifications

Initial state: 0 cameras. Action: Call delete_camera(999).

**Detailed Step**

1.  Ensure no cameras exist.

2.  Call delete_camera(999).

3.  Assert the return value is False.

4.  Assert total count remains 0.

Expected Result

\"Returns False. The internal state (e.g., \_total_camera_number) must
remain unchanged.\"

Actual Result (Pass/Fail/Exception)

Pass: Deletion of a non-existent camera was correctly rejected.

Comment (including references)

Input validation and state preservation check for deletion logic.

###### c. test_delete_camera_with_password (UT-CC-DEL-PW) {#c.-test_delete_camera_with_password-ut-cc-del-pw .unnumbered}

|                  |                   |            |            |             |
|------------------|-------------------|------------|------------|-------------|
| **Class**        | **Method**        | **Author** | **Date**   | **Version** |
| CameraController | delete_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies data consistency: when a camera with a stored password is
deleted, its entry is removed from the \_camera_passwords collection
alongside the camera object.\"

Input Specifications

Initial state: Camera ID 1 has a password set. Action: Call
delete_camera(1).

**Detailed Step**

1.  Add camera and set password.

2.  Call delete_camera(1).

3.  Assert \_camera_passwords no longer contains ID 1.

Expected Result

Returns True. ID 1 must be removed from the \_camera_passwords
dictionary.

Actual Result (Pass/Fail/Exception)

Pass: Associated password data was correctly cleaned up upon camera
deletion.

Comment (including references)

Data consistency and cleanup validation for linked attributes.

###### d. test_delete_camera_with_device_camera_stop (UT-CC-DEL-INT) {#d.-test_delete_camera_with_device_camera_stop-ut-cc-del-int .unnumbered}

|                  |                   |            |            |             |
|------------------|-------------------|------------|------------|-------------|
| **Class**        | **Method**        | **Author** | **Date**   | **Version** |
| CameraController | delete_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies integration: ensures that when a camera is deleted, the
underlying virtual device\'s stop() method is called once to correctly
shut down the device simulator.\"

Input Specifications

Initial state: Camera 1 exists with a mockable device. Action: Call
delete_camera(1).

**Detailed Step**

1.  Add camera. Patch the underlying device\'s stop method.

2.  Call delete_camera(1).

3.  Assert the mock stop method was called exactly once.

Expected Result

The underlying \_device_camera.stop() method must be called once.
Deletion returns True.

Actual Result (Pass/Fail/Exception)

Pass: Device cleanup protocol was correctly initiated.

Comment (including references)

Verification of the internal device cleanup protocol upon
de-registration.

###### e. test_delete_camera_handles_stop_exception (UT-CC-DEL-ROB) {#e.-test_delete_camera_handles_stop_exception-ut-cc-del-rob .unnumbered}

|                  |                   |            |            |             |
|------------------|-------------------|------------|------------|-------------|
| **Class**        | **Method**        | **Author** | **Date**   | **Version** |
| CameraController | delete_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies robustness: ensures that the deletion process completes
successfully (returns True) and the controller\'s state is updated, even
if the underlying device\'s stop() method throws an exception.\"

Input Specifications

Initial state: Camera 1 exists. Action: Mock the device\'s stop() method
to raise an Exception. Call delete_camera(1).

**Detailed Step**

1.  Add camera. Patch device stop() to raise an Exception.

2.  Call delete_camera(1).

3.  Assert the return value is True.

4.  Assert the camera is actually deleted (count decreased).

Expected Result

Returns True. The deletion must succeed despite the internal device
error.

Actual Result (Pass/Fail/Exception)

Pass: The system recovered from the device exception and completed the
deletion.

Comment (including references)

Robustness check for external component failure during cleanup.

##### C. enable_cameras() {#c.-enable_cameras .unnumbered}

###### a. test_enable_cameras_list (UT-CC-EN-LIST-PASS) {#a.-test_enable_cameras_list-ut-cc-en-list-pass .unnumbered}

|                  |                                |            |            |             |
|------------------|--------------------------------|------------|------------|-------------|
| **Class**        | **Method**                     | **Author** | **Date**   | **Version** |
| CameraController | enable_cameras(camera_id_list) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that calling enable_cameras() with a list of valid camera IDs
successfully switches all specified cameras to the enabled state.

Input Specifications

\"Initial state: Cameras 1 and 2 are disabled. Camera 3 is enabled.
Action: Call enable_cameras(\[1, 2\]).\"

**Detailed Step**

1.  Add 3 cameras; disable IDs 1 and 2.

2.  Call enable_cameras(\[1, 2\]).

3.  Assert the return value is True.

4.  Assert cameras 1, 2, and 3 are all enabled.

Expected Result

\"Returns True. Cameras 1 and 2 are successfully enabled, and the state
of Camera 3 is preserved as enabled.\"

Actual Result (Pass/Fail/Exception)

Pass: Bulk activation of cameras succeeded.

Comment (including references)

Core function test for bulk activation operation.

###### b. test_enable_cameras_partial_failure (UT-CC-EN-LIST-ROB) {#b.-test_enable_cameras_partial_failure-ut-cc-en-list-rob .unnumbered}

|                  |                                |            |            |             |
|------------------|--------------------------------|------------|------------|-------------|
| **Class**        | **Method**                     | **Author** | **Date**   | **Version** |
| CameraController | enable_cameras(camera_id_list) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the method\'s robustness by ensuring that it correctly
processes and enables valid cameras even if the input list contains
non-existent camera IDs, without crashing or failing the entire
operation.\"

Input Specifications

\"Initial state: Cameras 1 and 2 exist. Action: Call enable_cameras(\[1,
2, 999\]) (ID 999 does not exist).\"

**Detailed Step**

1.  Add 2 cameras.

2.  Call enable_cameras(\[1, 2, 999\]).

3.  Assert that cameras 1 and 2 are successfully enabled.

Expected Result

\"Cameras 1 and 2 must be successfully enabled, ignoring the
non-existent ID 999.\"

Actual Result (Pass/Fail/Exception)

Pass: Robustness verified; valid operations completed despite invalid
input in the list.

Comment (including references)

Robustness and error tolerance check for invalid inputs in bulk
operations.

##### D. disable_cameras() {#d.-disable_cameras .unnumbered}

###### a. test_disable_cameras_list (UT-CC-DIS-LIST-PASS) {#a.-test_disable_cameras_list-ut-cc-dis-list-pass .unnumbered}

|                  |                                 |            |            |             |
|------------------|---------------------------------|------------|------------|-------------|
| **Class**        | **Method**                      | **Author** | **Date**   | **Version** |
| CameraController | disable_cameras(camera_id_list) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that calling disable_cameras() with a list of valid camera IDs
successfully switches all specified cameras to the disabled state.

Input Specifications

\"Initial state: Cameras 1 and 2 are enabled. Action: Call
disable_cameras(\[1, 2\]).\"

**Detailed Step**

1.  Add 2 cameras; ensure both are enabled.

2.  Call disable_cameras(\[1, 2\]).

3.  Assert the return value is True.

4.  Assert cameras 1 and 2 are disabled.

Expected Result

Returns True. Cameras 1 and 2 are successfully disabled.

Actual Result (Pass/Fail/Exception)

Pass: Bulk deactivation of cameras succeeded.

Comment (including references)

Core function test for bulk deactivation operation.

###### b. test_disable_cameras_partial_failure (UT-CC-DIS-LIST-ROB) {#b.-test_disable_cameras_partial_failure-ut-cc-dis-list-rob .unnumbered}

|                  |                                 |            |            |             |
|------------------|---------------------------------|------------|------------|-------------|
| **Class**        | **Method**                      | **Author** | **Date**   | **Version** |
| CameraController | disable_cameras(camera_id_list) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the method\'s robustness by ensuring that it correctly
processes and disables valid cameras even if the input list contains
non-existent camera IDs, without failing the entire operation.\"

Input Specifications

\"Initial state: Cameras 1 and 2 exist and are enabled. Action: Call
disable_cameras(\[1, 2, 999\]) (ID 999 does not exist).\"

**Detailed Step**

1.  Add 2 cameras; ensure both are enabled.

2.  Call disable_cameras(\[1, 2, 999\]).

3.  Assert that cameras 1 and 2 are successfully disabled.

Expected Result

\"Cameras 1 and 2 must be successfully disabled, ignoring the
non-existent ID 999.\"

Actual Result (Pass/Fail/Exception)

Pass: Robustness verified; valid operations completed despite invalid
input in the list.

Comment (including references)

Robustness and error tolerance check for invalid inputs in bulk
operations.

##### E. enable_all_camera() {#e.-enable_all_camera .unnumbered}

###### a. test_enable_all_cameras (UT-CC-EN-ALL-PASS) {#a.-test_enable_all_cameras-ut-cc-en-all-pass .unnumbered}

|                  |                     |            |            |             |
|------------------|---------------------|------------|------------|-------------|
| **Class**        | **Method**          | **Author** | **Date**   | **Version** |
| CameraController | enable_all_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling enable_all_camera() successfully switches all
registered cameras to the enabled state, regardless of their previous
disabled state.\"

Input Specifications

\"Initial state: Two cameras exist, both are disabled. Action: Call
enable_all_camera().\"

**Detailed Step**

1.  Add 2 cameras; disable both.

2.  Call enable_all_camera().

3.  Assert the return value is True.

4.  Assert both cameras are enabled.

Expected Result

Returns True. All registered cameras must be successfully enabled.

Actual Result (Pass/Fail/Exception)

Pass: Global activation succeeded.

Comment (including references)

Core function test for bulk activation of all devices.

###### b. test_camera_enable_disable_workflow (UT-CC-EN-ALL-WORK) {#b.-test_camera_enable_disable_workflow-ut-cc-en-all-work .unnumbered}

|                  |                     |            |            |             |
|------------------|---------------------|------------|------------|-------------|
| **Class**        | **Method**          | **Author** | **Date**   | **Version** |
| CameraController | enable_all_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the operation of enable_all_camera() at the end of a complex
state change workflow (including individual and bulk disabling),
ensuring it correctly resets all cameras to the enabled state.\"

Input Specifications

\"Initial state: Three cameras exist. Action: Sequentially disable
various cameras, followed by a final call to enable_all_camera().\"

**Detailed Step**

1.  Add 3 cameras.

2.  Perform mixed disable/enable operations.

3.  Call disable_all_camera().

4.  Call enable_all_camera().

5.  Assert all 3 cameras are enabled.

Expected Result

All cameras must be confirmed to be in the enabled state (is_enabled()
is True).

Actual Result (Pass/Fail/Exception)

Pass: The final global enable operation correctly restored all camera
states.

Comment (including references)

Integration and consistency check across multiple bulk state changes.

##### F. disable_all_camera() {#f.-disable_all_camera .unnumbered}

###### a. test_disable_all_cameras (UT-CC-DIS-ALL-PASS) {#a.-test_disable_all_cameras-ut-cc-dis-all-pass .unnumbered}

|                  |                      |            |            |             |
|------------------|----------------------|------------|------------|-------------|
| **Class**        | **Method**           | **Author** | **Date**   | **Version** |
| CameraController | disable_all_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling disable_all_camera() successfully switches all
registered cameras to the disabled state, regardless of their previous
enabled state.\"

Input Specifications

\"Initial state: Two cameras exist, both are enabled. Action: Call
disable_all_camera().\"

**Detailed Step**

1.  Add 2 cameras; ensure both are enabled.

2.  Call disable_all_camera().

3.  Assert the return value is True.

4.  Assert both cameras are disabled.

Expected Result

Returns True. All registered cameras must be successfully disabled.

Actual Result (Pass/Fail/Exception)

Pass: Global deactivation succeeded.

Comment (including references)

Core function test for bulk deactivation of all devices.

###### b. test_camera_enable_disable_workflow (UT-CC-DIS-ALL-WORK) {#b.-test_camera_enable_disable_workflow-ut-cc-dis-all-work .unnumbered}

|                  |                      |            |            |             |
|------------------|----------------------|------------|------------|-------------|
| **Class**        | **Method**           | **Author** | **Date**   | **Version** |
| CameraController | disable_all_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the operation of disable_all_camera() within a complex state
change workflow, ensuring it correctly switches all cameras to the
disabled state after individual and bulk enabling/disabling
operations.\"

Input Specifications

\"Initial state: Three cameras exist. Action: Sequentially
disable/enable cameras, followed by a final call to
disable_all_camera().\"

**Detailed Step**

1.  Add 3 cameras.

2.  Perform mixed enable/disable operations.

3.  Call disable_all_camera().

4.  Assert all 3 cameras are disabled.

Expected Result

All cameras must be confirmed to be in the disabled state (is_enabled()
is False).

Actual Result (Pass/Fail/Exception)

Pass: The final global disable operation correctly set all camera states
to disabled.

Comment (including references)

Integration and consistency check across multiple bulk state changes.

##### G. enable_camera() {#g.-enable_camera .unnumbered}

###### a. test_enable_camera (UT-CC-EN-SINGLE-PASS) {#a.-test_enable_camera-ut-cc-en-single-pass .unnumbered}

|                  |                   |            |            |             |
|------------------|-------------------|------------|------------|-------------|
| **Class**        | **Method**        | **Author** | **Date**   | **Version** |
| CameraController | enable_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that calling enable_camera() with a valid ID successfully
transitions the specified camera from the disabled state to the active
state.

Input Specifications

Initial state: Camera ID 1 exists and is disabled. Action: Call
enable_camera(1).

**Detailed Step**

1.  Add camera and disable it.

2.  Call enable_camera(1).

3.  Assert the return value is True.

4.  Assert the camera\'s enabled state is True.

Expected Result

Returns True. The camera\'s enabled state must be True.

Actual Result (Pass/Fail/Exception)

Pass: The camera successfully transitioned to the enabled state.

Comment (including references)

Core function test for setting a single camera to an active state.

###### b. test_enable_nonexistent_camera (UT-CC-EN-SINGLE-FAIL) {#b.-test_enable_nonexistent_camera-ut-cc-en-single-fail .unnumbered}

|                  |                   |            |            |             |
|------------------|-------------------|------------|------------|-------------|
| **Class**        | **Method**        | **Author** | **Date**   | **Version** |
| CameraController | enable_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that attempting to call enable_camera() using a non-existent
ID fails, returns False, and does not alter the controller\'s state.\"

Input Specifications

Initial state: No camera with ID 999 exists. Action: Call
enable_camera(999).

**Detailed Step**

1.  Call enable_camera(999).

2.  Assert the return value is False.

Expected Result

Returns False.

Actual Result (Pass/Fail/Exception)

Pass: Request for a nonexistent camera was correctly rejected.

Comment (including references)

Input validation check for non-existent camera IDs.

##### H. disable_camera() {#h.-disable_camera .unnumbered}

###### a. test_disable_camera (UT-CC-DIS-SINGLE-PASS) {#a.-test_disable_camera-ut-cc-dis-single-pass .unnumbered}

|                  |                    |            |            |             |
|------------------|--------------------|------------|------------|-------------|
| **Class**        | **Method**         | **Author** | **Date**   | **Version** |
| CameraController | disable_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that calling disable_camera() with a valid ID successfully
transitions the specified camera from the active state to the inactive
state.

Input Specifications

Initial state: Camera ID 1 exists and is enabled. Action: Call
disable_camera(1).

**Detailed Step**

1.  Add camera and ensure it is enabled.

2.  Call disable_camera(1).

3.  Assert the return value is True.

4.  Assert the camera\'s enabled state is False.

Expected Result

Returns True. The camera\'s enabled state must be False.

Actual Result (Pass/Fail/Exception)

Pass: The camera successfully transitioned to the disabled state.

Comment (including references)

Core function test for setting a single camera to an inactive state.

###### b. test_disable_nonexistent_camera (UT-CC-DIS-SINGLE-FAIL) {#b.-test_disable_nonexistent_camera-ut-cc-dis-single-fail .unnumbered}

|                  |                    |            |            |             |
|------------------|--------------------|------------|------------|-------------|
| **Class**        | **Method**         | **Author** | **Date**   | **Version** |
| CameraController | disable_camera(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that attempting to call disable_camera() using a non-existent
ID fails, returns False, and does not alter the controller\'s state.\"

Input Specifications

Initial state: No camera with ID 999 exists. Action: Call
disable_camera(999).

**Detailed Step**

1.  Call disable_camera(999).

2.  Assert the return value is False.

Expected Result

Returns False.

Actual Result (Pass/Fail/Exception)

Pass: Request for a nonexistent camera was correctly rejected.

Comment (including references)

Input validation check for non-existent camera IDs.

##### I. control_single_camera() {#i.-control_single_camera .unnumbered}

###### a. test_control_single_camera_take_picture (UT-CC-CTRL-SNAP) {#a.-test_control_single_camera_take_picture-ut-cc-ctrl-snap .unnumbered}

|                  |                                       |            |            |             |
|------------------|---------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                            | **Author** | **Date**   | **Version** |
| CameraController | control_single_camera(id, control_id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that using control ID 0 successfully triggers the camera\'s
snapshot (take picture) functionality.

Input Specifications

\"Initial state: Camera 1 is enabled. Action: Call
control_single_camera(1, 0).\"

**Detailed Step**

1.  Add camera 1.

2.  Call control_single_camera(1, 0).

3.  Assert the return value is True.

Expected Result

Returns True. The snapshot command is correctly dispatched.

Actual Result (Pass/Fail/Exception)

Pass: Snapshot command execution succeeded.

Comment (including references)

Dispatcher test for core image capture action.

###### b. test_control_single_camera_start_recording (UT-CC-CTRL-REC-START) {#b.-test_control_single_camera_start_recording-ut-cc-ctrl-rec-start .unnumbered}

|                  |                                       |            |            |             |
|------------------|---------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                            | **Author** | **Date**   | **Version** |
| CameraController | control_single_camera(id, control_id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that using control ID 1 successfully triggers the recording
start functionality, and the camera\'s status transitions to
\"\"Recording\"\".\"

Input Specifications

\"Initial state: Camera 1 is idle. Action: Call control_single_camera(1,
1).\"

**Detailed Step**

1.  Call control_single_camera(1, 1).

2.  Assert the return value is True.

3.  Assert camera status is \"Recording\".

Expected Result

\"Returns True. Camera status is updated to \"\"Recording\"\".\"

Actual Result (Pass/Fail/Exception)

\"Pass: Recording start command succeeded, and status updated.\"

Comment (including references)

Dispatcher test for core recording start action.

###### c. test_control_single_camera_stop_recording (UT-CC-CTRL-REC-STOP) {#c.-test_control_single_camera_stop_recording-ut-cc-ctrl-rec-stop .unnumbered}

|                  |                                       |            |            |             |
|------------------|---------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                            | **Author** | **Date**   | **Version** |
| CameraController | control_single_camera(id, control_id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that using control ID 2 successfully triggers the recording
stop functionality, and the camera\'s status returns to its default
state (\"\"idle\"\").\"

Input Specifications

\"Initial state: Camera 1 is recording. Action: Call
control_single_camera(1, 2).\"

**Detailed Step**

1.  Start recording (ID 1).

2.  Call control_single_camera(1, 2).

3.  Assert the return value is True.

4.  Assert camera status is \"idle\".

Expected Result

\"Returns True. Camera status transitions away from \"\"Recording\"\".\"

Actual Result (Pass/Fail/Exception)

Pass: Recording stop command succeeded.

Comment (including references)

Dispatcher test for core recording stop action.

###### d. test_control_single_camera_pan_left (UT-CC-CTRL-PAN) {#d.-test_control_single_camera_pan_left-ut-cc-ctrl-pan .unnumbered}

|                  |                                       |            |            |             |
|------------------|---------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                            | **Author** | **Date**   | **Version** |
| CameraController | control_single_camera(id, control_id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the dispatcher correctly executes a movement command (e.g.,
pan left, using ID 0 in the coverage test\'s dispatcher context) by
checking the return value.\"

Input Specifications

\"Initial state: Camera 1 enabled. Action: Call control_single_camera(1,
0).\"

**Detailed Step**

1.  Add camera 1.

2.  Call control_single_camera(1, 0) (Pan Left).

3.  Assert the return value is True.

Expected Result

Returns True. The Pan Left command is successfully dispatched.

Actual Result (Pass/Fail/Exception)

Pass: Pan left command successfully dispatched.

Comment (including references)

Dispatcher test for movement control functionality.

###### e. test_control_disabled_camera (UT-CC-CTRL-FAIL-DIS) {#e.-test_control_disabled_camera-ut-cc-ctrl-fail-dis .unnumbered}

|                  |                                       |            |            |             |
|------------------|---------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                            | **Author** | **Date**   | **Version** |
| CameraController | control_single_camera(id, control_id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that attempting to control a disabled camera (e.g., snapshot,
ID 0) is rejected, returns False, and prevents the execution of the
command.\"

Input Specifications

\"Initial state: Camera 1 is disabled. Action: Call
control_single_camera(1, 0).\"

**Detailed Step**

1.  Disable camera 1.

2.  Call control_single_camera(1, 0).

3.  Assert the return value is False.

Expected Result

Returns False.

Actual Result (Pass/Fail/Exception)

Pass: Control command was correctly rejected in the disabled state.

Comment (including references)

Security validation check for controlling inactive devices.

###### f. test_control_nonexistent_camera (UT-CC-CTRL-FAIL-NON) {#f.-test_control_nonexistent_camera-ut-cc-ctrl-fail-non .unnumbered}

|                  |                                       |            |            |             |
|------------------|---------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                            | **Author** | **Date**   | **Version** |
| CameraController | control_single_camera(id, control_id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that attempting to control a non-existent camera ID is
rejected, returns False, and prevents the dispatcher from executing.\"

Input Specifications

\"Action: Call control_single_camera(999, 0) (ID 999 does not exist).\"

**Detailed Step**

1.  Call control_single_camera(999, 0).

2.  Assert the return value is False.

Expected Result

Returns False.

Actual Result (Pass/Fail/Exception)

Pass: Command was correctly rejected for a non-existent ID.

Comment (including references)

Input validation check for camera existence.

###### g. test_control_invalid_control_id (UT-CC-CTRL-FAIL-INV) {#g.-test_control_invalid_control_id-ut-cc-ctrl-fail-inv .unnumbered}

|                  |                                       |            |            |             |
|------------------|---------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                            | **Author** | **Date**   | **Version** |
| CameraController | control_single_camera(id, control_id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that providing an undefined or invalid control_id (e.g., 99)
is rejected by the dispatcher, returning False.\"

Input Specifications

\"Initial state: Camera 1 exists. Action: Call control_single_camera(1,
99).\"

**Detailed Step**

1.  Add camera 1.

2.  Call control_single_camera(1, 99).

3.  Assert the return value is False.

Expected Result

Returns False.

Actual Result (Pass/Fail/Exception)

Pass: Command was rejected due to an invalid control ID.

Comment (including references)

Dispatcher validation check for command ID range and definition.

##### J. display_thumbnail_view() {#j.-display_thumbnail_view .unnumbered}

###### a. test_display_thumbnail_view_no_cameras (UT-CC-THUMB-EMPTY) {#a.-test_display_thumbnail_view_no_cameras-ut-cc-thumb-empty .unnumbered}

|                  |                          |            |            |             |
|------------------|--------------------------|------------|------------|-------------|
| **Class**        | **Method**               | **Author** | **Date**   | **Version** |
| CameraController | display_thumbnail_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that calling display_thumbnail_view() when no cameras are
registered gracefully handles the empty list edge case by returning
None.

Input Specifications

Initial state: 0 cameras registered. Action: Call
display_thumbnail_view().

**Detailed Step**

1.  Ensure the controller is empty.

2.  Call display_thumbnail_view().

3.  Assert the return value is None.

Expected Result

Returns None.

Actual Result (Pass/Fail/Exception)

Pass: Empty state was handled correctly.

Comment (including references)

Input validation check for the empty list edge case.

###### b. test_display_thumbnail_view_with_multiple_cameras (UT-CC-THUMB-MULTI) {#b.-test_display_thumbnail_view_with_multiple_cameras-ut-cc-thumb-multi .unnumbered}

|                  |                          |            |            |             |
|------------------|--------------------------|------------|------------|-------------|
| **Class**        | **Method**               | **Author** | **Date**   | **Version** |
| CameraController | display_thumbnail_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling display_thumbnail_view() when multiple cameras
exist successfully initiates the composite view generation, returning a
valid image object or None if image files are unavailable.\"

Input Specifications

Initial state: 3 enabled cameras exist. Action: Call
display_thumbnail_view().

**Detailed Step**

1.  Add 3 cameras.

2.  Call display_thumbnail_view().

3.  Assert the result is None or an instance of PIL.Image.Image.

Expected Result

\"Returns a non-null object or None, confirming the operation succeeds
without crashing.\"

Actual Result (Pass/Fail/Exception)

Pass: Composite view generation succeeded.

Comment (including references)

Core functionality test for generating the composite thumbnail view.

###### c. test_display_thumbnail_view_with_mixed_cameras (UT-CC-THUMB-MIXED) {#c.-test_display_thumbnail_view_with_mixed_cameras-ut-cc-thumb-mixed .unnumbered}

|                  |                                            |            |            |             |
|------------------|--------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                 | **Author** | **Date**   | **Version** |
| CameraController | display_thumbnail_view(), disable_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when a mix of enabled and disabled cameras exists, the
thumbnail view correctly processes only the active cameras for
composition.\"

Input Specifications

Initial state: 3 cameras exist; Camera 1 is disabled. Action: Call
display_thumbnail_view().

**Detailed Step**

1.  Add 3 cameras.

2.  Disable Camera 1.

3.  Call display_thumbnail_view().

4.  Assert the operation succeeds (returns image or None), implying only
    enabled cameras were used.

Expected Result

\"Returns a non-null object or None, confirming the operation succeeds
and correctly handles disabled camera filtering.\"

Actual Result (Pass/Fail/Exception)

Pass: State awareness verified; view composition succeeded with mixed
camera states.

Comment (including references)

State awareness check for view composition (only enabled cameras should
contribute).

###### d. test_display_thumbnail_view_grid_calculation (UT-CC-THUMB-GRID) {#d.-test_display_thumbnail_view_grid_calculation-ut-cc-thumb-grid .unnumbered}

|                  |                          |            |            |             |
|------------------|--------------------------|------------|------------|-------------|
| **Class**        | **Method**               | **Author** | **Date**   | **Version** |
| CameraController | display_thumbnail_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the internal logic correctly calculates the grid
dimensions and processes the view generation for varying numbers of
cameras (e.g., 1, 3, 4), ensuring the layout is handled correctly.\"

Input Specifications

\"Sequential actions adding 1, 3, and 4 cameras and calling
display_thumbnail_view() after each addition.\"

**Detailed Step**

1.  Add 1 camera, call view.

2.  Add 2 more (total 3), call view.

3.  Add 1 more (total 4), call view.

4.  Assert all calls succeed.

Expected Result

\"The function must execute successfully for varying camera counts
without error, validating internal grid dimension calculations.\"

Actual Result (Pass/Fail/Exception)

Pass: Grid calculation logic passed for varying camera counts.

Comment (including references)

Coverage test for internal thumbnail layout/grid dimension calculations.

##### K. display_single_view() {#k.-display_single_view .unnumbered}

###### a. test_display_single_view (UT-CC-VIEW-SINGLE-PASS) {#a.-test_display_single_view-ut-cc-view-single-pass .unnumbered}

|                  |                         |            |            |             |
|------------------|-------------------------|------------|------------|-------------|
| **Class**        | **Method**              | **Author** | **Date**   | **Version** |
| CameraController | display_single_view(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling display_single_view() with a valid ID
successfully retrieves the view from the specified, enabled camera.\"

Input Specifications

Initial state: Camera 1 exists and is enabled. Action: Call
display_single_view(1).

**Detailed Step**

1.  Add camera 1.

2.  Call display_single_view(1).

3.  Assert the result is a non-null image object or None if image files
    are unavailable.

Expected Result

\"Returns a valid PIL.Image.Image object or None, confirming the
operation succeeds.\"

Actual Result (Pass/Fail/Exception)

Pass: Single view retrieval succeeded.

Comment (including references)

Core functionality test for retrieving a single camera feed.

###### b. test_display_single_view_disabled_camera (UT-CC-VIEW-SINGLE-FAIL-DIS) {#b.-test_display_single_view_disabled_camera-ut-cc-view-single-fail-dis .unnumbered}

|                  |                                           |            |            |             |
|------------------|-------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                | **Author** | **Date**   | **Version** |
| CameraController | display_single_view(id), disable_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that attempting to display the view of a disabled camera is
rejected, returning None, thus enforcing the security policy.\"

Input Specifications

Initial state: Camera 1 is disabled. Action: Call
display_single_view(1).

**Detailed Step**

1.  Disable camera 1.

2.  Call display_single_view(1).

3.  Assert the result is None.

Expected Result

Returns None.

Actual Result (Pass/Fail/Exception)

Pass: View access was correctly denied due to the disabled state.

Comment (including references)

Security validation check for view access control in a disabled state.

###### c. test_display_single_view_nonexistent_camera (UT-CC-VIEW-SINGLE-FAIL-NON) {#c.-test_display_single_view_nonexistent_camera-ut-cc-view-single-fail-non .unnumbered}

|                  |                         |            |            |             |
|------------------|-------------------------|------------|------------|-------------|
| **Class**        | **Method**              | **Author** | **Date**   | **Version** |
| CameraController | display_single_view(id) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that attempting to display the view of a non-existent camera
ID is correctly rejected, returning None.\"

Input Specifications

Action: Call display_single_view(999) (ID 999 does not exist).

**Detailed Step**

1.  Ensure no camera with ID 999 exists.

2.  Call display_single_view(999).

3.  Assert the result is None.

Expected Result

Returns None.

Actual Result (Pass/Fail/Exception)

Pass: Request for a nonexistent camera was correctly rejected.

Comment (including references)

Input validation check for non-existent camera IDs.

##### L. get_all_camera_info() {#l.-get_all_camera_info .unnumbered}

###### a. test_get_all_camera_info_empty (UT-CC-INFO-EMPTY) {#a.-test_get_all_camera_info_empty-ut-cc-info-empty .unnumbered}

|                  |                       |            |            |             |
|------------------|-----------------------|------------|------------|-------------|
| **Class**        | **Method**            | **Author** | **Date**   | **Version** |
| CameraController | get_all_camera_info() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that calling get_all_camera_info() when no cameras are
registered gracefully handles the empty controller edge case by
returning an empty list (\[\]).\"

Input Specifications

Initial state: 0 cameras registered. Action: Call get_all_camera_info().

**Detailed Step**

1.  Ensure the controller is empty.

2.  Call get_all_camera_info().

3.  Assert the returned value is \[\].

Expected Result

Returns \[\].

Actual Result (Pass/Fail/Exception)

Pass: Empty state was handled correctly.

Comment (including references)

Input validation check for the empty controller edge case.

###### b. test_get_all_camera_info (UT-CC-INFO-PASS) {#b.-test_get_all_camera_info-ut-cc-info-pass .unnumbered}

|                  |                       |            |            |             |
|------------------|-----------------------|------------|------------|-------------|
| **Class**        | **Method**            | **Author** | **Date**   | **Version** |
| CameraController | get_all_camera_info() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the method correctly retrieves the info list for all
registered cameras, including their ID, location, and enabled status.\"

Input Specifications

\"Initial state: 2 cameras exist (IDs 1, 2). Action: Call
get_all_camera_info().\"

**Detailed Step**

1.  Add 2 cameras.

2.  Call get_all_camera_info().

3.  Assert the list length is 2 and check the coordinates and enabled
    status (1) of the returned info.

Expected Result

\"Returns a list of length 2, where each element contains the correct
\[ID, X, Y, Enabled Status\].\"

Actual Result (Pass/Fail/Exception)

Pass: Global status information was correctly retrieved.

Comment (including references)

Core functionality test for retrieving global camera status.

###### c. test_get_all_camera_info_sorted_order (UT-CC-INFO-ORDER) {#c.-test_get_all_camera_info_sorted_order-ut-cc-info-order .unnumbered}

|                  |                       |            |            |             |
|------------------|-----------------------|------------|------------|-------------|
| **Class**        | **Method**            | **Author** | **Date**   | **Version** |
| CameraController | get_all_camera_info() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the camera information list is returned in a
predictable, sorted order based on the Camera ID, ensuring reliable data
display sequence.\"

Input Specifications

\"Initial state: 3 cameras added, possibly in non-sequential order if
IDs were deleted/reused (though IDs are sequential here). Action: Call
get_all_camera_info().\"

**Detailed Step**

1.  Add 3 cameras.

2.  Call get_all_camera_info().

3.  Extract the IDs from the returned list and assert they are in
    numerical ascending order.

Expected Result

\"The list of camera IDs in the output must be sorted numerically (e.g.,
\[1, 2, 3\]).\"

Actual Result (Pass/Fail/Exception)

Pass: Data ordering was confirmed to be reliable.

Comment (including references)

Integrity check for reliable data display ordering (sorting by ID).

##### M. set_camera_password() {#m.-set_camera_password .unnumbered}

###### a. test_set_camera_password (UT-CC-PW-SET-PASS) {#a.-test_set_camera_password-ut-cc-pw-set-pass .unnumbered}

|                  |                                         |            |            |             |
|------------------|-----------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                              | **Author** | **Date**   | **Version** |
| CameraController | set_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that a valid password is successfully set for an existing
camera, correctly updating the internal \_camera_passwords collection.\"

Input Specifications

\"Initial state: Camera 1 exists. Action: Call set_camera_password(1,
\"\"password123\"\").\"

**Detailed Step**

1.  Add camera 1.

2.  Call set_camera_password(1, \"password123\").

3.  Assert that ID 1 is present in \_camera_passwords with the correct
    value.

Expected Result

\"ID 1 must be present in \_camera_passwords with the value
\"\"password123\"\".\"

Actual Result (Pass/Fail/Exception)

Pass: Password was successfully assigned to the camera.

Comment (including references)

Core function test for password assignment and internal data
consistency.

###### b. test_set_password_nonexistent_camera (UT-CC-PW-SET-FAIL-NON) {#b.-test_set_password_nonexistent_camera-ut-cc-pw-set-fail-non .unnumbered}

|                  |                                         |            |            |             |
|------------------|-----------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                              | **Author** | **Date**   | **Version** |
| CameraController | set_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that attempting to set a password for a non-existent camera
ID is rejected, ensuring no unintended entries are created in the
internal collection.\"

Input Specifications

\"Initial state: 0 cameras exist. Action: Call set_camera_password(999,
\"\"password123\"\").\"

**Detailed Step**

1.  Call set_camera_password(999, \"password123\").

2.  Assert that ID 999 is not present in \_camera_passwords.

Expected Result

ID 999 must not be found in the \_camera_passwords dictionary.

Actual Result (Pass/Fail/Exception)

Pass: Password setting for a non-existent camera was correctly ignored.

Comment (including references)

Input validation check for camera existence prior to password
assignment.

###### c. test_set_camera_password_nonexistent_camera_handling (UT-CC-PW-SET-ROB) {#c.-test_set_camera_password_nonexistent_camera_handling-ut-cc-pw-set-rob .unnumbered}

|                  |                                         |            |            |             |
|------------------|-----------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                              | **Author** | **Date**   | **Version** |
| CameraController | set_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the system\'s robustness by ensuring that attempting to set a
password for a non-existent camera ID does not raise an unhandled
exception, confirming graceful failure.\"

Input Specifications

\"Action: Call set_camera_password(999, \"\"password123\"\") and monitor
for exceptions.\"

**Detailed Step**

1.  Call set_camera_password(999, \"password123\") within a try/except
    block (or implicitly check for raised exceptions).

2.  Assert that the process completes without raising an Exception.

Expected Result

The method must complete successfully (without crashing).

Actual Result (Pass/Fail/Exception)

Pass: Robustness verified; the process handled the invalid ID
gracefully.

Comment (including references)

Coverage check for robust handling of invalid IDs during password
assignment.

##### N. validate_camera_password() {#n.-validate_camera_password .unnumbered}

###### a. test_validate_camera_password_success (UT-CC-PW-VAL-PASS) {#a.-test_validate_camera_password_success-ut-cc-pw-val-pass .unnumbered}

|                  |                                              |            |            |             |
|------------------|----------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                   | **Author** | **Date**   | **Version** |
| CameraController | validate_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when the correct password is provided for a set camera,
the function returns the success code (0).\"

Input Specifications

\"Initial state: Camera 1 password set to \"\"password123\"\". Action:
Call validate_camera_password(1, \"\"password123\"\").\"

**Detailed Step**

1.  Set password for camera 1.

2.  Call validate_camera_password(1, \"password123\").

3.  Assert the returned code is 0.

Expected Result

Returns 0 (Success).

Actual Result (Pass/Fail/Exception)

Pass: Correct password validation succeeded.

Comment (including references)

Core function test for password validation success path.

###### b. test_validate_camera_password_failure (UT-CC-PW-VAL-FAIL) {#b.-test_validate_camera_password_failure-ut-cc-pw-val-fail .unnumbered}

|                  |                                              |            |            |             |
|------------------|----------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                   | **Author** | **Date**   | **Version** |
| CameraController | validate_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that when an incorrect password is provided for a set camera,
the function returns the password mismatch code (1).\"

Input Specifications

\"Initial state: Camera 1 password set to \"\"password123\"\". Action:
Call validate_camera_password(1, \"\"wrongpassword\"\").\"

**Detailed Step**

1.  Set password for camera 1.

2.  Call validate_camera_password(1, \"wrongpassword\").

3.  Assert the returned code is 1.

Expected Result

Returns 1 (Mismatch/Failure).

Actual Result (Pass/Fail/Exception)

Pass: Incorrect password validation failed as expected.

Comment (including references)

Validation test for the password mismatch path.

###### c. test_validate_camera_password_nonexistent_camera (UT-CC-PW-VAL-NON) {#c.-test_validate_camera_password_nonexistent_camera-ut-cc-pw-val-non .unnumbered}

|                  |                                              |            |            |             |
|------------------|----------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                   | **Author** | **Date**   | **Version** |
| CameraController | validate_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that attempting to validate a password for a non-existent
camera ID returns the camera not found code (-1).

Input Specifications

\"Initial state: Camera 999 does not exist. Action: Call
validate_camera_password(999, \"\"any\"\").\"

**Detailed Step**

1.  Call validate_camera_password(999, \"password123\").

2.  Assert the returned code is -1.

Expected Result

Returns -1 (Camera Not Found).

Actual Result (Pass/Fail/Exception)

Pass: Correct error code was returned for the nonexistent ID.

Comment (including references)

Security check for handling validation attempts on nonexistent
resources.

###### d. test_validate_camera_password_not_set (UT-CC-PW-VAL-UNSET) {#d.-test_validate_camera_password_not_set-ut-cc-pw-val-unset .unnumbered}

|                  |                                              |            |            |             |
|------------------|----------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                   | **Author** | **Date**   | **Version** |
| CameraController | validate_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that validating a camera that exists but has no password set
returns the password not set code (-2).

Input Specifications

\"Initial state: Camera 1 exists but has no password set. Action: Call
validate_camera_password(1, \"\"any\"\").\"

**Detailed Step**

1.  Add camera 1.

2.  Call validate_camera_password(1, \"password123\").

3.  Assert the returned code is -2.

Expected Result

Returns -2 (Password Not Set).

Actual Result (Pass/Fail/Exception)

Pass: Correct error code was returned for the unset password state.

Comment (including references)

Validation check for the initial state of the password attribute.

###### e. test_validate_camera_password_edge_cases (UT-CC-PW-VAL-EDGE) {#e.-test_validate_camera_password_edge_cases-ut-cc-pw-val-edge .unnumbered}

|                  |                                              |            |            |             |
|------------------|----------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                   | **Author** | **Date**   | **Version** |
| CameraController | validate_camera_password(id, input_password) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the security logic when an empty string (\"\"\"\") is
provided as the input password for a camera that has a password set
(should fail with mismatch code 1).\"

Input Specifications

\"Initial state: Camera 1 password set to \"\"test\"\". Action: Call
validate_camera_password(1, \"\"\"\").\"

**Detailed Step**

1.  Set password for camera 1 to \"test\".

2.  Call validate_camera_password(1, \"\").

3.  Assert the returned code is 1.

Expected Result

Returns 1 (Mismatch/Failure).

Actual Result (Pass/Fail/Exception)

Pass: Empty input was correctly handled as a failed validation attempt.

Comment (including references)

Coverage test for security logic on empty string input against a set
password.

##### O. delete_camera_password() {#o.-delete_camera_password .unnumbered}

###### a. test_delete_camera_with_password (UT-CC-PW-DEL-IMPL) {#a.-test_delete_camera_with_password-ut-cc-pw-del-impl .unnumbered}

|                  |                                                                   |            |            |             |
|------------------|-------------------------------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                                        | **Author** | **Date**   | **Version** |
| CameraController | delete_camera_password() (Implicitly verified by delete_camera()) | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies data consistency: when a camera with a stored password is
deleted, the underlying password removal logic is executed, ensuring the
entry is removed from the \_camera_passwords collection.\"

Input Specifications

Initial state: Camera ID 1 has a password set. Action: Call
delete_camera(1).

**Detailed Step**

1.  Add camera and set password.

2.  Call delete_camera(1).

3.  Assert the password entry for ID 1 is no longer present in
    \_camera_passwords.

Expected Result

\"Camera deletion must return True, and the associated password data
must be successfully removed.\"

Actual Result (Pass/Fail/Exception)

Pass: Associated password data was correctly cleaned up upon camera
deletion.

Comment (including references)

\"Verification of internal data cleanup and consistency, confirming the
password removal logic is executed as part of the de-registration
process.\"

## **3. Security** {#security .unnumbered}

### A. Alarm Core (SecuritySystem) {#a.-alarm-core-securitysystem .unnumbered}

| ID         | File:Line                            | Test                                                  | Scenario & Inputs                                                     | Expected Result                                       | Traceability        |
|------------|--------------------------------------|-------------------------------------------------------|-----------------------------------------------------------------------|-------------------------------------------------------|---------------------|
| UT-SEC-001 | security/test_security_system.py:70  | test_arm_disarm_basic                                 | Validates 'Arm disarm basic' behavior                                 | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-002 | security/test_security_system.py:83  | test_entry_delay_disarm_prevents_alarm                | Validates 'Entry delay disarm prevents alarm' behavior                | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-003 | security/test_security_system.py:107 | test_entry_delay_expires_triggers_alarm               | Validates 'Entry delay expires triggers alarm' behavior               | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-004 | security/test_security_system.py:127 | test_home_mode_door_triggers_delay_but_motion_ignored | Validates 'Home mode door triggers delay but motion ignored' behavior | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-005 | security/test_security_system.py:159 | test_home_mode_motion_ignored                         | Validates 'Home mode motion ignored' behavior                         | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-006 | security/test_security_system.py:179 | test_away_mode_motion_triggers_entry_delay_and_alarm  | Validates 'Away mode motion triggers entry delay and alarm' behavior  | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-007 | security/test_security_system.py:202 | test_zone_specific_arming_blocks_other_zones          | Validates 'Zone specific arming blocks other zones' behavior          | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-008 | security/test_security_system.py:236 | test_readiness_check_blocks_arming_when_door_open     | Validates 'Readiness check blocks arming when door open' behavior     | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |
| UT-SEC-009 | security/test_security_system.py:254 | test_trigger_panic_from_disarmed                      | Validates 'Trigger panic from disarmed' behavior                      | Pass: observed state/response matches SDS/SRS design. | SRS UC2 / SDS VI.2d |

For every alarm branch in `security/security_system.py`, there is a
corresponding test with explicit inputs:
`security/test_security_system.py:107` opens a DOOR sensor and advances
the fake clock past the entry delay to prove `SecuritySystem.tick`
raises the siren. `security/test_security_system.py:159` switches to
STAY mode, emits a motion event, and asserts the motion-only sub-test
leaves the system idle. `security/test_security_system.py:202`
introduces two zones to show that arming a subset keeps the inactive
zone silent. Finally, the readiness guard at
`security/test_security_system.py:236` prevents arming when a door
reports OPEN, matching SDS readiness diagrams.

**Per-test detail (UT-SEC)**

#### 1. `test_arm_disarm_basic` {#test_arm_disarm_basic .unnumbered}

| Field   | Value          |
|---------|----------------|
| Class   | SecuritySystem |
| Method  | arm / disarm   |
| Author  | Jonghwa An     |
| Date    | 2025-11-25     |
| Version | 2.0.0          |

**Test Case Description**  
Validates the happy path of arming then disarming with no sensor
activity.

**Input Specifications**  
- Call `arm(SecurityMode.AWAY)` followed by `disarm()`.

**Expected Result**  
- Mode transitions DISARMED ??AWAY ??DISARMED.  
- Siren remains off.

**Actual Result (Pass/Fail/Exception)**  
- Pass: FSM transitions recorded; no alarms fired.

**Comment (including references)**  
SRS UC2a; SDS VI.2d base flow.

#### 2. `test_entry_delay_disarm_prevents_alarm` {#test_entry_delay_disarm_prevents_alarm .unnumbered}

| Field   | Value                        |
|---------|------------------------------|
| Class   | SecuritySystem               |
| Method  | handle_sensor_event / disarm |
| Author  | Jonghwa An                   |
| Date    | 2025-11-25                   |
| Version | 2.0.0                        |

**Test Case Description**  
Ensures disarming during ENTRY_DELAY suppresses alarm activation.

**Input Specifications**  
- Arm AWAY, trigger door sensor, advance clock but call `disarm()`
before delay expires.

**Expected Result**  
- Countdown cancelled, state returns to DISARMED, no monitoring call.

**Actual Result (Pass/Fail/Exception)**  
- Pass: timer cleared and `alarm_state` never reaches ALARM_ACTIVE.

**Comment (including references)**  
SRS UC2c alternate; SDS VI.2d entry delay.

#### 3. `test_entry_delay_expires_triggers_alarm` {#test_entry_delay_expires_triggers_alarm .unnumbered}

| Field   | Value          |
|---------|----------------|
| Class   | SecuritySystem |
| Method  | tick           |
| Author  | Jonghwa An     |
| Date    | 2025-11-25     |
| Version | 2.0.0          |

**Test Case Description**  
Confirms that failing to disarm within the delay causes an alarm.

**Input Specifications**  
- Arm AWAY, trigger sensor, advance fake clock beyond configured delay.

**Expected Result**  
- `alarm_state` becomes `ALARM_ACTIVE`, siren + monitoring triggered.

**Actual Result (Pass/Fail/Exception)**  
- Pass: siren mock activated; monitoring stub records INTRUSION.

**Comment (including references)**  
SRS UC2c main flow; SDS VI.2d timing.

#### 4. `test_home_mode_door_triggers_delay_but_motion_ignored` {#test_home_mode_door_triggers_delay_but_motion_ignored .unnumbered}

| Field   | Value               |
|---------|---------------------|
| Class   | SecuritySystem      |
| Method  | handle_sensor_event |
| Author  | Jonghwa An          |
| Date    | 2025-11-25          |
| Version | 2.0.0               |

**Test Case Description**  
Home/STAY should watch perimeter sensors but ignore interior motion.

**Input Specifications**  
- Arm STAY, trigger door sensor then motion sensor.

**Expected Result**  
- Door event enters ENTRY_DELAY; motion event ignored.

**Actual Result (Pass/Fail/Exception)**  
- Pass: logs show door countdown, motion produces no change.

**Comment (including references)**  
SRS UC2b selective arming; SDS VI.2f zone handling.

#### 5. `test_home_mode_motion_ignored` {#test_home_mode_motion_ignored .unnumbered}

| Field   | Value               |
|---------|---------------------|
| Class   | SecuritySystem      |
| Method  | handle_sensor_event |
| Author  | Jonghwa An          |
| Date    | 2025-11-25          |
| Version | 2.0.0               |

**Test Case Description**  
Reinforces that interior-only events never change state under STAY.

**Input Specifications**  
- With STAY armed, emit motion event only.

**Expected Result**  
- State stays STAY; no timers started.

**Actual Result (Pass/Fail/Exception)**  
- Pass: `_pending_entry_delay` remains `None`.

**Comment (including references)**  
SRS UC2b alt; SDS VI.2f.

#### 6. `test_away_mode_motion_triggers_entry_delay_and_alarm` {#test_away_mode_motion_triggers_entry_delay_and_alarm .unnumbered}

| Field   | Value                      |
|---------|----------------------------|
| Class   | SecuritySystem             |
| Method  | handle_sensor_event / tick |
| Author  | Jonghwa An                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**  
Ensures motion sensors participate when the system is AWAY.

**Input Specifications**  
- Arm AWAY, emit motion event, advance time beyond delay.

**Expected Result**  
- Entry delay engaged then escalates to ALARM_ACTIVE.

**Actual Result (Pass/Fail/Exception)**  
- Pass: siren triggered and monitoring notified.

**Comment (including references)**  
SRS UC2d; SDS VI.2d AWAY branch.

#### 7. `test_zone_specific_arming_blocks_other_zones` {#test_zone_specific_arming_blocks_other_zones .unnumbered}

| Field   | Value              |
|---------|--------------------|
| Class   | SecuritySystem     |
| Method  | arm_selected_zones |
| Author  | Jonghwa An         |
| Date    | 2025-11-25         |
| Version | 2.0.0              |

**Test Case Description**  
Verifies that when arming subset of zones, other zones remain idle.

**Input Specifications**  
- Arm `["Front Door"]`, emit event from unarmed zone.

**Expected Result**  
- Unarmed zone events ignored; armed zone event triggers delay.

**Actual Result (Pass/Fail/Exception)**  
- Pass: `_armed_zones` filter enforces behavior.

**Comment (including references)**  
SRS UC2b; SDS VI.2f zone assignments.

#### 8. `test_readiness_check_blocks_arming_when_door_open` {#test_readiness_check_blocks_arming_when_door_open .unnumbered}

| Field   | Value          |
|---------|----------------|
| Class   | SecuritySystem |
| Method  | arm            |
| Author  | Jonghwa An     |
| Date    | 2025-11-25     |
| Version | 2.0.0          |

**Test Case Description**  
Readiness logic should refuse to arm when sensors report open/active.

**Input Specifications**  
- Mark door sensor OPEN, attempt `arm(SecurityMode.AWAY)`.

**Expected Result**  
- Returns `False`, readiness warning issued, state remains DISARMED.

**Actual Result (Pass/Fail/Exception)**  
- Pass: `arm` rejects request and records readiness issue.

**Comment (including references)**  
SRS UC2f readiness; SDS VI.2d guard.

#### 9. `test_trigger_panic_from_disarmed` {#test_trigger_panic_from_disarmed .unnumbered}

| Field   | Value          |
|---------|----------------|
| Class   | SecuritySystem |
| Method  | trigger_panic  |
| Author  | Jonghwa An     |
| Date    | 2025-11-25     |
| Version | 2.0.0          |

**Test Case Description**  
Confirms panic operates even when system is DISARMED.

**Input Specifications**  
- With DISARMED state, call `trigger_panic()`.

**Expected Result**  
- Immediate `ALARM_ACTIVE`, monitoring reason PANIC, siren activated.

**Actual Result (Pass/Fail/Exception)**  
- Pass: logs show panic escalation without entry delay.

**Comment (including references)**  
SRS UC2g; SDS VI.2h panic wiring.

### B. Lifecycle {#b.-lifecycle .unnumbered}

#### 1. System {#system .unnumbered}

##### A. turn_on() {#a.-turn_on .unnumbered}

###### a. test_turn_on_from_off_state (LT-001) {#a.-test_turn_on_from_off_state-lt-001 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that calling turn_on() when system is OFF results in successful
initialization and system state becomes READY.

**Input Specifications**

- System is in OFF state (initial state after constructor)

**Detailed Step**

1.  Instantiate System (initially OFF).

2.  Call turn_on().

3.  Verify return value and system state.

**Expected Result**

- turn_on() returns True

- system_state becomes SystemState.READY

- All core components are initialized (not None)

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on from off state\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Sequence Diagram on Turn the
System On, SDS

###### b. test_turn_on_when_already_running (LT-002) {#b.-test_turn_on_when_already_running-lt-002 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that calling turn_on() when system is already running returns
False and does not reinitialize components.

**Input Specifications**

- System is already in READY state (turn_on() called previously)

**Detailed Step**

1.  Ensure system is READY.

2.  Call turn_on() again.

**Expected Result**

- turn_on() returns False

- system_state remains READY (or current state)

- No exception is raised

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on when already running\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Error handling in Turn the
System On flow

###### c. test_turn_on_initializes_storage_manager (LT-003) {#c.-test_turn_on_initializes_storage_manager-lt-003 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that StorageManager is properly initialized and connected to
the database during system turn_on.

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Call turn_on().

2.  Inspect system.storage_manager.

**Expected Result**

- StorageManager is created

- Database connection is established

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on initializes storage manager\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Phase 5 (StorageManager) in Turn
the System On sequence

###### d. test_turn_on_initializes_configuration_manager (LT-004) {#d.-test_turn_on_initializes_configuration_manager-lt-004 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that ConfigurationManager is properly initialized with
SafeHomeModes, SafetyZones, and SystemSettings.

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Call turn_on().

2.  Inspect system.configuration_manager.

**Expected Result**

- ConfigurationManager is created

- SystemSettings are accessible

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on initializes configuration manager\' behavior
matched lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Phase 4-7 in Turn the System On
sequence

###### e. test_turn_on_initializes_login_manager (LT-005) {#e.-test_turn_on_initializes_login_manager-lt-005 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that LoginManager is properly initialized during turn_on.

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Call turn_on().

2.  Inspect system.login_manager and default accounts.

**Expected Result**

- LoginManager is created

- Default admin account exists

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on initializes login manager\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Phase 9 (LoginManager) in Turn
the System On sequence

###### f. test_turn_on_initializes_log_manager (LT-006) {#f.-test_turn_on_initializes_log_manager-lt-006 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that LogManager is properly initialized and logs the
SYSTEM_START event.

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Call turn_on().

2.  Check logs for SYSTEM_START event.

**Expected Result**

- LogManager is created

- SYSTEM_START event is logged

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on initializes log manager\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Phase 8 (LogManager) in Turn the
System On sequence

###### g. test_turn_on_initializes_security_system (LT-007) {#g.-test_turn_on_initializes_security_system-lt-007 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that SecuritySystem is properly initialized with alarm and
siren components.

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Call turn_on().

2.  Inspect system.security_system and its siren.

**Expected Result**

- SecuritySystem is created

- Siren component exists

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on initializes security system\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Phase 3 (Alarm) in Turn the
System On sequence

###### h. test_turn_on_initializes_camera_controller (LT-008) {#h.-test_turn_on_initializes_camera_controller-lt-008 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that CameraController is properly initialized.

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Call turn_on().

2.  Inspect system.camera_controller.

**Expected Result**

- CameraController is created

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on initializes camera controller\' behavior
matched lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Phase 2 (CameraController) in
Turn the System On sequence

###### i. test_turn_on_state_transition (LT-009) {#i.-test_turn_on_state_transition-lt-009 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-ON-009: State transitions during turn_on

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Assert state is OFF.

2.  Call turn_on().

3.  Assert state is READY.

**Expected Result**

- Initial state is OFF

- Final state is READY after successful turn_on

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on state transition\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); System lifecycle states in SDS

###### j. test_turn_on_callback_execution (LT-010) {#j.-test_turn_on_callback_execution-lt-010 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Verifies that the on_turn_on_complete callback is called after
successful initialization.

**Input Specifications**

- System has on_turn_on_complete callback set

**Detailed Step**

1.  Register callback.

2.  Call turn_on().

3.  Verify callback execution.

**Expected Result**

- Callback is executed after turn_on completes

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on callback execution\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Device initialization after
turn_on in main.py

###### k. test_turn_on_with_existing_database (LT-015) {#k.-test_turn_on_with_existing_database-lt-015 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validate that system correctly loads existing data when turning on with
a pre-existing database.

**Input Specifications**

- Turn on an initial System instance, modify persisted settings, and
  shut it down.

- Instantiate a second System pointing at the same storage and call
  turn_on().

**Detailed Step**

1.  Setup DB with specific data.

2.  Start new System instance.

3.  Verify loaded configuration matches DB.

**Expected Result**

- Second turn_on reads the stored configuration and keeps existing
  credentials intact.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on with existing database\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Database persistence in system
lifecycle

###### l. test_turn_on_turn_off_cycle (LT-016) {#l.-test_turn_on_turn_off_cycle-lt-016 .unnumbered}

|           |                        |            |            |             |
|-----------|------------------------|------------|------------|-------------|
| **Class** | **Method**             | **Author** | **Date**   | **Version** |
| System    | turn_on() / turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validate that system can be turned on and off multiple times without
issues.

**Input Specifications**

- Reuse one System instance and repeatedly invoke turn_on()/turn_off()
  across multiple cycles.

**Detailed Step**

1.  Call turn_on(), then turn_off().

2.  Repeat 3 times.

3.  Verify state after each transition.

**Expected Result**

- Every iteration succeeds without leaking resources, leaving state
  READY after turn_on and OFF after turn_off.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on turn off cycle\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); System lifecycle management

##### B. turn_off() {#b.-turn_off .unnumbered}

###### a. test_turn_off_from_ready_state (LT-017) {#a.-test_turn_off_from_ready_state-lt-017 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-001: Shuts the system down from READY.

**Input Specifications**

- Keep the fixture-prepared System in READY and call turn_off() once.

**Detailed Step**

1.  Ensure state is READY.

2.  Call turn_off().

**Expected Result**

- turn_off() returns True.

- System transitions to OFF with no errors.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off from ready state\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### b. test_turn_off_when_already_off (LT-018) {#b.-test_turn_off_when_already_off-lt-018 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-002: Guards double shutdown attempts.

**Input Specifications**

- Call turn_off() to reach OFF, then immediately call turn_off() again.

**Detailed Step**

1.  Call turn_off() (Returns True).

2.  Call turn_off() again.

**Expected Result**

- The second invocation returns False and leaves SystemState at OFF.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off when already off\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### c. test_turn_off_saves_configuration (LT-019) {#c.-test_turn_off_saves_configuration-lt-019 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-003: Verifies that configuration is saved before shutdown.

**Input Specifications**

- Modify configuration values via ConfigurationManager before invoking
  turn_off().

**Detailed Step**

1.  Modify a setting.

2.  Call turn_off().

3.  Verify storage persistence.

**Expected Result**

- Shutdown persists settings to storage and the system enters OFF
  cleanly.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off saves configuration\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### d. test_turn_off_deactivates_sensors (LT-020) {#d.-test_turn_off_deactivates_sensors-lt-020 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-004: Verifies that all sensors are deactivated during
shutdown.

**Input Specifications**

- Attach several MockSensor instances to system.sensors and call
  turn_off().

**Detailed Step**

1.  Add mock sensors.

2.  Call turn_off().

3.  Verify deactivate() was called on sensors.

**Expected Result**

- Each sensor receives deactivate() and monitoring stops.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off deactivates sensors\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### e. test_turn_off_disables_cameras (LT-021) {#e.-test_turn_off_disables_cameras-lt-021 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-005: Verifies that all cameras are disabled during shutdown.

**Input Specifications**

- Register cameras through CameraController and power down the system.

**Detailed Step**

1.  Add cameras.

2.  Call turn_off().

3.  Verify cameras are disabled.

**Expected Result**

- Camera controller disables every camera feed while transitioning to
  OFF.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off disables cameras\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### f. test_turn_off_deactivates_siren (LT-022) {#f.-test_turn_off_deactivates_siren-lt-022 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-006: Verifies that siren is deactivated during shutdown.

**Input Specifications**

- Force the siren into an active state prior to calling turn_off().

**Detailed Step**

1.  Activate siren.

2.  Call turn_off().

3.  Verify siren is inactive.

**Expected Result**

- Siren deactivates so no alarm remains latched after shutdown.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off deactivates siren\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### g. test_turn_off_logs_out_user (LT-023) {#g.-test_turn_off_logs_out_user-lt-023 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-007: Verifies that logged-in user is logged out during
shutdown.

**Input Specifications**

- Authenticate the default admin user through login_manager and then
  call turn_off().

**Detailed Step**

1.  Log in as admin.

2.  Call turn_off().

3.  Verify current user is None.

**Expected Result**

- Shutdown logs the user out and moves SystemState to OFF.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off logs out user\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### h. test_turn_off_logs_shutdown_event (LT-024) {#h.-test_turn_off_logs_shutdown_event-lt-024 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-008: Verifies that SYSTEM_SHUTDOWN event is logged.

**Input Specifications**

- Ensure LogManager is bound and call turn_off().

**Detailed Step**

1.  Call turn_off().

2.  Check log for SYSTEM_SHUTDOWN.

**Expected Result**

- A SYSTEM_SHUTDOWN event is appended to the audit log.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off logs shutdown event\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### i. test_turn_off_disconnects_database (LT-025) {#i.-test_turn_off_disconnects_database-lt-025 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-009: Verifies that database connection is closed during
shutdown.

**Input Specifications**

- Keep StorageManager connected to the DB before invoking turn_off().

**Detailed Step**

1.  Ensure DB connected.

2.  Call turn_off().

3.  Verify DB connection is closed.

**Expected Result**

- StorageManager.disconnect() executes so no connections remain open.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off disconnects database\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### j. test_turn_off_state_transition (LT-026) {#j.-test_turn_off_state_transition-lt-026 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-OFF-010: Verifies the state transitions: READY -\> SHUTDOWN -\>
OFF

**Input Specifications**

- Operate from READY state and call turn_off().

**Detailed Step**

1.  Monitor state changes during turn_off() execution.

**Expected Result**

- Lifecycle transitions progress from READY to SHUTDOWN to OFF without
  stalls.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off state transition\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### k. test_turn_off_executes_shutdown_sequence (LT-047) {#k.-test_turn_off_executes_shutdown_sequence-lt-047 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validates \'Turn off executes shutdown sequence\' behavior

**Input Specifications**

- Build a System wired with stubbed managers, sensors, siren, and
  cameras, then call turn_off().

**Detailed Step**

1.  Configure stubs with hooks.

2.  Call turn_off().

3.  Verify all hooks called.

**Expected Result**

- Each stub records its shutdown hook (config saved,
  sensors/cameras/siren deactivated, auth logged out, logs written,
  storage disconnected).

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off executes shutdown sequence\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### l. test_turn_off_returns_false_if_already_off (LT-048) {#l.-test_turn_off_returns_false_if_already_off-lt-048 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validates \'Turn off returns false if already off\' behavior

**Input Specifications**

- Instantiate a fresh System that is still OFF and call turn_off()
  immediately.

**Detailed Step**

1.  Create System (OFF).

2.  Call turn_off().

**Expected Result**

- Operation returns False because lifecycle preconditions are not met.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off returns false if already off\' behavior
matched lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

##### C. reset() {#c.-reset .unnumbered}

###### a. test_reset_from_ready_state (LT-033) {#a.-test_reset_from_ready_state-lt-033 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-001: Verifies that reset() from READY state succeeds and
system returns to READY state.

**Input Specifications**

- Ensure SystemState is READY and call reset().

**Detailed Step**

1.  Call reset().

2.  Verify return value and final state.

**Expected Result**

- reset() reports success, completes all phases, and leaves state READY.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset from ready state\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### b. test_reset_when_system_off (LT-034) {#b.-test_reset_when_system_off-lt-034 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-002: Verifies that reset() when system is OFF returns error
and does not proceed.

**Input Specifications**

- Transition the system to OFF first, then call reset().

**Detailed Step**

1.  Turn off system.

2.  Call reset().

**Expected Result**

- reset() immediately fails with a phase 0 error because lifecycle
  preconditions are unmet.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset when system off\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### c. test_reset_preserves_settings (LT-035) {#c.-test_reset_preserves_settings-lt-035 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-003: Verifies that settings are preserved after reset.

**Input Specifications**

- Adjust lock time and alarm delay values before invoking reset().

**Detailed Step**

1.  Change settings.

2.  Call reset().

3.  Verify settings match initial changes.

**Expected Result**

- Post-reset settings remain at the modified values (no persistence
  loss).

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset preserves settings\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### d. test_reset_recreates_components (LT-036) {#d.-test_reset_recreates_components-lt-036 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-004: Verifies that all components are recreated after reset.

**Input Specifications**

- Capture references to current managers, call reset(), and inspect the
  refreshed component graph.

**Detailed Step**

1.  Store refs to old components.

2.  Call reset().

3.  Compare new component refs.

**Expected Result**

- All core managers and controllers are reinitialized and non-null.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset recreates components\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### e. test_reset_deactivates_sensors (LT-037) {#e.-test_reset_deactivates_sensors-lt-037 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-005: Verifies that sensors are deactivated during Phase 1.

**Input Specifications**

- Populate system.sensors with mock devices and call reset().

**Detailed Step**

1.  Add mock sensors.

2.  Call reset().

3.  Verify deactivate() called.

**Expected Result**

- Each sensor is deactivated during Phase 1 before components restart.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset deactivates sensors\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### f. test_reset_logs_out_user (LT-038) {#f.-test_reset_logs_out_user-lt-038 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-006: Verifies that logged-in user is logged out during reset.

**Input Specifications**

- Authenticate admin to push the system into ACTIVE, then invoke
  reset().

**Detailed Step**

1.  Login.

2.  Call reset().

3.  Verify user is logged out.

**Expected Result**

- reset() logs the user out and returns the lifecycle to READY.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset logs out user\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### g. test_reset_logs_events (LT-039) {#g.-test_reset_logs_events-lt-039 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-007: Verifies that reset events are logged.

**Input Specifications**

- With LogManager ready, trigger reset().

**Detailed Step**

1.  Call reset().

2.  Check logs.

**Expected Result**

- Reset flow emits start/complete events for the audit trail.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset logs events\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

###### h. test_reset_state_transitions (LT-040) {#h.-test_reset_state_transitions-lt-040 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

UT-SYS-RST-008: Verifies state transitions: READY -\> OFF -\> READY

**Input Specifications**

- Operate from READY and issue reset().

**Detailed Step**

1.  Monitor state during reset().

**Expected Result**

- Lifecycle transitions READY -\> OFF -\> READY are observed without
  error.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset state transitions\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

## **4. Configuration and Data Management** {#configuration-and-data-management .unnumbered}

### **A. Log Management** {#a.-log-management .unnumbered}

#### **1. X** {#x .unnumbered}

##### **A. X** {#a.-x .unnumbered}

###### **a. X** {#a.-x-1 .unnumbered}

### **B. LoginManager (Backend Authentication Logic)** {#b.-loginmanager-backend-authentication-logic .unnumbered}

#### **1. LoginManager class** {#loginmanager-class .unnumbered}

##### **A. login_with_details() (detailed login response)** {#a.-login_with_details-detailed-login-response .unnumbered}

###### **a. test_login_with_details_success (UT-LM-001)** {#a.-test_login_with_details_success-ut-lm-001 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | LoginManager         |
| Method  | login_with_details() |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that successful login returns detailed information including
username and access level.

**Input Specifications**

• Username: \"admin\"

• Password: \"1234\"

• Interface: \"control_panel\"

• Account is not locked

• Credentials are correct

**Expected Result**

{  
\'success\': True,  
\'message\': \'Login successful\',  
\'username\': \'admin\',  
\'access_level\': 1  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns success with detailed information

• Pass: Username and access level included in response

**Comment**

Enhanced login method provides additional information for UI display and
logging. Replaces boolean-only return value.

###### **b. test_locked_account_with_auto_unlock (UT-LM-002)** {#b.-test_locked_account_with_auto_unlock-ut-lm-002 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | LoginManager         |
| Method  | login_with_details() |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that the system automatically unlocks an account when the
configured lock duration has elapsed.

**Input Specifications**

• User account locked at timestamp T

• system_lock_time = 30 seconds (default)

• Current time = T + 31 seconds

• User attempts login

**Expected Result**

• Account is automatically unlocked

• Login proceeds with credential validation

• If credentials correct, login succeeds

**Actual Result (Pass/Fail/Exception)**

• Pass: Account automatically unlocked after duration

• Pass: Console message: \"Account \'admin\' automatically unlocked
after 30 seconds\"

• Pass: Successful login after auto-unlock

**Comment**

Implements time-based automatic unlock feature. Uses
\_check_and_unlock_if_time_passed() internal method.

###### **c. test_locked_account_returns_remaining_time (UT-LM-003)** {#c.-test_locked_account_returns_remaining_time-ut-lm-003 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | LoginManager         |
| Method  | login_with_details() |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that attempting to login with a locked account returns the
remaining lock time.

**Input Specifications**

• User account locked at timestamp T

• system_lock_time = 30 seconds

• Current time = T + 10 seconds

• Remaining time = 20 seconds

**Expected Result**

{  
\'success\': False,  
\'message\': \'Account is locked. Please try again in 20 seconds.\',  
\'locked\': True,  
\'tries\': 5,  
\'remaining_time\': 20  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns locked status with remaining time

• Pass: Remaining time calculated correctly (30 - 10 = 20)

**Comment**

Provides user feedback on when they can attempt login again.

### **C. System Integration (Login & Configuration)** {#c.-system-integration-login-configuration .unnumbered}

#### **1. System class - Login Integration** {#system-class---login-integration .unnumbered}

##### **A. login_with_details() (system-level login)** {#a.-login_with_details-system-level-login .unnumbered}

###### **a. test_login_system_off (UT-SYS-Login-001)** {#a.-test_login_system_off-ut-sys-login-001 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | System               |
| Method  | login_with_details() |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that login attempt fails when system is OFF.

**Input Specifications**

• System state: SystemState.OFF

• Valid credentials provided

**Expected Result**

{  
\'success\': False,  
\'message\': \'System is off. Please turn on the system first.\',  
\'system_off\': True  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Login fails with system_off flag

• Pass: Appropriate error message returned

**Comment**

Precondition check: System must be ON for login.

###### **b. test_login_system_locked (UT-SYS-Login-002)** {#b.-test_login_system_locked-ut-sys-login-002 .unnumbered}

|         |                      |
|---------|----------------------|
| Field   | Value                |
| Class   | System               |
| Method  | login_with_details() |
| Author  | Minseok Jo           |
| Date    | 2025-11-25           |
| Version | 2.0.0                |

**Test Case Description**

Verifies that login attempt fails when system is LOCKED.

**Input Specifications**

• System state: SystemState.LOCKED

• Valid credentials provided

**Expected Result**

{  
\'success\': False,  
\'message\': \'System is locked. Please contact administrator.\',  
\'system_locked\': True  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Login fails with system_locked flag

• Pass: Appropriate error message returned

**Comment**

System-level lock prevents all logins regardless of user credentials.

#### **2. System class - Configuration Integration** {#system-class---configuration-integration .unnumbered}

##### **A. configure_system_setting() (system-level configuration)** {#a.-configure_system_setting-system-level-configuration .unnumbered}

###### **a. test_configure_system_setting (UT-SYS-Config-001)** {#a.-test_configure_system_setting-ut-sys-config-001 .unnumbered}

|         |                            |
|---------|----------------------------|
| Field   | Value                      |
| Class   | System                     |
| Method  | configure_system_setting() |
| Author  | Minseok Jo                 |
| Date    | 2025-11-25                 |
| Version | 2.0.0                      |

**Test Case Description**

Verifies that system settings can be configured through the System
class.

**Input Specifications**

• System is ON

• monitoring_phone: \"111-222-3333\"

• homeowner_phone: \"444-555-6666\"

• lock_time: 45

• alarm_delay: 90

**Expected Result**

• Method returns True

• Settings are persisted to database

• SettingsService is invoked correctly

**Actual Result (Pass/Fail/Exception)**

• Pass: Returns True

• Pass: Settings saved successfully

• Pass: Database contains updated values

**Comment**

Uses SettingsService internally for separation of concerns.

### **D. Password Management** {#d.-password-management .unnumbered}

#### **1. System class - Password Change** {#system-class---password-change .unnumbered}

##### **A. change_master_password() (system-level password change)** {#a.-change_master_password-system-level-password-change .unnumbered}

###### **a. test_change_password_success (UT-PWD-001)** {#a.-test_change_password_success-ut-pwd-001 .unnumbered}

|         |                          |
|---------|--------------------------|
| Field   | Value                    |
| Class   | System                   |
| Method  | change_master_password() |
| Author  | Minseok Jo               |
| Date    | 2025-11-25               |
| Version | 2.0.0                    |

**Test Case Description**

Verifies that password change succeeds with correct inputs through all 3
phases.

**Input Specifications**

• User is logged in (admin/1234)

• current_password: \'1234\'

• new_password: \'newpass5678\'

• confirm_password: \'newpass5678\'

**Expected Result**

{  
\'success\': True,  
\'message\': \'Password changed successfully\',  
\'phase\': 3  
}

• Password is updated in database

• User remains logged in

**Actual Result (Pass/Fail/Exception)**

• Pass: Password change succeeds with phase 3

• Pass: New password works for subsequent login

**Comment**

Complete 3-phase password change flow. Test file:
test_change_master_password.py:68

###### **b. test_change_password_wrong_current (UT-PWD-002)** {#b.-test_change_password_wrong_current-ut-pwd-002 .unnumbered}

|         |                          |
|---------|--------------------------|
| Field   | Value                    |
| Class   | System                   |
| Method  | change_master_password() |
| Author  | Minseok Jo               |
| Date    | 2025-11-25               |
| Version | 2.0.0                    |

**Test Case Description**

Verifies that password change fails with wrong current password at Phase
1.

**Input Specifications**

• User is logged in

• current_password: \'wrongpass\' (incorrect)

• new_password: \'newpass5678\'

• confirm_password: \'newpass5678\'

**Expected Result**

{  
\'success\': False,  
\'phase\': 1,  
\'error_type\': \'INCORRECT_PASSWORD\',  
\'message\': \'Current password is incorrect\'  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Fails at Phase 1 with INCORRECT_PASSWORD error

• Pass: Password remains unchanged

**Comment**

Phase 1 validation prevents unauthorized password changes. Test file:
test_change_master_password.py:91

###### **c. test_change_password_mismatch (UT-PWD-003)** {#c.-test_change_password_mismatch-ut-pwd-003 .unnumbered}

|         |                          |
|---------|--------------------------|
| Field   | Value                    |
| Class   | System                   |
| Method  | change_master_password() |
| Author  | Minseok Jo               |
| Date    | 2025-11-25               |
| Version | 2.0.0                    |

**Test Case Description**

Verifies that password change fails when new passwords don\'t match at
Phase 3.

**Input Specifications**

• User is logged in

• current_password: \'1234\'

• new_password: \'newpass1111\'

• confirm_password: \'newpass2222\' (mismatch)

**Expected Result**

{  
\'success\': False,  
\'phase\': 3,  
\'error_type\': \'PASSWORD_MISMATCH\',  
\'message\': \'New passwords do not match\'  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Fails at Phase 3 with PASSWORD_MISMATCH error

• Pass: Password remains unchanged

**Comment**

Phase 3 confirmation prevents accidental password changes. Test file:
test_change_master_password.py:108

###### **d. test_change_password_same_as_current (UT-PWD-004)** {#d.-test_change_password_same_as_current-ut-pwd-004 .unnumbered}

|         |                          |
|---------|--------------------------|
| Field   | Value                    |
| Class   | System                   |
| Method  | change_master_password() |
| Author  | Minseok Jo               |
| Date    | 2025-11-25               |
| Version | 2.0.0                    |

**Test Case Description**

Verifies that password change fails when new password is same as
current.

**Input Specifications**

• current_password: \'1234\'

• new_password: \'1234\'

• confirm_password: \'1234\'

**Expected Result**

{  
\'success\': False,  
\'error_type\': \'SAME_PASSWORD\',  
\'message\': \'New password must be different from current password\'  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Fails with SAME_PASSWORD error

• Pass: Password remains unchanged

**Comment**

Security policy requires different password. Test file:
test_change_master_password.py:125

###### **e. test_change_password_not_authenticated (UT-PWD-005)** {#e.-test_change_password_not_authenticated-ut-pwd-005 .unnumbered}

|         |                          |
|---------|--------------------------|
| Field   | Value                    |
| Class   | System                   |
| Method  | change_master_password() |
| Author  | Minseok Jo               |
| Date    | 2025-11-25               |
| Version | 2.0.0                    |

**Test Case Description**

Verifies that password change fails when user is not authenticated.

**Input Specifications**

• User is NOT logged in

• Attempt to change password

**Expected Result**

{  
\'success\': False,  
\'phase\': 0,  
\'error_type\': \'NOT_AUTHENTICATED\',  
\'message\': \'Authentication required to change password\'  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Fails at Phase 0 with NOT_AUTHENTICATED error

**Comment**

Precondition: User must be logged in. Test file:
test_change_master_password.py:141

###### **f. test_change_password_system_off (UT-PWD-006)** {#f.-test_change_password_system_off-ut-pwd-006 .unnumbered}

|         |                          |
|---------|--------------------------|
| Field   | Value                    |
| Class   | System                   |
| Method  | change_master_password() |
| Author  | Minseok Jo               |
| Date    | 2025-11-25               |
| Version | 2.0.0                    |

**Test Case Description**

Verifies that password change fails when system is OFF.

**Input Specifications**

• System is OFF

• Attempt to change password

**Expected Result**

{  
\'success\': False,  
\'error_type\': \'SYSTEM_OFF\',  
\'message\': \'System is off. Please turn on the system first.\'  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Fails with SYSTEM_OFF error

**Comment**

Precondition: System must be ON. Test file:
test_change_master_password.py:162

###### **g. test_change_password_system_locked (UT-PWD-007)** {#g.-test_change_password_system_locked-ut-pwd-007 .unnumbered}

|         |                          |
|---------|--------------------------|
| Field   | Value                    |
| Class   | System                   |
| Method  | change_master_password() |
| Author  | Minseok Jo               |
| Date    | 2025-11-25               |
| Version | 2.0.0                    |

**Test Case Description**

Verifies that password change fails when system is LOCKED.

**Input Specifications**

• System is LOCKED

• Attempt to change password

**Expected Result**

{  
\'success\': False,  
\'error_type\': \'SYSTEM_LOCKED\',  
\'message\': \'System is locked. Please contact administrator.\'  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: Fails with SYSTEM_LOCKED error

**Comment**

Precondition: System must not be locked. Test file:
test_change_master_password.py:182

### **E. System Power Management** {#e.-system-power-management .unnumbered}

#### **1. System class - Power On** {#system-class---power-on .unnumbered}

##### **A. turn_on() (system power on)** {#a.-turn_on-system-power-on .unnumbered}

###### **a. test_turn_on_from_off_state (UT-SYS-ON-001)** {#a.-test_turn_on_from_off_state-ut-sys-on-001 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | turn_on()  |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that calling turn_on() when system is OFF results in successful
initialization and system state becomes READY.

**Input Specifications**

• System is in OFF state (initial state after constructor)

**Expected Result**

• turn_on() returns True

• system_state becomes SystemState.READY

• All core components are initialized (not None):

• StorageManager

• ConfigurationManager

• LoginManager

• LogManager

• SystemController

• SecuritySystem

• CameraController

• Siren

**Actual Result (Pass/Fail/Exception)**

• Pass: turn_on() returns True

• Pass: system_state is SystemState.READY

• Pass: All components initialized

**Comment**

Complete system initialization sequence as specified in SDS page 50.
Includes initialization of AuthService and SettingsService (new in Phase
2).

###### **b. test_turn_on_when_already_running (UT-SYS-ON-002)** {#b.-test_turn_on_when_already_running-ut-sys-on-002 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | turn_on()  |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that calling turn_on() when system is already running returns
False and does not reinitialize components.

**Input Specifications**

• System is already in READY state (turn_on() called previously)

**Expected Result**

• turn_on() returns False

• system_state remains READY

• No exception is raised

• Console message: \"System is already Ready\"

**Actual Result (Pass/Fail/Exception)**

• Pass: turn_on() returns False

• Pass: system_state remains READY

• Pass: Components are not reinitialized

**Comment**

Error handling prevents double initialization.

#### **2. System class - Power Off** {#system-class---power-off .unnumbered}

##### **A. turn_off() (system power off)** {#a.-turn_off-system-power-off .unnumbered}

###### **a. test_turn_off_from_ready_state (UT-SYS-OFF-001)** {#a.-test_turn_off_from_ready_state-ut-sys-off-001 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | turn_off() |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that calling turn_off() when system is READY results in
successful shutdown following the complete sequence.

**Input Specifications**

• System is in READY state (after turn_on() was called)

**Expected Result**

• turn_off() returns True

• system_state becomes SystemState.OFF

• Shutdown sequence executed:

1\. Configuration saved

2\. Sensors deactivated

3\. Cameras disabled

4\. Siren deactivated

5\. User logged out

6\. SYSTEM_SHUTDOWN event logged

7\. Database disconnected

**Actual Result (Pass/Fail/Exception)**

• Pass: turn_off() returns True

• Pass: system_state is SystemState.OFF

• Pass: All shutdown steps completed

**Comment**

Complete shutdown sequence as specified in SDS page 51. Test file:
test_system_power_flow.py:115

###### **b. test_turn_off_when_already_off (UT-SYS-OFF-002)** {#b.-test_turn_off_when_already_off-ut-sys-off-002 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | turn_off() |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that calling turn_off() when system is already OFF returns
False and does not cause errors.

**Input Specifications**

• System is already in OFF state

**Expected Result**

• turn_off() returns False

• system_state remains OFF

• No exception is raised

• Console message: \"System is already off\"

**Actual Result (Pass/Fail/Exception)**

• Pass: turn_off() returns False

• Pass: system_state remains OFF

• Pass: No exception raised

**Comment**

Prevents redundant shutdown operations. Test file:
test_system_power_flow.py:133

###### **c. test_turn_off_deactivates_sensors (UT-SYS-OFF-003)** {#c.-test_turn_off_deactivates_sensors-ut-sys-off-003 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | turn_off() |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that all sensors are deactivated during shutdown (Phase 2 of
turn_off sequence).

**Input Specifications**

• System is running with multiple sensors registered

**Expected Result**

• All sensors are deactivated

• turn_off() returns True

• Console message: \"N sensors deactivated\"

**Actual Result (Pass/Fail/Exception)**

• Pass: All sensors deactivated

• Pass: Each sensor\'s deactivate() method called

**Comment**

Phase 2 of Turn the System Off sequence. Test file:
test_system_power_flow.py:115

###### **d. test_turn_off_disables_cameras (UT-SYS-OFF-004)** {#d.-test_turn_off_disables_cameras-ut-sys-off-004 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | turn_off() |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that all cameras are disabled during shutdown (Phase 3 of
turn_off sequence).

**Input Specifications**

• System is running with CameraController and cameras added

**Expected Result**

• CameraController.disable_all_camera() is called

• All cameras in SystemController are deactivated

• turn_off() returns True

**Actual Result (Pass/Fail/Exception)**

• Pass: Camera controller disabled flag is True

• Pass: All camera objects deactivated

**Comment**

Phase 3 of Turn the System Off sequence. Test file:
test_system_power_flow.py:115

#### **3. System class - System Reset** {#system-class---system-reset .unnumbered}

##### **A. reset() (system reset)** {#a.-reset-system-reset .unnumbered}

###### **a. test_reset_from_ready_state (UT-SYS-RST-001)** {#a.-test_reset_from_ready_state-ut-sys-rst-001 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | reset()    |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that calling reset() from READY state succeeds and system
returns to READY state.

**Input Specifications**

• System is in READY state (after turn_on() was called)

**Expected Result**

{  
\'success\': True,  
\'message\': \'System reset successfully\',  
\'phase\': 3  
}

• system_state becomes SystemState.READY

**Actual Result (Pass/Fail/Exception)**

• Pass: reset() returns success with phase 3

• Pass: system_state is SystemState.READY

• Pass: Reset = Turn Off + Turn On

**Comment**

Reset executes turn_off() followed by turn_on(). Enhanced return format
includes phase information.

###### **b. test_reset_when_system_off (UT-SYS-RST-002)** {#b.-test_reset_when_system_off-ut-sys-rst-002 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | reset()    |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that calling reset() when system is OFF returns error and does
not proceed.

**Input Specifications**

• System is in OFF state

**Expected Result**

{  
\'success\': False,  
\'message\': \'Cannot reset: System is not running\',  
\'phase\': 0  
}

**Actual Result (Pass/Fail/Exception)**

• Pass: reset() returns False with phase 0

• Pass: Error message indicates system not running

**Comment**

Precondition: System must be ON to perform reset.

###### **c. test_reset_preserves_settings (UT-SYS-RST-003)** {#c.-test_reset_preserves_settings-ut-sys-rst-003 .unnumbered}

|         |            |
|---------|------------|
| Field   | Value      |
| Class   | System     |
| Method  | reset()    |
| Author  | Minseok Jo |
| Date    | 2025-11-25 |
| Version | 2.0.1      |

**Test Case Description**

Verifies that settings are preserved after reset.

**Input Specifications**

• System is in READY state

• Settings modified:

• lock_time = 45

• alarm_delay = 90

**Expected Result**

• reset() succeeds

• Modified settings are preserved after reset

• lock_time remains 45

• alarm_delay remains 90

**Actual Result (Pass/Fail/Exception)**

• Pass: reset() returns success

• Pass: Settings values preserved

**Comment**

Settings are saved during Turn Off (Phase 1) and loaded during Turn On
(Phase 2).

# **IV. Integration Tests** {#iv.-integration-tests .unnumbered}

## **A. Control Panel Login Process** {#a.-control-panel-login-process .unnumbered}

### **1. test_control_panel_login_with_presenter_and_system (IT-CP-Login-001)** {#test_control_panel_login_with_presenter_and_system-it-cp-login-001 .unnumbered}

|          |                                                                  |
|----------|------------------------------------------------------------------|
| Field    | Value                                                            |
| Class    | ControlPanelLoginPresenter, System, LoginManager, StorageManager |
| Function | Log onto the system via Control Panel                            |
| Author   | Minseok Jo                                                       |
| Date     | 2025-11-25                                                       |

**Test Case Description**

Validate that ControlPanelLoginPresenter successfully coordinates with
System and LoginManager to authenticate a user when valid credentials
are provided.

**Input Specifications**

• Database has predefined username and password: \"admin\" and \"1234\"

• User ID: \"admin\"

• Password: \"1234\"

**Detailed Step**

1\. Initialize System and call turn_on() to initialize all components
including LoginManager and StorageManager.

2\. Create ControlPanelLoginPresenter with reference to the System
instance.

3\. Call presenter.attempt_login() with \"admin\" as user_id and
\"1234\" as password.

4\. Presenter delegates to System.login_with_details() which internally
calls LoginManager.login_with_details().

5\. LoginManager validates credentials against StorageManager data.

6\. System returns success response with navigation information.

7\. Presenter transforms response into LoginOutcome dataclass.

**Expected Result**

• LoginOutcome.success equals True

• LoginOutcome.navigate_to equals \"MainMenu\"

• System.login_tries equals 0 after successful authentication

• User session is established in System

**Actual Result (Pass/Fail/Exception)**

• Pass: LoginOutcome.success equals True

• Pass: LoginOutcome.navigate_to equals \"MainMenu\"

• Pass: System.login_tries equals 0

**Comment (including references)**

Integration between Presenter layer and System/LoginManager layer.
Validates the MVP pattern implementation introduced in Phase 2.

### **2. test_control_panel_login_lockout_integration (IT-CP-Login-002)** {#test_control_panel_login_lockout_integration-it-cp-login-002 .unnumbered}

|          |                                                  |
|----------|--------------------------------------------------|
| Field    | Value                                            |
| Class    | ControlPanelLoginPresenter, System, LoginManager |
| Function | Account lockout after failed attempts            |
| Author   | Minseok Jo                                       |
| Date     | 2025-11-25                                       |

**Test Case Description**

Validate that the integration between ControlPanelLoginPresenter and
LoginManager correctly handles account lockout after maximum failed
attempts.

**Input Specifications**

• Database has predefined username: \"admin\" with password: \"1234\"

• Incorrect password attempts: 5 times with \"wrongpw\"

• system_lock_time: 30 seconds

**Detailed Step**

1\. Initialize System with turn_on().

2\. Create ControlPanelLoginPresenter with System reference.

3\. Attempt login 5 times with incorrect password \"wrongpw\".

4\. On each failed attempt, LoginManager increments tries counter.

5\. After 5th failed attempt, LoginManager locks the account.

6\. 6th attempt returns locked status with remaining_time.

7\. Presenter formats the lock message with time remaining.

**Expected Result**

• After 5 failed attempts, account is locked

• LoginOutcome.success equals False

• LoginOutcome.status_color equals \"red\"

• LoginOutcome.alert_level equals \"error\"

• LoginOutcome.alert_title equals \"Account Locked\"

• remaining_time is included in status_text

**Actual Result (Pass/Fail/Exception)**

• Pass: Account locked after 5 attempts

• Pass: LoginOutcome contains lock information

• Pass: Time remaining is formatted correctly

**Comment (including references)**

Tests the complete lockout flow from UI through business logic.
Implements time-based unlock feature.

## **B. Control Panel Settings Configuration** {#b.-control-panel-settings-configuration .unnumbered}

### **1. test_settings_save_integration (IT-CP-Settings-001)** {#test_settings_save_integration-it-cp-settings-001 .unnumbered}

|          |                                                                             |
|----------|-----------------------------------------------------------------------------|
| Field    | Value                                                                       |
| Class    | ControlPanelSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Save system settings via Control Panel                                      |
| Author   | Minseok Jo                                                                  |
| Date     | 2025-11-25                                                                  |

**Test Case Description**

Validate that ControlPanelSettingsPresenter correctly saves settings
through the System layer and persists them to the database.

**Input Specifications**

• monitoring_phone: \"911\"

• homeowner_phone: \"010-1234-5678\"

• lock_time: \"45\"

• alarm_delay: \"90\"

**Detailed Step**

1\. Initialize System with turn_on().

2\. Create ControlPanelSettingsPresenter with System reference.

3\. Call presenter.save_settings() with the input values.

4\. Presenter validates inputs (non-numeric check, negative check).

5\. Presenter converts string time values to integers.

6\. Presenter calls System.configure_system_setting().

7\. System delegates to SettingsService which updates
ConfigurationManager.

8\. ConfigurationManager persists changes via StorageManager.

**Expected Result**

• SettingsOutcome.success equals True

• SettingsOutcome.alert_level equals \"info\"

• ConfigurationManager.lock_time equals 45

• ConfigurationManager.alarm_delay equals 90

• Database contains updated values

**Actual Result (Pass/Fail/Exception)**

• Pass: SettingsOutcome.success equals True

• Pass: Settings persisted correctly

• Pass: Values retrievable after save

**Comment (including references)**

Tests complete settings flow from UI validation through persistence
layer.

## **C. Control Panel Password Change** {#c.-control-panel-password-change .unnumbered}

### **1. test_password_change_full_flow_integration (IT-CP-PWD-001)** {#test_password_change_full_flow_integration-it-cp-pwd-001 .unnumbered}

|          |                                                                           |
|----------|---------------------------------------------------------------------------|
| Field    | Value                                                                     |
| Class    | ControlPanelChangePasswordPresenter, System, LoginManager, StorageManager |
| Function | Change master password via Control Panel                                  |
| Author   | Minseok Jo                                                                |
| Date     | 2025-11-25                                                                |

**Test Case Description**

Validate the complete password change flow from
ControlPanelChangePasswordPresenter through System to database
persistence.

**Input Specifications**

• User is logged in as \"admin\"

• current_password: \"1234\"

• new_password: \"newpass5678\"

• confirm_password: \"newpass5678\"

**Detailed Step**

1\. Initialize System and login with admin/1234.

2\. Create ControlPanelChangePasswordPresenter with System reference.

3\. Call presenter.change_password() with current, new, and confirm
passwords.

4\. Presenter validates: passwords match, minimum length met.

5\. Presenter calls System.change_master_password().

6\. System executes 3-phase password change:

• Phase 1: Verify current password

• Phase 2: Validate new password rules

• Phase 3: Confirm and save

7\. StorageManager updates password in database.

**Expected Result**

• ChangePasswordOutcome.success equals True

• ChangePasswordOutcome.message equals \"Password changed
successfully!\"

• New password works for subsequent login

• Old password no longer works

**Actual Result (Pass/Fail/Exception)**

• Pass: Password change succeeds

• Pass: New password authenticates correctly

• Pass: Old password rejected

**Comment (including references)**

Validates complete 3-phase password change flow. Test file:
test_change_master_password.py

## **D. Web Login Process (2FA)** {#d.-web-login-process-2fa .unnumbered}

### **1. test_web_login_two_factor_integration (IT-Web-Login-001)** {#test_web_login_two_factor_integration-it-web-login-001 .unnumbered}

|          |                                                         |
|----------|---------------------------------------------------------|
| Field    | Value                                                   |
| Class    | WebLoginPresenter, System, LoginManager, StorageManager |
| Function | Two-factor authentication via Web interface             |
| Author   | Minseok Jo                                              |
| Date     | 2025-11-25                                              |

**Test Case Description**

Validate the complete 2-factor authentication flow for web login,
including first password and second password/PIN validation.

**Input Specifications**

• username: \"admin\"

• first_password: \"password123\"

• second_password: \"pin1234\"

**Detailed Step**

1\. Initialize System with turn_on().

2\. Create WebLoginPresenter with System reference.

3\. Call presenter.validate_first_password() with username and
first_password.

4\. Presenter calls LoginManager.validate_first_password() with
interface=\'web_browser\'.

5\. LoginManager validates first credential against StorageManager.

6\. On success, call presenter.validate_second_password() with username
and second_password.

7\. LoginManager validates second credential (PIN).

8\. On success, user session is established and redirect URL is
returned.

**Expected Result**

• First password validation: WebLoginOutcome.success equals True

• Second password validation: WebLoginOutcome.success equals True

• WebLoginOutcome.redirect_url equals \"/dashboard\"

• User session established in System

**Actual Result (Pass/Fail/Exception)**

• Pass: First password validated successfully

• Pass: Second password validated successfully

• Pass: Redirect to dashboard

**Comment (including references)**

Tests complete 2FA flow for web interface. Implements separate tracking
for each authentication factor.

### **2. test_web_login_lockout_across_factors (IT-Web-Login-002)** {#test_web_login_lockout_across_factors-it-web-login-002 .unnumbered}

|          |                                         |
|----------|-----------------------------------------|
| Field    | Value                                   |
| Class    | WebLoginPresenter, System, LoginManager |
| Function | Account lockout during 2FA              |
| Author   | Minseok Jo                              |
| Date     | 2025-11-25                              |

**Test Case Description**

Validate that account lockout works correctly across both authentication
factors in 2FA.

**Input Specifications**

• username: \"admin\"

• Incorrect first_password attempts: 5 times

• system_lock_time: 30 seconds

**Detailed Step**

1\. Initialize System with turn_on().

2\. Create WebLoginPresenter.

3\. Attempt first password validation 5 times with wrong password.

4\. Verify account gets locked after 5 failed attempts.

5\. Verify that even correct credentials are rejected while locked.

6\. Verify remaining_time is returned in response.

**Expected Result**

• Account locked after 5 failed first password attempts

• WebLoginOutcome.locked equals True

• WebLoginOutcome.remaining_time shows seconds until unlock

• Correct credentials rejected while locked

**Actual Result (Pass/Fail/Exception)**

• Pass: Account locked correctly

• Pass: Remaining time calculated

• Pass: Locked state enforced

**Comment (including references)**

Tests lockout behavior specific to web 2FA authentication.

## **E. Web Settings Configuration** {#e.-web-settings-configuration .unnumbered}

### **1. test_web_settings_update_integration (IT-Web-Settings-001)** {#test_web_settings_update_integration-it-web-settings-001 .unnumbered}

|          |                                                                    |
|----------|--------------------------------------------------------------------|
| Field    | Value                                                              |
| Class    | WebSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Update system settings via Web interface                           |
| Author   | Minseok Jo                                                         |
| Date     | 2025-11-25                                                         |

**Test Case Description**

Validate that WebSettingsPresenter correctly validates and saves
settings through the System layer.

**Input Specifications**

• monitoring_service_phone: \"111-222-3333\"

• homeowner_phone: \"444-555-6666\"

• system_lock_time: 30

• alarm_delay_time: 60

**Detailed Step**

1\. Initialize System with turn_on().

2\. Create WebSettingsPresenter with System reference.

3\. Call presenter.update_settings() with all parameters.

4\. Presenter validates:

• Phone number formats

• Lock time \> 0

• Alarm delay \>= 0

• Type checking for numeric fields

5\. Presenter calls System.configure_system_setting().

6\. Settings are persisted to database.

**Expected Result**

• WebSettingsOutcome.success equals True

• WebSettingsOutcome.message equals \"Settings updated successfully\"

• All values persisted correctly

• No validation errors

**Actual Result (Pass/Fail/Exception)**

• Pass: Settings saved successfully

• Pass: Values retrievable via get_settings()

**Comment (including references)**

Tests web-specific validation rules including phone format validation.

## **F. System Power Management** {#f.-system-power-management .unnumbered}

### **1. test_system_power_cycle_integration (IT-SYS-Power-001)** {#test_system_power_cycle_integration-it-sys-power-001 .unnumbered}

|          |                                                                                              |
|----------|----------------------------------------------------------------------------------------------|
| Field    | Value                                                                                        |
| Class    | System, StorageManager, ConfigurationManager, LoginManager, SecuritySystem, CameraController |
| Function | Complete power cycle (On -\> Off -\> On)                                                     |
| Author   | Minseok Jo                                                                                   |
| Date     | 2025-11-25                                                                                   |

**Test Case Description**

Validate that System correctly initializes and shuts down all components
during power cycle.

**Input Specifications**

• System starts in OFF state

• Modified settings: lock_time=45, alarm_delay=90

**Detailed Step**

1\. Create System instance (starts in OFF state).

2\. Call turn_on() - Phase 1: Initialize all components.

3\. Verify all managers and controllers are initialized.

4\. Modify settings: lock_time=45, alarm_delay=90.

5\. Call turn_off() - Execute shutdown sequence:

• Save configuration

• Deactivate sensors

• Disable cameras

• Deactivate siren

• Logout user

• Log SYSTEM_SHUTDOWN

• Disconnect database

6\. Call turn_on() again.

7\. Verify settings are preserved.

**Expected Result**

• First turn_on(): Returns True, state becomes READY

• turn_off(): Returns True, state becomes OFF

• Second turn_on(): Returns True, state becomes READY

• Settings preserved: lock_time=45, alarm_delay=90

**Actual Result (Pass/Fail/Exception)**

• Pass: Power cycle completes successfully

• Pass: All components initialized/shutdown correctly

• Pass: Settings preserved across cycle

**Comment (including references)**

Tests complete initialization and shutdown sequences as specified in SDS
pages 50-51.

### **2. test_system_reset_integration (IT-SYS-Reset-001)** {#test_system_reset_integration-it-sys-reset-001 .unnumbered}

|          |                                                  |
|----------|--------------------------------------------------|
| Field    | Value                                            |
| Class    | System, ControlPanelResetPresenter, all managers |
| Function | System reset via Control Panel                   |
| Author   | Minseok Jo                                       |
| Date     | 2025-11-25                                       |

**Test Case Description**

Validate that system reset correctly executes turn_off followed by
turn_on and preserves settings.

**Input Specifications**

• System is running (READY state)

• User is logged in

• Custom settings configured

**Detailed Step**

1\. Initialize System and turn_on().

2\. Login as admin.

3\. Configure custom settings.

4\. Create ControlPanelResetPresenter.

5\. Call presenter.perform_reset().

6\. Presenter calls System.reset().

7\. System executes turn_off() then turn_on().

8\. Verify system returns to READY state.

9\. Verify settings are preserved.

10\. Verify user is logged out (must re-authenticate).

**Expected Result**

• ResetOutcome.success equals True

• ResetOutcome.phase equals 3

• System state equals READY

• Settings preserved

• User session cleared (logged out)

**Actual Result (Pass/Fail/Exception)**

• Pass: Reset completes successfully

• Pass: Settings preserved

• Pass: User logged out

**Comment (including references)**

Tests reset as combination of turn_off and turn_on sequences.

## **G. LoginManager Backend Integration** {#g.-loginmanager-backend-integration .unnumbered}

### **1. test_login_manager_auto_unlock_integration (IT-LM-001)** {#test_login_manager_auto_unlock_integration-it-lm-001 .unnumbered}

|          |                                                    |
|----------|----------------------------------------------------|
| Field    | Value                                              |
| Class    | LoginManager, StorageManager, ConfigurationManager |
| Function | Automatic account unlock after time elapsed        |
| Author   | Minseok Jo                                         |
| Date     | 2025-11-25                                         |

**Test Case Description**

Validate that LoginManager automatically unlocks an account when the
configured lock duration has elapsed.

**Input Specifications**

• Account locked at timestamp T

• system_lock_time: 30 seconds

• Current time: T + 31 seconds

**Detailed Step**

1\. Initialize LoginManager with StorageManager and
ConfigurationManager.

2\. Simulate 5 failed login attempts to lock account.

3\. Record lock timestamp.

4\. Advance time by 31 seconds (mock time).

5\. Attempt login with correct credentials.

6\. LoginManager checks \_check_and_unlock_if_time_passed().

7\. Account is automatically unlocked.

8\. Login proceeds and succeeds.

**Expected Result**

• Account automatically unlocked after 30 seconds

• Console message: \"Account \'admin\' automatically unlocked after 30
seconds\"

• Login succeeds with correct credentials

**Actual Result (Pass/Fail/Exception)**

• Pass: Auto-unlock triggered

• Pass: Login succeeds after unlock

**Comment (including references)**

Tests time-based automatic unlock feature implementation.

## **H. Surveillance Integration Tests** {#h.-surveillance-integration-tests .unnumbered}

### a. test_camera_lifecycle (IT-CAM-LIFECYCLE) {#a.-test_camera_lifecycle-it-cam-lifecycle .unnumbered}

|                                  |                                                                                                 |            |            |             |
|----------------------------------|-------------------------------------------------------------------------------------------------|------------|------------|-------------|
| **Class**                        | **Method**                                                                                      | **Author** | **Date**   | **Version** |
| CameraController, SafeHomeCamera | add_camera(), set_camera_password(), disable_camera(), control_single_camera(), delete_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the complete integrated lifecycle of a single camera:
successful addition, password setup and validation, state change
(enable/disable), control execution (capture/record), and final
deletion.\"

Input Specifications

\"Sequential operations starting with add_camera(100, 200) and including
password setting (\"\"test123\"\"), control commands (0, 1), and
delete_camera().\"

**Detailed Step**

1.  Add camera (ID 1).

2.  Set/validate password.

3.  Disable/re-enable state and check view denial.

4.  Execute control commands (record start/stop).

5.  Delete the camera and check count is 0.

Expected Result

\"All sequential operations must return True (or success code 0). State
changes (e.g., view denial when disabled, record status update) must be
correctly observed.\"

Actual Result (Pass/Fail/Exception)

Pass: The full camera lifecycle succeeded without error.

Comment (including references)

Fundamental integration test verifying the collaboration between the
Controller and the Camera object across all major states.

### b. test_camera_password_workflow_comprehensive (IT-CAM-PW-FLOW) {#b.-test_camera_password_workflow_comprehensive-it-cam-pw-flow .unnumbered}

|                                  |                                                                    |            |            |             |
|----------------------------------|--------------------------------------------------------------------|------------|------------|-------------|
| **Class**                        | **Method**                                                         | **Author** | **Date**   | **Version** |
| CameraController, SafeHomeCamera | set_camera_password(), validate_camera_password(), delete_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies the comprehensive password management workflow, checking all
possible validation codes (-2, 0, 1) and ensuring the password data is
cleanly removed upon camera deletion (-1 returned for validation after
deletion).\"

Input Specifications

\"Actions include validation before setting, setting \"\"secure123\"\",
validating with success/failure inputs, and deleting the camera.\"

**Detailed Step**

1.  Assert -2 (Not Set).

2.  Set password.

3.  Assert 0 (Match) and 1 (Mismatch).

4.  Delete camera.

5.  Assert final validation returns -1 (Nonexistent).

Expected Result

\"Validation must return the correct sequence: -2, 0, 1, and finally -1.
Password data must be cleaned up upon deletion.\"

Actual Result (Pass/Fail/Exception)

Pass: Password workflow and data cleanup succeeded according to security
codes.

Comment (including references)

Critical security integration test verifying all validation paths and
data consistency during de-registration.

### c. test_camera_lifecycle_with_security_events (IT-CAM-SEC-EVENT) {#c.-test_camera_lifecycle_with_security_events-it-cam-sec-event .unnumbered}

|                                  |                                                          |            |            |             |
|----------------------------------|----------------------------------------------------------|------------|------------|-------------|
| **Class**                        | **Method**                                               | **Author** | **Date**   | **Version** |
| CameraController, SafeHomeCamera | add_camera(), trigger_security_event(), disable_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the CameraController correctly dispatches the
take_picture command to only the currently enabled cameras upon
receiving a security event (\"\"INTRUSION\"\", \"\"PANIC\"\").\"

Input Specifications

Initial state: Two cameras exist. Actions: Trigger event (all enabled);
disable one camera; trigger event again.

**Detailed Step**

1.  Add 2 cameras.

2.  Trigger event, assert 2 calls to take_picture (mocked).

3.  Disable camera 1.

4.  Trigger event again, assert 1 call to take_picture.

Expected Result

The mocked take_picture function must be called only for cameras whose
state is enabled=True at the time of the event.

Actual Result (Pass/Fail/Exception)

Pass: Security event dispatch correctly respected the camera\'s
enabled/disabled status.

Comment (including references)

Integration test verifying controller state awareness and dispatch
filtering for security operations.

### d. test_camera_view_integration (IT-CAM-VIEW-CTRL) {#d.-test_camera_view_integration-it-cam-view-ctrl .unnumbered}

|                                  |                                                                   |            |            |             |
|----------------------------------|-------------------------------------------------------------------|------------|------------|-------------|
| **Class**                        | **Method**                                                        | **Author** | **Date**   | **Version** |
| CameraController, SafeHomeCamera | display_single_view(), display_thumbnail_view(), disable_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Verifies that CameraController successfully integrates view retrieval
from multiple cameras (single view and thumbnail view) and correctly
enforces view denial when a camera is disabled.

Input Specifications

\"Actions include retrieving single views for IDs 1 and 2, retrieving
the composite thumbnail view, and checking the single view for ID 1
after disabling it.\"

**Detailed Step**

1.  Add 2 cameras.

2.  Retrieve both single views and the composite view.

3.  Disable camera 1.

4.  Assert display_single_view(1) returns None.

Expected Result

\"View retrieval must succeed when enabled, and return None when
disabled. Both single and thumbnail views must execute without error.\"

Actual Result (Pass/Fail/Exception)

\"Pass: View and state integration succeeded, and view denial was
confirmed.\"

Comment (including references)

Integration test verifying the display interface and state management
for view access control.

### e. test_camera_info_consistency_comprehensive (IT-CAM-INFO-CONS) {#e.-test_camera_info_consistency_comprehensive-it-cam-info-cons .unnumbered}

|                  |                                                       |            |            |             |
|------------------|-------------------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                            | **Author** | **Date**   | **Version** |
| CameraController | add_camera(), get_all_camera_info(), disable_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Verifies that the global information retrieved via
get_all_camera_info() remains consistent and accurate, reflecting the
current state (location, enabled status) even after multiple state
changes (e.g., disabling individual cameras).\"

Input Specifications

Initial state: Four cameras added. Actions: Retrieve info; disable
cameras 2 and 4; retrieve info again.

**Detailed Step**

1.  Add 4 cameras and retrieve info.

2.  Assert initial enabled status (1).

3.  Disable cameras 2 and 4.

4.  Retrieve info again and assert status is 0 for IDs 2 and 4.

Expected Result

The get_all_camera_info() list must accurately report the location and
the updated enabled status (0 or 1) for all cameras.

Actual Result (Pass/Fail/Exception)

Pass: Global state retrieval was consistent and accurate after state
changes.

Comment (including references)

Comprehensive integration test ensuring data integrity and consistency
between the controller\'s internal state and the exposed information.

## I. Security Integration Tests {#i.-security-integration-tests .unnumbered}

| ID                 | Location                                                                   | Scenario                      | Steps                                                               | Expected Result                                                       | Trace                |
|--------------------|----------------------------------------------------------------------------|-------------------------------|---------------------------------------------------------------------|-----------------------------------------------------------------------|----------------------|
| IT-UC2-CTRL-ALARM  | tests/test_controller_security_flow.py:73                                  | Controller-driven alarm cycle | Arm AWAY via controller, emit door event, advance time beyond delay | DISARMED -\> ENTRY_DELAY -\> ALARM_ACTIVE, monitoring INTRUSION_ALARM | SDS VI.2a/VI.2d      |
| IT-UC2-CTRL-DISARM | tests/test_controller_security_flow.py:96                                  | Disarm during entry delay     | Arm STAY, trigger entry event, disarm before deadline               | Alarm returns to IDLE, siren off                                      | SRS UC2d alt         |
| IT-UC2-PANIC       | tests/test_controller_security_flow.py:119                                 | Panic integration             | Invoke panic while disarmed                                         | Immediate ALARM_ACTIVE, monitoring PANIC                              | SRS UC2h             |
| IT-UC2-LIFECYCLE   | tests/common_tests/test_turn_system_on.py:579 / est_turn_system_off.py:318 | Full turn-on/off flows        | Execute start/stop suites and inspect subsystem wiring              | Modules initialized/disposed per SDS lifecycle diagrams               | SDS startup/shutdown |
| IT-UC2-RESTSYNC    | QA Postman run 2025-11-24                                                  | Web REST vs Tk panel sync     | Arm/disarm via /api/security/\* while Tk simulator emits events     | /api/security/status + intrusion logs mirror Tk view                  | SDS VI.2b/VI.2j      |

**Per-test detail (IT-UC2)**

### 1. Alarm test {#alarm-test .unnumbered}

#### a. Alarm `test` {#a.-alarm-test .unnumbered}

| Field             | Value                                              |
|-------------------|----------------------------------------------------|
| Classes / Modules | SystemController, SecuritySystem, MonitoringStub   |
| Functions         | `set_security_mode`, `handle_sensor_event`, `tick` |
| Author            | Jonghwa An                                         |
| Date              | 2025-11-25                                         |
| Version           | 2.0.0                                              |

**Test Case Description**  
Validates that controller-driven arming propagates through the full FSM,
including entry delay timers and monitoring callbacks.

**Input Specifications**  
- Start system in DISARMED state.  
- Authenticated session established.  
- Door sensor assigned to perimeter zone.

**Detailed Steps**  
1. Invoke `set_security_mode("AWAY")` via SystemController.  
2. Emit a mocked door `SensorEvent` (status OPEN).  
3. Advance fake clock past configured entry delay by calling `tick()`
repeatedly.

**Expected Result**  
- State transitions DISARMED -\> ENTRY_DELAY -\> ALARM_ACTIVE.  
- Monitoring stub records `INTRUSION_ALARM`.  
- Event log contains countdown and alarm entries.

**Actual Result (Pass/Fail/Exception)**  
- Pass: assertions capture state changes, monitoring call payload, and
log entries.

**Comment (including references)**  
SDS VI.2d AWAY main flow; SRS UC2c.

#### b. Disarm `tests/test_controller_security_flow.py:96` {#b.-disarm-teststest_controller_security_flow.py96 .unnumbered}

| Field             | Value                                                            |
|-------------------|------------------------------------------------------------------|
| Classes / Modules | SystemController, SecuritySystem                                 |
| Functions         | `set_security_mode`, `handle_sensor_event`, `cancel_entry_delay` |
| Author            | Jonghwa An                                                       |
| Date              | 2025-11-25                                                       |
| Version           | 2.0.0                                                            |

**Test Case Description**  
Demonstrates disarming during ENTRY_DELAY suppresses alarms and resets
readiness.

**Input Specifications**  
- Logged-in user.  
- STAY mode selected.  
- Perimeter door sensor configured.

**Detailed Steps**  
1. Call `set_security_mode("STAY")`.  
2. Emit door OPEN event to enter ENTRY_DELAY.  
3. Before timer expires, invoke `set_security_mode("DISARMED")`.

**Expected Result**  
- Countdown cancelled; siren remains idle.  
- State returns to DISARMED.  
- Monitoring stub receives no alarm.  
- Event log marks intrusion as cancelled.

**Actual Result (Pass/Fail/Exception)**  
- Pass: timer handle cleared, monitoring call absent, log shows
cancellation.

**Comment (including references)**  
SRS UC2d alternate course; SDS VI.2d stay-mode timing.

#### c. Panic `test` {#c.-panic-test .unnumbered}

| Field             | Value                                                         |
|-------------------|---------------------------------------------------------------|
| Classes / Modules | Flask `/api/security/panic`, SystemController, SecuritySystem |
| Functions         | `trigger_panic`, monitoring dispatch                          |
| Author            | Jonghwa An                                                    |
| Date              | 2025-11-25                                                    |
| Version           | 2.0.0                                                         |

**Test Case Description**  
Ensures REST panic endpoint bypasses entry delays and instantly
escalates to monitoring and cameras.

**Input Specifications**  
- System DISARMED.  
- Flask test client authenticated.

**Detailed Steps**  
1. Issue POST `/api/security/panic` via test client.  
2. Inspect controller panic handler invocation.  
3. Verify monitoring stub and camera controller hooks receive panic
reason.

**Expected Result**  
- `alarm_state` switches to ALARM_ACTIVE immediately.  
- Monitoring called with `reason="PANIC"`.  
- Camera controller `trigger_security_event` invoked.  
- Response payload returns HTTP 200 with panic acknowledgment.

**Actual Result (Pass/Fail/Exception)**  
- Pass: all hooks triggered in same tick; response payload matches
expectation.

**Comment (including references)**  
SRS UC2g/UC2h; SDS VI.2h panic escalation pathway.

#### d. Lifecycle `test` {#d.-lifecycle-test .unnumbered}

| Field             | Value                                                           |
|-------------------|-----------------------------------------------------------------|
| Classes / Modules | System (turn_on/turn_off), ConfigurationManager, StorageManager |
| Functions         | `turn_on`, `turn_off`, lifecycle callbacks                      |
| Author            | Jonghwa An                                                      |
| Date              | 2025-11-25                                                      |
| Version           | 2.0.0                                                           |

**Test Case Description**  
Verifies startup and shutdown orchestration initializes and tears down
every UC2 subsystem in order.

**Input Specifications**  
- Fresh System instance with temporary SQLite DB.  
- Mocked device/camera factories registered.

**Detailed Steps**  
1. Call `turn_on()` and capture component references.  
2. Assert each manager/controller is non-null and wired.  
3. Invoke `turn_off()` and confirm sensors, cameras, siren, DB
connections are cleaned up.

**Expected Result**  
- `turn_on()` returns True with state READY.  
- All managers initialized (login, config, storage, controller,
security, cameras, log).  
- `turn_off()` returns True, state OFF, and cleanup log entries
recorded.

**Actual Result (Pass/Fail/Exception)**  
- Pass: lifecycle tests confirm initialization order and teardown
artifacts.

**Comment (including references)**  
SDS startup/shutdown diagrams; SRS UC2j logging expectations.

#### e. Restsync {#e.-restsync .unnumbered}

| Field      | Value                                               |
|------------|-----------------------------------------------------|
| Interfaces | Flask `/api/security/*`, Tk Control Panel simulator |
| Tools      | Postman collection + Tk harness                     |
| Author     | Jonghwa An                                          |
| Date       | 2025-11-24                                          |
| Version    | 1.0.0                                               |

**Test Case Description**  
Demonstrates that REST endpoints and the Tk Control Panel stay
synchronized when commands are issued from both surfaces.

**Input Specifications**  
- Running SafeHome system with seeded sensors.  
- Postman scripts for `/api/security/arm`, `/api/security/status`,
`/api/security/disarm`.  
- Tk simulator capable of emitting sensor events.

**Detailed Steps**  
1. Arm STAY via `/api/security/arm` and confirm Tk UI reflects STAY.  
2. Trigger door event from Tk; poll `/api/security/status` for
ENTRY_DELAY countdown.  
3. Disarm from Tk keypad; verify REST status returns DISARMED and
intrusion log shows cancellation.  
4. Repeat by arming via Tk and polling REST responses for parity.

**Expected Result**  
- REST status JSON matches Tk indicator lights at each step.  
- Intrusion log entries align between dashboard and Tk view.  
- No desynchronization even when commands originate from different
clients.

**Actual Result (Pass/Fail/Exception)**  
- Pass: QA capture shows identical timestamps between
`/api/security/status` payloads and Tk screenshot overlays.

**Comment (including references)**  
SDS VI.2b/VI.2j requirement for UI/API parity; evidence stored in QA
Postman report (docs/UC2_manual_logs/RESTSYNC.pdf).

### 2. System Lifecycle Integration {#system-lifecycle-integration .unnumbered}

#### a. test_turn_on_component_dependencies (LT-011) {#a.-test_turn_on_component_dependencies-lt-011 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validate that all components are initialized in correct order and can
communicate with each other.

**Input Specifications**

- System is in OFF state.

- Steps: Initialize, turn_on(), verify creation order and interactions.

**Detailed Step**

1.  Call turn_on().

2.  Check StorageManager \> ConfigManager \> LoginManager sequence.

**Expected Result**

- All components are initialized

- Components can interact properly

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on component dependencies\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Initialization order in Turn the
System On sequence

#### b. test_turn_on_then_login (LT-012) {#b.-test_turn_on_then_login-lt-012 .unnumbered}

|                      |            |            |            |             |
|----------------------|------------|------------|------------|-------------|
| **Class**            | **Method** | **Author** | **Date**   | **Version** |
| System, LoginManager | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validate that after turn_on, users can successfully log in.

**Input Specifications**

- System is turned on, Default admin account exists.

**Detailed Step**

1.  Turn on system.

2.  Attempt login (admin/1234).

**Expected Result**

- System turns on successfully

- Login with admin/1234 succeeds

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on then login\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Login after system startup flow

#### c. test_turn_on_security_system_integration (LT-013) {#c.-test_turn_on_security_system_integration-lt-013 .unnumbered}

|                        |            |            |            |             |
|------------------------|------------|------------|------------|-------------|
| **Class**              | **Method** | **Author** | **Date**   | **Version** |
| System, SecuritySystem | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validate that SecuritySystem is properly configured with settings from
ConfigurationManager after turn_on.

**Input Specifications**

- System is in OFF state

**Detailed Step**

1.  Call turn_on().

2.  Verify SecuritySystem config matches ConfigManager.

**Expected Result**

- SecuritySystem is initialized

- SecuritySystem uses configuration from ConfigurationManager

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on security system integration\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Security system configuration in
turn_on sequence

#### d. test_turn_off_component_cleanup (LT-027) {#d.-test_turn_off_component_cleanup-lt-027 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

IT-SYS-OFF-001: Validate that all components are properly cleaned up and
can communicate during shutdown sequence.

**Input Specifications**

- Verify all subsystem references are non-null, then run turn_off().

**Detailed Step**

1.  Verify components exist.

2.  Call turn_off().

3.  Verify components cleaned up.

**Expected Result**

- Every component cleans up and releases resources during shutdown.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off component cleanup\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### e. test_turn_off_after_login (LT-028) {#e.-test_turn_off_after_login-lt-028 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

IT-SYS-OFF-002: Validate that system can be turned off after user login.

**Input Specifications**

- Set the system to ACTIVE by logging in, then invoke turn_off().

**Detailed Step**

1.  Login.

2.  Call turn_off().

**Expected Result**

- System gracefully signs out and advances to OFF directly from ACTIVE.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off after login\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### f. test_turn_off_security_system_integration (LT-029) {#f.-test_turn_off_security_system_integration-lt-029 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

IT-SYS-OFF-003: Validate that SecuritySystem alarm is deactivated during
shutdown.

**Input Specifications**

- Confirm SecuritySystem is armed/initialized and call turn_off().

**Detailed Step**

1.  Arm system.

2.  Call turn_off().

3.  Verify alarm deactivated.

**Expected Result**

- Alarm controller and siren deactivate as part of shutdown.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off security system integration\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### g. test_reset_turn_off_turn_on_sequence (LT-041) {#g.-test_reset_turn_off_turn_on_sequence-lt-041 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

IT-SYS-RST-001: Validate that reset properly executes Turn Off followed
by Turn On.

**Input Specifications**

- Ensure every subsystem is initialized, then run reset() to force an
  internal turn_off/turn_on.

**Detailed Step**

1.  Initialize components.

2.  Call reset().

**Expected Result**

- reset() reports success and state returns to READY after the composite
  sequence.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset turn off turn on sequence\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### h. test_reset_after_login_and_settings_change (LT-042) {#h.-test_reset_after_login_and_settings_change-lt-042 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

IT-SYS-RST-002: Validate reset after user login and settings change.

**Input Specifications**

- Login and change configuration data before calling reset().

**Detailed Step**

1.  Login & Change settings.

2.  Call reset().

3.  Verify settings & logout.

**Expected Result**

- Settings remain at the new values while the logged-in session is
  cleared.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset after login and settings change\' behavior
matched lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### i. test_reset_camera_controller_integration (LT-043) {#i.-test_reset_camera_controller_integration-lt-043 .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

IT-SYS-RST-003: Validate CameraController is properly reset.

**Input Specifications**

- Add several cameras via CameraController and then call reset().

**Detailed Step**

1.  Add cameras.

2.  Call reset().

3.  Check camera controller state.

**Expected Result**

- Reset rebuilds the camera controller so it can accept new commands
  post-reset.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset camera controller integration\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

# **V. System Level Tests** {#v.-system-level-tests .unnumbered}

## **A. Log onto the System through Control Panel** {#a.-log-onto-the-system-through-control-panel .unnumbered}

### **1. test_control_panel_login_success_flow (ST-CP-Login-001)** {#test_control_panel_login_success_flow-st-cp-login-001 .unnumbered}

|          |                                                                                |
|----------|--------------------------------------------------------------------------------|
| Field    | Value                                                                          |
| Class    | ControlPanel, ControlPanelLoginPresenter, System, LoginManager, StorageManager |
| Function | Log onto the system through Control Panel                                      |
| Author   | Minseok Jo                                                                     |
| Date     | 2025-11-25                                                                     |

**Test Case Description**

Validate the complete login flow from Control Panel UI through all
system layers to successful authentication.

**Input Specifications**

• ControlPanel receives user_id \"admin\" and password \"1234\"

• StorageManager contains admin credentials (\"admin\", \"1234\")

**Detailed Step**

1\. Seed StorageManager with admin user and password \"1234\".

2\. Initialize System with turn_on().

3\. Initialize ControlPanel connected to System.

4\. Simulate user entering \"admin\" as user_id.

5\. Simulate user entering \"1234\" as password.

6\. Simulate pressing Login button.

7\. ControlPanel creates ControlPanelLoginPresenter.

8\. Presenter.attempt_login() is called.

9\. System.login_with_details() processes authentication.

10\. LoginManager validates against StorageManager.

11\. Success response flows back through layers.

12\. ControlPanel displays success and navigates to MainMenu.

**Expected Result**

• System.login_with_details() returns success

• ControlPanel displays \"Login successful\"

• ControlPanel navigates to MainMenu screen

• User session is established

• Login attempts counter reset to 0

**Actual Result (Pass/Fail/Exception)**

• Pass: Login succeeds through all layers

• Pass: UI displays success message

• Pass: Navigation to MainMenu

**Comment (including references)**

End-to-end test of Control Panel login. Validates complete MVP pattern
flow.

### **2. test_control_panel_login_lockout_and_unlock_flow (ST-CP-Login-002)** {#test_control_panel_login_lockout_and_unlock_flow-st-cp-login-002 .unnumbered}

|          |                                                                |
|----------|----------------------------------------------------------------|
| Field    | Value                                                          |
| Class    | ControlPanel, ControlPanelLoginPresenter, System, LoginManager |
| Function | Account lockout and time-based unlock via Control Panel        |
| Author   | Minseok Jo                                                     |
| Date     | 2025-11-25                                                     |

**Test Case Description**

Validate the complete lockout flow including time-based automatic unlock
through Control Panel.

**Input Specifications**

• 5 failed login attempts with wrong password

• system_lock_time: 30 seconds

• Wait 31 seconds, then try with correct password

**Detailed Step**

1\. Initialize full system stack.

2\. Attempt login 5 times with wrong password \"wrongpw\".

3\. Verify ControlPanel displays remaining attempts on each failure.

4\. After 5th attempt, verify account locked message displayed.

5\. Verify ControlPanel shows \"Account locked. Try again in X
seconds\".

6\. Wait for lock_time to elapse (30 seconds).

7\. Attempt login with correct password \"1234\".

8\. Verify account auto-unlocks and login succeeds.

9\. Verify ControlPanel navigates to MainMenu.

**Expected Result**

• Failed attempts show remaining count

• Account locked after 5 attempts

• Lock message shows remaining time

• Auto-unlock after 30 seconds

• Successful login after unlock

**Actual Result (Pass/Fail/Exception)**

• Pass: Lockout enforced

• Pass: Time-based unlock works

• Pass: Successful login after unlock

**Comment (including references)**

Tests complete lockout lifecycle including automatic unlock feature.

## **B. Configure System Settings through Control Panel** {#b.-configure-system-settings-through-control-panel .unnumbered}

### **1. test_control_panel_settings_save_flow (ST-CP-Settings-001)** {#test_control_panel_settings_save_flow-st-cp-settings-001 .unnumbered}

|          |                                                                                           |
|----------|-------------------------------------------------------------------------------------------|
| Field    | Value                                                                                     |
| Class    | ControlPanel, ControlPanelSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Configure system settings through Control Panel                                           |
| Author   | Minseok Jo                                                                                |
| Date     | 2025-11-25                                                                                |

**Test Case Description**

Validate the complete settings configuration flow from Control Panel UI
through persistence.

**Input Specifications**

• User is logged in

• monitoring_phone: \"911\"

• homeowner_phone: \"010-1234-5678\"

• lock_time: \"45\"

• alarm_delay: \"90\"

**Detailed Step**

1\. Initialize System and login as admin.

2\. Navigate to Settings screen in ControlPanel.

3\. Enter monitoring_phone: \"911\".

4\. Enter homeowner_phone: \"010-1234-5678\".

5\. Enter lock_time: \"45\".

6\. Enter alarm_delay: \"90\".

7\. Press Save button.

8\. ControlPanel creates ControlPanelSettingsPresenter.

9\. Presenter validates all inputs.

10\. Presenter converts strings to appropriate types.

11\. System.configure_system_setting() is called.

12\. ConfigurationManager updates values.

13\. StorageManager persists to database.

14\. ControlPanel displays success message.

**Expected Result**

• Validation passes for all inputs

• Settings saved successfully

• ControlPanel displays \"System settings saved successfully!\"

• Values persist in database

• Values retrievable after system restart

**Actual Result (Pass/Fail/Exception)**

• Pass: All validations pass

• Pass: Settings persisted

• Pass: Success message displayed

**Comment (including references)**

End-to-end settings configuration test.

### **2. test_control_panel_settings_validation_errors (ST-CP-Settings-002)** {#test_control_panel_settings_validation_errors-st-cp-settings-002 .unnumbered}

|          |                                                     |
|----------|-----------------------------------------------------|
| Field    | Value                                               |
| Class    | ControlPanel, ControlPanelSettingsPresenter, System |
| Function | Settings validation error handling                  |
| Author   | Minseok Jo                                          |
| Date     | 2025-11-25                                          |

**Test Case Description**

Validate that invalid settings inputs are properly rejected with
appropriate error messages.

**Input Specifications**

• lock_time: \"abc\" (non-numeric)

• alarm_delay: \"-5\" (negative)

**Detailed Step**

1\. Initialize System and login as admin.

2\. Navigate to Settings screen.

3\. Enter invalid lock_time: \"abc\".

4\. Enter invalid alarm_delay: \"-5\".

5\. Press Save button.

6\. Presenter validates inputs.

7\. Validation fails with multiple errors.

8\. ControlPanel displays error messages.

9\. Settings are NOT saved.

**Expected Result**

• Validation fails

• Error message: \"Invalid input. Please enter valid numbers for time
fields.\"

• Settings not modified

• User remains on Settings screen

**Actual Result (Pass/Fail/Exception)**

• Pass: Validation rejects invalid inputs

• Pass: Error messages displayed

• Pass: No changes persisted

**Comment (including references)**

Tests presenter-level validation preventing invalid data.

## **C. Change Password through Control Panel** {#c.-change-password-through-control-panel .unnumbered}

### **1. test_control_panel_password_change_success (ST-CP-PWD-001)** {#test_control_panel_password_change_success-st-cp-pwd-001 .unnumbered}

|          |                                                                                         |
|----------|-----------------------------------------------------------------------------------------|
| Field    | Value                                                                                   |
| Class    | ControlPanel, ControlPanelChangePasswordPresenter, System, LoginManager, StorageManager |
| Function | Change master password through Control Panel                                            |
| Author   | Minseok Jo                                                                              |
| Date     | 2025-11-25                                                                              |

**Test Case Description**

Validate the complete password change flow from Control Panel through
all phases.

**Input Specifications**

• User logged in as admin with password \"1234\"

• current_password: \"1234\"

• new_password: \"newpass5678\"

• confirm_password: \"newpass5678\"

**Detailed Step**

1\. Initialize System and login with admin/1234.

2\. Navigate to Change Password screen.

3\. Enter current password: \"1234\".

4\. Enter new password: \"newpass5678\".

5\. Enter confirm password: \"newpass5678\".

6\. Press Change Password button.

7\. Presenter validates passwords match and length.

8\. System.change_master_password() executes 3 phases:

• Phase 1: Verify current password

• Phase 2: Validate new password rules

• Phase 3: Confirm and save

9\. Password updated in database.

10\. ControlPanel displays success message.

11\. Logout and login with new password succeeds.

**Expected Result**

• All 3 phases complete successfully

• ControlPanel displays \"Password changed successfully!\"

• Old password no longer works

• New password authenticates correctly

**Actual Result (Pass/Fail/Exception)**

• Pass: Password change completes

• Pass: New password works

• Pass: Old password rejected

**Comment (including references)**

Tests complete 3-phase password change flow through UI.

### **2. test_control_panel_password_change_mismatch (ST-CP-PWD-002)** {#test_control_panel_password_change_mismatch-st-cp-pwd-002 .unnumbered}

|          |                                                           |
|----------|-----------------------------------------------------------|
| Field    | Value                                                     |
| Class    | ControlPanel, ControlPanelChangePasswordPresenter, System |
| Function | Password change with mismatched confirmation              |
| Author   | Minseok Jo                                                |
| Date     | 2025-11-25                                                |

**Test Case Description**

Validate that password change fails when new password and confirmation
don\'t match.

**Input Specifications**

• current_password: \"1234\"

• new_password: \"newpass1111\"

• confirm_password: \"newpass2222\" (mismatch)

**Detailed Step**

1\. Initialize System and login.

2\. Navigate to Change Password screen.

3\. Enter current password: \"1234\".

4\. Enter new password: \"newpass1111\".

5\. Enter confirm password: \"newpass2222\".

6\. Press Change Password button.

7\. Presenter validates passwords do not match.

8\. Error returned before calling System.

9\. ControlPanel displays error message.

10\. Password remains unchanged.

**Expected Result**

• Validation fails at presenter level

• Error message: \"New passwords do not match!\"

• System.change_master_password() is NOT called

• Original password still works

**Actual Result (Pass/Fail/Exception)**

• Pass: Mismatch detected

• Pass: Error displayed

• Pass: Password unchanged

**Comment (including references)**

Tests early validation at presenter layer preventing unnecessary system
calls.

## **D. Log onto the System through Web Browser (2FA)** {#d.-log-onto-the-system-through-web-browser-2fa .unnumbered}

### **1. test_web_login_two_factor_success (ST-Web-Login-001)** {#test_web_login_two_factor_success-st-web-login-001 .unnumbered}

|          |                                                                     |
|----------|---------------------------------------------------------------------|
| Field    | Value                                                               |
| Class    | WebBrowser, WebLoginPresenter, System, LoginManager, StorageManager |
| Function | Two-factor authentication through Web Browser                       |
| Author   | Minseok Jo                                                          |
| Date     | 2025-11-25                                                          |

**Test Case Description**

Validate the complete 2-factor authentication flow through the web
interface.

**Input Specifications**

• username: \"admin\"

• first_password: \"password123\"

• second_password: \"pin1234\"

**Detailed Step**

1\. Initialize System with turn_on().

2\. Open WebBrowser and navigate to login page.

3\. Enter username: \"admin\".

4\. Enter first password: \"password123\".

5\. Click \"Next\" or \"Continue\".

6\. WebLoginPresenter.validate_first_password() called.

7\. First password validated successfully.

8\. Web page transitions to second password input.

9\. Enter second password/PIN: \"pin1234\".

10\. Click \"Login\".

11\. WebLoginPresenter.validate_second_password() called.

12\. Second password validated successfully.

13\. User redirected to dashboard.

14\. Session established.

**Expected Result**

• First password validation succeeds

• UI transitions to second factor input

• Second password validation succeeds

• Redirect to \"/dashboard\"

• User session active

**Actual Result (Pass/Fail/Exception)**

• Pass: Both factors validated

• Pass: Redirect successful

• Pass: Session established

**Comment (including references)**

End-to-end test of 2FA web login flow.

### **2. test_web_login_system_off_rejected (ST-Web-Login-002)** {#test_web_login_system_off_rejected-st-web-login-002 .unnumbered}

|          |                                       |
|----------|---------------------------------------|
| Field    | Value                                 |
| Class    | WebBrowser, WebLoginPresenter, System |
| Function | Web login rejected when system is OFF |
| Author   | Minseok Jo                            |
| Date     | 2025-11-25                            |

**Test Case Description**

Validate that web login is rejected when the system is in OFF state.

**Input Specifications**

• System is OFF (not initialized)

• Valid credentials provided

**Detailed Step**

1\. Create System instance but do NOT call turn_on().

2\. Open WebBrowser and navigate to login page.

3\. Enter valid username and password.

4\. Click login.

5\. WebLoginPresenter checks system state.

6\. System state is OFF.

7\. Login rejected with appropriate message.

8\. User remains on login page.

**Expected Result**

• WebLoginOutcome.success equals False

• WebLoginOutcome.system_off equals True

• Error message: \"System is currently off\"

• No redirect occurs

**Actual Result (Pass/Fail/Exception)**

• Pass: Login rejected

• Pass: System off message displayed

• Pass: User stays on login page

**Comment (including references)**

Precondition validation: System must be ON for login.

## **E. Configure System Settings through Web Browser** {#e.-configure-system-settings-through-web-browser .unnumbered}

### **1. test_web_settings_full_update_flow (ST-Web-Settings-001)** {#test_web_settings_full_update_flow-st-web-settings-001 .unnumbered}

|          |                                                                                |
|----------|--------------------------------------------------------------------------------|
| Field    | Value                                                                          |
| Class    | WebBrowser, WebSettingsPresenter, System, ConfigurationManager, StorageManager |
| Function | Full settings update through Web Browser                                       |
| Author   | Minseok Jo                                                                     |
| Date     | 2025-11-25                                                                     |

**Test Case Description**

Validate the complete settings configuration flow through the web
interface.

**Input Specifications**

• User is logged in via web

• monitoring_service_phone: \"111-222-3333\"

• homeowner_phone: \"444-555-6666\"

• system_lock_time: 30

• alarm_delay_time: 60

**Detailed Step**

1\. Initialize System and complete web 2FA login.

2\. Navigate to Settings page in web interface.

3\. Enter monitoring_service_phone: \"111-222-3333\".

4\. Enter homeowner_phone: \"444-555-6666\".

5\. Enter system_lock_time: 30.

6\. Enter alarm_delay_time: 60.

7\. Click \"Save Settings\".

8\. WebSettingsPresenter.update_settings() called.

9\. Presenter validates all fields.

10\. System.configure_system_setting() called.

11\. Settings persisted to database.

12\. Success message displayed.

13\. Verify settings via get_settings().

**Expected Result**

• All validations pass

• WebSettingsOutcome.success equals True

• Success message: \"Settings updated successfully\"

• Values persisted and retrievable

**Actual Result (Pass/Fail/Exception)**

• Pass: Settings saved

• Pass: Success displayed

• Pass: Values persist

**Comment (including references)**

End-to-end web settings configuration test.

### **2. test_web_settings_multiple_validation_errors (ST-Web-Settings-002)** {#test_web_settings_multiple_validation_errors-st-web-settings-002 .unnumbered}

|          |                                            |
|----------|--------------------------------------------|
| Field    | Value                                      |
| Class    | WebBrowser, WebSettingsPresenter, System   |
| Function | Multiple validation errors in web settings |
| Author   | Minseok Jo                                 |
| Date     | 2025-11-25                                 |

**Test Case Description**

Validate that multiple validation errors are collected and displayed
together.

**Input Specifications**

• monitoring_service_phone: \"invalid\"

• homeowner_phone: \"bad\"

• system_lock_time: 0

• alarm_delay_time: -5

**Detailed Step**

1\. Initialize System and login via web.

2\. Navigate to Settings page.

3\. Enter all invalid values.

4\. Click \"Save Settings\".

5\. WebSettingsPresenter validates all fields.

6\. Multiple validation errors collected:

• Invalid monitoring phone format

• Invalid homeowner phone format

• Lock time must be \> 0

• Alarm delay must be \>= 0

7\. All errors returned in response.

8\. Web page displays all errors.

9\. Settings NOT saved.

**Expected Result**

• WebSettingsOutcome.success equals False

• WebSettingsOutcome.errors contains 4+ errors

• All errors displayed to user

• No changes persisted

**Actual Result (Pass/Fail/Exception)**

• Pass: All errors collected

• Pass: Comprehensive error display

• Pass: No persistence

**Comment (including references)**

Tests comprehensive validation feedback for better user experience.

## **F. System Power On/Off through Control Panel** {#f.-system-power-onoff-through-control-panel .unnumbered}

### **1. test_system_turn_on_full_initialization (ST-SYS-ON-001)** {#test_system_turn_on_full_initialization-st-sys-on-001 .unnumbered}

|          |                                                                                                                   |
|----------|-------------------------------------------------------------------------------------------------------------------|
| Field    | Value                                                                                                             |
| Class    | ControlPanel, System, StorageManager, ConfigurationManager, LoginManager, SecuritySystem, CameraController, Siren |
| Function | System turn on through Control Panel                                                                              |
| Author   | Minseok Jo                                                                                                        |
| Date     | 2025-11-25                                                                                                        |

**Test Case Description**

Validate complete system initialization when turning on through Control
Panel.

**Input Specifications**

• System is in OFF state

• ControlPanel power button pressed

**Detailed Step**

1\. System starts in OFF state.

2\. User presses Power On button on ControlPanel.

3\. ControlPanel calls System.turn_on().

4\. System initialization sequence:

• Initialize StorageManager (connect to database)

• Initialize ConfigurationManager (load settings)

• Initialize LoginManager (setup authentication)

• Initialize LogManager (setup logging)

• Initialize SystemController

• Initialize SecuritySystem (sensors)

• Initialize CameraController

• Initialize Siren

• Initialize AuthService

• Initialize SettingsService

5\. System state changes to READY.

6\. ControlPanel displays \"System Ready\".

7\. All components operational.

**Expected Result**

• System.turn_on() returns True

• System.system_state equals READY

• All components initialized (not None)

• ControlPanel shows ready status

**Actual Result (Pass/Fail/Exception)**

• Pass: Initialization complete

• Pass: All components ready

• Pass: UI updated

**Comment (including references)**

Complete system initialization as per SDS page 50.

### **2. test_system_turn_off_full_shutdown (ST-SYS-OFF-001)** {#test_system_turn_off_full_shutdown-st-sys-off-001 .unnumbered}

|          |                                                    |
|----------|----------------------------------------------------|
| Field    | Value                                              |
| Class    | ControlPanel, System, all managers and controllers |
| Function | System turn off through Control Panel              |
| Author   | Minseok Jo                                         |
| Date     | 2025-11-25                                         |

**Test Case Description**

Validate complete system shutdown sequence when turning off through
Control Panel.

**Input Specifications**

• System is in READY state

• User is logged in

• Sensors and cameras are active

**Detailed Step**

1\. System is running with user logged in.

2\. Some sensors and cameras are active.

3\. User presses Power Off button on ControlPanel.

4\. ControlPanel calls System.turn_off().

5\. System shutdown sequence:

• Phase 1: Save configuration to database

• Phase 2: Deactivate all sensors

• Phase 3: Disable all cameras

• Phase 4: Deactivate siren

• Phase 5: Logout current user

• Phase 6: Log SYSTEM_SHUTDOWN event

• Phase 7: Disconnect database

6\. System state changes to OFF.

7\. ControlPanel displays \"System Off\".

**Expected Result**

• System.turn_off() returns True

• System.system_state equals OFF

• All sensors deactivated

• All cameras disabled

• Siren off

• User logged out

• Configuration saved

**Actual Result (Pass/Fail/Exception)**

• Pass: Shutdown complete

• Pass: All components deactivated

• Pass: Data persisted

**Comment (including references)**

Complete shutdown sequence as per SDS page 51.

### **3. test_system_reset_through_control_panel (ST-SYS-Reset-001)** {#test_system_reset_through_control_panel-st-sys-reset-001 .unnumbered}

|          |                                                                  |
|----------|------------------------------------------------------------------|
| Field    | Value                                                            |
| Class    | ControlPanel, ControlPanelResetPresenter, System, all components |
| Function | System reset through Control Panel                               |
| Author   | Minseok Jo                                                       |
| Date     | 2025-11-25                                                       |

**Test Case Description**

Validate complete system reset flow through Control Panel.

**Input Specifications**

• System is running

• User is logged in

• Custom settings: lock_time=45, alarm_delay=90

**Detailed Step**

1\. System running with custom settings configured.

2\. User logged in as admin.

3\. User selects Reset option in ControlPanel menu.

4\. ControlPanel shows confirmation dialog.

5\. User confirms reset.

6\. ControlPanel creates ControlPanelResetPresenter.

7\. Presenter calls System.reset().

8\. System.reset() executes:

• turn_off() (saves settings)

• turn_on() (reloads settings)

9\. System returns to READY state.

10\. User is logged out (session cleared).

11\. Settings are preserved.

12\. ControlPanel shows login screen.

**Expected Result**

• Reset completes with phase 3

• System in READY state

• Settings preserved (lock_time=45, alarm_delay=90)

• User logged out

• ControlPanel on login screen

**Actual Result (Pass/Fail/Exception)**

• Pass: Reset successful

• Pass: Settings preserved

• Pass: User logged out

**Comment (including references)**

Reset combines turn_off and turn_on sequences with data preservation.

## G. Surveillance Level Tests {#g.-surveillance-level-tests .unnumbered}

### 1. Display Specific Camera View (test_st_surv_a_001_display_camera_view_complete_flow) {#display-specific-camera-view-test_st_surv_a_001_display_camera_view_complete_flow .unnumbered}

|                          |                                                                                       |            |            |             |
|--------------------------|---------------------------------------------------------------------------------------|------------|------------|-------------|
| **Class**                | **Method**                                                                            | **Author** | **Date**   | **Version** |
| System, CameraController | login_with_details(), add_camera(), validate_camera_password(), display_single_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Validate the complete end-to-end flow from web login to displaying
specific camera view (UC a) at 1 frame per second.

Input Specifications

\"Web login (admin/1234), Camera 1 setup, Password validation
(\"\"camera123\"\").\"

**Detailed Step**

1.  Web login.

2.  Setup Camera 1 with password.

3.  Validate password (Step 6-7).

4.  Call display_single_view(1) (Step 9-10).

Expected Result

Login succeeds; Password validation returns 0 (Success);
display_single_view returns a non-null view object or is handled
gracefully (not crash).

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

Complete flow test for viewing the feed after necessary authentication
and setup.

### 2. Display View Disabled Camera (test_st_surv_a_002_display_view_disabled_camera) {#display-view-disabled-camera-test_st_surv_a_002_display_view_disabled_camera .unnumbered}

|                          |                                         |            |            |             |
|--------------------------|-----------------------------------------|------------|------------|-------------|
| **Class**                | **Method**                              | **Author** | **Date**   | **Version** |
| System, CameraController | disable_camera(), display_single_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Validate that the view button is disabled (view access is denied) when
the camera is explicitly disabled.

Input Specifications

Camera 1 setup; Action: disable_camera(1). Attempt to view.

**Detailed Step**

1.  Login/Setup Camera 1.

2.  Disable the camera.

3.  Call display_single_view(1).

4.  Assert view access is blocked.

Expected Result

display_single_view returns None (view access denied/blocked).

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

Security policy verification: disabled cameras must not expose their
feed.

### 3. Pan/Zoom Functionality (test_st_surv_b_001_pan_zoom_camera_view) {#panzoom-functionality-test_st_surv_b_001_pan_zoom_camera_view .unnumbered}

|                                 |                                                |            |            |             |
|---------------------------------|------------------------------------------------|------------|------------|-------------|
| **Class**                       | **Method**                                     | **Author** | **Date**   | **Version** |
| SafeHomeCamera (via Controller) | pan_left(), pan_right(), zoom_in(), zoom_out() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Validate the integrated pan and zoom functionality (UC b) for the
specific camera view.

Input Specifications

\"Login/Setup Camera 1. Action: Direct calls to camera.pan_left(),
camera.pan_right(), camera.zoom_in(), camera.zoom_out().\"

**Detailed Step**

1.  Validate password.

2.  Get Camera object.

3.  Call pan_left() and assert angle decreases (or hits min).

4.  Call zoom_in() and assert level increases.

Expected Result

\"All pan and zoom operations must return True. Angles and levels must
update correctly, adhering to boundary conditions (-180.0 to 180.0, 1 to
10).\"

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

Integrated test verifying low-level camera control operations.

### 5. Set Camera Password (test_st_surv_c_001_set_camera_password_complete_flow) {#set-camera-password-test_st_surv_c_001_set_camera_password_complete_flow .unnumbered}

|                          |                                                   |            |            |             |
|--------------------------|---------------------------------------------------|------------|------------|-------------|
| **Class**                | **Method**                                        | **Author** | **Date**   | **Version** |
| System, CameraController | set_camera_password(), validate_camera_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Validate the complete end-to-end flow for setting a new camera
password (UC c), ensuring the old password no longer works and the new
one is valid.\"

Input Specifications

\"Setup Camera 1 with \"\"oldpass123\"\". Action: Set new password
\"\"newpass456\"\".\"

**Detailed Step**

1.  Validate existing password (oldpass123).

2.  Set new password (newpass456).

3.  Verify the new password works (0).

4.  Verify the old password fails (1).

Expected Result

New password validation returns 0. Old password validation returns 1.
The password update succeeds.

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

Complete flow test verifying password update functionality and security.

### 6. Set Password Mismatch Handling (test_st_surv_c_003_set_password_mismatch_handling) {#set-password-mismatch-handling-test_st_surv_c_003_set_password_mismatch_handling .unnumbered}

|                  |                                                   |            |            |             |
|------------------|---------------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                        | **Author** | **Date**   | **Version** |
| CameraController | set_camera_password(), validate_camera_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Validate that if new passwords mismatch (simulated UI error), the
system correctly rejects the change, and the original password remains
valid .\"

Input Specifications

\"Setup Camera 1 with \"\"oldpass123\"\". Action: Attempt to set
mismatched passwords (\"\"newpass1\"\" and \"\"newpass2\"\").\"

**Detailed Step**

1.  Validate existing password (oldpass123).

2.  Simulate password mismatch attempt.

3.  Assert old password still works (0).

4.  Assert new passwords fail validation.

Expected Result

Original password validation returns 0. New password validation returns
non-0 (mismatch failure).

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

System robustness check for rejecting inconsistent inputs during a
critical setting process.

### 7. Delete Camera Password (test_st_surv_d_001_delete_camera_password_complete_flow) {#delete-camera-password-test_st_surv_d_001_delete_camera_password_complete_flow .unnumbered}

|                  |                                                        |            |            |             |
|------------------|--------------------------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                                             | **Author** | **Date**   | **Version** |
| CameraController | validate_camera_password(), \_delete_camera_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Validate the complete end-to-end flow for deleting a camera password
(UC d), ensuring the final state is \'Password Not Set\'.\"

Input Specifications

\"Setup Camera 1 with \"\"delete123\"\". Action: Call internal
\_delete_camera_password(1).\"

**Detailed Step**

1.  Validate existing password (0).

2.  Call \_delete_camera_password(1).

3.  Manually clear state of SafeHomeCamera object (simulated
    consequence).

4.  Assert final validation returns -2 (Password Not Set).

Expected Result

Password deletion succeeds. Final password validation returns -2.

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

Complete flow test verifying password removal and resulting status
consistency.

### 8. View Thumbnail Shots (test_st_surv_e_001_view_thumbnail_shots_complete_flow) {#view-thumbnail-shots-test_st_surv_e_001_view_thumbnail_shots_complete_flow .unnumbered}

|                  |                                        |            |            |             |
|------------------|----------------------------------------|------------|------------|-------------|
| **Class**        | **Method**                             | **Author** | **Date**   | **Version** |
| CameraController | add_camera(), display_thumbnail_view() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Validate the complete flow from web login to viewing the composite
thumbnail shots (UC e) of multiple cameras.

Input Specifications

Web login. Action: Add three cameras. Call display_thumbnail_view().

**Detailed Step**

1.  Login.

2.  Add cameras 1, 2, and 3.

3.  Call display_thumbnail_view().

4.  Assert result is non-None (Image) or handled gracefully.

5.  Verify camera count is 3.

Expected Result

\"display_thumbnail_view executes successfully, returning a composite
view object or handled gracefully, and all three cameras are included in
the info list.\"

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

System test for the composite view generation functionality.

### 9. Enable Camera (test_st_surv_f_001_enable_camera_complete_flow) {#enable-camera-test_st_surv_f_001_enable_camera_complete_flow .unnumbered}

|                  |                                   |            |            |             |
|------------------|-----------------------------------|------------|------------|-------------|
| **Class**        | **Method**                        | **Author** | **Date**   | **Version** |
| CameraController | disable_camera(), enable_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Validate the complete flow for enabling a camera (UC f), ensuring the
status transitions from disabled to enabled and the state is correctly
reflected in the system.\"

Input Specifications

\"Setup Camera 1. Action: Disable camera, then call enable_camera(1).\"

**Detailed Step**

1.  Disable camera 1.

2.  Call enable_camera(1).

3.  Assert the returned result is True.

4.  Assert the camera\'s state is enabled=True in both the controller
    info and the camera object.

Expected Result

enable_camera returns True. Final camera state is confirmed to be
Enabled (True).

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

System test for state change operation (Disabled to Enabled).

### 10. Disable Camera (test_st_surv_g_001_disable_camera_complete_flow) {#disable-camera-test_st_surv_g_001_disable_camera_complete_flow .unnumbered}

|                  |                  |            |            |             |
|------------------|------------------|------------|------------|-------------|
| **Class**        | **Method**       | **Author** | **Date**   | **Version** |
| CameraController | disable_camera() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

\"Validate the complete flow for disabling a camera (UC g), ensuring the
status transitions from enabled to disabled and the state is correctly
reflected in the system.\"

Input Specifications

Setup Camera 1. Action: Call disable_camera(1).

**Detailed Step**

1.  Assert initial state is Enabled (True).

2.  Call disable_camera(1).

3.  Assert the returned result is True.

4.  Assert the camera\'s state is enabled=False in both the controller
    info and the camera object.

Expected Result

disable_camera returns True. Final camera state is confirmed to be
Disabled (False).

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

System test for state change operation (Enabled to Disabled).

### 11. Password Lockout Exception (test_st_surv_exception_002_password_lockout_after_three_attempts) {#password-lockout-exception-test_st_surv_exception_002_password_lockout_after_three_attempts .unnumbered}

|                          |                            |            |            |             |
|--------------------------|----------------------------|------------|------------|-------------|
| **Class**                | **Method**                 | **Author** | **Date**   | **Version** |
| System, CameraController | validate_camera_password() | Jien Lee   | 2025.11.23 | 1.0.1       |

Test Case Description

Validate that the system correctly tracks failed password attempts (3)
and triggers a system lockout or appropriate failure response upon the
third failure.

Input Specifications

\"Setup Camera 1 with \"\"correct123\"\". Action: Call
validate_camera_password(1, \"\"wrong\"\") three consecutive times.\"

**Detailed Step**

1.  Call validate_camera_password with incorrect input 3 times.

2.  Assert that attempts are tracked (attempts \>= 3).

3.  Verify that the logic path for system lockout is triggered/reached
    (implied by the test structure).

Expected Result

\"Password validation fails three times, indicating the condition for
system lockout is met.\"

Actual Result (Pass/Fail/Exception)

Pass

Comment (including references)

System robustness check for security measures against brute-force
password guessing.

## H. Security System-Level Tests {#h.-security-system-level-tests .unnumbered}

| ID             | Scenario                           | Steps                                                            | Expected Outputs                                                                          | Evidence                                  |
|----------------|------------------------------------|------------------------------------------------------------------|-------------------------------------------------------------------------------------------|-------------------------------------------|
| SLT-UC2-STAY   | Tk Control Panel Stay flow         | Launch python main.py, log in, arm STAY, open Front Door, disarm | Stay indicator lit, entry delay banner counts down, intrusion log entry cleared on disarm | docs/UC2_manual_logs/SLT-UC2-STAY.png     |
| SLT-UC2-PANIC  | Web dashboard panic                | /dashboard panic button while system DISARMED                    | Toast "Panic alarm dispatched", siren LED red, monitoring pane shows PANIC                | Video clip 2025-11-25 (QA SharePoint)     |
| SLT-UC2-ZONE   | Dashboard zone CRUD                | Create "Guest Wing", assign/remove sensors via web UI            | Zones table + Tk panel badges update immediately                                          | Operator journal screenshots (2025-11-24) |
| SLT-UC2-LEGACY | Legacy /arm//status//disarm routes | Hit legacy endpoints via browser                                 | HTML feedback matches SDS legacy Control Panel spec                                       | Browser capture archived in QA log        |

**Manual execution notes** - `SLT-UC2-STAY` - Conducted on Windows 11
with a USB keypad simulator; screenshots capture the Tk timer overlay,
siren LED state, and the intrusion log entries before/after disarm to
prove log cleanup. - `SLT-UC2-PANIC` - Recorded as a 30 second MP4
showing the Flask dashboard panic button, the siren widget flipping red
immediately, and the monitoring list populating `PANIC`; audio output
muted per lab policy. - `SLT-UC2-ZONE` - Creates, assigns, and deletes a
"Guest Wing" zone using `/api/zones` indirectly through the dashboard;
simultaneously records the Tk screen to show that badges refresh without
application restart. - `SLT-UC2-LEGACY` - Uses curl + browser to access
`/arm`, `/status`, `/disarm`; verifies HTML text aligns with SDS's
legacy copy and that event logs still populate even when using the
deprecated endpoints.

**Per-test detail (SLT)**

### 1. Security Level Tests {#security-level-tests .unnumbered}

#### a. STAY - Tk Control Panel Stay Flow {#a.-stay---tk-control-panel-stay-flow .unnumbered}

| Field       | Value                                   |
|-------------|-----------------------------------------|
| Interface   | Tk Control Panel (main.py)              |
| Test Lead   | Jonghwa An                              |
| Date        | 2025-11-24                              |
| Environment | Windows 11, USB keypad simulator        |
| Evidence    | `docs/UC2_manual_logs/SLT-UC2-STAY.png` |

**Test Case Description**  
Validates the full Stay-mode UX on the Tk control panel, including entry
delay countdown, siren indicator, and log cleanup after disarm.

**Input Specifications**  
- Use seeded admin credentials.  
- Default entry delay 30 seconds.  
- Front Door sensor assigned to perimeter zone.

**Detailed Steps**  
1. Launch `python main.py` and log in via control panel keypad.  
2. Select STAY mode; verify STAY indicator lights.  
3. Open the Front Door (simulated sensor).  
4. Observe entry delay banner countdown.  
5. Disarm before the countdown expires.

**Expected Result**  
- STAY LED turns on; entry delay banner counts down from 30s.  
- Siren indicator remains amber until disarm.  
- Intrusion log entry recorded, then marked cleared after disarm.

**Actual Result (Pass/Fail/Exception)**  
- Pass: screenshot captures countdown overlay, LED colors, and
before/after log entries.

**Comment (including references)**  
SDS VI.2a UI spec; evidence stored alongside coverage artefacts.

#### b. PANIC - Web Dashboard Panic {#b.-panic---web-dashboard-panic .unnumbered}

| Field       | Value                                    |
|-------------|------------------------------------------|
| Interface   | Flask `/dashboard`                       |
| Test Lead   | Jonghwa An                               |
| Date        | 2025-11-25                               |
| Environment | Windows 11, Chrome                       |
| Evidence    | QA SharePoint video (link noted in docs) |

**Test Case Description**  
Demonstrates panic behavior via the web dashboard, showing immediate
siren activation and monitoring update even when disarmed.

**Input Specifications**  
- System DISARMED.  
- Authenticated web session.

**Detailed Steps**  
1. Navigate to `/dashboard` and log in via 2FA.  
2. Click the Panic button.  
3. Observe toast notification, siren LED, and monitoring pane updates.  
4. Verify event log captures panic entry.

**Expected Result**  
- Toast "Panic alarm dispatched".  
- Siren widget turns red.  
- Monitoring list shows `PANIC`.  
- Intrusion log entry flagged as panic.

**Actual Result (Pass/Fail/Exception)**  
- Pass: video capture shows UI transitions and monitoring entry
appearing immediately.

**Comment (including references)**  
SRS UC2g/UC2h; SDS VI.2h panic UI flow.

#### c. ZONE - Dashboard Zone CRUD {#c.-zone---dashboard-zone-crud .unnumbered}

| Field       | Value                                     |
|-------------|-------------------------------------------|
| Interface   | `/configure` dashboard                    |
| Test Lead   | Jonghwa An                                |
| Date        | 2025-11-24                                |
| Environment | Windows 11, Chrome                        |
| Evidence    | Operator journal screenshots (2025-11-24) |

**Test Case Description**  
Ensures zone creation, sensor assignment, and deletion propagate to both
web UI and Tk badges without restart.

**Input Specifications**  
- Logged-in admin session.  
- Access to `/api/zones` through dashboard controls.  
- Tk panel running simultaneously.

**Detailed Steps**  
1. Navigate to Configure page.  
2. Create zone "Guest Wing".  
3. Assign Front Door sensor to the new zone.  
4. Remove assignment and delete the zone.  
5. Observe Tk panel badges during each step.

**Expected Result**  
- Zones table updates in real time.  
- Tk badges display the new zone, then update after removal.  
- Database reflects CRUD operations.

**Actual Result (Pass/Fail/Exception)**  
- Pass: screenshots show synchronized updates across dashboard and Tk.

**Comment (including references)**  
SRS UC2e; SDS II.5 zone management.

#### d. LEGACY - Legacy `/arm` `/status` `/disarm` {#d.-legacy---legacy-arm-status-disarm .unnumbered}

| Field       | Value                                                 |
|-------------|-------------------------------------------------------|
| Interface   | Legacy Flask templates (`/arm`, `/status`, `/disarm`) |
| Test Lead   | Jonghwa An                                            |
| Date        | 2025-11-23                                            |
| Environment | Windows 11, Edge + curl                               |
| Evidence    | Browser capture archived in QA log                    |

**Test Case Description**  
Confirms legacy endpoints remain functional and match SDS copy, ensuring
backward compatibility.

**Input Specifications**  
- System running with legacy pages enabled.  
- Browser and curl client available.

**Detailed Steps**  
1. Hit `/arm` to arm the system; note HTML response.  
2. Invoke `/status` to confirm state text matches SDS spec.  
3. Trigger `/disarm`; verify message and log entry.  
4. Review intrusion log to ensure events recorded despite legacy path
usage.

**Expected Result**  
- HTML content matches SDS legacy text.  
- Alarm state changes accordingly.  
- Logs capture each command invocation.

**Actual Result (Pass/Fail/Exception)**  
- Pass: screenshots show expected copy; event log entries recorded.

**Comment (including references)**  
SDS VI.2a legacy path requirements; ensures compatibility during
migration.

### 2. System Lifecycle End-to-End {#system-lifecycle-end-to-end .unnumbered}

#### a. test_complete_turn_on_flow  {#a.-test_complete_turn_on_flow .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_on()  | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validate the complete system turn on flow including all component
initialization and state transitions.

**Input Specifications**

- Fresh system instance.

**Detailed Step**

1.  Execute full turn_on sequence.

2.  Verify all subsystems.

**Expected Result**

- System transitions from OFF to READY

- All components functional

- Admin login works

- Settings are accessible

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Complete turn on flow\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset); Complete Turn the System On
sequence diagram

#### b. test_complete_turn_off_flow {#b.-test_complete_turn_off_flow .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

ST-SYS-OFF-001: Validate the complete system turn off flow including all
component cleanup and state transitions.

**Input Specifications**

- Create a fresh System, turn it on, log in, interact, then call
  turn_off().

**Detailed Step**

1.  Use system (login, etc.).

2.  Call turn_off().

3.  Verify full shutdown.

**Expected Result**

- Composite flow completes with every subsystem stopped and system state
  OFF.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Complete turn off flow\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### c. test_turn_off_data_persistence {#c.-test_turn_off_data_persistence .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

ST-SYS-OFF-002: Validate that data is persisted correctly during
shutdown and can be loaded on next turn_on.

**Input Specifications**

- Turn on the system, mutate configuration data, turn off, then back on
  for verification.

**Detailed Step**

1.  Modify data.

2.  Turn off.

3.  Turn on and verify data.

**Expected Result**

- Data persists across the shutdown/start cycle and settings remain
  accessible.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn off data persistence\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### d. test_turn_on_turn_off_cycle {#d.-test_turn_on_turn_off_cycle .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | turn_off() | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

ST-SYS-OFF-003: Validate that system can be turned on and off multiple
times without issues.

**Input Specifications**

- Iterate through several turn_on()/turn_off() cycles using one System
  instance.

**Detailed Step**

1.  Cycle On/Off multiple times.

2.  Verify stability.

**Expected Result**

- Each iteration succeeds, with READY reached after turn_on and OFF
  after turn_off.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Turn on turn off cycle\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### e. test_complete_reset_flow  {#e.-test_complete_reset_flow .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

ST-SYS-RST-001: Validate complete reset flow including all phases and
state transitions.

**Input Specifications**

- Drive the full lifecycle: turn on, login, adjust settings, then invoke
  reset().

**Detailed Step**

1.  Use system fully.

2.  Call reset().

3.  Verify restoration to READY.

**Expected Result**

- All three phases finish, settings persist, and the system is ready for
  another login.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Complete reset flow\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### f. test_multiple_reset_cycles  {#f.-test_multiple_reset_cycles .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

ST-SYS-RST-002: Validate system can be reset multiple times.

**Input Specifications**

- Turn on once, then execute three consecutive reset() calls within a
  loop.

**Detailed Step**

1.  Loop reset() 3 times.

2.  Check success each time.

**Expected Result**

- Every reset succeeds and leaves the system READY with managers intact.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Multiple reset cycles\' behavior matched lifecycle
expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

#### g. test_reset_preserves_all_settings {#g.-test_reset_preserves_all_settings .unnumbered}

|           |            |            |            |             |
|-----------|------------|------------|------------|-------------|
| **Class** | **Method** | **Author** | **Date**   | **Version** |
| System    | reset()    | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

ST-SYS-RST-003: Validate all types of settings are preserved.

**Input Specifications**

- Configure monitoring/homeowner phones plus timing values before
  invoking reset().

**Detailed Step**

1.  Configure all setting types.

2.  Call reset().

3.  Verify values.

**Expected Result**

- After reset, all configured values remain unchanged.

Actual Result (Pass/Fail/Exception)

Pass: Observed \'Reset preserves all settings\' behavior matched
lifecycle expectations.

Comment (including references)

SDS lifecycle (startup/shutdown/reset)

### 3. Zone Assignments {#zone-assignments .unnumbered}

#### A. SecuritySystem {#a.-securitysystem .unnumbered}

##### a. Explicit Zone Tracking {#a.-explicit-zone-tracking .unnumbered}

|                |                  |            |            |             |
|----------------|------------------|------------|------------|-------------|
| **Class**      | **Method**       | **Author** | **Date**   | **Version** |
| SecuritySystem | N/A (Zone Logic) | Jonghwa An | 2025-11-25 | 2.0.0       |

Test Case Description

Validates \'Security system tracks explicit zone assignments\' behavior.

Input Specifications

See tests/test_zone_assignments.py

Detailed Step

Run tests/test_zone_assignments.py:52

Expected Result

Security system correctly tracks assignments.

Actual Result (Pass/Fail/Exception)

Pass: observed state/response matches SDS/SRS design.

Comment (including references)

Trace: SRS UC2e / SDS VI.2f

# VI. Who did what {#vi.-who-did-what .unnumbered}

<table>
<colgroup>
<col style="width: 14%" />
<col style="width: 85%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Name</strong></th>
<th><strong>Contribution</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>Jien Lee</strong></td>
<td><p>The scope of work focused on core feature development, quality
assurance, and essential project documentation for the SafeHome
system.</p>
<p>Core Feature Development: Development of the surveillance system was
completed with the implementation of the SafeHomeCamera and Camera
classes, establishing the camera object definitions and primary control
logic. The core security response mechanism was also integrated, which
included the implementation of the Alarm class and the establishment of
the required sensor-to-alarm connection logic for automated intrusion
handling. Additionally, the User Interface (UI) underwent functional and
aesthetic refinement to improve the overall user experience.</p>
<p>Documentation and Quality Assurance (QA): Contributions to the
Implementation and Testing document included the authoring of Unit Tests
specifically for the surveillance components. The system's architecture
was documented through the creation of a Class Diagram that reflected
the implemented classes. Furthermore, the necessary Integration Test and
System Level Test cases were developed to validate the end-to-end
functionality of the surveillance features. The final deliverable
involved drafting the "Who Did What" documentation to formally record
individual contributions. Also wrote the Overview of Implementation and
Testing</p></td>
</tr>
<tr class="even">
<td><strong>Jonghwa An</strong></td>
<td><p>The scope of work was comprehensive, covering core security
feature implementation, quality assurance for the security subsystem,
and overall project documentation and file management.</p>
<p>Core Feature Development: The primary implementation task was the
development of the security features of the SafeHome system. This
involved defining and implementing all necessary classes and logic to
handle system states (e.g., Armed, Disarmed) and user
authentication.</p>
<p>Code Quality and Coverage: A significant effort was dedicated to
improving the project's overall code quality. This included analyzing
and enhancing the entire file coverage, specifically addressing and
documenting the Coverage Branch details to ensure robust and fully
tested code paths across the project.</p>
<p>Documentation and Quality Assurance (QA): Extensive testing and
documentation were completed for the security subsystem. This work
included authoring the Unit Tests for all security-related components to
ensure individual module integrity. The system's design was documented
by creating the necessary Class Diagram that includes the security
features. Furthermore, the required Integration Test and System Level
Test cases were developed to validate the security subsystem's
end-to-end functionality. Finally, all independently authored
documentation files were consolidated through the document integration
effort, ensuring a unified and consistent final project document
structure.</p></td>
</tr>
<tr class="odd">
<td><strong>Minseok Jo</strong></td>
<td><p>The scope of work encompassed the implementation of common system
functionalities, the foundational setup of the user interface, and
comprehensive documentation for the common subsystem.</p>
<p>Core Feature Development and Foundation: Implementation of the common
system functionalities was completed, providing shared resources and
utilities for other subsystems. This involved laying the initial
foundation for both the Control Panel and the Web User Interface (UI),
establishing the basic structural framework and navigation for both
access points.</p>
<p>Project Management and Documentation: A significant project
management responsibility was fulfilled through the consistent creation
and maintenance of the Meeting Log, documenting decisions and progress
across team meetings.</p>
<p>Documentation and Quality Assurance (QA): Extensive testing and
documentation were performed for the common subsystem. This work
included authoring the Unit Tests for all common components to ensure
individual module integrity. The system's design was documented by
creating the necessary Class Diagram that includes the common features.
Furthermore, the required Integration Test and System Level Test cases
were developed to validate the common subsystem's functionality and its
interactions with other modules.</p></td>
</tr>
</tbody>
</table>

# **VII. Meeting Log** {#vii.-meeting-log .unnumbered}

## **Python UI and Integration Planning** {#python-ui-and-integration-planning .unnumbered}

<table>
<colgroup>
<col style="width: 18%" />
<col style="width: 81%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Category</strong></th>
<th><strong>Details</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Date &amp; Time</td>
<td>November 20, 2025 (Thursday), 5:30 PM – 9:30 AM (4h)</td>
</tr>
<tr class="even">
<td>Attendees</td>
<td>Jien Lee, Jonghwa An, Minseok Jo </td>
</tr>
<tr class="odd">
<td>Purpose</td>
<td>Review code and UI status, discuss role assignments and integration
testing strategy</td>
</tr>
<tr class="even">
<td>Discussion Summary</td>
<td><p>- Reviewed current Python-based UI implementations; noted main
screens incomplete, control panel functional </p>
<p>- Decided UI button linking is primary front-end task, with minimal
additional front-end design </p>
<p>- Role assignment via ladder draw: Minseok for common + integration
testing, Jien for security, Jonghwa for surveillance </p>
<p>- Discussed need for integration testing to combine feature modules,
agreeing team lead to handle integration effort </p>
<p>- Mentioned associated test documentation to be prepared as part of
coursework following class content </p>
<p>- Clarified testing documentation templates available in class
resources (KLMS) </p>
<p>- Considered feasibility of using web hosting vs. local web server;
consensus on local hosting for project </p>
<p>- Debated choice of frameworks and infrastructure setup for fastest
lightweight deployment (FastAPI favored over Flask) </p>
<p>- Assigned responsibilities for documentation processing and project
progress tracking </p>
<p>- Planned further meetings and project check-ins to monitor progress
and resolve issues</p></td>
</tr>
<tr class="odd">
<td>Decisions Made</td>
<td><p>- Each member proceeds on assigned functional modules and
documentation </p>
<p>- Team lead to integrate modules and handle GUI linking </p>
<p>- Use local server deployment for web UI </p>
<p>- Follow class-provided test documentation formats for integration
and system testing </p>
<p>- Regular progress reviews planned, including short meeting Saturday
afternoon and code review on Sunday night</p></td>
</tr>
<tr class="even">
<td>Next Steps</td>
<td>Complete individual module implementation, prepare associated test
documentation, integrate modules, and continue UI enhancements; monitor
status at upcoming meetings</td>
</tr>
</tbody>
</table>

## **Progress Update & Integration Planning** {#progress-update-integration-planning .unnumbered}

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 80%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Category</strong></th>
<th><strong>Details</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Date &amp; Time</td>
<td>November 22, 2025, 3:00 PM – 3:15 PM (15 minutes)</td>
</tr>
<tr class="even">
<td>Attendees</td>
<td>Jien Lee, Jonghwa An, Minseok Jo </td>
</tr>
<tr class="odd">
<td>Meeting Purpose</td>
<td>Share current development progress, review API implementation,
synchronize branch merges, and plan next steps for feature
completion</td>
</tr>
<tr class="even">
<td>Discussion Summary</td>
<td><p>- Jien completed thorough document review and noted significant
API implementations ready to deploy. </p>
<p>- Plans to complete development within the day and assist others as
needed. </p>
<p>- Jonghwa confirmed details available in the security folder; advised
usage of related files. </p>
<p>- Minseok finished login and control panel features; UI wireframe
roughly completed. </p>
<p>- Remaining tasks include system on/off/reset and password changes
pending manager-side implementations. </p>
<p>- Code branches merged and pushed to main repository. </p>
<p>- DB file added to gitignore for version control. </p>
<p>- Future coordination to continue post-merge for integrated
development progress.</p></td>
</tr>
<tr class="odd">
<td>Key Decisions</td>
<td><p>- Proceed with completing individual development parts and offer
cross-support. </p>
<p>- Maintain up-to-date branch merges to ensure seamless
collaboration. </p>
<p>- Utilize existing security module resources effectively. </p>
<p>- Track development status regularly with brief sync
meetings.</p></td>
</tr>
</tbody>
</table>

## **Directory Organization, Development Progress, and Testing Status** {#directory-organization-development-progress-and-testing-status .unnumbered}

<table>
<colgroup>
<col style="width: 19%" />
<col style="width: 80%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Category</strong></th>
<th><strong>Details</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Date &amp; Time</td>
<td>November 24, 2025 (Monday), 12:00 AM – 6:00 AM (6h)</td>
</tr>
<tr class="even">
<td>Attendees</td>
<td>Jien Lee, Jonghwa An, Minseok Jo </td>
</tr>
<tr class="odd">
<td>Meeting Purpose</td>
<td>Discuss directory restructuring, individual weekend development
progress, testing coverage, bug fixes, and task coordination</td>
</tr>
<tr class="even">
<td>Discussion Summary</td>
<td><p>- Directory reorganized due to clutter; each member shared
weekend development achievements.</p>
<p> - Completed class diagrams, document review, and UI connections
tested. </p>
<p>- Security folder contains detailed implementations and extensive
tests. </p>
<p>- Some code cleanups planned (removal of redundant code). </p>
<p>- Coverage tests passed with meaningful coverage percentages.</p>
<p> - Multiple merges and pushes planned with sequential task
handoffs.</p>
<p> - Testing documents created and coverage documentation to be
uploaded. </p>
<p>- Bug fixes include camera info retrieval and image load path
corrections. - Decided to push sequentially with proper checks to avoid
conflicts. </p>
<p>- Discussed tool usage preferences and code review schedules. </p>
<p>- Planned upcoming meetings and progress updates, including a
Saturday afternoon check-in.</p>
<p>- General discussions on project documents, AI-assisted testing code
generation, and resource management.</p></td>
</tr>
<tr class="odd">
<td>Key Decisions</td>
<td><p>- Maintain restructured directory for clarity. </p>
<p>- Prioritize completing and merging individual development
tasks. </p>
<p>- Upload test coverage documentation. </p>
<p>- Perform detailed bug fix verification before pushing. </p>
<p>- Keep regular progress meetings and code reviews scheduled. </p>
<p>- Assign team roles flexibly with collaborative problem
solving.</p></td>
</tr>
<tr class="even">
<td>Next Steps</td>
<td>Finalize pending fixes, continue documentation, integrate code with
proper testing, and participate in upcoming scheduled meetings.</td>
</tr>
</tbody>
</table>

## **Test Coverage, Documentation, and SRS Alignment** {#test-coverage-documentation-and-srs-alignment .unnumbered}

| **Category** | **Details**                                                                                                                                     |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------|
| Date & Time  | November 26, 2025 (Wednesday), 16:00 \~ 18:00 (2h)                                                                                              |
| Attendees    | Jien Lee, Jonghwa An, Minseok Jo                                                                                                                |
| Purpose      | Review missing web interface tests, raise coverage to required threshold, align test/documentation with SRS/SDS, and coordinate remaining work. |

<table>
<colgroup>
<col style="width: 17%" />
<col style="width: 82%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Category</strong></th>
<th><strong>Details</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Discussion Summary</td>
<td><p>- Identified missing test code for the web interface and added
new tests; initial push was blocked by low coverage, so more tests were
written to meet the coverage gate. </p>
<p>- Current tests number around 400 cases, with many UI-level and
function-level unit tests, especially for configuration and control
functions. </p>
<p>- Some modules inherently show lower coverage (e.g., pure state/enum
holders), but overall coverage is considered reasonable (around or above
~70% in most core areas). </p>
<p>- Unit test documentation is large (dozens of pages for some parts)
due to detailed per-test-case descriptions. </p>
<p>- Integration and system test documents are being written based on
implemented feature groups; length depends on the number of combined
scenarios each member implemented. </p>
<p>- Clarified that much of the detailed test code and documentation was
generated with AI assistance but manually reviewed and adjusted. </p>
<p>- Reconfirmed Git strategy: work in personal branches, run full test
suites locally, then merge into main only after verification to avoid
broken pushes under coverage checks. </p>
<p>- Discussed inconsistencies between SRS/SDS and the given GUI
prototype (e.g., safety zone handling, control panel capabilities) and
noted that the team is prioritizing the provided prototype while
recording assumptions in documentation.</p></td>
</tr>
<tr class="even">
<td>Decisions Made</td>
<td><p>- Keep the current directory and test structure and continue to
rely on coverage reports as a quality bar. </p>
<p>- Complete unit, integration, and system test documents this week,
using existing templates and AI only as a helper, not a source of
record. - When SRS/SDS and GUI conflict, follow the shipped prototype
and clearly state assumptions and rationale in the documents. </p>
<p>- Maintain the coverage gate on CI to prevent low-tested code from
being merged into main.</p></td>
</tr>
</tbody>
</table>

Web UI/SDS Alignment & Final Tasks

<table>
<colgroup>
<col style="width: 20%" />
<col style="width: 79%" />
</colgroup>
<thead>
<tr class="header">
<th><strong>Category</strong></th>
<th><strong>Details</strong></th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td>Date &amp; Time</td>
<td>December 1, 2025 (Mon), 12AM - 9AM (9h)</td>
</tr>
<tr class="even">
<td>Attendees</td>
<td>Jien Lee, Jonghwa An, Minseok Jo </td>
</tr>
<tr class="odd">
<td>Purpose</td>
<td><p>- Verify web pages vs SDS requirements </p>
<p>- Clarify panic alarm/monitoring behavior from SRS/SDS </p>
<p>- Plan code fixes, doc merging, final submission</p></td>
</tr>
</tbody>
</table>

| **Progress Summary** |                                                                                                              |
|----------------------|--------------------------------------------------------------------------------------------------------------|
| Docs/Templates       | Created MD files/checklists; unified format to match Minseok\'s PDF template                                 |
| Impl/UI/Manual       | Finished Implementation & Testing doc; cleaned cluttered web home screen post-login; drafted web user manual |

| **SRS/SDS Issues** |                                                                                                                                                                     |
|--------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Panic Alarm        | Sends notifications (phone/monitoring sys), logs events, sirens; some ops blocked (e.g. safety zone edits per use-case exceptions). Not full system freeze          |
| Monitoring/Delay   | Intrusion detect → delay → if uncleared, escalate (log/notify monitoring sys, retrigger alarm). \"Monitoring sys\" = internal logging (no real external svc needed) |
| Sensor Trigger     | UI trigger for detection sim lost in merges; restore in app/web for testing                                                                                         |

| **Web UI vs SDS** |                                                                                                                             |
|-------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Page Check        | Most SDS pages exist (safety zone config, camera views, surveillance, sys config).Missing: Web \"View Log\" page→ implement |
| Phone Validation  | SDS lists it, but prof said skip → omit & document as intentional                                                           |
