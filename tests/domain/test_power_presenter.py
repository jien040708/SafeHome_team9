from domain.services.power_presenter import PowerControlPresenter, PowerOutcome


class StubLoginManager:
    def __init__(self, authenticated=True):
        self.authenticated = authenticated
        self.logout_calls = 0

    def is_user_authenticated(self):
        return self.authenticated


class StubSystem:
    def __init__(self, turn_off_result=True, authenticated=True):
        self.login_manager = StubLoginManager(authenticated)
        self.turn_off_result = turn_off_result
        self.logout_calls = 0

    def logout(self):
        self.logout_calls += 1
        self.login_manager.authenticated = False

    def turn_off(self):
        return self.turn_off_result


def test_turn_off_logs_out_authenticated_users():
    system = StubSystem(turn_off_result=True, authenticated=True)
    presenter = PowerControlPresenter(system)

    outcome = presenter.turn_off_system()
    assert outcome.success
    assert system.logout_calls == 1


def test_turn_off_skips_logout_when_not_authenticated():
    system = StubSystem(turn_off_result=True, authenticated=False)
    presenter = PowerControlPresenter(system)

    presenter.turn_off_system()
    assert system.logout_calls == 0


def test_turn_off_failure_returns_error():
    system = StubSystem(turn_off_result=False, authenticated=False)
    presenter = PowerControlPresenter(system)

    outcome = presenter.turn_off_system()
    assert not outcome.success
    assert outcome.alert_level == "error"
