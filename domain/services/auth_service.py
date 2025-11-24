from __future__ import annotations

from typing import Callable, Optional

from auth.login_manager import LoginManager
from event_logging.log_manager import LogManager


class AuthService:
    """Encapsulates login/logout workflows for both UI surfaces."""

    def __init__(
        self,
        login_manager: LoginManager,
        log_manager: LogManager,
        on_success: Optional[Callable[[str], None]] = None,
    ) -> None:
        self._login_manager = login_manager
        self._log_manager = log_manager
        self._on_success = on_success

    def login(self, username: str, password: str, interface: str) -> dict:
        """Perform login and emit audit logs."""
        result = self._login_manager.login_with_details(username, password, interface)
        if result.get("success"):
            self._log_manager.log_event(
                event_type="LOGIN_SUCCESS",
                description=f"User logged in via {interface}",
                user_id=username,
            )
            if self._on_success:
                self._on_success(username)
        else:
            self._log_manager.log_event(
                event_type="LOGIN_FAILED",
                description=f"Failed login attempt via {interface}",
                user_id=username,
            )
        return result

    def logout(self) -> Optional[str]:
        """Logout current user and write a log entry."""
        if not self._login_manager.is_user_authenticated():
            return None

        current_user = self._login_manager.get_current_user().get_username()
        self._login_manager.logout()
        self._log_manager.log_event(
            event_type="LOGOUT",
            description="User logged out",
            user_id=current_user,
        )
        return current_user
