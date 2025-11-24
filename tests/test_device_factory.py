import pytest

from devices.camera import Camera
from devices.device_factory import (
    DeviceFactory,
    DeviceFactoryError,
    create_default_device_factory,
)
from devices.motion_detector import MotionDetector
from devices.windoor_sensor import WindowDoorSensor
from utils.constants import (
    SENSOR_CAMERA,
    SENSOR_MOTION,
    SENSOR_WIN_DOOR,
    STATE_CLOSED,
    STATE_OPEN,
    STATE_CLEAR,
    STATE_DETECTED,
    STATE_IDLE,
    STATE_RECORDING,
)


class ObserverStub:
    def __init__(self):
        self.events = []

    def update_sensor_status(self, device_id, device_type, status):
        self.events.append((device_id, device_type, status))


@pytest.mark.parametrize(
    "device_type, expected_cls, expected_status",
    [
        (SENSOR_WIN_DOOR, WindowDoorSensor, STATE_CLOSED),
        (SENSOR_MOTION, MotionDetector, STATE_CLEAR),
        (SENSOR_CAMERA, Camera, STATE_IDLE),
    ],
)
def test_default_factory_creates_registered_sensors(device_type, expected_cls, expected_status):
    factory = create_default_device_factory()

    sensor = factory.create(device_type, "Device-01")

    assert isinstance(sensor, expected_cls)
    assert sensor.get_id() == "Device-01"
    assert sensor.get_type() == device_type
    assert sensor.get_status() == expected_status


def test_factory_build_many_preserves_order():
    factory = create_default_device_factory()
    records = [
        ("Front Door", SENSOR_WIN_DOOR),
        ("Living Room", SENSOR_MOTION),
        ("Garden Cam", SENSOR_CAMERA),
    ]

    sensors = factory.build_many(records)

    assert [sensor.get_id() for sensor in sensors] == [rec[0] for rec in records]
    assert [sensor.get_type() for sensor in sensors] == [rec[1] for rec in records]


def test_unknown_device_type_raises_error():
    factory = create_default_device_factory()

    with pytest.raises(DeviceFactoryError):
        factory.create("Unknown Sensor", "Ghost")


def test_register_duplicate_without_override_fails():
    factory = DeviceFactory()
    factory.register(SENSOR_WIN_DOOR, WindowDoorSensor)

    with pytest.raises(DeviceFactoryError):
        factory.register(SENSOR_WIN_DOOR, WindowDoorSensor)


def test_window_sensor_notifies_on_state_changes():
    sensor = WindowDoorSensor("Front Door")
    observer = ObserverStub()
    sensor.add_observer(observer)

    sensor.set_open()
    assert sensor.get_status() == STATE_OPEN
    assert observer.events[-1] == ("Front Door", SENSOR_WIN_DOOR, STATE_OPEN)

    sensor.set_closed()
    assert sensor.get_status() == STATE_CLOSED
    assert observer.events[-1] == ("Front Door", SENSOR_WIN_DOOR, STATE_CLOSED)


def test_motion_detector_detect_motion_triggers_notification():
    sensor = MotionDetector("Living Room")
    observer = ObserverStub()
    sensor.add_observer(observer)

    sensor.detect_motion()

    assert sensor.get_status() == STATE_DETECTED
    assert observer.events[-1] == ("Living Room", SENSOR_MOTION, STATE_DETECTED)


def test_camera_start_recording_updates_status():
    camera = Camera("Garden Cam")
    observer = ObserverStub()
    camera.add_observer(observer)

    camera.start_recording()

    assert camera.get_status() == STATE_RECORDING
    assert observer.events[-1] == ("Garden Cam", SENSOR_CAMERA, STATE_RECORDING)
