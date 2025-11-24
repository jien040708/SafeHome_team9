from __future__ import annotations

from dataclasses import dataclass


@dataclass
class WebLoginOutcome:
    """Result of a web login operation (first or second password validation)."""
    success: bool
    message: str
    locked: bool = False
    remaining_time: int = 0
    tries: int = 0
    remaining: int = 0
    system_off: bool = False
    system_locked: bool = False
    redirect_url: str | None = None


class WebLoginPresenter:
    """Encapsulates login decision logic for the web interface (2-factor authentication)."""

    def __init__(self, system):
        self.system = system

    def validate_first_password(self, username: str, password: str) -> WebLoginOutcome:
        """
        Validate first password for web interface login.

        Args:
            username: User ID
            password: First password

        Returns:
            WebLoginOutcome with validation result
        """
        # Input validation
        if not username or not password:
            return WebLoginOutcome(
                success=False,
                message="Username and password are required"
            )

        # Call LoginManager through system
        if not self.system or not self.system.login_manager:
            return WebLoginOutcome(
                success=False,
                message="System not available"
            )

        result = self.system.login_manager.validate_first_password(
            username,
            password,
            'web_browser'
        )

        # Handle various response scenarios
        if result.get('success'):
            return WebLoginOutcome(
                success=True,
                message='First password correct'
            )

        # Account locked
        if result.get('locked'):
            return WebLoginOutcome(
                success=False,
                locked=True,
                message=result.get('message', 'Account is locked'),
                remaining_time=result.get('remaining_time', 0),
                tries=result.get('tries', 0)
            )

        # System state errors
        if result.get('system_off'):
            return WebLoginOutcome(
                success=False,
                system_off=True,
                message=result.get('message', 'System is off')
            )

        if result.get('system_locked'):
            return WebLoginOutcome(
                success=False,
                system_locked=True,
                message=result.get('message', 'System is locked')
            )

        # Failed attempts
        return WebLoginOutcome(
            success=False,
            message=result.get('message', 'First password validation failed'),
            tries=result.get('tries', 0),
            remaining=result.get('remaining', 0)
        )

    def validate_second_password(self, username: str, second_password: str) -> WebLoginOutcome:
        """
        Validate second password for web interface login.

        Args:
            username: User ID (from session after first password validation)
            second_password: Second password

        Returns:
            WebLoginOutcome with validation result
        """
        # Input validation
        if not second_password:
            return WebLoginOutcome(
                success=False,
                message="Second password is required"
            )

        # Call LoginManager through system
        if not self.system or not self.system.login_manager:
            return WebLoginOutcome(
                success=False,
                message="System not available"
            )

        result = self.system.login_manager.validate_second_password(
            username,
            second_password,
            'web_browser'
        )

        # Handle various response scenarios
        if result.get('success'):
            return WebLoginOutcome(
                success=True,
                message='Login successful',
                redirect_url='/dashboard'
            )

        # Account locked
        if result.get('locked'):
            return WebLoginOutcome(
                success=False,
                locked=True,
                message=result.get('message', 'Account is locked'),
                remaining_time=result.get('remaining_time', 0),
                tries=result.get('tries', 0)
            )

        # System state errors
        if result.get('system_off'):
            return WebLoginOutcome(
                success=False,
                system_off=True,
                message=result.get('message', 'System is off')
            )

        if result.get('system_locked'):
            return WebLoginOutcome(
                success=False,
                system_locked=True,
                message=result.get('message', 'System is locked')
            )

        # Failed attempts
        return WebLoginOutcome(
            success=False,
            message=result.get('message', 'Second password validation failed'),
            tries=result.get('tries', 0),
            remaining=result.get('remaining', 0)
        )
