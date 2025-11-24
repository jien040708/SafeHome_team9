from __future__ import annotations

from dataclasses import dataclass

from domain.services.auth_service import AuthService
from domain.services.settings_service import SettingsService


class FakeUser:
    def __init__(self, username: str) -> None:
        self._username = username

    def get_username(self) -> str:
        return self._username


class FakeLoginManager:
    def __init__(self) -> None:
        self._users = {"admin": "1234"}
        self._current_user: FakeUser | None = None
        self.last_login_payload = None
        self.logout_called = False

    def login_with_details(self, username: str, password: str, interface: str) -> dict:
        self.last_login_payload = (username, interface)
        if self._users.get(username) == password:
            self._current_user = FakeUser(username)
            return {"success": True}
        return {"success": False}

    def is_user_authenticated(self) -> bool:
        return self._current_user is not None

    def get_current_user(self):
        return self._current_user

    def logout(self) -> None:
        self.logout_called = True
        self._current_user = None

    # SettingsService helpers
    def simulate_login(self, username: str = "admin") -> None:
        self._current_user = FakeUser(username)


class FakeLogManager:
    def __init__(self) -> None:
        self.events = []

    def log_event(self, event_type, description, user_id=None, **kwargs):
        self.events.append((event_type, description, user_id))


@dataclass
class FakeSystemSettings:
    monitoring_service_phone: str = "911"
    homeowner_phone: str = "010-0000-0000"
    system_lock_time: int = 30
    alarm_delay_time: int = 60

    def set_monitoring_service_phone(self, value: str):
        self.monitoring_service_phone = value

    def set_homeowner_phone(self, value: str):
        self.homeowner_phone = value

    def set_system_lock_time(self, value: int):
        self.system_lock_time = value

    def set_alarm_delay_time(self, value: int):
        self.alarm_delay_time = value


class FakeConfigurationManager:
    def __init__(self) -> None:
        self.settings = FakeSystemSettings()
        self.updated_settings = None

    def get_system_setting(self):
        return self.settings

    def update_system_settings(self, settings: FakeSystemSettings) -> bool:
        self.updated_settings = settings
        return True


def test_auth_service_logs_success_and_failure():
    login_manager = FakeLoginManager()
    log_manager = FakeLogManager()
    service = AuthService(login_manager, log_manager)

    ok = service.login("admin", "1234", "web_browser")
    assert ok["success"] is True
    assert log_manager.events[-1][0] == "LOGIN_SUCCESS"

    fail = service.login("admin", "wrong", "web_browser")
    assert fail["success"] is False
    assert log_manager.events[-1][0] == "LOGIN_FAILED"


def test_auth_service_logout_emits_event():
    login_manager = FakeLoginManager()
    log_manager = FakeLogManager()
    service = AuthService(login_manager, log_manager)

    # logout when not authenticated should be a no-op
    assert service.logout() is None

    login_manager.simulate_login()
    assert service.logout() == "admin"
    assert log_manager.events[-1][0] == "LOGOUT"
    assert login_manager.logout_called is True


def test_settings_service_requires_authentication():
    login_manager = FakeLoginManager()
    config_manager = FakeConfigurationManager()
    log_manager = FakeLogManager()
    service = SettingsService(config_manager, login_manager, log_manager)

    result = service.update_settings(monitoring_phone="111-222-3333")
    assert result.success is False
    assert "Authentication required" in result.message


def test_settings_service_updates_and_logs():
    login_manager = FakeLoginManager()
    login_manager.simulate_login("ops")
    config_manager = FakeConfigurationManager()
    log_manager = FakeLogManager()
    service = SettingsService(config_manager, login_manager, log_manager)

    result = service.update_settings(
        monitoring_phone="111-222-3333",
        homeowner_phone="444-555-6666",
        lock_time=45,
        alarm_delay=15,
    )

    assert result.success is True
    saved = config_manager.updated_settings
    assert saved.monitoring_service_phone == "111-222-3333"
    assert saved.homeowner_phone == "444-555-6666"
    assert saved.system_lock_time == 45
    assert saved.alarm_delay_time == 15
    assert log_manager.events[-1][0] == "CONFIG_UPDATE"
