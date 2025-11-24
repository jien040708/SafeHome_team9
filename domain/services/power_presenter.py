from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PowerOutcome:
    success: bool
    message: str
    alert_level: str  # "info" or "error"


class PowerControlPresenter:
    """Handles turn-off/log-out orchestration for the control panel."""

    def __init__(self, system):
        self.system = system

    def turn_off_system(self) -> PowerOutcome:
        login_manager = getattr(self.system, "login_manager", None)
        if login_manager and login_manager.is_user_authenticated():
            self.system.logout()

        success = self.system.turn_off()
        if success:
            return PowerOutcome(
                success=True,
                message="System has been turned off successfully.",
                alert_level="info",
            )
        return PowerOutcome(
            success=False,
            message="Failed to turn off the system.",
            alert_level="error",
        )
