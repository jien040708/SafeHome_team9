from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass
class WebSettingsOutcome:
    """Result of a web settings operation."""
    success: bool
    message: str
    errors: list[str] | None = None


class WebSettingsPresenter:
    """Validates and persists system configuration via web interface."""

    def __init__(self, system):
        self.system = system
        self.phone_pattern = r'^\d{3}-\d{3}-\d{4}$'
        self.flexible_phone_pattern = r'^[\d\-+() ]+$'

    def update_settings(
        self,
        *,
        monitoring_service_phone: str | None = None,
        homeowner_phone: str | None = None,
        system_lock_time: int | None = None,
        alarm_delay_time: int | None = None,
    ) -> WebSettingsOutcome:
        """
        Update system settings with validation.

        Args:
            monitoring_service_phone: Monitoring service phone number
            homeowner_phone: Homeowner phone number
            system_lock_time: System lock time in seconds
            alarm_delay_time: Alarm delay time in seconds

        Returns:
            WebSettingsOutcome with operation result
        """
        errors = []

        # Validate phone numbers
        if monitoring_service_phone is not None:
            if not self._validate_phone(monitoring_service_phone):
                errors.append('Invalid monitoring service phone format (recommended: XXX-XXX-XXXX)')

        if homeowner_phone is not None:
            if not self._validate_phone(homeowner_phone):
                errors.append('Invalid homeowner phone format (recommended: XXX-XXX-XXXX)')

        # Validate time values
        if system_lock_time is not None:
            try:
                lock_time_int = int(system_lock_time)
                if lock_time_int <= 0:
                    errors.append('System lock time must be greater than 0')
            except (ValueError, TypeError):
                errors.append('System lock time must be a valid number')

        if alarm_delay_time is not None:
            try:
                alarm_delay_int = int(alarm_delay_time)
                if alarm_delay_int < 0:
                    errors.append('Alarm delay time must be non-negative')
            except (ValueError, TypeError):
                errors.append('Alarm delay time must be a valid number')

        # Return validation errors if any
        if errors:
            return WebSettingsOutcome(
                success=False,
                message='Validation failed',
                errors=errors
            )

        # Update settings through system
        if not self.system or not self.system.configuration_manager:
            return WebSettingsOutcome(
                success=False,
                message='System not available'
            )

        try:
            settings = self.system.configuration_manager.get_system_setting()

            # Apply updates
            if monitoring_service_phone is not None:
                settings.set_monitoring_service_phone(monitoring_service_phone)
            if homeowner_phone is not None:
                settings.set_homeowner_phone(homeowner_phone)
            if system_lock_time is not None:
                settings.set_system_lock_time(int(system_lock_time))
            if alarm_delay_time is not None:
                settings.set_alarm_delay_time(int(alarm_delay_time))

            # Save to database
            success = settings.save()

            if success:
                return WebSettingsOutcome(
                    success=True,
                    message='Settings updated successfully'
                )
            else:
                return WebSettingsOutcome(
                    success=False,
                    message='Failed to save settings'
                )

        except Exception as e:
            return WebSettingsOutcome(
                success=False,
                message=f'Server error: {str(e)}'
            )

    def get_settings(self) -> WebSettingsOutcome:
        """
        Retrieve current system settings.

        Returns:
            WebSettingsOutcome with current settings
        """
        if not self.system or not self.system.configuration_manager:
            return WebSettingsOutcome(
                success=False,
                message='System not available'
            )

        try:
            settings = self.system.configuration_manager.get_system_setting()
            return WebSettingsOutcome(
                success=True,
                message='Settings retrieved successfully',
                # Note: Actual settings would be included in a more complete implementation
                # For now, we just return success
            )
        except Exception as e:
            return WebSettingsOutcome(
                success=False,
                message=f'Server error: {str(e)}'
            )

    def _validate_phone(self, phone: str) -> bool:
        """
        Validate phone number format.

        Args:
            phone: Phone number string

        Returns:
            True if valid, False otherwise
        """
        if re.match(self.phone_pattern, phone):
            return True
        if re.match(self.flexible_phone_pattern, phone) and len(phone) >= 3:
            return True
        return False
