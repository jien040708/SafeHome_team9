from types import SimpleNamespace

import pytest

from domain.system_controller import SystemController
from security.events import SensorStatus, SensorType
from utils.constants import MODE_AWAY, MODE_DISARMED


class StubUserManager:
    def __init__(self, should_authenticate=True):
        self.should_authenticate = should_authenticate
        self.attempts = []

    def authenticate(self, user_id, password):
        self.attempts.append((user_id, password))
        return self.should_authenticate


class DummySecuritySystem:
    def __init__(self):
        self.disarm_calls = []
        self.arm_calls = []
        self.handled_events = []
        self.mode = SimpleNamespace(name="INIT")

    def disarm(self, cleared_by):
        self.disarm_calls.append(cleared_by)
        self.mode = SimpleNamespace(name=MODE_DISARMED)

    def arm(self, mode):
        self.arm_calls.append(mode)
        self.mode = SimpleNamespace(name=mode.name)

    def handle_sensor_event(self, event):
        self.handled_events.append(event)


class DummyCamera:
    def __init__(self):
        self.picture_count = 0

    def take_picture(self):
        self.picture_count += 1


@pytest.fixture
def controller():
    return SystemController(DummySecuritySystem(), user_manager=StubUserManager())


def test_set_security_mode_requires_login(controller):
    assert controller.set_security_mode(MODE_AWAY) is False
    assert controller.last_error_message == "Login required"


def test_set_security_mode_disarm_updates_security_system(controller):
    controller.login("admin", "pw")

    assert controller.set_security_mode(MODE_DISARMED) is True
    assert controller.security_system.disarm_calls == ["admin"]
    assert controller.security_system.mode.name == MODE_DISARMED


def test_set_security_mode_invalid_string_tracks_error(controller):
    controller.login("user", "pw")

    assert controller.set_security_mode("UNKNOWN") is False
    assert controller.last_error_message == "Unsupported security mode: UNKNOWN"
    assert controller.security_system.disarm_calls == []
    assert controller.security_system.arm_calls == []


def test_update_sensor_status_maps_event_fields(controller):
    controller.update_sensor_status(
        device_id="sensor-1",
        device_type="Motion Detector",
        status="Motion Detected",
    )

    assert len(controller.security_system.handled_events) == 1
    event = controller.security_system.handled_events[0]
    assert event.sensor_id == "sensor-1"
    assert event.sensor_type == SensorType.MOTION
    assert event.status == SensorStatus.MOTION_DETECTED


def test_trigger_camera_invokes_take_picture_on_all_cameras(controller):
    cam_a, cam_b = DummyCamera(), DummyCamera()
    controller.add_camera(cam_a)
    controller.add_camera(cam_b)

    controller.trigger_camera("intrusion")

    assert cam_a.picture_count == 1
    assert cam_b.picture_count == 1
