import pytest

from domain.services.login_presenter import ControlPanelLoginPresenter


class StubSystem:
    def __init__(self, response):
        self.response = response
        self.calls = []

    def login_with_details(self, user_id, password, interface):
        self.calls.append((user_id, password, interface))
        return dict(self.response)


def make_presenter(response):
    return ControlPanelLoginPresenter(StubSystem(response))


def test_missing_credentials_triggers_warning():
    presenter = make_presenter({})
    outcome = presenter.attempt_login("", "pw")

    assert not outcome.success
    assert outcome.alert_level == "warning"
    assert "Please enter both User ID" in outcome.alert_message


def test_success_navigates_to_main_menu():
    presenter = make_presenter({"success": True})

    outcome = presenter.attempt_login("user", "pw")

    assert outcome.success
    assert outcome.navigate_to == "MainMenu"


def test_locked_with_remaining_time_sets_status():
    presenter = make_presenter(
        {"locked": True, "remaining_time": 90, "message": "Locked due to attempts"}
    )
    outcome = presenter.attempt_login("user", "pw")

    assert not outcome.success
    assert "Try again in" in outcome.status_text
    assert outcome.status_color == "red"
    assert outcome.alert_title == "Account Locked"


def test_general_failure_with_attempts_shows_message():
    presenter = make_presenter({"success": False, "tries": 2, "remaining": 1})

    outcome = presenter.attempt_login("user", "pw")

    assert not outcome.success
    assert "Remaining attempts: 1" in outcome.status_text
    assert "Failed attempts: 2" in outcome.alert_message


def test_system_locked_alert():
    presenter = make_presenter({"system_locked": True, "message": "Admin lock"})

    outcome = presenter.attempt_login("user", "pw")

    assert outcome.alert_title == "System Locked"
    assert "Admin lock" in outcome.alert_message
