from __future__ import annotations

from dataclasses import dataclass


@dataclass
class LoginOutcome:
    success: bool
    status_text: str = ""
    status_color: str = "blue"
    alert_level: str | None = None  # "warning" or "error"
    alert_title: str | None = None
    alert_message: str | None = None
    navigate_to: str | None = None


class ControlPanelLoginPresenter:
    """Encapsulates login decision logic for the control panel UI."""

    def __init__(self, system):
        self.system = system

    def attempt_login(self, user_id: str, password: str) -> LoginOutcome:
        if not user_id or not password:
            return LoginOutcome(
                success=False,
                alert_level="warning",
                alert_title="Input Required",
                alert_message="Please enter both User ID and Password",
            )

        result = self.system.login_with_details(user_id, password, interface="control_panel")
        if result.get("success"):
            return LoginOutcome(success=True, navigate_to="MainMenu")

        if result.get("locked"):
            remaining_time = result.get("remaining_time", 0)
            if remaining_time > 0:
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                time_msg = (
                    f"{minutes} minutes {seconds} seconds"
                    if minutes > 0
                    else f"{seconds} seconds"
                )
                return LoginOutcome(
                    success=False,
                    status_text=f"Account locked. Try again in {time_msg}",
                    status_color="red",
                    alert_level="error",
                    alert_title="Account Locked",
                    alert_message=f"{result.get('message', 'Account is locked.')}\n\n"
                    f"Please try again in {time_msg}.",
                )
            return LoginOutcome(
                success=False,
                status_text="Account locked. Please wait and try again.",
                status_color="red",
                alert_level="error",
                alert_title="Account Locked",
                alert_message=result.get("message", "Account is locked."),
            )

        if result.get("system_locked"):
            return LoginOutcome(
                success=False,
                alert_level="error",
                alert_title="System Locked",
                alert_message=result.get("message", "System is locked."),
            )

        if result.get("system_off"):
            return LoginOutcome(
                success=False,
                alert_level="error",
                alert_title="System Off",
                alert_message=result.get("message", "System is off."),
            )

        remaining = result.get("remaining", 0)
        tries = result.get("tries", 0)
        if remaining > 0:
            return LoginOutcome(
                success=False,
                status_text=f"Login failed. Remaining attempts: {remaining}",
                status_color="red",
                alert_level="error",
                alert_title="Login Failed",
                alert_message=(
                    "Incorrect password.\n\n"
                    f"Failed attempts: {tries}\n"
                    f"Remaining attempts: {remaining}"
                ),
            )

        return LoginOutcome(
            success=False,
            alert_level="error",
            alert_title="Login Failed",
            alert_message=result.get("message", "Login failed"),
        )
