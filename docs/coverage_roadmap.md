# SafeHome Coverage & Refactoring Roadmap

## Requirements & Design Touchpoints
| Source | Key takeaways | Relevant areas |
| --- | --- | --- |
| `docs/SRS_document_parsed.txt:28-72` | SRS enumerates 3 families of use cases (common, security, surveillance) that must all be supported from control panel and web flows. | Ensures tests cover login, configuration, arming/disarming, alarms, monitoring service calls, camera operations. |
| `docs/SDS_document_parsed.txt:94-121` | SDS goals emphasize low coupling, testability, and modular subsystems (External Communication, Surveillance, Security, Configuration/Data). | Refactors should isolate each subsystem into service layers to match the intended architecture. |

## Baseline (2025-11-24 run)
- Command: `pytest --cov=. --cov-report=term --cov-report=json:coverage.json --cov-report=html`
- Result: 239 tests passed, 70% overall coverage (`docs/test_coverage.md:3-82`).
- Gap concentration: `main.py`, `ui/main_window.py`, `domain/system_controller.py`, `domain/system_states.py`, `event_logging/log_manager.py`, and `virtual_device_v3/device/safehome_sensor_test.py`.

## Coverage Roadmap
| Phase | Coverage target | Requirement alignment | Refactoring & test focus | Owner cues |
| --- | --- | --- | --- | --- |
| 1. Stabilize domain states | Raise `domain/system.py` + controller/state trio from 48-53% → ≥85%. | Covers SRS common + security flows (login, arm/disarm, reset) and SDS state diagrams. | Extract state machine & orchestration logic from `main.py` into injectable services; author state-transition unit tests + property tests; add negative tests for failed login, lockouts, and alarm triggers. | Domain & security team |
| 2. Harden device + notification layer | Lift devices + notification/log managers (<60%) → ≥80%. | Supports sensor-based security use cases + monitoring service per SRS. | Refactor `devices/device_factory.py` into registry, stub hardware I/O to enable deterministic tests; add contract tests for each sensor type; write LogManager/NotificationManager tests simulating DB failures and event fan-out. | Device & infra team |
| 3. Decouple UI / external interfaces | Reduce `main.py` (22%) and `ui/main_window.py` (11%) to thin shells with ≤200 LOC, push logic into services with ≥70% coverage. | Ensures control-panel/web UIs for all SRS use cases remain functional (login, configure, camera view). | Introduce Presenter/ViewModel layer; wrap Tkinter + Flask endpoints around service APIs; add Flask view tests + Tkinter view-model tests via dependency injection. | UI team |
| 4. Extend surveillance & virtual device coverage | Maintain ≥95% for camera stack; boost `virtual_device_v3/device/safehome_sensor_test.py` 9% → ≥70%. | Aligns with SRS surveillance cases (display, pan/zoom, camera password) and SDS surveillance sequence diagrams. | Convert simulator script into pytest fixtures; add scenario tests for enable/disable, password enforcement, and degraded network. | Surveillance team |

## Targeted TODOs
1. **Domain state machine**
   - Split `domain/system.py` into `SystemService`, `AuthService`, and `ModeService` to isolate state logic from UI entrypoints.
   - Implement parametrized tests mapping each SRS security use case (arm/disarm via control panel/web, safety zone updates) to state transitions.
   - Model panic-call + monitoring service escalation tests to reflect SDS sequence diagrams.
2. **Device factory + sensors**
   - Replace if/else factory with registration map and add pytest parametrized instantiation tests that assert sensor interface compliance.
   - Mock device I/O signals to verify alarm propagation and ensure misconfigured devices raise clear exceptions.
3. **Logging & notification**
   - Add fixtures around `LogManager` to test persistence, filtering, and failure handling; simulate DB write errors and ensure retries/logging.
   - Cover `NotificationManager` callbacks for monitoring service + UI toast updates.
4. **UI/service boundary**
   - Move control panel workflows (login, configure settings, password change) into a controller class with dependency injection for services and storage.
   - Cover Flask routes with client tests verifying JSON payloads for `/arm`, `/disarm`, `/status`.
   - Add Tkinter presenter tests using `pytest-qt` or pure unit tests on view-model objects.
5. **Virtual devices & surveillance**
   - Decompose `virtual_device_v3/device/safehome_sensor_test.py` into reusable fixtures that drive integration tests across `surveillance/*`.
   - Extend camera controller tests with failure modes (network drop, credential mismatch) to satisfy SRS camera password scenarios.

## Progress (2025-11-24)
| Item | Status | Notes |
| --- | --- | --- |
| Phase 1 – Domain auth/settings extraction | ✅ Completed | Introduced `domain/services/auth_service.py` and `settings_service.py`; `System` now delegates login/configure flows through these services, reducing direct UI coupling. |
| Coverage bump (domain services) | ✅ Completed | Added `tests/domain/test_services.py` to validate login/logout logging and configuration persistence. Full pytest run now counts 111 tests. |
| Remaining Phase 1 work | ⏳ Pending | Still need to extract full state/mode handling and add arm/disarm transition tests per SDS diagrams. |
