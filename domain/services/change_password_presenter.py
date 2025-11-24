from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ChangePasswordOutcome:
    success: bool
    message: str
    alert_level: str  # "info" or "error"


class ControlPanelChangePasswordPresenter:
    """Encapsulates validation and orchestration for the Change Password panel."""

    def __init__(self, system, min_length: int = 4):
        self.system = system
        self.min_length = max(1, min_length)

    def change_password(self, current_password: str, new_password: str, confirm_password: str) -> ChangePasswordOutcome:
        if new_password != confirm_password:
            return ChangePasswordOutcome(
                success=False,
                message="New passwords do not match!",
                alert_level="error",
            )

        if len(new_password or "") < self.min_length:
            return ChangePasswordOutcome(
                success=False,
                message=f"Password must be at least {self.min_length} characters long.",
                alert_level="error",
            )

        success = self.system.change_password(current_password, new_password)
        if success:
            return ChangePasswordOutcome(
                success=True,
                message="Password changed successfully!",
                alert_level="info",
            )

        return ChangePasswordOutcome(
            success=False,
            message="Failed to change password. Please check your current password.",
            alert_level="error",
        )
