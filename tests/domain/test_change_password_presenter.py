from domain.services.change_password_presenter import (
    ControlPanelChangePasswordPresenter,
    ChangePasswordOutcome,
)


class StubSystem:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed
        self.calls = []

    def change_password(self, old_pw, new_pw):
        self.calls.append((old_pw, new_pw))
        return self.should_succeed


def presenter_for(system=None):
    return ControlPanelChangePasswordPresenter(system or StubSystem())


def test_mismatched_passwords_return_error():
    presenter = presenter_for()
    outcome = presenter.change_password("old", "new-1", "new-2")
    assert not outcome.success
    assert "match" in outcome.message.lower()


def test_short_password_rejected():
    presenter = presenter_for()
    outcome = presenter.change_password("old", "123", "123")
    assert not outcome.success
    assert "least" in outcome.message.lower()


def test_successful_change_returns_info():
    system = StubSystem(should_succeed=True)
    presenter = presenter_for(system)
    outcome = presenter.change_password("old", "1234", "1234")
    assert outcome.success
    assert outcome.alert_level == "info"
    assert system.calls == [("old", "1234")]


def test_failed_change_returns_error():
    system = StubSystem(should_succeed=False)
    presenter = presenter_for(system)
    outcome = presenter.change_password("old", "abcd", "abcd")
    assert not outcome.success
    assert outcome.alert_level == "error"
