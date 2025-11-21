# UC2 (Security) – TODO List

## 1. Missing Features / Behaviors (from SRS/SDS & previous review)

- Implement full mode support:
  - HOME, AWAY, STAY/OVERNIGHT, EXTENDED_TRAVEL as described in SRS.
- Implement safety zones:
  - create/update/delete zones
  - assign sensors to zones
  - arm/disarm by zone
- Door/window readiness check:
  - before arming, verify all perimeter sensors in the selected mode/zones are closed.
- Entry delay + monitoring-service behavior:
  - start entry delay when an armed sensor is triggered
  - allow disarm during delay to prevent alarm and monitoring call
  - if not disarmed in time, trigger siren and call monitoring service
- Panic button:
  - immediate alarm + monitoring service call regardless of mode.
- Intrusion logging:
  - record sensor/zone, timestamp, mode, action taken (siren, call)
  - provide a way to query/view these logs.

## 2. Architectural / Design Tasks

- Introduce a dedicated `SecuritySystem` domain service:
  - responsible for arm/disarm, zones, modes, intrusion handling, panic.
  - keep UI (Tkinter/Flask) and authentication logic outside.
- Introduce a `SensorEvent` dataclass:
  - contains sensor_id, zone_id, sensor_type, status, timestamp.
- Define relationships:
  - SafetyZone ↔ Sensors
  - SafeHomeMode ↔ Zones/Sensors
- Separate concerns:
  - Move authentication code from `SystemController` to UC1 (LoginManager/AuthService).
  - `SystemController` should delegate security-related concerns to `SecuritySystem`.

## 3. Integration with UC1 / UC3

- Rely on UC1 for:
  - `LoginManager` (verify password, lock state, etc.)
  - `SystemSettings` (delay time, lock duration, phone numbers).
- Expose clear interfaces/events so that:
  - UC3 or UI can subscribe to security status changes and alarm state.

## 4. Code Quality & PEP 8

- Remove wildcard imports:
  - e.g., `from utils.constants import *`.
- Ensure method and variable names follow PEP 8:
  - `lower_case_with_underscores` for functions/methods.
- Add docstrings for key domain classes and methods.

## 5. Testing

- Unit tests:
  - state transitions (disarmed ↔ armed modes),
  - entry delay behavior,
  - zone-specific arming behavior,
  - panic button behavior.
- Integration tests:
  - login via UC1 + arm AWAY + trigger sensor + disarm during delay,
  - zone-specific arming.
- System-level scenarios for the test document:
  - match the SRS use cases for UC2 (arm/disarm, intrusion, panic, etc.).
