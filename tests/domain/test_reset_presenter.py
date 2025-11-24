import pytest

from domain.services.reset_presenter import ControlPanelResetPresenter, ResetOutcome


class StubSystem:
    def __init__(self, response):
        self.response = response
        self.calls = 0

    def reset(self):
        self.calls += 1
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def make_presenter(response):
    return ControlPanelResetPresenter(StubSystem(response))


def test_reset_success_dict():
    presenter = make_presenter({"success": True, "message": "All good", "phase": 3})
    outcome = presenter.perform_reset()

    assert outcome == ResetOutcome(
        success=True,
        alert_level="info",
        alert_title="Success",
        alert_message="All good",
        phase=3,
    )


def test_reset_failure_dict():
    presenter = make_presenter({"success": False, "message": "Turn off failed", "phase": 1})
    outcome = presenter.perform_reset()

    assert not outcome.success
    assert outcome.alert_level == "error"
    assert outcome.alert_title == "Error"
    assert "Turn off failed" in outcome.alert_message
    assert outcome.phase == 1


def test_reset_boolean_response():
    presenter = make_presenter(True)
    outcome = presenter.perform_reset()

    assert outcome.success
    assert outcome.alert_message == "System reset successfully!"


def test_reset_exception_becomes_error():
    presenter = make_presenter(Exception("DB down"))
    outcome = presenter.perform_reset()

    assert not outcome.success
    assert outcome.alert_level == "error"
    assert "DB down" in outcome.alert_message
