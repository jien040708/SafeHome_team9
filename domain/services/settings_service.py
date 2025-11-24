from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from auth.login_manager import LoginManager
from config.configuration_manager import ConfigurationManager
from event_logging.log_manager import LogManager


@dataclass
class SettingsResult:
    success: bool
    message: str = ""


class SettingsService:
    """Coordinates configuration updates with validation and auditing."""

    def __init__(
        self,
        configuration_manager: ConfigurationManager,
        login_manager: LoginManager,
        log_manager: LogManager,
    ) -> None:
        self._config_manager = configuration_manager
        self._login_manager = login_manager
        self._log_manager = log_manager

    def update_settings(
        self,
        *,
        monitoring_phone: Optional[str] = None,
        homeowner_phone: Optional[str] = None,
        lock_time: Optional[int] = None,
        alarm_delay: Optional[int] = None,
    ) -> SettingsResult:
        if not self._login_manager.is_user_authenticated():
            return SettingsResult(False, "Authentication required to configure settings.")

        settings = self._config_manager.get_system_setting()

        if monitoring_phone:
            settings.set_monitoring_service_phone(monitoring_phone)
        if homeowner_phone:
            settings.set_homeowner_phone(homeowner_phone)
        if lock_time is not None:
            settings.set_system_lock_time(lock_time)
        if alarm_delay is not None:
            settings.set_alarm_delay_time(alarm_delay)

        if not self._config_manager.update_system_settings(settings):
            return SettingsResult(False, "Failed to persist system settings.")

        user = self._login_manager.get_current_user().get_username()
        self._log_manager.log_event(
            event_type="CONFIG_UPDATE",
            description="System settings updated",
            user_id=user,
        )
        return SettingsResult(True, "Settings updated successfully.")
