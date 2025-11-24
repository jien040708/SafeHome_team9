from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SettingsOutcome:
    success: bool
    alert_level: str  # "info" or "error"
    message: str


class ControlPanelSettingsPresenter:
    """Validates and persists monitoring/homeowner phone and timing configuration."""

    def __init__(self, system, min_lock_time: int = 0, min_alarm_delay: int = 0):
        self.system = system
        self.min_lock_time = min_lock_time
        self.min_alarm_delay = min_alarm_delay

    def save_settings(
        self,
        *,
        monitoring_phone: str,
        homeowner_phone: str,
        lock_time: str,
        alarm_delay: str,
    ) -> SettingsOutcome:
        try:
            lock_time_int = int(lock_time)
            alarm_delay_int = int(alarm_delay)
        except ValueError:
            return SettingsOutcome(False, "error", "Invalid input. Please enter valid numbers for time fields.")

        if lock_time_int < self.min_lock_time or alarm_delay_int < self.min_alarm_delay:
            return SettingsOutcome(False, "error", "Timing values cannot be negative.")

        success = self.system.configure_system_setting(
            monitoring_phone=monitoring_phone,
            homeowner_phone=homeowner_phone,
            lock_time=lock_time_int,
            alarm_delay=alarm_delay_int,
        )
        if success:
            return SettingsOutcome(True, "info", "System settings saved successfully!")
        return SettingsOutcome(False, "error", "Failed to save settings.")
