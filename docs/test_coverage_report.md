# SafeHome Test & Coverage Report (2025-11-24)

## Test Execution
| Item | Details |
| --- | --- |
| Command | `pytest --cov=. --cov-report=term --cov-report=json:coverage.json --cov-report=html` |
| Result | 120 tests passed |
| Duration | 27.82 s |
| Python | 3.8.6 |
| Timestamp | 2025-11-24 15:48:09 |

## Coverage Summary
- Total statements: 4,841 • Missed: 1,771 • Overall coverage: **63%**
- Artifacts: `coverage.json`, `htmlcov/index.html`

## Full Coverage Results
| Module | Stmts | Miss | Cover |
| --- | --- | --- | --- |
| `auth/__init__.py` | 0 | 0 | 100% |
| `auth/login_interface.py` | 110 | 30 | 73% |
| `auth/login_manager.py` | 155 | 61 | 61% |
| `config/__init__.py` | 0 | 0 | 100% |
| `config/configuration_manager.py` | 188 | 69 | 63% |
| `config/system_settings.py` | 65 | 10 | 85% |
| `devices/__init__.py` | 0 | 0 | 100% |
| `devices/camera.py` | 15 | 0 | 100% |
| `devices/device_base.py` | 17 | 1 | 94% |
| `devices/device_factory.py` | 60 | 7 | 88% |
| `devices/motion_detector.py` | 11 | 0 | 100% |
| `devices/siren.py` | 12 | 5 | 58% |
| `devices/windoor_sensor.py` | 14 | 0 | 100% |
| `domain/__init__.py` | 0 | 0 | 100% |
| `domain/device_manager.py` | 54 | 11 | 80% |
| `domain/services/__init__.py` | 0 | 0 | 100% |
| `domain/services/auth_service.py` | 24 | 1 | 96% |
| `domain/services/settings_service.py` | 32 | 1 | 97% |
| `domain/system.py` | 247 | 105 | 57% |
| `domain/system_controller.py` | 75 | 39 | 48% |
| `domain/user_manager.py` | 16 | 8 | 50% |
| `event_logging/__init__.py` | 0 | 0 | 100% |
| `event_logging/log.py` | 44 | 12 | 73% |
| `event_logging/log_manager.py` | 74 | 45 | 39% |
| `interfaces/sensor_interface.py` | 11 | 3 | 73% |
| `main.py` | 713 | 560 | 21% |
| `security/__init__.py` | 0 | 0 | 100% |
| `security/events.py` | 21 | 0 | 100% |
| `security/interfaces.py` | 33 | 7 | 79% |
| `security/security_system.py` | 193 | 28 | 85% |
| `security/test_security_system.py` | 133 | 1 | 99% |
| `storage/__init__.py` | 0 | 0 | 100% |
| `storage/storage_manager.py` | 145 | 36 | 75% |
| `surveillance/__init__.py` | 0 | 0 | 100% |
| `surveillance/camera_controller.py` | 196 | 47 | 76% |
| `surveillance/safehome_camera.py` | 117 | 6 | 95% |
| `tests/__init__.py` | 0 | 0 | 100% |
| `tests/conftest.py` | 28 | 0 | 100% |
| `tests/domain/test_services.py` | 99 | 0 | 100% |
| `tests/surveillance_tests/__init__.py` | 0 | 0 | 100% |
| `tests/surveillance_tests/conftest.py` | 11 | 2 | 82% |
| `tests/surveillance_tests/test_camera_controller.py` | 207 | 1 | 99% |
| `tests/surveillance_tests/test_safehome_camera.py` | 177 | 1 | 99% |
| `tests/surveillance_tests/test_surveillance_integration.py` | 103 | 1 | 99% |
| `tests/test_account_lock.py` | 49 | 2 | 96% |
| `tests/test_configure_settings.py` | 58 | 0 | 100% |
| `tests/test_control_panel_login.py` | 77 | 8 | 90% |
| `tests/test_controller_security_flow.py` | 70 | 1 | 99% |
| `tests/test_device_factory.py` | 58 | 0 | 100% |
| `tests/test_first_password_lock.py` | 50 | 2 | 96% |
| `tests/test_integration_api.py` | 24 | 0 | 100% |
| `tests/test_time_based_lock.py` | 70 | 2 | 97% |
| `tests/test_time_based_unlock_cp.py` | 69 | 12 | 83% |
| `tests/test_time_unlock.py` | 52 | 2 | 96% |
| `tests/test_unit_system_settings.py` | 121 | 21 | 83% |
| `tests/test_zone_assignments.py` | 39 | 5 | 87% |
| `ui/__init__.py` | 0 | 0 | 100% |
| `ui/main_window.py` | 610 | 544 | 11% |
| `utils/__init__.py` | 0 | 0 | 100% |
| `utils/constants.py` | 13 | 0 | 100% |
| `virtual_device_v3/device/__init__.py` | 0 | 0 | 100% |
| `virtual_device_v3/device/safehome_sensor_test.py` | 81 | 74 | 9% |
| **TOTAL** | **4,841** | **1,771** | **63%** |

## Observations
- **Device layer hardened:** Camera, motion, and window sensors plus the new factory now carry 88-100% coverage with notifier behavior validated end-to-end.
- **Main/UI still dominant gaps:** `main.py` and `ui/main_window.py` together contribute >60% of the remaining misses; logic needs extraction into service layers.
- **Security orchestration risk:** `domain/system.py` and `domain/system_controller.py` hover below 60% with no direct state-transition tests, so regressions could slip through.
- **Logging/notification remain dark:** `event_logging/log_manager.py` and `devices/siren.py` still lack regression tests, leaving alarm fan-out largely unverified.

## Recommendations
1. Continue Phase 1 refactors by extracting state/mode orchestration from `main.py` and covering the new services directly.
2. Author targeted tests for `domain/system_controller.py` covering arm/disarm, mode errors, and observer wiring.
3. Introduce persistence and failure-mode tests for `event_logging/log_manager.py` plus `devices/siren.py` activation paths.
4. Keep the coverage command in CI so regressions, especially within UI/service seams, surface quickly.
