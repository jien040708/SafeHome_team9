from domain.services.settings_presenter import (
    ControlPanelSettingsPresenter,
    SettingsOutcome,
)


class StubSystem:
    def __init__(self, should_succeed=True):
        self.should_succeed = should_succeed
        self.calls = []

    def configure_system_setting(self, **kwargs):
        self.calls.append(kwargs)
        return self.should_succeed


def presenter_for(system=None):
    return ControlPanelSettingsPresenter(system or StubSystem())


def test_rejects_non_numeric_values():
    presenter = presenter_for()
    outcome = presenter.save_settings(
        monitoring_phone="911",
        homeowner_phone="010",
        lock_time="abc",
        alarm_delay="5",
    )
    assert not outcome.success
    assert "invalid" in outcome.message.lower()


def test_rejects_negative_values():
    presenter = presenter_for()
    outcome = presenter.save_settings(
        monitoring_phone="911",
        homeowner_phone="010",
        lock_time="-1",
        alarm_delay="0",
    )
    assert not outcome.success
    assert "negative" in outcome.message.lower()


def test_successful_save_invokes_system():
    system = StubSystem(should_succeed=True)
    presenter = presenter_for(system)
    outcome = presenter.save_settings(
        monitoring_phone="911",
        homeowner_phone="010",
        lock_time="30",
        alarm_delay="60",
    )
    assert outcome.success
    assert system.calls == [
        {
            "monitoring_phone": "911",
            "homeowner_phone": "010",
            "lock_time": 30,
            "alarm_delay": 60,
        }
    ]


def test_failure_surfaces_error():
    system = StubSystem(should_succeed=False)
    presenter = presenter_for(system)
    outcome = presenter.save_settings(
        monitoring_phone="911",
        homeowner_phone="010",
        lock_time="30",
        alarm_delay="60",
    )
    assert not outcome.success
    assert "failed" in outcome.message.lower()
