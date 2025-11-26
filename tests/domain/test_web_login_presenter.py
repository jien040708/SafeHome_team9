"""Unit tests for WebLoginPresenter (Web Interface Login)."""
import pytest

from domain.services.web_login_presenter import WebLoginPresenter


class StubLoginManager:
    """Stub LoginManager for testing."""
    def __init__(self, first_response=None, second_response=None):
        self.first_response = first_response or {}
        self.second_response = second_response or {}
        self.first_calls = []
        self.second_calls = []

    def validate_first_password(self, username, password, interface):
        self.first_calls.append((username, password, interface))
        return dict(self.first_response)

    def validate_second_password(self, username, second_password, interface):
        self.second_calls.append((username, second_password, interface))
        return dict(self.second_response)


class StubSystem:
    """Stub System for testing."""
    def __init__(self, login_manager=None):
        self.login_manager = login_manager


def make_presenter(first_response=None, second_response=None):
    """Helper to create presenter with stub system."""
    login_manager = StubLoginManager(first_response, second_response)
    system = StubSystem(login_manager)
    return WebLoginPresenter(system)


# ========== First Password Validation Tests ==========

def test_first_password_missing_username():
    """Test that empty username triggers validation error."""
    presenter = make_presenter()
    outcome = presenter.validate_first_password("", "password123")

    assert not outcome.success
    assert "Username and password are required" in outcome.message


def test_first_password_missing_password():
    """Test that empty password triggers validation error."""
    presenter = make_presenter()
    outcome = presenter.validate_first_password("admin", "")

    assert not outcome.success
    assert "Username and password are required" in outcome.message


def test_first_password_success():
    """Test successful first password validation."""
    presenter = make_presenter(first_response={"success": True})
    outcome = presenter.validate_first_password("admin", "password123")

    assert outcome.success
    assert outcome.message == "First password correct"


def test_first_password_locked_with_remaining_time():
    """Test locked account with remaining time for first password."""
    presenter = make_presenter(first_response={
        "locked": True,
        "remaining_time": 30,
        "message": "Account locked due to too many attempts",
        "tries": 5
    })
    outcome = presenter.validate_first_password("admin", "wrong")

    assert not outcome.success
    assert outcome.locked
    assert outcome.remaining_time == 30
    assert outcome.tries == 5
    assert "locked" in outcome.message.lower()


def test_first_password_system_off():
    """Test first password validation when system is off."""
    presenter = make_presenter(first_response={
        "system_off": True,
        "message": "System is currently off"
    })
    outcome = presenter.validate_first_password("admin", "password123")

    assert not outcome.success
    assert outcome.system_off
    assert "off" in outcome.message.lower()


def test_first_password_system_locked():
    """Test first password validation when system is locked."""
    presenter = make_presenter(first_response={
        "system_locked": True,
        "message": "System is locked by administrator"
    })
    outcome = presenter.validate_first_password("admin", "password123")

    assert not outcome.success
    assert outcome.system_locked
    assert "locked" in outcome.message.lower()


def test_first_password_failed_with_attempts():
    """Test first password validation failure with remaining attempts."""
    presenter = make_presenter(first_response={
        "success": False,
        "message": "Incorrect first password",
        "tries": 2,
        "remaining": 3
    })
    outcome = presenter.validate_first_password("admin", "wrong")

    assert not outcome.success
    assert outcome.tries == 2
    assert outcome.remaining == 3


def test_first_password_system_not_available():
    """Test first password validation when system is not available."""
    presenter = WebLoginPresenter(None)
    outcome = presenter.validate_first_password("admin", "password123")

    assert not outcome.success
    assert "not available" in outcome.message.lower()


# ========== Second Password Validation Tests ==========

def test_second_password_missing():
    """Test that empty second password triggers validation error."""
    presenter = make_presenter()
    outcome = presenter.validate_second_password("admin", "")

    assert not outcome.success
    assert "Second password is required" in outcome.message


def test_second_password_success():
    """Test successful second password validation."""
    presenter = make_presenter(second_response={"success": True})
    outcome = presenter.validate_second_password("admin", "pin1234")

    assert outcome.success
    assert outcome.message == "Login successful"
    assert outcome.redirect_url == "/dashboard"


def test_second_password_locked_with_remaining_time():
    """Test locked account with remaining time for second password."""
    presenter = make_presenter(second_response={
        "locked": True,
        "remaining_time": 45,
        "message": "Account locked",
        "tries": 5
    })
    outcome = presenter.validate_second_password("admin", "wrong")

    assert not outcome.success
    assert outcome.locked
    assert outcome.remaining_time == 45
    assert outcome.tries == 5


def test_second_password_system_off():
    """Test second password validation when system is off."""
    presenter = make_presenter(second_response={
        "system_off": True,
        "message": "System is off"
    })
    outcome = presenter.validate_second_password("admin", "pin1234")

    assert not outcome.success
    assert outcome.system_off


def test_second_password_system_locked():
    """Test second password validation when system is locked."""
    presenter = make_presenter(second_response={
        "system_locked": True,
        "message": "System locked"
    })
    outcome = presenter.validate_second_password("admin", "pin1234")

    assert not outcome.success
    assert outcome.system_locked


def test_second_password_failed_with_attempts():
    """Test second password validation failure with remaining attempts."""
    presenter = make_presenter(second_response={
        "success": False,
        "message": "Incorrect second password",
        "tries": 1,
        "remaining": 4
    })
    outcome = presenter.validate_second_password("admin", "wrong")

    assert not outcome.success
    assert outcome.tries == 1
    assert outcome.remaining == 4


def test_second_password_system_not_available():
    """Test second password validation when system is not available."""
    presenter = WebLoginPresenter(None)
    outcome = presenter.validate_second_password("admin", "pin1234")

    assert not outcome.success
    assert "not available" in outcome.message.lower()


# ========== Integration Tests ==========

def test_calls_login_manager_with_correct_interface():
    """Test that presenter calls LoginManager with 'web_browser' interface."""
    presenter = make_presenter(first_response={"success": True})
    presenter.validate_first_password("admin", "password123")

    calls = presenter.system.login_manager.first_calls
    assert len(calls) == 1
    assert calls[0] == ("admin", "password123", "web_browser")


def test_second_password_calls_with_correct_interface():
    """Test that second password validation uses correct interface."""
    presenter = make_presenter(second_response={"success": True})
    presenter.validate_second_password("admin", "pin1234")

    calls = presenter.system.login_manager.second_calls
    assert len(calls) == 1
    assert calls[0] == ("admin", "pin1234", "web_browser")
