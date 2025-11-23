# SafeHome UC2 Implementation Notes

This document links the UC2 (Security) requirements from the SRS/SDS to the current codebase and describes how to demo the feature set.

## Domain & Persistence
- `security/security_system.py` contains the alarm logic for arming, delays, panic, monitoring calls, and intrusion logging.
- `config/configuration_manager.py` now persists explicit sensor→zone assignments via `DeviceManager` and automatically reconfigures the SecuritySystem whenever zones or assignments change.
- Schema updates (`storage/storage_manager.py`) add a `sensor_zone_assignments` table and enable SQLite foreign keys so deleting a zone also cleans up assignments.

## Desktop UI (Tkinter)
- **Zones view (`ui/main_window.py:326-547`)**  
  - Left panel lists safety zones with add/rename/delete controls wired to `ConfigurationManager`.  
  - Sensor assignment tools let you pick a device and zone, persist the mapping, and immediately refresh the SecuritySystem.  
  - Sensor trigger buttons simulate open/close/motion events and forward them to `SystemController.update_sensor_status`, keeping simulator state aligned with UC2.
- **Modes view (`ui/main_window.py:438-520`)**  
  - Shows a live armed-zone list translated into friendly names plus a color indicator (green = none armed, red = armed).  
  - Refresh logic pulls the latest `SecurityStatus` snapshot whenever the screen becomes visible.
- **Monitoring view (`ui/main_window.py:500-705`)**  
  - Intrusion logs are hydrated from `SafeHomeApp.intrusion_logs` whenever you return to the page so history survives navigation.  
  - Includes quick access to system settings, password changes, and reset/refresh actions.

## Web UI / REST (Flask)
- `/api/security/status`, `/api/security/intrusions`, `/api/security/arm|disarm|panic` supply the Security Overview + control buttons (`main.py:423-603` and `templates/dashboard.html:257`).  
- `/api/security/zones`, `/api/security/sensors`, and `/api/security/assignments` expose CRUD operations for zones and sensor mappings so the browser can mirror the Tk workflow.  
- The dashboard now renders:
  - Security Overview card (mode, alarm state badge, entry delay countdown, armed zones).  
  - Intrusion log table that auto-refreshes every 20 seconds.  
  - Away/Stay/Disarm/Panic buttons that surface readiness errors inline.  
  - **Zone & Sensor Management** card with zone creation, rename/delete actions, and sensor assignment dropdowns that call the new REST APIs.

## Surveillance Integration
- `Domain.system.SystemCameraGateway` ties UC2 alarm events to both `SystemController.trigger_camera` and `surveillance.camera_controller.CameraController.trigger_security_event()`, ensuring UC3 thumbnails/logs fire whenever UC2 raises an alarm or panic.

## Testing
- `tests/test_zone_assignments.py` seeds an isolated SQLite DB, exercises zone CRUD + assignments, and verifies the SecuritySystem reflects those mappings (including unassignment).
- `tests/test_controller_security_flow.py` simulates controller-level workflows (arm/disarm, entry delay, panic) to ensure the UI adapter and `SecuritySystem` cooperate correctly.
- `security/test_security_system.py` remains the authoritative suite for domain behavior (modes, readiness checks, entry delays, panic).
- Run `pytest tests/test_zone_assignments.py tests/test_controller_security_flow.py security/test_security_system.py` to validate persistence, controller integration, and domain logic.

## Demo Flow
1. Start the system (`python main.py`) and log into the Tk control panel.  
2. Navigate to **SECURITY** (Zones) to create/rename/delete zones and assign sensors; trigger a sensor to see simulator updates propagate to Monitoring.  
3. Switch to **SURVEILLANCE** (Modes) to arm/disarm and observe the zone indicator, then visit **CONFIGURE** (Monitoring) to confirm intrusion logs update automatically.  
4. Log into `http://localhost:5000`, open the dashboard, and review the Security Overview + intrusion feed.  
5. Scroll to **Zone & Sensor Management** to perform the same CRUD/assignment actions from the web, verifying that Tk and web stay in sync.  
6. Use the Away/Stay/Disarm/Panic buttons to exercise UC2 flows while monitoring the log table; readiness errors (e.g., door open) surface as toast messages.  
7. Confirm UC3 captures via the surveillance pages or by watching console output from `CameraController.trigger_security_event`.  
8. Run the pytest command above to document verification steps for QA.
