from domain.services.modes_presenter import ModesViewModel


class StubController:
    def __init__(self, should_raise=False):
        self.modes = []
        self.should_raise = should_raise

    def set_security_mode(self, mode):
        if self.should_raise:
            raise RuntimeError("boom")
        self.modes.append(mode)
        return True


class StubConfigManager:
    def get_zone_name_map(self):
        return {"1": "Front", "2": "Back"}


class StubSystem:
    def __init__(self, controller=None, config=None):
        self.system_controller = controller
        self.configuration_manager = config


def test_change_mode_requires_controller():
    presenter = ModesViewModel(StubSystem())
    success, error = presenter.change_mode("Away")
    assert not success
    assert "System is not running" in error


def test_change_mode_delegates_to_controller():
    controller = StubController()
    presenter = ModesViewModel(StubSystem(controller=controller))

    success, error = presenter.change_mode("Away")
    assert success
    assert error is None
    assert controller.modes == ["Away"]


def test_zone_name_resolution_uses_config():
    presenter = ModesViewModel(
        StubSystem(config=StubConfigManager())
    )
    names = presenter.resolve_zone_names([2, 1])
    assert names == ["Front", "Back"]


def test_zone_name_resolution_without_config():
    presenter = ModesViewModel(StubSystem())
    names = presenter.resolve_zone_names([3, 1])
    assert names == ["1", "3"]
