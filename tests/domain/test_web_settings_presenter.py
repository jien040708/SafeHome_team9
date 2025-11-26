"""Unit tests for WebSettingsPresenter (Web Interface Settings)."""
import pytest

from domain.services.web_settings_presenter import WebSettingsPresenter


class StubSystemSetting:
    """Stub SystemSetting for testing."""
    def __init__(self, should_save_succeed=True):
        self.should_save_succeed = should_save_succeed
        self.monitoring_phone = None
        self.homeowner_phone = None
        self.lock_time = None
        self.alarm_delay = None

    def set_monitoring_service_phone(self, phone):
        self.monitoring_phone = phone

    def set_homeowner_phone(self, phone):
        self.homeowner_phone = phone

    def set_system_lock_time(self, time):
        self.lock_time = time

    def set_alarm_delay_time(self, time):
        self.alarm_delay = time

    def save(self):
        return self.should_save_succeed


class StubConfigurationManager:
    """Stub ConfigurationManager for testing."""
    def __init__(self, system_setting=None):
        self.system_setting = system_setting or StubSystemSetting()

    def get_system_setting(self):
        return self.system_setting


class StubSystem:
    """Stub System for testing."""
    def __init__(self, configuration_manager=None):
        self.configuration_manager = configuration_manager


def make_presenter(should_save_succeed=True):
    """Helper to create presenter with stub system."""
    setting = StubSystemSetting(should_save_succeed)
    config_manager = StubConfigurationManager(setting)
    system = StubSystem(config_manager)
    return WebSettingsPresenter(system)


# ========== Phone Validation Tests ==========

def test_invalid_monitoring_phone_format():
    """Test that invalid monitoring phone format is rejected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        monitoring_service_phone="invalid",
        homeowner_phone="123-456-7890"
    )

    assert not outcome.success
    assert "Validation failed" in outcome.message
    assert any("monitoring" in err.lower() for err in outcome.errors)


def test_invalid_homeowner_phone_format():
    """Test that invalid homeowner phone format is rejected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        monitoring_service_phone="123-456-7890",
        homeowner_phone="abc"
    )

    assert not outcome.success
    assert "Validation failed" in outcome.message
    assert any("homeowner" in err.lower() for err in outcome.errors)


def test_valid_phone_formats_accepted():
    """Test that valid phone formats are accepted."""
    presenter = make_presenter()

    # Standard format XXX-XXX-XXXX
    outcome = presenter.update_settings(
        monitoring_service_phone="111-222-3333",
        homeowner_phone="444-555-6666"
    )
    assert outcome.success

    # Flexible format with at least 3 characters
    outcome2 = presenter.update_settings(
        monitoring_service_phone="(123) 456-7890",
        homeowner_phone="+1-234-567-8900"
    )
    assert outcome2.success


# ========== Time Value Validation Tests ==========

def test_zero_lock_time_rejected():
    """Test that zero lock time is rejected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        system_lock_time=0
    )

    assert not outcome.success
    assert any("lock time must be greater than 0" in err for err in outcome.errors)


def test_negative_lock_time_rejected():
    """Test that negative lock time is rejected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        system_lock_time=-5
    )

    assert not outcome.success
    assert any("lock time must be greater than 0" in err for err in outcome.errors)


def test_negative_alarm_delay_rejected():
    """Test that negative alarm delay is rejected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        alarm_delay_time=-10
    )

    assert not outcome.success
    assert any("alarm delay time must be non-negative" in err.lower() for err in outcome.errors)


def test_invalid_lock_time_type():
    """Test that invalid lock time type is rejected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        system_lock_time="abc"
    )

    assert not outcome.success
    assert any("valid number" in err for err in outcome.errors)


def test_invalid_alarm_delay_type():
    """Test that invalid alarm delay type is rejected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        alarm_delay_time="xyz"
    )

    assert not outcome.success
    assert any("valid number" in err for err in outcome.errors)


# ========== Multiple Validation Errors ==========

def test_multiple_validation_errors():
    """Test that multiple validation errors are collected."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        monitoring_service_phone="invalid",
        homeowner_phone="bad",
        system_lock_time=0,
        alarm_delay_time=-5
    )

    assert not outcome.success
    assert len(outcome.errors) >= 4


# ========== Successful Update Tests ==========

def test_successful_settings_update():
    """Test successful settings update."""
    presenter = make_presenter(should_save_succeed=True)
    outcome = presenter.update_settings(
        monitoring_service_phone="111-222-3333",
        homeowner_phone="444-555-6666",
        system_lock_time=30,
        alarm_delay_time=60
    )

    assert outcome.success
    assert outcome.message == "Settings updated successfully"


def test_partial_update_only_phones():
    """Test updating only phone numbers."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        monitoring_service_phone="123-456-7890",
        homeowner_phone="098-765-4321"
    )

    assert outcome.success
    settings = presenter.system.configuration_manager.system_setting
    assert settings.monitoring_phone == "123-456-7890"
    assert settings.homeowner_phone == "098-765-4321"


def test_partial_update_only_times():
    """Test updating only time values."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        system_lock_time=45,
        alarm_delay_time=90
    )

    assert outcome.success
    settings = presenter.system.configuration_manager.system_setting
    assert settings.lock_time == 45
    assert settings.alarm_delay == 90


def test_update_converts_string_times_to_int():
    """Test that string time values are converted to integers."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        system_lock_time="30",
        alarm_delay_time="60"
    )

    assert outcome.success
    settings = presenter.system.configuration_manager.system_setting
    assert settings.lock_time == 30
    assert settings.alarm_delay == 60
    assert isinstance(settings.lock_time, int)
    assert isinstance(settings.alarm_delay, int)


# ========== Save Failure Tests ==========

def test_save_failure_returns_error():
    """Test that save failure returns appropriate error."""
    presenter = make_presenter(should_save_succeed=False)
    outcome = presenter.update_settings(
        monitoring_service_phone="123-456-7890",
        system_lock_time=30
    )

    assert not outcome.success
    assert "Failed to save settings" in outcome.message


# ========== System Availability Tests ==========

def test_system_not_available():
    """Test handling when system is not available."""
    presenter = WebSettingsPresenter(None)
    outcome = presenter.update_settings(
        monitoring_service_phone="123-456-7890"
    )

    assert not outcome.success
    assert "not available" in outcome.message.lower()


def test_get_settings_system_not_available():
    """Test get settings when system is not available."""
    presenter = WebSettingsPresenter(None)
    outcome = presenter.get_settings()

    assert not outcome.success
    assert "not available" in outcome.message.lower()


# ========== Get Settings Tests ==========

def test_get_settings_success():
    """Test successful retrieval of settings."""
    presenter = make_presenter()
    outcome = presenter.get_settings()

    assert outcome.success
    assert "retrieved successfully" in outcome.message.lower()


# ========== Edge Cases ==========

def test_empty_update_succeeds():
    """Test that updating with no parameters succeeds."""
    presenter = make_presenter()
    outcome = presenter.update_settings()

    assert outcome.success


def test_zero_alarm_delay_accepted():
    """Test that zero alarm delay is accepted (only lock time must be > 0)."""
    presenter = make_presenter()
    outcome = presenter.update_settings(
        alarm_delay_time=0
    )

    assert outcome.success
