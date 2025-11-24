import pytest

from domain.system_states import AwayState, DisarmedState, StayState
from utils.constants import (
    MODE_AWAY,
    MODE_DISARMED,
    MODE_STAY,
    SENSOR_CAMERA,
    SENSOR_MOTION,
    SENSOR_WIN_DOOR,
    STATE_CLOSED,
    STATE_DETECTED,
    STATE_OPEN,
)


class DummyController:
    def __init__(self):
        self.alarm_calls = 0

    def initiate_alarm_sequence(self):
        self.alarm_calls += 1


@pytest.mark.parametrize(
    "state_cls, expected_name",
    [
        (DisarmedState, MODE_DISARMED),
        (AwayState, MODE_AWAY),
        (StayState, MODE_STAY),
    ],
)
def test_state_name_mapping(state_cls, expected_name):
    assert state_cls().get_name() == expected_name


def test_disarmed_state_ignores_sensor_signals():
    controller = DummyController()
    state = DisarmedState()

    state.handle_sensor(controller, "sensor-1", SENSOR_WIN_DOOR, STATE_OPEN)
    assert controller.alarm_calls == 0


@pytest.mark.parametrize(
    "status, expected_calls",
    [
        (STATE_OPEN, 1),
        (STATE_DETECTED, 1),
        ("Picture Taken", 1),
        (STATE_CLOSED, 0),
    ],
)
def test_away_state_triggers_on_all_intrusions(status, expected_calls):
    controller = DummyController()
    state = AwayState()

    state.handle_sensor(controller, "camera-1", SENSOR_CAMERA, status)
    assert controller.alarm_calls == expected_calls


@pytest.mark.parametrize(
    "device_type, status, expected_calls",
    [
        (SENSOR_WIN_DOOR, STATE_OPEN, 1),
        (SENSOR_WIN_DOOR, STATE_CLOSED, 0),
        (SENSOR_MOTION, STATE_DETECTED, 0),
        (SENSOR_CAMERA, "Picture Taken", 0),
    ],
)
def test_stay_state_only_triggers_on_perimeter(device_type, status, expected_calls):
    controller = DummyController()
    state = StayState()

    state.handle_sensor(controller, "sensor-2", device_type, status)
    assert controller.alarm_calls == expected_calls
