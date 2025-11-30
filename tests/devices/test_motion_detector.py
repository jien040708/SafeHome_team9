"""
Test cases for MotionDetector class functionality.

Tests cover:
- MotionDetector initialization
- detect_motion() method
- clear_motion() method (toggle functionality)
- State transitions between DETECTED and CLEAR
- Observer notifications on state changes
"""

from __future__ import annotations

import pytest

from devices.motion_detector import MotionDetector
from utils.constants import SENSOR_MOTION, STATE_CLEAR, STATE_DETECTED


class ObserverStub:
    """Stub observer for testing notifications."""
    def __init__(self):
        self.events = []

    def update_sensor_status(self, device_id, device_type, status):
        self.events.append((device_id, device_type, status))


def test_motion_detector_initialization():
    """Test MotionDetector initializes with correct default values."""
    detector = MotionDetector("Living Room")

    assert detector.get_id() == "Living Room"
    assert detector.get_type() == SENSOR_MOTION
    assert detector.get_status() == STATE_CLEAR


def test_motion_detector_detect_motion():
    """Test detect_motion() sets status to DETECTED."""
    detector = MotionDetector("Living Room")

    detector.detect_motion()

    assert detector.get_status() == STATE_DETECTED


def test_motion_detector_clear_motion():
    """Test clear_motion() sets status to CLEAR."""
    detector = MotionDetector("Living Room")

    # First detect motion
    detector.detect_motion()
    assert detector.get_status() == STATE_DETECTED

    # Then clear motion
    detector.clear_motion()
    assert detector.get_status() == STATE_CLEAR


def test_motion_detector_toggle_state():
    """Test that detect_motion and clear_motion can toggle state repeatedly."""
    detector = MotionDetector("Living Room")

    # Initial state
    assert detector.get_status() == STATE_CLEAR

    # Toggle to DETECTED
    detector.detect_motion()
    assert detector.get_status() == STATE_DETECTED

    # Toggle to CLEAR
    detector.clear_motion()
    assert detector.get_status() == STATE_CLEAR

    # Toggle to DETECTED again
    detector.detect_motion()
    assert detector.get_status() == STATE_DETECTED

    # Toggle to CLEAR again
    detector.clear_motion()
    assert detector.get_status() == STATE_CLEAR


def test_motion_detector_detect_motion_notifies_observers():
    """Test that detect_motion() notifies observers."""
    detector = MotionDetector("Living Room")
    observer = ObserverStub()
    detector.add_observer(observer)

    detector.detect_motion()

    assert len(observer.events) == 1
    assert observer.events[-1] == ("Living Room", SENSOR_MOTION, STATE_DETECTED)


def test_motion_detector_clear_motion_notifies_observers():
    """Test that clear_motion() notifies observers."""
    detector = MotionDetector("Living Room")
    observer = ObserverStub()
    detector.add_observer(observer)

    # First detect motion (will notify)
    detector.detect_motion()
    assert len(observer.events) == 1

    # Clear motion (should also notify)
    detector.clear_motion()

    assert len(observer.events) == 2
    assert observer.events[-1] == ("Living Room", SENSOR_MOTION, STATE_CLEAR)


def test_motion_detector_multiple_observers():
    """Test that multiple observers are notified on state changes."""
    detector = MotionDetector("Living Room")
    observer1 = ObserverStub()
    observer2 = ObserverStub()
    detector.add_observer(observer1)
    detector.add_observer(observer2)

    detector.detect_motion()

    assert len(observer1.events) == 1
    assert len(observer2.events) == 1
    assert observer1.events[-1] == ("Living Room", SENSOR_MOTION, STATE_DETECTED)
    assert observer2.events[-1] == ("Living Room", SENSOR_MOTION, STATE_DETECTED)

    detector.clear_motion()

    assert len(observer1.events) == 2
    assert len(observer2.events) == 2
    assert observer1.events[-1] == ("Living Room", SENSOR_MOTION, STATE_CLEAR)
    assert observer2.events[-1] == ("Living Room", SENSOR_MOTION, STATE_CLEAR)


def test_motion_detector_clear_motion_when_already_clear():
    """Test that clear_motion() works even when already clear."""
    detector = MotionDetector("Living Room")
    observer = ObserverStub()
    detector.add_observer(observer)

    # Already clear initially
    assert detector.get_status() == STATE_CLEAR

    # Call clear_motion() when already clear
    detector.clear_motion()

    # Should still work and notify
    assert detector.get_status() == STATE_CLEAR
    assert len(observer.events) == 1


def test_motion_detector_detect_motion_when_already_detected():
    """Test that detect_motion() works even when already detected."""
    detector = MotionDetector("Living Room")
    observer = ObserverStub()
    detector.add_observer(observer)

    # First detect
    detector.detect_motion()
    assert detector.get_status() == STATE_DETECTED
    assert len(observer.events) == 1

    # Detect again
    detector.detect_motion()

    # Should still work and notify
    assert detector.get_status() == STATE_DETECTED
    assert len(observer.events) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
