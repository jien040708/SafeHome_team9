# SafeHome Test & Coverage Report (2025-11-24)

## Test Execution
| Item | Details |
| --- | --- |
| Command | `pytest --cov=. --cov-report=term --cov-report=json:coverage.json --cov-report=html` |
| Result | 239 tests passed (53 warnings from custom `@pytest.mark.coverage`) |
| Duration | 111.45 s |
| Python | 3.8.6 |
| Timestamp | 2025-11-24 20:04:09 |

## Coverage Summary
- Total statements: 6,499 | Missed: 1,927 | Overall coverage: **70%**
- Artifacts: `coverage.json`, `htmlcov/index.html`

## Full Coverage Results
| Module | Stmts | Miss | Cover |
| --- | --- | --- | --- |
| `auth/__init__.py` | 0 | 0 | 100% |
| `auth/login_interface.py` | 110 | 22 | 80% |
| `auth/login_manager.py` | 184 | 54 | 71% |
| `config/__init__.py` | 0 | 0 | 100% |
| `config/configuration_manager.py` | 188 | 67 | 64% |
| `config/system_settings.py` | 65 | 10 | 85% |
| `devices/__init__.py` | 0 | 0 | 100% |
| `devices/camera.py` | 15 | 0 | 100% |
| `devices/device_base.py` | 17 | 1 | 94% |
| `devices/device_factory.py` | 60 | 7 | 88% |
| `devices/motion_detector.py` | 11 | 0 | 100% |
| `devices/siren.py` | 12 | 3 | 75% |
| `devices/windoor_sensor.py` | 14 | 0 | 100% |
| `domain/__init__.py` | 0 | 0 | 100% |
| `domain/device_manager.py` | 54 | 11 | 80% |
| `domain/services/__init__.py` | 0 | 0 | 100% |
| `domain/services/auth_service.py` | 24 | 1 | 96% |
| `domain/services/settings_service.py` | 32 | 1 | 97% |
| `domain/system.py` | 330 | 89 | 73% |
| `domain/system_controller.py` | 75 | 39 | 48% |
| `domain/system_states.py` | 33 | 33 | 0% |
| `domain/user_manager.py` | 16 | 8 | 50% |
| `event_logging/__init__.py` | 0 | 0 | 100% |
| `event_logging/log.py` | 44 | 12 | 73% |
| `event_logging/log_manager.py` | 74 | 45 | 39% |
| `interfaces/sensor_interface.py` | 11 | 3 | 73% |
| `main.py` | 724 | 567 | 22% |
| `security/__init__.py` | 0 | 0 | 100% |
| `security/events.py` | 21 | 0 | 100% |
| `security/interfaces.py` | 33 | 7 | 79% |
| `security/security_system.py` | 193 | 25 | 87% |
| `security/test_security_system.py` | 133 | 1 | 99% |
| `storage/__init__.py` | 0 | 0 | 100% |
| `storage/storage_manager.py` | 145 | 36 | 75% |
| `surveillance/__init__.py` | 0 | 0 | 100% |
| `surveillance/camera_controller.py` | 210 | 20 | 90% |
| `surveillance/safehome_camera.py` | 141 | 11 | 92% |
| `tests/__init__.py` | 0 | 0 | 100% |
| `tests/common_tests/test_account_lock.py` | 49 | 2 | 96% |
| `tests/common_tests/test_change_master_password.py` | 196 | 4 | 98% |
| `tests/common_tests/test_configure_settings.py` | 58 | 0 | 100% |
| `tests/common_tests/test_control_panel_login.py` | 77 | 8 | 90% |
| `tests/common_tests/test_first_password_lock.py` | 50 | 2 | 96% |
| `tests/common_tests/test_integration_api.py` | 24 | 0 | 100% |
| `tests/common_tests/test_reset_system.py` | 168 | 2 | 99% |
| `tests/common_tests/test_time_based_lock.py` | 70 | 2 | 97% |
| `tests/common_tests/test_time_based_unlock_cp.py` | 69 | 12 | 83% |
| `tests/common_tests/test_time_unlock.py` | 52 | 2 | 96% |
| `tests/common_tests/test_turn_system_off.py` | 161 | 5 | 97% |
| `tests/common_tests/test_turn_system_on.py` | 216 | 35 | 84% |
| `tests/common_tests/test_unit_system_settings.py` | 121 | 21 | 83% |
| `tests/conftest.py` | 28 | 0 | 100% |
| `tests/domain/test_services.py` | 99 | 0 | 100% |
| `tests/surveillance_tests/__init__.py` | 0 | 0 | 100% |
| `tests/surveillance_tests/conftest.py` | 11 | 2 | 82% |
| `tests/surveillance_tests/test_camera_controller.py` | 207 | 1 | 99% |
| `tests/surveillance_tests/test_camera_controller_coverage.py` | 168 | 7 | 96% |
| `tests/surveillance_tests/test_safehome_camera.py` | 177 | 1 | 99% |
| `tests/surveillance_tests/test_safehome_camera_coverage.py` | 160 | 1 | 99% |
| `tests/surveillance_tests/test_surveillance_integration.py` | 103 | 1 | 99% |
| `tests/surveillance_tests/test_surveillance_integration_coverage.py` | 137 | 1 | 99% |
| `tests/test_controller_security_flow.py` | 70 | 1 | 99% |
| `tests/test_device_factory.py` | 58 | 0 | 100% |
| `tests/test_zone_assignments.py` | 39 | 5 | 87% |
| `ui/__init__.py` | 0 | 0 | 100% |
| `ui/main_window.py` | 728 | 646 | 11% |
| `utils/__init__.py` | 0 | 0 | 100% |
| `utils/constants.py` | 13 | 0 | 100% |
| `virtual_device_v3/device/__init__.py` | 0 | 0 | 100% |
| `virtual_device_v3/device/device_camera.py` | 117 | 12 | 90% |
| `virtual_device_v3/device/interface_camera.py` | 23 | 7 | 70% |
| `virtual_device_v3/device/safehome_sensor_test.py` | 81 | 74 | 9% |
| **TOTAL** | **6,499** | **1,927** | **70%** |

## Observations
- **Phase 2 wins:** Device factory registry, SafeHome camera stack, and surveillance controllers now sit at 88-99% coverage, validating new turn-on workflows and password enforcement.
- **State handling lag:** `domain/system_states.py` remains untested (0%), and `domain/system_controller.py` still sits below 50%, so arm/disarm regressions could slip past CI.
- **Presentation layer hotspots:** `main.py` (22%) and `ui/main_window.py` (11%) still dominate misses; continuing to pull orchestration into services will move the needle fastest.
- **Legacy logging gap:** `event_logging/log_manager.py` (39%) and `devices/siren.py` (75%) lack failure-mode coverage, leaving alarm fan-out brittle.

## Recommendations
1. Backfill unit tests around `domain/system_states.py` transitions and `domain/system_controller.py` orchestration, mirroring the integration flows already covered.
2. Continue extracting UI/business glue from `main.py` into injectable services so it can be exercised without the Tkinter runtime.
3. Add persistence/fan-out tests for `event_logging/log_manager.py` and `devices/siren.py`, including DB failures and redundant alerts.
4. Keep regenerating `coverage.json` + `htmlcov` artifacts after major refactors so roadmap metrics stay current.
