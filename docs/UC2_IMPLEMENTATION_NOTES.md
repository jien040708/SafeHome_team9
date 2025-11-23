# SafeHome UC2 Implementation Notes

This document links the UC2 (Security) requirements from the SRS/SDS to the current codebase.

## Domain & Persistence
- `security/security_system.py` contains the alarm logic for arming, delays, panic, monitoring calls, and intrusion logging.
- `config/configuration_manager.py` now persists explicit sensor→zone assignments via `DeviceManager` and reconfigures the SecuritySystem whenever zones or assignments change.
- Schema changes (see `storage/storage_manager.py`) add a `sensor_zone_assignments` table and enable SQLite foreign keys so deleting a zone also cleans up assignments.

## Desktop UI (Tkinter)
- **Zones view (`ui/main_window.py:320-485`)**  
  - Left panel lists safety zones with add/rename/delete controls wired to `ConfigurationManager`.  
  - Sensor assignment section lets you pick a device and zone, persist the mapping, and immediately refresh the SecuritySystem.  
  - Sensor trigger buttons simulate open/close/motion events and forward them to `SystemController.update_sensor_status` so the backend state stays in sync.
- **Modes view (`ui/main_window.py:438-520`)**  
  - Shows a live armed-zone list translated into friendly names plus a color indicator (green = none armed, red = armed).  
  - Refresh logic pulls the latest `SecurityStatus` snapshot whenever the screen becomes visible.
- **Monitoring view (`ui/main_window.py:500-705`)**  
  - Intrusion log list is hydrated from `SafeHomeApp.intrusion_logs` when the view loads and after every event to guarantee consistent history even after navigation.

## Web UI / REST (Flask)
- `/api/security/status`, `/api/security/intrusions`, `/api/security/arm|disarm|panic` (see `main.py:423-603`) return structured data used by `templates/dashboard.html`.  
- The dashboard now renders Security Overview, armed-zone indicators, intrusion tables, and has buttons for Away/Stay/Disarm/Panic that surface readiness errors inline.

## Surveillance Integration
- `Domain.system.SystemCameraGateway` ties `SecuritySystem` alarms to both `SystemController.trigger_camera` and `surveillance.camera_controller.CameraController.trigger_security_event()`, ensuring UC3 thumbnails/logs fire whenever UC2 raises an alarm or panic.

## Testing
- `tests/test_zone_assignments.py` seeds an isolated SQLite DB, exercises zone CRUD + assignments, and verifies the SecuritySystem reflects those mappings (including unassignment).
- Run `pytest tests/test_zone_assignments.py security/test_security_system.py` to validate both the domain logic and the new persistence layer.

## Demo Flow
1. Start the system (`python main.py`) and log into the Tk control panel.  
2. Navigate to **SECURITY** (Zones), create/rename/delete zones, and assign sensors.  
3. Trigger a sensor to see simulator state changes propagate to logs and to the Monitoring view.  
4. Switch to **SURVEILLANCE** (Modes) to arm/disarm; watch the zone indicator update.  
5. Log into `http://localhost:5000`, open the dashboard, and exercise the Away/Stay/Disarm/Panic controls while monitoring intrusion logs refreshed automatically.  
6. Confirm camera captures via the UC3 pages or by inspecting console output from `CameraController`.
