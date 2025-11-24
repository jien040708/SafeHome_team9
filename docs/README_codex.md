# SafeHome Project – Codex Review Guide (UC2 Focus)

## Team & Use Cases

Our team has 3 members. Each member is responsible for one main use case:

- Use Case 1 (UC1): Common functions
  - Login, user authentication
  - System settings
  - System on/off/reset
  - Account lock behavior

- Use Case 2 (UC2): Security  **← THIS IS MY PART**
  - Arm/disarm via control panel and web
  - Security modes (HOME, AWAY, OVERNIGHT, EXTENDED_TRAVEL, etc.)
  - Safety zones (create/update/delete/assign sensors, per-zone arming)
  - Intrusion handling:
    - door/window readiness checks before arming
    - entry delay
    - disarm during delay vs. full alarm
    - monitoring service call
    - panic button
  - Intrusion logging (sensor, zone, timestamp, mode, actions taken)
  - Intrusion log querying

- Use Case 3 (UC3): Surveillance
  - Cameras, thumbnails
  - Pan/zoom
  - Camera passwords
  - Enabling/disabling cameras

I am responsible for **UC2 (Security)** but the whole SafeHome system must work together.

---

## Important Documents

These are in the `docs/` folder:

- `SRS_document.doc` – System Requirement Specification
- `SDS_document.docx` – Software Design Specification (architecture, class/state/sequence diagrams)
- `Implementation_and_Testing_template_v4.docx` – Test & implementation template
- `UC2_TODO.md` – My current UC2-specific task list

---

## Current Code Structure (UC2-relevant)

- `safehome/domain/system_controller.py`
- `safehome/domain/system_states.py`
- `safehome/config/system_settings.py`
- `safehome/config/configuration_manager.py`
- `safehome/main.py`
- (new) `safehome/security/security_system.py`
- (new) `safehome/security/events.py`

The previous Codex review already pointed out several issues:

- SystemController and SecurityState only partially cover UC2.
- Safety zones and modes exist but are not actually used in the arming logic.
- No intrusion logs, no panic behavior, no monitoring-service calls.
- Web endpoints lack full authentication and mode selection.
- Code mixing responsibilities (authentication, UI callbacks, security domain logic).

---

## What I Want From Codex (High-Level)

1. Help me design and refine a proper **SecuritySystem** domain service for UC2.
2. Help me refactor existing code in `domain/system_controller.py` and `domain/system_states.py` so that:
   - UC1 (login/auth) stays in the UC1 module
   - UC2 (security) logic is moved into `security/security_system.py`
3. Help me implement the missing UC2 behaviors according to SRS/SDS:
   - modes, safety zones, entry delay, monitoring calls, panic, logs
4. Help me design and implement unit/integration tests for UC2 under `tests/security/`.
5. Ensure the code follows PEP 8 and has a clean separation of concerns.

For each step, I will provide the relevant files and a focused prompt.
Please read `UC2_TODO.md` for the detailed task list and context.

---

## Coverage Workflow

- We run `pytest --cov=. --cov-report=term --cov-report=json:coverage.json --cov-report=html` for every major change. The CI workflow in `.github/workflows/coverage.yml` enforces a **68%** minimum via `--cov-fail-under=68`, so coverage cannot regress silently.
- Tests marked with `@pytest.mark.coverage` (see `pytest.ini`) are instrumentation-heavy scenarios; run `pytest -m coverage` when you need to regenerate detailed artifacts or investigate gaps.
- After major refactors, update both `docs/test_coverage.md` and `docs/coverage_improvement_plan.md` so the snapshot and roadmap stay aligned with the latest run.
