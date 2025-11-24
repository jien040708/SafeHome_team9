import pytest

from domain.services.bootstrap_service import SystemBootstrapper
from utils.constants import SENSOR_CAMERA, SENSOR_MOTION


class FakeDeviceFactory:
    def __init__(self):
        self.created = []

    def create(self, device_type, device_id):
        device = DummySensor(device_type, device_id)
        self.created.append((device_type, device_id))
        return device


class DummyDeviceManager:
    def __init__(self, devices):
        self.devices = devices

    def load_all_devices(self):
        return list(self.devices)


class DummySensor:
    def __init__(self, sensor_type, device_id="sensor"):
        self.sensor_type = sensor_type
        self.device_id = device_id
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def get_type(self):
        return self.sensor_type

    def take_picture(self):
        pass


class DummyController:
    def __init__(self):
        self.added_cameras = []

    def add_camera(self, camera):
        self.added_cameras.append(camera)


class DummyCameraController:
    def __init__(self):
        self.positions = []

    def add_camera(self, x_coord, y_coord):
        self.positions.append((x_coord, y_coord))


class DummySystem:
    def __init__(self):
        self.configuration_manager = SimpleNamespace(
            device_manager=None
        )
        self.system_controller = None
        self.camera_controller = None
        self.sensors = []
        self.on_turn_on_complete = None


class SimpleNamespace:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


def test_load_sensors_uses_device_manager_records():
    factory = FakeDeviceFactory()
    bootstrapper = SystemBootstrapper(device_factory=factory)
    system = DummySystem()
    system.configuration_manager.device_manager = DummyDeviceManager([
        ("Door1", "Window/Door Sensor"),
        ("Motion1", "Motion Detector"),
    ])

    sensors = bootstrapper.load_sensors(system)

    assert len(sensors) == 2
    assert factory.created == [
        ("Window/Door Sensor", "Door1"),
        ("Motion Detector", "Motion1"),
    ]


def test_initialize_devices_after_turn_on_updates_ui_sensors():
    controller = DummyController()
    system = DummySystem()
    system.system_controller = controller
    system.camera_controller = DummyCameraController()

    custom_sensor = DummySensor(SENSOR_CAMERA)

    class FakeBootstrap(SystemBootstrapper):
        def load_sensors(self, _system):
            return [custom_sensor]

    bootstrapper = FakeBootstrap()
    ui_sensors = [DummySensor(SENSOR_MOTION)]

    bootstrapper.initialize_devices_after_turn_on(system, ui_sensors)

    assert system.sensors == ui_sensors
    assert ui_sensors == [custom_sensor]
    assert controller.added_cameras == [custom_sensor]
    assert custom_sensor.observers == [controller]
    assert system.camera_controller.positions == [(350, 20), (330, 208), (332, 262)]


def test_attach_post_turn_on_hook_sets_callback():
    bootstrapper = SystemBootstrapper()
    system = DummySystem()
    sensors = []

    bootstrapper.attach_post_turn_on_hook(system, sensors)

    assert callable(system.on_turn_on_complete)
