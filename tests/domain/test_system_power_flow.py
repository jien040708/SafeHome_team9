from types import SimpleNamespace

from domain.system import System, SystemState


class StubSensor:
    def __init__(self):
        self.deactivated = False

    def deactivate(self):
        self.deactivated = True


class StubCamera:
    def __init__(self):
        self.deactivated = False

    def deactivate(self):
        self.deactivated = True


class StubCameraController:
    def __init__(self):
        self.disabled = False

    def disable_all_camera(self):
        self.disabled = True


class StubSiren:
    def __init__(self):
        self.deactivated = False

    def deactivate(self):
        self.deactivated = True


class StubSecuritySystem:
    def __init__(self):
        self.deactivated = False

    def deactivate_alarm(self):
        self.deactivated = True


class StubConfigManager:
    def __init__(self):
        self.update_called = False

    def get_system_setting(self):
        return object()

    def update_system_settings(self, settings):
        self.update_called = True
        return True


class StubLogManager:
    def __init__(self):
        self.events = []

    def log_event(self, event_type, description, user_id=None):
        self.events.append((event_type, description, user_id))


class StubStorageManager:
    def __init__(self):
        self.disconnected = False

    def disconnect(self):
        self.disconnected = True


class StubUser:
    def get_username(self):
        return "admin"


class StubLoginManager:
    def __init__(self, authenticated=True):
        self.authenticated = authenticated

    def is_user_authenticated(self):
        return self.authenticated

    def get_current_user(self):
        return StubUser()


class StubAuthService:
    def __init__(self):
        self.logout_calls = 0

    def logout(self):
        self.logout_calls += 1
        return "admin"


def build_system():
    system = System()
    system.system_state = SystemState.READY
    system.configuration_manager = StubConfigManager()
    system.sensors = [StubSensor(), StubSensor()]
    system.camera_controller = StubCameraController()
    system.system_controller = SimpleNamespace(cameras=[StubCamera()])
    system.siren = StubSiren()
    system.security_system = StubSecuritySystem()
    system.login_manager = StubLoginManager(authenticated=True)
    system._auth_service = StubAuthService()
    system.log_manager = StubLogManager()
    system.storage_manager = StubStorageManager()
    return system


def test_turn_off_executes_shutdown_sequence():
    system = build_system()

    result = system.turn_off()

    assert result
    assert system.system_state == SystemState.OFF
    assert system.configuration_manager.update_called
    assert all(sensor.deactivated for sensor in system.sensors)
    assert system.camera_controller.disabled
    assert all(cam.deactivated for cam in system.system_controller.cameras)
    assert system.siren.deactivated
    assert system.security_system.deactivated
    assert system._auth_service.logout_calls == 1
    assert ("SYSTEM_SHUTDOWN", "SafeHome system shutting down", None) in system.log_manager.events
    assert system.storage_manager.disconnected


def test_turn_off_returns_false_if_already_off():
    system = System()
    assert system.turn_off() is False
