import pytest

from virtual_device_v4.device.safehome_sensor_test import (
    SensorInputError,
    normalize_sensor_id,
    find_sensor_by_id,
    require_sensor,
)


class DummySensor:
    def __init__(self, sensor_id, next_sensor=None):
        self.sensor_id = sensor_id
        self.next_sensor = next_sensor
        self.events = []

    def intrude(self):
        self.events.append("intrude")

    def release(self):
        self.events.append("release")


def make_chain(count=3):
    head = None
    for idx in reversed(range(1, count + 1)):
        head = DummySensor(idx, head)
    return head


def test_normalize_sensor_id_accepts_digits():
    assert normalize_sensor_id(" 42 ", "Need ID") == 42


def test_normalize_sensor_id_rejects_empty():
    with pytest.raises(SensorInputError, match="WinDoor"):
        normalize_sensor_id("   ", "WinDoor message")


def test_normalize_sensor_id_rejects_non_digits():
    with pytest.raises(SensorInputError, match="only digit allowed"):
        normalize_sensor_id("abc", "ignored")


def test_find_sensor_by_id_traverses_chain():
    chain = make_chain()
    sensor = find_sensor_by_id(chain, 2)
    assert sensor is not None
    assert sensor.sensor_id == 2


def test_find_sensor_by_id_returns_none_when_missing():
    chain = make_chain()
    assert find_sensor_by_id(chain, 99) is None


def test_require_sensor_returns_sensor_or_raises():
    chain = make_chain()
    sensor = require_sensor(chain, 1)
    assert sensor.sensor_id == 1

    with pytest.raises(LookupError):
        require_sensor(chain, 999)
