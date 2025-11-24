# Coverage Improvement Plan (2025-11-24)

## Snapshot
- Latest run: `pytest --cov=. --cov-report=term --cov-report=json:coverage.json --cov-report=html`
- Result: 268 tests, **73%** overall coverage (6,809 statements / 1,838 misses)
- Largest gaps: `main.py` (23%), `ui/main_window.py` (12%), `event_logging/log_manager.py` (39%), `devices/siren.py` (75%), `virtual_device_v3/device/safehome_sensor_test.py` (9%)

## Roadmap To 80%+
| Milestone | Target | Key Modules | Approach | Owners |
| --- | --- | --- | --- | --- |
| Phase 1 – Domain State Coverage | Raise `domain/system_states.py` to 70% and `domain/system_controller.py` to >65% | `domain/system_states.py`, `domain/system_controller.py` | ✅ Complete: Parametrized tests now cover arm/disarm flows plus controller observer wiring. | Domain + Security |
| Phase 2 - Presentation Layer Thin-out | Cut `main.py` and `ui/main_window.py` misses by 30% (target 40% and 25% coverage, respectively) | `main.py`, `ui/main_window.py` | Complete: SystemBootstrapper now wires devices post-boot and login/reset/zone/mode flows live in presenters with unit tests; keep monitoring coverage drift. | UI + Platform |
| Phase 3 – Logging & Notifier Hardening | Lift `event_logging/log_manager.py` to 70% and `devices/siren.py` to 95% | `event_logging/log_manager.py`, `devices/siren.py`, `event_logging/log.py` | Introduce in-memory DB/mocked storage fixtures verifying persistence, retries, fan-out; add siren activation/inhibit tests. | Infra |
| Phase 4 – Virtual Device Parity | Increase `virtual_device_v3/device/safehome_sensor_test.py` to 60% and `interface_camera.py` to 85% | `virtual_device_v3/device/safehome_sensor_test.py`, `virtual_device_v3/device/interface_camera.py` | Break monolithic script into functions; add pytest-driven simulation tests verifying camera/mock sensor behavior. | Surveillance |
| Phase 5 – High-risk Regression Nets | Reach 75% overall | Touchpoints above + `devices/siren.py`, `domain/system.py`, `storage/storage_manager.py` | Layer targeted regression tests focused on high-risk flows (reset, monitoring service escalation, system off). | All teams |

## To-Do List
1. **State Machine Test Suite**
   - [x] Draft a state transition table (inputs, expected next state/alarm) for arm/disarm/offline scenarios.
   - [x] Implement pytest parametrized cases feeding dummy controllers through `domain/system_states.py`.
   - [x] Unit-test `SystemController` observers with fake sensors to cover turn-on/off, password lock, entry delays.
2. **Presenter Extraction**
   - [x] Extract turn-system-on orchestration from `main.py` into `SystemBootstrapper`.
   - [x] Create `ControlPanelPresenter` for login/reset flows (change-password pending) and cover with pure unit tests.
   - [x] Mirror `ui/main_window.py` Zones/Modes widgets with view-model classes tested via headless fixtures.
3. **Logging Reliability**
   - [ ] Build in-memory SQLite fixture to test `event_logging/log_manager.py` insert/filter logic.
   - [ ] Simulate DB failure (raise `sqlite3.Error`) to assert retry/error logging behavior.
   - [ ] Cover `devices/siren.py` activation/deactivation transitions including duplicate calls.
4. **Virtual Device Stabilization**
   - [ ] Split `virtual_device_v3/device/safehome_sensor_test.py` into importable helpers; add tests for windoor/motion pathways.
   - [ ] Flesh out `interface_camera.py` tests ensuring each abstract method raises `NotImplementedError`.
   - [ ] Provide placeholder image fixture for camera IDs > existing JPGs (done in code; add regression test).
5. **Continuous Coverage Hygiene**
   - [ ] Add coverage job to CI (if absent) to fail builds when overall coverage drops below 68% (ratchet upward per milestone).
   - [ ] Document the `coverage` pytest mark usage in `README_codex.md` and ensure `pytest.ini` lives in source tree.
   - [ ] Update `docs/test_coverage.md` + `docs/coverage_roadmap.md` after each major refactor.

## Notes
- This plan complements `docs/coverage_roadmap.md`; phase numbering aligns but adds concrete owners/deliverables.
- Prioritize modules with logic risk over sheer line count; UI/`main.py` refactors should accompany service extraction to keep behavior stable.
