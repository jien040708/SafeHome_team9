from __future__ import annotations

from dataclasses import dataclass


@dataclass
class ResetOutcome:
    success: bool
    alert_level: str
    alert_title: str
    alert_message: str
    phase: int | None = None


class ControlPanelResetPresenter:
    """Encapsulates system reset orchestration for the monitoring view."""

    def __init__(self, system):
        self.system = system

    def perform_reset(self) -> ResetOutcome:
        try:
            result = self.system.reset()
        except Exception as exc:
            return ResetOutcome(
                success=False,
                alert_level="error",
                alert_title="Error",
                alert_message=f"Reset failed: {exc}",
            )

        if isinstance(result, dict):
            success = bool(result.get("success"))
            message = result.get("message", "")
            phase = result.get("phase")
        else:  # Support legacy boolean returns
            success = bool(result)
            message = "System reset successfully!" if success else "Failed to reset system."
            phase = None

        return ResetOutcome(
            success=success,
            alert_level="info" if success else "error",
            alert_title="Success" if success else "Error",
            alert_message=message or ("System reset successfully!" if success else "Failed to reset system."),
            phase=phase,
        )
